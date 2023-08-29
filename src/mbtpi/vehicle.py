from urls import urls, session
from universals import set_params, get


class VEHICLE(object):
    """Represents a MBTA vehicle. Takes in json with 'id', 'type' keys, 'links', 'relationships' and 'attributes' dict"""

    def __init__(self, json):
        """Stores each value returned from the MBTA API as a field"""
        self.type = json["type"]
        self.id = json["id"]
        self.links = json["links"]

        if "relationships" in json:
            self.__set_relationships(json["relationships"])

        self.__set_attributes(json["attributes"])

    def __str__(self):
        """Returns the id and label of the vehicle"""
        return self.id + ": " + self.label

    def __set_relationships(self, json):
        """Sets each given relationship"""
        if "route" in json:
            self.route = json["route"]["data"]["id"]
        if "stop" in json:
            self.stop = json["stop"]["data"]["id"]
        if "trip" in json:
            self.trip = json["trip"]["data"]["id"]

    def __set_attributes(self, json):
        """Sets each given attribute of the vehicle"""
        self.bearing = json["bearing"]
        self.carriages = json["carriages"]
        self.current_status = json["current_status"]
        self.current_stop_sequence = json["current_stop_sequence"]
        self.label = json["label"]
        self.direction_id = json["direction_id"]
        self.latitude = json["latitude"]
        self.longitude = json["longitude"]
        self.occupancy_status = json["occupancy_status"]
        self.speed = json["speed"]
        self.updated_at = json["updated_at"]


def vehicles(page_offset: int = None,
             page_limit: int = None,
             sort: str = None,
             fields_vehicle: list[str] | str = None,
             include: list[str] = None,
             filter_id: list[str] | str = None,
             trip: list[str] | str = None,
             label: list[str] | str = None,
             route: list[str] | str = None,
             direction_id: str = None,
             route_type: list[str] | str = None,
             json: bool = False):
    """Makes a request to the API.
    Default behavior returns unsorted list of VEHICLE objects containing all vehicles from API.
    Accepts all parameters that can be passed to the /vehicles endpoint.

    :param json: return JSON instead of VEHICLE objects
    """
    vehicle_session = set_params(session, page_offset=page_offset, page_limit=page_limit, sort=sort,
                                 fields_vehicle=fields_vehicle, include=include, filter_id=filter_id, trip=trip,
                                 label=label, route=route, direction_id=direction_id, route_type=route_type)
    json_response = get(vehicle_session, urls.vehicle_url())

    if json:
        return json_response
    else:
        vehicles = []
        for json in json_response["data"]:
            vehicles.append(VEHICLE(json))
        return vehicles


def vehicle_by_id(vehicle_id: str,
                  fields_vehicle: list[str] | str = None,
                  include: list[str] = None,
                  json: bool = False):
    """Makes a request to the API.
    Default behavior returns a VEHICLE object with the id given.
    Accepts all parameters that can be passed to the /vehicles/{id} endpoint.

    :param vehicle_id: id of vehicle to return
    :param json: return JSON instead of VEHICLE object
    """
    vehicle_session = set_params(session, fields_vehicle=fields_vehicle, include=include)
    json_response = get(vehicle_session, urls.vehicle_by_id_url(vehicle_id))

    if json:
        return json_response
    else:
        return VEHICLE(json_response["data"])


def all_vehicles(json: bool = False):
    """Makes a request to the API. Default behavior returns unsorted list of VEHICLE objects containing all vehicles from API, passing no optional parameters.

    :param json: return JSON instead of VEHICLE objects
    """
    return vehicles(json=json)
