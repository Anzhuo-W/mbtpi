from urls import urls, session
from universals import set_params, get


class STOP(object):
    """Represents a MBTA stop. Takes in json with 'id', 'type' keys, 'links', 'relationships' and 'attributes' dict"""

    def __init__(self, json):
        """Stores each value returned from the MBTA API as a field"""
        self.type = json["type"]
        self.id = json["id"]
        self.links = json["links"]

        if "relationships" in json:
            self.__set_relationships(json["relationships"])

        self.__set_attributes(json["attributes"])

    def __str__(self):
        """Returns the id and name of the stop, and a line/route description"""
        return self.id + ": " + self.name + " " + self.description

    def __set_relationships(self, json):
        """Sets each given relationship"""
        if "child_stops" in json:
            self.child_stops = json["child_stops"]["data"]
        if "connecting_stops" in json:
            self.connecting_stops = json["connecting_stops"]["data"]
        if "facilities" in json:
            self.facilities = json["facilities"]["data"]
        if "parent_station" in json:
            self.route = json["parent_station"]["data"]["id"]
        if "route" in json:
            self.route = json["route"]["data"]["id"]

    def __set_attributes(self, json):
        """Sets each given attribute of the stop"""
        self.wheelchair_boarding = json["wheelchair_boarding"]
        self.vehicle_type = json["vehicle_type"]
        self.platform_name = json["platform_name"]
        self.platform_code = json["platform_code"]
        self.on_street = json["on_street"]
        self.name = json["name"]
        self.municipality = json["municipality"]
        self.longitude = json["longitude"]
        self.location_type = json["location_type"]
        self.latitude = json["latitude"]
        self.description = json["description"]
        self.at_street = json["at_street"]
        self.address = json["address"]

    def coordinates(self) -> list[float]:
        """Returns the [latitude, longitude] of the stop"""
        return [float(self.latitude), float(self.longitude)]


def stops(page_offset: int = None,
          page_limit: int = None,
          sort: str = None,
          fields_stop: list[str] | str = None,
          include: list[str] = None,
          date: str = None,
          direction_id: str = None,
          latitude: str = None,
          longitude: str = None,
          radius: str = None,
          filter_id: list[str] | str = None,
          route_type: list[str] | str = None,
          route: list[str] | str = None,
          service: list[str] | str = None,
          location_type: list[str] | str = None,
          json: bool = None):
    """Makes a request to the API.
    Default behavior returns unsorted list of STOP objects containing all stops from API.
    Accepts all parameters that can be passed to the /stops endpoint.

    :param json: return JSON instead of STOP objects
    """
    stop_session = set_params(session, page_offset=page_offset, page_limit=page_limit, sort=sort,
                              fields_stop=fields_stop, include=include, date=date, direction_id=direction_id,
                              latitude=latitude, longitude=longitude, radius=radius, filter_id=filter_id,
                              route_type=route_type, route=route, service=service, location_type=location_type)
    json_response = get(stop_session, urls.stop_url())

    if json:
        return json_response
    else:
        stops = []
        for json in json_response["data"]:
            stops.append(STOP(json))
        return stops


def stop_by_id(stop_id: str,
               fields_stop: list[str] | str = None,
               include: list[str] = None,
               json: bool = False):
    """Makes a request to the API.
    Default behavior returns a STOP object with the id given.
    Accepts all parameters that can be passed to the /stops/{id} endpoint.

    :param stop_id: id of stop to return
    :param json: return JSON instead of STOP object
    """
    stop_session = set_params(session, fields_stop=fields_stop, include=include)
    json_response = get(stop_session, urls.stop_by_id_url(stop_id))

    if json:
        return json_response
    else:
        return STOP(json_response["data"])


def all_stops(json: bool = False):
    """Makes a request to the API. Default behavior returns unsorted list of STOP objects containing all stops from API, passing no optional parameters.

    :param json: return JSON instead of STOP objects
    """
    return stops(json=json)
