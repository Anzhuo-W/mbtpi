from urls import urls, session
from universals import set_params, get


class LIVE_FACILITY(object):
    """Represents a MBTA live facility. Takes in json with 'id', 'links', 'type' keys, 'relationships' and 'attributes' dicts"""

    def __init__(self, json):
        """Stores each value returned from the MBTA API as a field"""
        self.type = json["type"]
        self.links = json["links"]
        self.id = json["id"]

        if "relationships" in json:
            self.__set_relationships(json["relationships"])

        self.__set_attributes(json["attributes"])

    def __str__(self):
        """Returns the id and last update time of the live facility"""
        return self.id + ": " + self.updated_at

    def __set_relationships(self, json):
        """Sets each given relationship"""
        if "facility" in json:
            self.facility = json["facility"]["data"]["id"]

    def __set_attributes(self, json):
        """Sets each given attribute of the live facility"""
        self.updated_at = json["updated_at"]
        self.properties = json["properties"]


def live_facilities(filter_id: list[str] | str,
                    page_offset: int = None,
                    page_limit: int = None,
                    sort: str = None,
                    include: str = None,
                    json: bool = False):
    """Makes a request to the API. Requires at least one filter[]. Returns live data about specific parking facilities.
    Accepts all parameters that can be passed to the /live_facilities endpoint.

    :param json: return JSON instead of LIVE_FACILITY objects
    """
    facility_session = set_params(session, page_offset=page_offset, page_limit=page_limit, sort=sort,
                                  include=include, filter_id=filter_id)
    json_response = get(facility_session, urls.live_facility_url())

    if json:
        return json_response
    else:
        live_facilities = []
        for json in json_response["data"]:
            live_facilities.append(LIVE_FACILITY(json))
        return live_facilities


def live_facility_by_id(facility_id: str,
                        include: list[str] = None,
                        json: bool = False):
    """Makes a request to the API. Returns live data about a specific parking facility.
    Default behavior returns a LIVE_FACILITY object with the facility id given.
    Accepts all parameters that can be passed to the /live_facilities/{id} endpoint.

    :param facility_id: id of facility to return
    :param json: return JSON instead of LIVE_FACILITY object
    """
    facility_session = set_params(session, include=include)
    json_response = get(facility_session, urls.live_facility_by_id_url(facility_id))

    if json:
        return json_response
    else:
        return LIVE_FACILITY(json_response["data"])
