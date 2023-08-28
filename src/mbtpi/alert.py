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


class ALERT(object):
    """Represents a MBTA alert. Takes in json with 'id', 'links', 'type' keys, 'relationships' and 'attributes' dict"""

    def __init__(self, json):
        """Stores each value returned from the MBTA API as a field"""
        self.id = json["id"]
        self.links = json["links"]
        self.type = json["type"]

        if "relationships" in json:
            self.__set_relationships(json["relationships"])

        self.__set_attributes(json["attributes"])

    def __str__(self):
        """Returns the id and header of the alert"""
        return self.id + ": " + self.header

    def __set_relationships(self, json):
        """Sets each given relationship"""
        if "stops" in json:
            self.stops = json["stops"]["data"]
        if "routes" in json:
            self.routes = json["routes"]["data"]
        if "trips" in json:
            self.trips = json["trips"]["data"]
        if "facilities" in json:
            self.facilities = json["facilities"]["data"]

    def __set_attributes(self, json):
        """Sets each given attribute of the alert"""
        self.active_period = json["active_period"]
        self.banner = json["banner"]
        self.cause = json["cause"]
        self.created_at = json["created_at"]
        self.description = json["description"].strip()
        self.effect = json["effect"]
        self.header = json["header"].strip()
        self.informed_entity = json["informed_entity"]
        self.lifecycle = json["lifecycle"]
        self.service_effect = json["service_effect"]
        self.severity = json["severity"]
        self.short_header = json["short_header"].strip()
        self.timeframe = json["timeframe"]
        self.updated_at = json["updated_at"]
        self.url = json["url"]

    def full_description(self):
        """Returns the alert header and its description"""
        return self.header + "\n" + self.description


def alerts(page_offset: int = None,
           page_limit: int = None,
           sort: str = None,
           fields_alert: list[str] | str = None,
           include: list[str] = None,
           activity: list[str] | str = None,
           route_type: str = None,
           direction_id: str = None,
           route: list[str] | str = None,
           stop: list[str] | str = None,
           trip: list[str] | str = None,
           facility: list[str] | str = None,
           filter_id: list[str] | str = None,
           banner: bool = None,
           datetime: str = None,
           lifecycle: list[str] = None,
           severity: list[str] = None,
           json: bool = False):
    """Makes a request to the API.
    Default behavior returns unsorted list of ALERT objects containing all alerts from API.
    Accepts all parameters that can be passed to the /alerts endpoint.

    :param json: return JSON instead of ALERT objects
    """
    alert_session = set_params(session, page_offset=page_offset, page_limit=page_limit, sort=sort,
                               fields_alert=fields_alert, include=include, activity=activity, route_type=route_type,
                               direction_id=direction_id, route=route, stop=stop, trip=trip, facility=facility,
                               filter_id=filter_id, banner=banner, datetime=datetime, lifecycle=lifecycle,
                               severity=severity)
    json_response = get(alert_session, urls.alert_url())

    if json:
        return json_response
    else:
        alerts = []
        for json in json_response["data"]:
            alerts.append(ALERT(json))
        return alerts


def alert_by_id(alert_id: int, fields_alert: list[str] | str = None, include: list[str] = None, json: bool = False):
    """Makes a request to the API.
    Default behavior returns an ALERT object with the id given.
    Accepts all parameters that can be passed to the /alerts/{id} endpoint.

    :param alert_id: id of alert to return
    :param json: return JSON instead of ALERT object
    """
    alert_session = set_params(session, fields_alert=fields_alert, include=include)
    json_response = get(alert_session, urls.alert_by_id_url(alert_id))

    if json:
        return json_response
    else:
        return ALERT(json_response["data"])


def all_alerts(json: bool = False):
    """Makes a request to the API. Default behavior returns unsorted list of ALERT objects containing all alerts from API, passing no optional parameters.

    :param json: return JSON instead of ALERT objects
    """
    return alerts(json=json)
