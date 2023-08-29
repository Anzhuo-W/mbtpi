from urls import urls, session
from universals import set_params, get


class ROUTE(object):
    """Represents a MBTA route. Takes in json with 'id', 'type', 'links', 'relationships' keys, and 'attributes' list"""

    def __init__(self, json):
        """Stores each value returned from the MBTA API as a field"""
        self.type = json["type"]
        self.links = json["links"]
        self.id = json["id"]

        if "relationships" in json:
            self.__set_relationships(json["relationships"])

        self.__set_attributes(json["attributes"])

    def __str__(self):
        """Returns the id and long name of the route"""
        return self.id + ": " + self.long_name

    def __set_relationships(self, json):
        """Sets each given relationship"""
        if "stop" in json:
            self.stop = json["stop"]["data"]["id"]
        if "line" in json:
            self.line = json["line"]["data"]["id"]
        if "route_patterns" in json:
            self.route_patterns = json["route_patterns"]["data"]

    def __set_attributes(self, json):
        """Sets each given attribute of the route"""
        self.route_type = json["type"]
        self.text_color = json["text_color"]
        self.sort_order = json["sort_order"]
        self.short_name = json["short_name"]
        self.long_name = json["long_name"]
        self.fare_class = json["fare_class"]
        self.direction_names = json["direction_names"]
        self.direction_destinations = json["direction_destinations"]
        self.description = json["description"]
        self.color = json["color"]


def routes(page_offset: int = None,
           page_limit: int = None,
           sort: str = None,
           fields_route: list[str] | str = None,
           include: list[str] = None,
           stop: list[str] | str = None,
           type: list[str] | str = None,
           direction_id: str = None,
           date: str = None,
           filter_id: list[str] | str = None,
           json: bool = False):
    """Makes a request to the API.
    Default behavior returns unsorted list of ROUTE objects containing all routes from API.
    Accepts all parameters that can be passed to the /routes endpoint.

    :param json: return JSON instead of ROUTE objects
    """
    route_session = set_params(session, page_offset=page_offset, page_limit=page_limit, sort=sort,
                               fields_route=fields_route, include=include, stop=stop, type=type,
                               direction_id=direction_id, date=date, filter_id=filter_id)
    json_response = get(route_session, urls.route_url())

    if json:
        return json_response
    else:
        routes = []
        for json in json_response["data"]:
            routes.append(ROUTE(json))
        return routes


def route_by_id(route_id: str,
                fields_route: list[str] | str = None,
                include: list[str] = None,
                json: bool = False):
    """Makes a request to the API.
    Default behavior returns a ROUTE object with the id given.
    Accepts all parameters that can be passed to the /routes/{id} endpoint.

    :param route_id: id of route to return
    :param json: return JSON instead of ROUTE object
    """
    route_session = set_params(session, fields_route=fields_route, include=include)
    json_response = get(route_session, urls.route_by_id_url(route_id))

    if json:
        return json_response
    else:
        return ROUTE(json_response["data"])


def all_routes(json: bool = False):
    """Makes a request to the API. Default behavior returns unsorted list of ROUTE objects containing all routes from
    API, passing no optional parameters.

    :param json: return JSON instead of ROUTE objects
    """
    return routes(json=json)
