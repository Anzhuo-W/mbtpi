# Copyright (c) 2023 Anzhuo-W
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from urls import urls, session
from universals import set_params, get


class ROUTE_PATTERN(object):
    """Represents a MBTA route pattern. Takes in json with 'id', 'type', 'links', 'relationships' keys,
    and 'attributes' dict"""

    def __init__(self, json):
        """Stores each value returned from the MBTA API as a field"""
        self.type = json["type"]
        self.links = json["links"]
        self.id = json["id"]

        if "relationships" in json:
            self.__set_relationships(json["relationships"])

        self.__set_attributes(json["attributes"])

    def __str__(self):
        """Returns the id and name of the route pattern"""
        return self.id + ": " + self.name

    def __set_relationships(self, json):
        """Sets each given relationship"""
        if "route" in json:
            self.route = json["route"]["data"]["id"]
        if "representative_trip" in json:
            self.representative_trip = json["representative_trip"]["data"]["id"]

    def __set_attributes(self, json):
        """Sets each given attribute of the route pattern"""
        self.canonical = json["canonical"]
        self.direction_id = json["direction_id"]
        self.name = json["name"]
        self.sort_order = json["sort_order"]
        self.time_desc = json["time_desc"]
        self.typicality = json["typicality"]


def route_patterns(page_offset: int = None,
                   page_limit: int = None,
                   sort: str = None,
                   fields_route_pattern: list[str] | str = None,
                   include: list[str] = None,
                   filter_id: list[str] | str = None,
                   route: list[str] | str = None,
                   direction_id: str = None,
                   stop: list[str] | str = None,
                   canonical: bool = None,
                   json: bool = False):
    """Makes a request to the API.
    Default behavior returns unsorted list of ROUTE_PATTERN objects containing all route patterns from API.
    Accepts all parameters that can be passed to the /route_patterns endpoint.

    :param json: return JSON instead of ROUTE_PATTERN objects
    """
    route_pattern_session = set_params(session, page_offset=page_offset, page_limit=page_limit, sort=sort,
                                       fields_route_pattern=fields_route_pattern, include=include, filter_id=filter_id,
                                       route=route, direction_id=direction_id, stop=stop, canonical=canonical)
    json_response = get(route_pattern_session, urls.route_pattern_url())

    if json:
        return json_response
    else:
        route_patterns = []
        for json in json_response["data"]:
            route_patterns.append(ROUTE_PATTERN(json))
        return route_patterns


def route_pattern_by_id(route_pattern_id: str, fields_route_pattern: list[str] | str = None, include: list[str] = None,
                        json: bool = False):
    """Makes a request to the API.
    Default behavior returns a ROUTE_PATTERN object with the id given.
    Accepts all parameters that can be passed to the /route_patterns/{id} endpoint.

    :param route_pattern_id: id of route pattern to return
    :param json: return JSON instead of ROUTE_PATTERN object
    """
    route_pattern_session = set_params(session, fields_route_pattern=fields_route_pattern, include=include)
    json_response = get(route_pattern_session, urls.route_pattern_by_id_url(route_pattern_id))

    if json:
        return json_response
    else:
        return ROUTE_PATTERN(json_response["data"])


def all_route_patterns(json: bool = False):
    """Makes a request to the API.
    Default behavior returns unsorted list of ROUTE_PATTERN objects containing all route patterns from API, passing no optional parameters.

    :param json: return JSON instead of ROUTE_PATTERN objects
    """
    return route_patterns(json=json)
