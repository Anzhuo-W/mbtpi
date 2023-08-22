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

from urls import MBTA_API_KEY
from errors import BadRequestError, ForbiddenError, NotFoundError, NotAcceptableError, TooManyRequestsError
from os import environ
from dotenv import load_dotenv

load_dotenv()
OK = int(environ.get('OK'))
BAD_REQUEST = int(environ.get('BAD_REQUEST'))
FORBIDDEN = int(environ.get('FORBIDDEN'))
NOT_FOUND = int(environ.get('NOT_FOUND'))
NOT_ACCEPTABLE = int(environ.get('NOT_ACCEPTABLE'))
TOO_MANY_REQUESTS = int(environ.get('TOO_MANY_REQUESTS'))


def set_params(session,
               page_offset: int = None,
               page_limit: int = None,
               sort: str = None,
               fields_alert: list[str] | str = None,
               fields_facility: list[str] | str = None,
               fields_line: list[str] | str = None,
               fields_prediction: list[str] | str = None,
               fields_route: list[str] | str = None,
               fields_route_pattern: list[str] | str = None,
               fields_schedule: list[str] | str = None,
               fields_service: list[str] | str = None,
               fields_shape: list[str] | str = None,
               fields_stop: list[str] | str = None,
               fields_trip: list[str] | str = None,
               fields_vehicle: list[str] | str = None,
               include: list[str] = None,
               activity: list[str] | str = None,
               route_type: list[str] | str = None,
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
               facility_type: str = None,
               latitude: str = None,
               longitude: str = None,
               radius: str = None,
               route_pattern: list[str] | str = None,
               date: str = None,
               canonical: bool = None,
               min_time: str = None,
               max_time: str = None,
               stop_sequence: str = None,
               service: list[str] | str = None,
               location_type: list[str] | str = None,
               name: list[str] | str = None,
               label: list[str] | str = None):
    """Adds params to the session passed in. Supports all parameters for any endpoint of the MBTA API
    listed at https://api-v3.mbta.com/docs/swagger/index.html."""

    session.params = {}
    session.params['api_key'] = MBTA_API_KEY

    if page_offset:
        session.params["page[offset]"] = page_offset
    if page_limit:
        session.params["page[limit]"] = page_limit
    if sort:
        session.params["sort"] = sort

    # choose fields
    if fields_alert:
        session.params["fields[alert]"] = fields_alert
    if fields_facility:
        session.params["fields[facility]"] = fields_facility
    if fields_line:
        session.params["fields[line]"] = fields_line
    if fields_prediction:
        session.params["fields[prediction]"] = fields_prediction
    if fields_route:
        session.params["fields[route]"] = fields_route
    if fields_route_pattern:
        session.params["fields[route_pattern]"] = fields_route_pattern
    if fields_schedule:
        session.params["fields[schedule]"] = fields_schedule
    if fields_service:
        session.params["fields[service]"] = fields_service
    if fields_shape:
        session.params["fields[shape]"] = fields_shape
    if fields_stop:
        session.params["fields[stop]"] = fields_stop
    if fields_trip:
        session.params["fields[trip]"] = fields_trip
    if fields_vehicle:
        session.params["fields[vehicle]"] = fields_vehicle

    if include:
        session.params["include"] = include
    if activity:
        session.params["filter[activity]"] = activity
    if route_type:
        session.params["filter[route_type]"] = route_type
    if direction_id:
        session.params["filter[direction_id"] = direction_id
    if route:
        session.params["filter[route]"] = route
    if stop:
        session.params["filter[stop]"] = stop
    if trip:
        session.params["filter[trip]"] = trip
    if facility:
        session.params["filter[facility]"] = facility
    if filter_id:
        session.params["filter[id]"] = filter_id
    if banner:
        session.params["filter[banner]"] = banner
    if datetime:
        session.params["filter[datetime]"] = datetime
    if lifecycle:
        session.params["filter[lifecycle]"] = lifecycle
    if severity:
        session.params["filter[severity]"] = severity
    if facility_type:
        session.params["filter[type]"] = facility_type
    if latitude:
        session.params["filter[latitude]"] = latitude
    if longitude:
        session.params["filter[longitude]"] = longitude
    if radius:
        session.params["filter[radius]"] = radius
    if route_pattern:
        session.params["filter[route_pattern]"] = route_pattern
    if date:
        session.params["filter[date]"] = date
    if canonical:
        session.params["filter[canonical]"] = canonical

    # schedules
    if min_time:
        session.params["filter[min_time]"] = min_time
    if max_time:
        session.params["filter[max_time]"] = max_time
    if stop_sequence:
        session.params["filter[stop_sequence]"] = stop_sequence

    if service:
        session.params["filter[service]"] = service
    if location_type:
        session.params["filter[location_type]"] = location_type
    if name:
        session.params["filter[name]"] = name
    if label:
        session.params["filter[label]"] = label

    return session


def get(session, path):
    """Makes a request to the given path with the given session. Returns response in a JSON format if request is valid.
    Otherwise, raises an error."""
    response = session.get(path)
    status = response.status_code

    if status == OK:
        return response.json()
    else:
        error = response.json()["errors"][0]

        if status == BAD_REQUEST:
            raise BadRequestError(error)
        elif status == FORBIDDEN:
            raise ForbiddenError(error)
        elif status == NOT_FOUND:
            raise NotFoundError(error)
        elif status == NOT_ACCEPTABLE:
            raise NotAcceptableError(error)
        elif status == TOO_MANY_REQUESTS:
            raise TooManyRequestsError(error)
        else:
            raise RuntimeError
# swap for match case