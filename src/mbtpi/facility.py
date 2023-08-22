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


class FACILITY(object):
    """Represents a MBTA facility. Takes in json with 'id', 'links', 'type', 'relationships' keys,
    and 'attributes' list"""

    def __init__(self, json):
        """Stores each value returned from the MBTA API as a field"""
        self.id = json["id"]
        self.links = json["links"]
        self.relationships = json["relationships"]
        self.type = json["type"]

        self.__set_attributes(json["attributes"])

    def __str__(self):
        """Returns the id and long name of the facility"""
        return self.id + ": " + self.long_name

    def __set_attributes(self, json):
        """Sets each given attribute of the facility"""
        self.latitude = json["latitude"]
        self.long_name = json["long_name"]
        self.longitude = json["longitude"]
        self.properties = json["properties"]
        self.short_name = json["short_name"]
        self.facility_type = json["type"]


def facilities(page_offset: int = None, page_limit: int = None, sort: str = None,
               fields_facility: list[str] | str = None, include: list[str] = None,
               stop: list[str] | str = None, facility_type: list[str] | str = None, json: bool = False):
    """Makes a request to the API.
    Default behavior returns unsorted list of FACILITY objects containing all facilities from API.
    Accepts all parameters that can be passed to the /facilities endpoint.

    :param json: return JSON instead of FACILITY object
    """
    facility_session = set_params(session, page_offset=page_offset, page_limit=page_limit, sort=sort,
                                  fields_facility=fields_facility, include=include, stop=stop,
                                  facility_type=facility_type)
    json_response = get(facility_session, urls.facility_url())

    if json:
        return json_response
    else:
        facilities = []
        for json in json_response["data"]:
            facilities.append(FACILITY(json))
        return facilities


def facility_by_id(facility_id: str, fields_facility: list[str] | str = None, include: list[str] = None,
                   json: bool = False):
    """Makes a request to the API.
    Default behavior returns a FACILITY object with the id given.
    Accepts all parameters that can be passed to the /facilities/{id} endpoint.

    :param facility_id: id of facility to return
    :param json: return JSON instead of FACILITY objects
    """
    facility_session = set_params(session, fields_facility=fields_facility, include=include)
    json_response = get(facility_session, urls.facility_by_id_url(facility_id))

    if json:
        return json_response
    else:
        return FACILITY(json_response["data"])


def all_facilities(json: bool = False):
    """Makes a request to the API. Default behavior returns unsorted list of FACILITY objects containing all facilities
    from API, passing no optional parameters.

    :param json: return JSON instead of FACILITY objects
    """
    return facilities(json=json)
