# TODO: this weight is based on trial and error. Subject to reconsideration
ORIENTATION_WEIGHT = 0.15


# TODO: This way of estimating the distance is a fast, possibly not accurate estimation of it. Better use smthng better.
def compute_magnetic_distance(fp1, fp2):
    distance = 0
    distance += abs(fp1.magnetic_x - fp2.magnetic_x)
    distance += abs(fp1.magnetic_y - fp2.magnetic_y)
    distance += abs(fp1.magnetic_z - fp2.magnetic_z)
    return distance


def compute_orientation_distance(fp1, fp2):
    distance = 0
    distance += ORIENTATION_WEIGHT * abs(fp1.orientation_x - fp2.orientation_x)
    distance += ORIENTATION_WEIGHT * abs(fp1.orientation_y - fp2.orientation_y)
    distance += ORIENTATION_WEIGHT * abs(fp1.orientation_z - fp2.orientation_z)
    return distance


def wifi_rssi_distance(fp1, fp2):
    distance = 0
    distance += abs(fp1.wifi_rssi - fp2.wifi_rssi)
    return distance


def compute_distance(fp1, fp2):
    distance = 0
    distance += compute_magnetic_distance(fp1, fp2)
    distance += compute_orientation_distance(fp1, fp2)
    distance += wifi_rssi_distance(fp1, fp2)
    return distance


def create_location_response_json(fingerprint_loc, poi, distance):
    # TODO: If it is a POI
    #       and has a creator
    #       include in the response Creator attrs (at least id)
    if not fingerprint_loc.is_poi and poi is not None:
        closest_poi = poi.related_poi.id
        image = poi.related_poi.image
    else:
        closest_poi = -1
    return dict(
        fingerPrintDistance=int(distance),
        closestFingerPrintedLocation=fingerprint_loc.id,
        closestPoi=closest_poi)
