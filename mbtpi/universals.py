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


def set_params(session,
               page_offset: int = None,
               page_limit: int = None,
               sort: str = None,
               fields_alert: str = None,
               fields_facility: str = None,
               fields_line: str = None,
               fields_prediction: str = None,
               fields_route: str = None,
               fields_route_pattern: str = None,
               fields_schedule: str = None,
               fields_service: str = None,
               fields_shape: str = None,
               fields_stop: str = None,
               fields_trip: str = None,
               fields_vehicle: str = None,
               include: str = None,
               activity: str = None,
               route_type: str = None,
               direction_id: str = None,
               route: str = None,
               stop: str = None,
               trip: str = None,
               facility: str = None,
               filter_id: str = None,
               banner: str = None,
               datetime: str = None,
               lifecycle: str = None,
               severity: str = None,
               facility_type: str = None,
               latitude: str = None,
               longitude: str = None,
               radius: str = None,
               route_pattern: str = None,
               date: str = None,
               canonical: str = None,
               min_time: str = None,
               max_time: str = None,
               stop_sequence: str = None,
               service: str = None,
               location_type: str = None,
               name: str = None,
               label: str = None):
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
    """Makes a request to the given path with the given session. Returns response in a JSON format"""
    response = session.get(path)
    return response.json()
