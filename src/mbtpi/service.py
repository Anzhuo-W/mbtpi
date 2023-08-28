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


class SERVICE(object):
    """Represents a MBTA service. Takes in json with 'id', 'links', 'type', 'relationships' keys,
    and 'attributes' dict"""

    def __init__(self, json):
        """Stores each value returned from the MBTA API as a field"""
        self.type = json["type"]
        self.links = json["links"]
        self.id = json["id"]

        if "relationships" in json:
            self.relationships = json["relationships"]

        self.__set_attributes(json["attributes"])

    def __str__(self):
        """Returns the id and description of the service"""
        return self.id + ": " + self.description

    def __set_attributes(self, json):
        """Sets each given attribute of the service"""
        self.valid_days = json["valid_days"]
        self.start_date = json["start_date"]
        self.schedule_typicality = json["schedule_typicality"]
        self.schedule_type = json["schedule_type"]
        self.schedule_name = json["schedule_name"]
        self.removed_dates_notes = json["removed_dates_notes"]
        self.removed_dates = json["removed_dates"]
        self.rating_start_date = json["rating_start_date"]
        self.rating_end_date = json["rating_end_date"]
        self.rating_description = json["rating_description"]
        self.end_date = json["end_date"]
        self.description = json["description"]
        self.added_dates_notes = json["added_dates_notes"]
        self.added_dates = json["added_dates"]


def services(page_offset: int = None, page_limit: int = None, sort: str = None, fields_service: list[str] | str = None,
             filter_id: list[str] | str = None, route: list[str] | str = None, json: bool = False):
    """Makes a request to the API. A filter[] must be applied.
    Default behavior returns unsorted list of SERVICE objects containing all services from API.
    Accepts all parameters that can be passed to the /services endpoint.

    :param json: return JSON instead of SERVICE objects
    """
    filters = [filter_id, route]
    if filters.count(None) == len(filters):
        raise ValueError("At least one filter[] must be present for services to be returned.")

    service_session = set_params(session, page_offset=page_offset, page_limit=page_limit, sort=sort,
                                 fields_service=fields_service, filter_id=filter_id, route=route)
    json_response = get(service_session, urls.service_url())

    if json:
        return json_response
    else:
        services = []
        for json in json_response["data"]:
            services.append(SERVICE(json))
        return services


def service_by_id(service_id: str, fields_service: list[str] | str = None, json: bool = False):
    """Makes a request to the API.
    Default behavior returns a SERVICE object with the id given.
    Accepts all parameters that can be passed to the /services/{id} endpoint.

    :param service_id: id of service to return
    :param json: return JSON instead of SERVICE object
    """
    service_session = set_params(session, fields_service=fields_service)
    json_response = get(service_session, urls.service_by_id_url(service_id))

    if json:
        return json_response
    else:
        return SERVICE(json_response["data"])
