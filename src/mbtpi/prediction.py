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


class PREDICTION(object):
    """Represents a MBTA prediction. Takes in json with 'id', 'type' keys, 'relationships' and 'attributes' dict"""

    def __init__(self, json):
        """Stores each value returned from the MBTA API as a field"""
        self.type = json["type"]
        self.id = json["id"]

        self.__set_relationships(json["relationships"])
        self.__set_attributes(json["attributes"])

    def __str__(self):
        """Returns the id and route of the prediction"""
        return self.id + ": " + self.route

    def __set_relationships(self, json):
        if "vehicle" in json:
            self.vehicle = json["vehicle"]["data"]["id"]
        if "trip" in json:
            self.trip = json["trip"]["data"]["id"]
        if "stop" in json:
            self.stop = json["stop"]["data"]["id"]
        if "schedule" in json:
            self.schedule = json["schedule"]["data"]["id"]
        if "route" in json:
            self.route = json["route"]["data"]["id"]
        if "alerts" in json:
            self.alerts = json["alerts"]["data"]["id"]

    def __set_attributes(self, json):
        """Sets each given attribute of the prediction"""
        self.stop_sequence = json["stop_sequence"]
        self.status = json["status"]
        self.schedule_relationship = json["schedule_relationship"]
        self.direction_id = json["direction_id"]
        self.departure_time = json["departure_time"]
        self.arrival_time = json["arrival_time"]


def predictions(page_offset: int = None,
                page_limit: int = None,
                sort: str = None,
                fields_prediction: list[str] | str = None,
                include: list[str] = None,
                latitude: str = None,
                longitude: str = None,
                radius: str = None,
                direction_id: str = None,
                route_type: list[str] | str = None,
                stop: list[str] | str = None,
                route: list[str] | str = None,
                trip: list[str] | str = None,
                route_pattern: list[str] | str = None,
                json: bool = False):
    """Makes a request to the API. A filter[] must be applied.
    Default behavior returns unsorted list of PREDICTION objects containing all predictions from API.
    Accepts all parameters that can be passed to the /predictions endpoint.

    :param json: return JSON instead of PREDICTION objects
    """
    filters = [latitude, longitude, radius, direction_id, route_type, stop, route, trip, route_pattern]
    if filters.count(None) == len(filters):
        raise ValueError("At least one filter[] must be present for predictions to be returned.")

    if latitude and not longitude or longitude and not latitude:
        raise ValueError("If setting latitude or longitude filters, both must be provided.")

    prediction_session = set_params(session, page_offset=page_offset, page_limit=page_limit, sort=sort,
                                    fields_prediction=fields_prediction, include=include, latitude=latitude,
                                    longitude=longitude, radius=radius, direction_id=direction_id,
                                    route_type=route_type, stop=stop,
                                    route=route, trip=trip, route_pattern=route_pattern)
    json_response = get(prediction_session, urls.predictions_url())

    if json:
        return json_response
    else:
        prediction_list = []
        for json in json_response["data"]:
            prediction_list.append(PREDICTION(json))
        return prediction_list
