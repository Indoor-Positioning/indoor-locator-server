from json import dumps, loads

import sys

from indoor_locator.fingerprint_utils import compute_distance, create_location_response_json
from locator import models


def ws_receive(message):
    message_json = loads(message["text"])
    print("Received message : " + dumps(message_json))
    command = message_json["command"]
    response = None
    if command == "GET_FLOOR_PLANS":
        response = [floor_plan.as_json() for floor_plan in models.FloorPlan.objects.all()]
    elif command == "GET_LOCATIONS":
        requested_floor_plan = message_json["floorPlanId"]
        response = [location.as_json() for location in models.FingerPrintedLocation.objects
            .filter(floor_plan=requested_floor_plan)]
    elif command == "GET_POIS":
        requested_floor_plan = message_json["floorPlanId"]
        response = [location.as_poi_json() for location in models.FingerPrintedLocation.objects
            .filter(floor_plan=requested_floor_plan).filter(is_poi=True)]
    elif command == "ADD_LOCATION":
        new_location = message_json["location"]
        added_loc = models.FingerPrintedLocation.add_from_json(new_location)
        response = added_loc.as_json()
    elif command == "ADD_POI":
        new_location = message_json["poi"]
        added_poi = models.FingerPrintedLocation.add_poi_from_json(new_location)
        response = added_poi.as_poi_json()
    elif command == "ADD_FINGERPRINTS":
        fingerprints = message_json["fingerPrintList"]
        models.FingerPrint.add_from_json(fingerprints)
    elif command == "LOCATE":
        fingerprint = message_json["fingerPrint"]
        floor_plan_id = message_json["floorPlanId"]
        fingerprint = models.FingerPrint.get_from_json(fingerprint)
        min_distance = sys.maxsize
        min_poi_distance = sys.maxsize
        closest_loc_id = None
        closest_poi_id = None
        closest_poi = None
        closest_loc = None
        floor_plan_fingerprint_ids = [fingerprint_loc_id.id for fingerprint_loc_id in models.FingerPrintedLocation.
                                                        objects.filter(floor_plan_id=floor_plan_id)]
        for fingerprint_loc in models.FingerPrint.objects.all():
            if fingerprint_loc.location_id not in floor_plan_fingerprint_ids:
                continue
            new_distance = compute_distance(fingerprint_loc, fingerprint)
            if new_distance < min_distance:
                min_distance = new_distance
                closest_loc_id = fingerprint_loc.location_id
            related_fingerprint_loc = models.FingerPrintedLocation.objects.get(pk=fingerprint_loc.location_id)
            if related_fingerprint_loc.is_poi:
                if new_distance < min_poi_distance:
                    min_poi_distance = new_distance
                    closest_poi_id = related_fingerprint_loc.id
        if closest_loc_id is not None:
            closest_loc = models.FingerPrintedLocation.objects.get(pk=closest_loc_id)
        if closest_poi_id is not None:
            closest_poi = models.FingerPrintedLocation.objects.get(pk=closest_poi_id) if closest_poi_id is not None else None
        response = create_location_response_json(closest_loc, closest_poi, min_distance)
        print(response)
    if response is not None:
        message.reply_channel.send({
            "text": dumps(response)
        })
