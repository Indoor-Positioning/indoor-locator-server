from json import dumps, loads

import sys

from indoor_locator.fingerprint_utils import compute_distance, create_location_response_json
from .models import FloorPlan, FingerPrintedLocation, PointOfInterest, FingerPrint
from channels import Group

# Create a group of all analytics channels
def analytics_receive(message):
    Group('analytics').add(message.reply_channel)
    message.reply_channel.send({
        "text": dumps({
            "status": "accepted"
        })
    })


def ws_receive(message):
    message_json = loads(message["text"])
    print("Received message : " + dumps(message_json))
    command = message_json["command"]
    response = None
    if command == "GET_FLOOR_PLANS":
        # Example: every new request produces a message to analytics Group
        # TODO: is an example REMOVE it, not useful info
        response = [floor_plan.as_json() for floor_plan in FloorPlan.objects.all()]
        Group('analytics').send({
            'text': dumps({
                'action': "GET_FLOOR_PLANS"
            })
        })
    elif command == "GET_LOCATIONS":
        requested_floor_plan = message_json["floorPlanId"]
        response = [location.as_json() for location in FingerPrintedLocation.objects.filter(floor_plan=requested_floor_plan)]
    elif command == "GET_POIS":
        requested_floor_plan = message_json["floorPlanId"]
        response = [location.as_poi_json() for location in FingerPrintedLocation.objects
            .filter(floor_plan=requested_floor_plan).filter(is_poi=True)]
    elif command == "ADD_LOCATION":
        new_location = message_json["location"]
        added_loc = FingerPrintedLocation.add_from_json(new_location)
        response = added_loc.as_json()
    elif command == "ADD_POI":
        new_location = message_json["poi"]
        added_poi = FingerPrintedLocation.add_poi_from_json(new_location)
        response = added_poi.as_poi_json()
    elif command == "ADD_FINGERPRINTS":
        fingerprints = message_json["fingerPrintList"]
        FingerPrint.add_from_json(fingerprints)
    elif command == "LOCATE":
        fingerprint = message_json["fingerPrint"]
        floor_plan_id = message_json["floorPlanId"]
        fingerprint = FingerPrint.get_from_json(fingerprint)
        min_distance = sys.maxsize
        min_poi_distance = sys.maxsize
        closest_loc_id = None
        closest_poi_id = None
        closest_poi = None
        closest_loc = None
        floor_plan_fingerprint_ids = [fingerprint_loc_id.id for fingerprint_loc_id in FingerPrintedLocation.
                                                        objects.filter(floor_plan_id=floor_plan_id)]
        for fingerprint_loc in FingerPrint.objects.all():
            if fingerprint_loc.location_id not in floor_plan_fingerprint_ids:
                continue
            new_distance = compute_distance(fingerprint_loc, fingerprint)
            if new_distance < min_distance:
                min_distance = new_distance
                closest_loc_id = fingerprint_loc.location_id
            related_fingerprint_loc = FingerPrintedLocation.objects.get(pk=fingerprint_loc.location_id)
            if related_fingerprint_loc.is_poi:
                if new_distance < min_poi_distance:
                    min_poi_distance = new_distance
                    closest_poi_id = related_fingerprint_loc.id
        if closest_loc_id is not None:
            closest_loc = FingerPrintedLocation.objects.get(pk=closest_loc_id)
        if closest_poi_id is not None:
            closest_poi = FingerPrintedLocation.objects.get(pk=closest_poi_id) if closest_poi_id is not None else None
        response = create_location_response_json(closest_loc, closest_poi, min_distance)
        #TODO: if you locate user inform  GROUP analytics (see example) + create a db Entry in UserLocation model
        print(response)
    if response is not None:
        message.reply_channel.send({
            "text": dumps(response)
        })
