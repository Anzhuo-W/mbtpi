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


class SHAPE(object):
    """Represents a MBTA shape. Takes in json with 'id', 'type' keys, 'links' and 'attributes' dict"""

    def __init__(self, json):
        """Stores each value returned from the MBTA API as a field"""
        self.type = json["type"]
        self.id = json["id"]
        self.links = json["links"]

        self.__set_attributes(json["attributes"])

    def __str__(self):
        """Returns the id of the shape"""
        return self.id

    def __set_attributes(self, json):
        """Sets each given attribute of the shape"""
        self.polyline = json["polyline"]


def shapes(route: list[str] | str, page_offset: int = None, page_limit: int = None, sort: str = None,
           fields_shape: list[str] | str = None, json: bool = False):
    """Makes a request to the API. A route filter[] must be applied.
    Default behavior returns unsorted list of SHAPE objects containing all shapes from API.
    Accepts all parameters that can be passed to the /shapes endpoint.

    :param json: return JSON instead of SHAPE objects
    """
    shape_session = set_params(session, page_offset=page_offset, page_limit=page_limit, sort=sort,
                               fields_shape=fields_shape, route=route)
    json_response = get(shape_session, urls.shape_url())

    if json:
        return json_response
    else:
        shapes = []
        for json in json_response["data"]:
            shapes.append(SHAPE(json))
        return shapes


def shape_by_id(shape_id: str, fields_shape: list[str] | str = None, json: bool = False):
    """Makes a request to the API.
    Default behavior returns a SHAPE object with the id given.
    Accepts all parameters that can be passed to the /shapes/{id} endpoint.

    :param shape_id: id of shape to return
    :param json: return JSON instead of SERVICE object
    """
    shape_session = set_params(session, fields_shape=fields_shape)
    json_response = get(shape_session, urls.shape_by_id_url(shape_id))

    if json:
        return json_response
    else:
        return SHAPE(json_response["data"])
