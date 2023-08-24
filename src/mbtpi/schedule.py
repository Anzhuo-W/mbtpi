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


class SCHEDULE(object):
    """Represents a MBTA schedule. Takes in json with 'id', 'type' keys, 'relationships' and 'attributes' dict"""

    def __init__(self, json):
        """Stores each value returned from the MBTA API as a field"""
        self.type = json["type"]
        self.id = json["id"]

        self.__set_relationships(json["relationships"])
        self.__set_attributes(json["attributes"])

    def __str__(self):
        """Returns the id and route of the schedule"""
        return self.id + ": " + self.route

    def __set_relationships(self, json):
        if "trip" in json:
            self.trip = json["trip"]["data"]["id"]
        if "stop" in json:
            self.stop = json["stop"]["data"]["id"]
        if "route" in json:
            self.route = json["route"]["data"]["id"]
        if "prediction" in json:
            self.prediction = json["prediction"]["data"]["id"]

    def __set_attributes(self, json):
        """Sets each given attribute of the schedule"""
        self.timepoint = json["timepoint"]
        self.stop_sequence = json["stop_sequence"]
        self.stop_headsign = json["stop_headsign"]
        self.pickup_type = json["pickup_type"]
        self.drop_off_type = json["drop_off_type"]
        self.direction_id = json["direction_id"]
        self.departure_time = json["departure_time"]
        self.arrival_time = json["arrival_time"]


def schedules(page_offset: int = None,
              page_limit: int = None,
              sort: str = None,
              fields_schedule: list[str] | str = None,
              include: list[str] = None,
              date: str = None,
              direction_id: str = None,
              route_type: list[str] | str = None,
              min_time: str = None,
              max_time: str = None,
              route: list[str] | str = None,
              stop: list[str] | str = None,
              trip: list[str] | str = None,
              stop_sequence: str = None,
              json: bool = False):
    """Makes a request to the API. A filter[] must be applied.
    Default behavior returns unsorted list of SCHEDULE objects containing all schedules from API.
    Accepts all parameters that can be passed to the /schedules endpoint.

    :param json: return JSON instead of SCHEDULE objects
    """
    primary_filters = [route, stop, trip]
    if primary_filters.count(None) == len(primary_filters):
        raise ValueError("At least one route, stop, or trip filter[] must be present for predictions to be returned.")

    schedule_session = set_params(session, page_offset=page_offset, page_limit=page_limit, sort=sort,
                                  fields_schedule=fields_schedule, include=include, date=date,
                                  direction_id=direction_id, route_type=route_type, min_time=min_time,
                                  max_time=max_time, route=route, stop=stop, trip=trip, stop_sequence=stop_sequence)
    json_response = get(schedule_session, urls.schedules_url())

    if json:
        return json_response
    else:
        schedule_list = []
        for json in json_response["data"]:
            schedule_list.append(SCHEDULE(json))
        return schedule_list
