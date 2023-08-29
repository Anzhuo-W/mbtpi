from urls import urls, session
from universals import set_params, get


class TRIP(object):
    """Represents a MBTA trip. Takes in json with 'id', 'type' keys, 'links', 'relationships' and 'attributes' dict"""

    def __init__(self, json):
        """Stores each value returned from the MBTA API as a field"""
        self.type = json["type"]
        self.id = json["id"]
        self.links = json["links"]

        if "relationships" in json:
            self.__set_relationships(json["relationships"])
        self.__set_attributes(json["attributes"])

    def __str__(self):
        """Returns the id and name of the trip, and the headsign"""
        return self.id + ": " + self.name + " " + self.headsign

    def __set_relationships(self, json):
        """Sets each given relationship"""
        if "route" in json:
            self.route = json["route"]["data"]["id"]
        if "vehicle" in json:
            self.vehicle = json["vehicle"]["data"]["id"]
        if "service" in json:
            self.service = json["service"]["data"]["id"]
        if "shape" in json:
            self.shape = json["shape"]["data"]["id"]
        if "predictions" in json:
            self.predictions = json["predictions"]["data"]
        if "route_pattern" in json:
            self.route_pattern = json["route_pattern"]["data"]["id"]
        if "stops" in json:
            self.stops = json["stops"]["data"]

        # experimental feature
        if "occupancy" in json:
            self.occupancy = json["occupancy"]["data"]

    def __set_attributes(self, json):
        """Sets each given attribute of the trip"""
        self.wheelchair_accessible = json["wheelchair_accessible"]
        self.name = json["name"]
        self.headsign = json["headsign"]
        self.direction_id = json["direction_id"]
        self.block_id = json["block_id"]
        self.bikes_allowed = json["bikes_allowed"]


def trips(page_offset: int = None,
          page_limit: int = None,
          sort: str = None,
          fields_trip: list[str] | str = None,
          include: list[str] = None,
          date: str = None,
          direction_id: str = None,
          route: list[str] | str = None,
          route_pattern: list[str] | str = None,
          filter_id: list[str] | str = None,
          name: list[str] | str = None,
          json: bool = False):
    """Makes a request to the API. At least one id, route, route_pattern, or name filter[] must be applied.
    Default behavior returns unsorted list of TRIP objects containing all trips from API.
    Accepts all parameters that can be passed to the /trips endpoint.

    :param json: return JSON instead of TRIP objects
    """
    primary_filters = [filter_id, route, route_pattern, name]
    if primary_filters.count(None) == len(primary_filters):
        raise ValueError(
            "At least one id, route, route_pattern, or name filter[] must be present for trips to be returned.")

    trip_session = set_params(session, page_offset=page_offset, page_limit=page_limit, sort=sort,
                              fields_trip=fields_trip, include=include, date=date, direction_id=direction_id,
                              route=route, route_pattern=route_pattern, filter_id=filter_id, name=name)
    json_response = get(trip_session, urls.trip_url())

    if json:
        return json_response
    else:
        trips = []
        for json in json_response["data"]:
            trips.append(TRIP(json))
        return trips


def trip_by_id(trip_id: str,
               fields_trip: list[str] | str = None,
               include: list[str] = None,
               json: bool = False):
    """Makes a request to the API.
    Default behavior returns a TRIP object with the id given.
    Accepts all parameters that can be passed to the /trips/{id} endpoint.

    :param trip_id: id of trip to return
    :param json: return JSON instead of TRIP object
    """
    trip_session = set_params(session, fields_trip=fields_trip, include=include)
    json_response = get(trip_session, urls.trip_by_id_url(trip_id))

    if json:
        return json_response
    else:
        return TRIP(json_response["data"])
