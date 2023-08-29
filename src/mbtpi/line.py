from urls import urls, session
from universals import set_params, get


class LINE(object):
    """Represents a MBTA line. Takes in json with 'id', 'links', 'type' keys, 'relationships' and 'attributes' dicts"""

    def __init__(self, json):
        """Stores each value returned from the MBTA API as a field"""
        self.id = json["id"]
        self.links = json["links"]
        self.type = json["type"]

        if "relationships" in json:
            self.__set_relationships(json["relationships"])

        self.__set_attributes(json["attributes"])

    def __str__(self):
        """Returns the id and long name of the line"""
        return self.id + ": " + self.long_name

    def __set_relationships(self, json):
        """Sets each given relationship"""
        if "routes" in json:
            self.routes = json["routes"]["data"]["id"]

    def __set_attributes(self, json):
        """Sets each given attribute of the line"""
        self.color = json["color"]
        self.long_name = json["long_name"]
        self.short_name = json["short_name"]
        self.sort_order = json["sort_order"]
        self.text_color = json["text_color"]


def lines(page_offset: int = None,
          page_limit: int = None,
          sort: str = None,
          fields_line: list[str] | str = None,
          include: list[str] = None,
          filter_id: list[str] = None,
          json: bool = False):
    """Makes a request to the API.
    Default behavior returns unsorted list of LINE objects containing all lines from API.
    Accepts all parameters that can be passed to the /lines endpoint.

    :param json: return JSON instead of LINE objects
    """
    line_session = set_params(session, page_offset=page_offset, page_limit=page_limit, sort=sort,
                              fields_line=fields_line, include=include, filter_id=filter_id)
    json_response = get(line_session, urls.line_url())

    if json:
        return json_response
    else:
        lines = []
        for json in json_response["data"]:
            lines.append(LINE(json))
        return lines


def line_by_id(line_id: int,
               fields_line: list[str] | str = None,
               include: list[str] = None,
               json: bool = False):
    """Makes a request to the API.
    Default behavior returns a LINE object with the id given.
    Accepts all parameters that can be passed to the /lines/{id} endpoint.

    :param line_id: id of line to return
    :param json: return JSON instead of LINE object
    """
    line_session = set_params(session, fields_line=fields_line, include=include)
    json_response = get(line_session, urls.line_by_id_url(line_id))

    if json:
        return json_response
    else:
        return LINE(json_response["data"])


def all_lines(json: bool = False):
    """Makes a request to the API. Default behavior returns unsorted list of LINE objects containing all lines from API, passing no optional parameters.

    :param json: return JSON instead of LINE objects
    """
    return lines(json=json)
