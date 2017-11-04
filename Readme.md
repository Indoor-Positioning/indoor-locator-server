# Indoor locator server

This server is to support the [indoor locator](https://github.com/Indoor-Positioning/indoor-locator) android app.
The client (android app) talks via a websocket - powered by [django channels](https://channels.readthedocs.io/en/stable/) - to the server
in order to add Point of Interests, Finger Printed locations, and Fingerprints, and retrieve the matched
location from the server.

### Deploy

* Install requirements stored in requirements.txt
* Deploy local Redis server (should listen at port 6379). If docker is available: `docker pull redis` and then `docker run  -p 6379:6379 -d redis`
* Run django server.

Database Schema:

![Database Schema](db_diagram_updated.png)

#### Tables Explanation

* `Floor Plan`. Stores the floor plans. Must be added beforehand, by the django admin. The resource_name corresponds to the drawable png that should reside
in the android apk.
* `PointOfInterest`. Stores the POIs of the current floor plan. These can be paintings / statues on a museum, etc
* `FingerPrintedLocation`. Stores the locations that are about to be fingerprinted.
* `FingerPrint`. Stores the fingerprint of the various locations.
* `Creators`. (Work in Progress)  This table is about to store the creators of the "PointOfInterest" (e.g the paintings in a museum).
* `UserLocations`. (Work in Progress) This table is about to store the locations where the users are located. Something like a location timeline.

### Supported Commands

Django models are serialized - deserialized to the jSon commands below through the websocket. In order to add a new command, update `ws_receive` method 
of [consumers.py](locator/consumers.py#L19) and add the logic to serialize - deserialize  the django model (in the class of the model).

1. `GET_FLOOR_PLANS`.

This command is sent by the client so as to retrieve the floor plans which are currently saved in the database.

```json
{
  "command" : "GET_FLOOR_PLANS"
}
```

The server responds with a json of the following form:

```json
[
    {
      "id" : "<floor_plan_id>",
      "name" : "<floor_plan_name>",
      "resourceName" : "<resource_name_of_floor_plan_image>"
    }
]

```

2. `GET_LOCATIONS`

This command is sent by the client to retrieve the locations which are fingerprinted inside the requested floorPlan

```json
{
  "command" : "GET_LOCATIONS",
  "floorPlanId" : "<floor_plan_id>"
}
```
The server responds with the saved locations in the database:

```json
[
    {
      "id" : "<point_of_interest_id>",
      "floorPlanId" : "<floor_plan_id of the requested locations>",
      "relatedFingerPrintedLocId" : "<the related entry in the FingerPrintedLocation table>",
      "relatedPoi" : "<the related (closest) POI id - this may also be the POI it self if isPoi is true",
      "isPoi" : "<True if this entry is a POI / False otherwise>",
      "xCoord" : "<the X coordinate of the location with respect to the floor plan>",
      "yCoord" : "<the X coordinate of the location with respect to the floor plan>"
    }
]

```


3. `GET_POIS`

This command is sent by the client to retrieve the locations which are fingerprinted inside the requested floorPlan

```json
{
  "command" : "GET_POIS",
  "floorPlanId" : "<floor_plan_id>"
}
```

The server responds with the saved Points of Interest in the database:

```json
[
    {
      "id" : "<point_of_interest_id>",
      "name" : "<point_of_interest_name (if applicable) or else N/A>",
      "floorPlanId" : "<floor_plan_id of the requested POIs>",
      "relatedFingerPrintedLocId" : "<the related entry in the FingerPrintedLocation table>",
      "xCoord" : "<the X coordinate of the POI with respect to the floor plan>",
      "yCoord" : "<the X coordinate of the POI with respect to the floor plan>"
    }
]

```

4. `ADD_LOCATION`

This command is sent by the client to add a new location to the floor plan (user taps on the floor plan image, then coordinates are captured)

```json
{
  "command" : "ADD_LOCATION",
  "location" :
  {
        "floorPlanId" : "<floor_plan_id",
        "isPoi" : "False",
        "xCoord" : "<x_coordinate>",
        "yCoord" : "<Y_coordinate>"
  }
}
```
The server responds with the newly added location:

```json
  {
        "id" : "<new_location_id>",
        "floorPlanId" : "<floor_plan_id",
        "relatedPoi" : "-1 ; Must be added later by the floor plan administrator",
        "isPoi" : "False",
        "xCoord" : "<x_coordinate>",
        "yCoord" : "<Y_coordinate>"
  }

```


5. `ADD_POI`

This command is sent by the client to add a new POI to the floor plan (user long taps on the floor plan image, then coordinates are captured)
A respective FingerPrintedLoc entry is added to the database (see the schema for more details).

```json
{
  "command" : "ADD_POI",
  "poi" :
  {
        "floorPlanId" : "<floor_plan_id",
        "xCoord" : "<x_coordinate>",
        "yCoord" : "<Y_coordinate>"
  }
}
```
The server responds with the newly added location:

```json
  {
        "id" : "<new_poi_id>",
        "floorPlanId" : "<floor_plan_id",
        "name" : "<empty ; Must be added later by administrator",
        "relatedFingerPrintedLocId" : "The id of the respective FingerPrintedLocationId that was created along with this POI",
        "xCoord" : "<x_coordinate>",
        "yCoord" : "<Y_coordinate>"
  }

```

6. `ADD_FINGERPRINTS`

This command is sent by the client to upload recorded fingerprints (snapshots of the magnetic field values, orientation info, and wifi Rssi)

```json
{
  "command" : "ADD_FINGERPRINTS",
  "fingerPrintList" :
  [
    {
        "fingerPrintedLocationId" : "<id_of_FingerPrintedLocation>",
        "magneticX" : "<magnetic X value on X axis>",
        "magneticY" : "<magnetic X value on Y axis>",
        "magneticZ" : "<magnetic X value on Z axis>",
        "orientationX" : "<orientation (in degrees) on X axis>",
        "orientationY" : "<orientation (in degrees) on Y axis>",
        "orientationZ" : "<orientation (in degrees) on Z axis>",
        "wifiRssi" : "<rssi of the currently connected WLAN network (if enabled and connected)>"
    }
  ]
}
```
The server does not respond on this command (it just stores the fingerprints).

7. `LOCATE`

This command is sent by the client, along with the fingerprint of the client's current location,
and asks server to provide the estimated location by comparing the fingerprint with the already
stored fingerprints of the database.

```json
{
  "command" : "LOCATE",
  "floorPlanId" : "<id_of_the_current_floor_plan>",
  "fingerPrint" :
    {
        "magneticX" : "<magnetic X value on X axis>",
        "magneticY" : "<magnetic X value on Y axis>",
        "magneticZ" : "<magnetic X value on Z axis>",
        "orientationX" : "<orientation (in degrees) on X axis>",
        "orientationY" : "<orientation (in degrees) on Y axis>",
        "orientationZ" : "<orientation (in degrees) on Z axis>",
        "wifiRssi" : "<rssi of the currently connected WLAN network (if enabled and connected)>"
    }
}
```
The server then responds with the best matched FingerPrintedLocation:

```json
{
  "fingerPrintDistance" : "<the distance between the given fingerprint and its best match>",
  "closestFingerPrintedLocation" : "<the id of the matched fingerprint>",
  "closestPoi" : "<the closest PointOfInterest>"
}
```

### Locating the User

The `FingerPrint` table stores the recorded fingerprints - which where added to the server via the `ADD_FINGERPRINT` command. 
In order to locate the user we want to match the fingerprint (from the `LOCATE` command) with the fingerprints that are present in 
the database. The closest fingerprint (and its respective location - that it was recorded from) is assumed to be the user location.

Each fingerprint has 3 values that correspond to the 3 coordinates of the magnetic field, 3 values that correspond to the orientation of the
mobile and, optionally, the wifiRssi of the connected WLAN.

We compute the distance by simply substracting every coordinate from its counterpart, and summing the absolute values of these differences.
This is ofc a very basic estimation of the distance, and more sophisticated methods should be used (e.g Clustering Algorithms, nearest neighbors etc).

Each metric has a weight. For example, the orientation sensor is quite noisy so we try to minimize its effect via this weight. See 
[fingerprint_utils.py](indoor_locator/fingerprint_utils.py) for more details.

As soon as the closest fingerprint is found, we respond to the client with the id and the distance of the closest fingerprint. It is up to the
client to choose if this distance is close enough to assume a match against the current location of the mobile. A client may for example get 
a response with a distance that is considered far (e.g above a configured threshold) to assume a location match - in that case the user could not be located.


### Future work - Needs improvement

* Use a proper distance estimation algorithm and / or some Clustering - Nearest Neighbor techniques.
* Add "Creator" info for each Point Of Interest. Then we could recommend POIs from the same "Creator" when we locate a user in a POI
* Add info about user past locations (add entries to the `UserLocation` table).
* Add "Group Notifications" (utilizing group django channels) for events like user "log in " (first location of the user), location updates.
* Use some noise reduction techniques (e.g Kalman Filtering) to deal with the noisy measurements that come from the mobile's sensors?

Various TODOs have been added to the respective source files that capture the above reccomendations.