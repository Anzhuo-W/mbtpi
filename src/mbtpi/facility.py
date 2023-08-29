from urls import urls, session
from universals import set_params, get


class FACILITY(object):
    """Represents a MBTA facility. Takes in json with 'id', 'links', 'type' keys, 'relationships' and 'attributes' dicts"""

    def __init__(self, json):
        """Stores each value returned from the MBTA API as a field"""
        self.id = json["id"]
        self.links = json["links"]
        self.type = json["type"]

        if "relationships" in json:
            self.__set_relationships(json["relationships"])

        self.__set_attributes(json["attributes"])

    def __str__(self):
        """Returns the id and long name of the facility"""
        return self.id + ": " + self.long_name

    def __set_relationships(self, json):
        """Sets each given relationship"""
        if "stop" in json:
            self.stop = json["stop"]["data"]["id"]

    def __set_attributes(self, json):
        """Sets each given attribute of the facility"""
        self.latitude = json["latitude"]
        self.long_name = json["long_name"]
        self.longitude = json["longitude"]
        self.properties = json["properties"]
        self.short_name = json["short_name"]
        self.facility_type = json["type"]


def facilities(page_offset: int = None,
               page_limit: int = None,
               sort: str = None,
               fields_facility: list[str] | str = None,
               include: list[str] = None,
               stop: list[str] | str = None,
               type: list[str] | str = None,
               json: bool = False):
    """Makes a request to the API.
    Default behavior returns unsorted list of FACILITY objects containing all facilities from API.
    Accepts all parameters that can be passed to the /facilities endpoint.

    :param json: return JSON instead of FACILITY object
    """
    facility_session = set_params(session, page_offset=page_offset, page_limit=page_limit, sort=sort,
                                  fields_facility=fields_facility, include=include, stop=stop, type=type)
    json_response = get(facility_session, urls.facility_url())

    if json:
        return json_response
    else:
        facilities = []
        for json in json_response["data"]:
            facilities.append(FACILITY(json))
        return facilities


def facility_by_id(facility_id: str,
                   fields_facility: list[str] | str = None,
                   include: list[str] = None,
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
    """Makes a request to the API. Default behavior returns unsorted list of FACILITY objects containing all facilities from API, passing no optional parameters.

    :param json: return JSON instead of FACILITY objects
    """
    return facilities(json=json)
