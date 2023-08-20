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


import os
import requests
from dotenv import load_dotenv


class URLs:
    """
    Class with functions to access MBTA API urls. Docstrings quoted from API swagger docs
    """
    def __init__(self):
        """Sets each url field for construction within methods"""
        self.__base_url = "https://api-v3.mbta.com/"

        self.__alerts = "alerts/"
        self.__facilities = "facilities/"
        self.__lines = "lines/"
        self.__live_facilities = "live_facilities/"
        self.__predictions = "predictions/"
        self.__routes = "routes/"
        self.__route_patterns = "route_patterns/"
        self.__schedules = "schedules/"
        self.__services = "services/"
        self.__shapes = "shapes/"
        self.__stops = "stops/"
        self.__trips = "trips/"
        self.__vehicles = "vehicles/"

    def alert_url(self):
        """List active and upcoming system alerts"""
        return self.__base_url + self.__alerts

    def alert_by_id_url(self, alert_id: int):
        """Show a particular alert by the alert’s id"""
        return self.alert_url() + str(alert_id)

    def facility_url(self):
        """List Escalators and Elevators"""
        return self.__base_url + self.__facilities

    def facility_by_id_url(self, facility_id: int):
        """Specific Escalator or Elevator"""
        return self.facility_url() + str(facility_id)

    def line_url(self):
        """List of lines. A line is a combination of routes."""
        return self.__base_url + self.__lines

    def line_by_id_url(self, line_id: id):
        """Single line, which represents a combination of routes."""
        return self.line_url() + str(line_id)

    def live_facility_url(self):
        """Live data about a given facility."""
        return self.__base_url + self.__live_facilities

    def live_facility_by_id_url(self, live_facility_id: int):
        """List live parking data for specific parking facility"""
        return self.live_facility_url() + str(live_facility_id)

    def predictions_url(self, predictions_filter: str):
        """List of predictions for trips. To get the scheduled times instead of the predictions, use /schedules.
        A filter must be present for any predictions to be returned"""
        return self.__base_url + self.__predictions + predictions_filter

    def route_url(self):
        """List of routes."""
        return self.__base_url + self.__routes

    def route_by_id_url(self, route_id: int):
        """Show a particular route by the route’s id."""
        return self.route_url() + str(route_id)

    def route_pattern_url(self):
        """List of route patterns. Route patterns are used to describe the subsets of a route,
        representing different possible patterns of where trips may serve."""
        return self.__base_url + self.__route_patterns

    def route_pattern_by_id(self, route_pattern_id: int):
        """Show a particular route_pattern by the route’s id."""
        return self.route_pattern_url() + str(route_pattern_id)

    def schedules_url(self, schedule_filter: str):
        """List of schedules. To get a realtime prediction instead of the scheduled times, use /predictions.
        A filter must be present for any schedules to be returned"""
        return self.__base_url + self.__schedules + schedule_filter

    def service_url(self):
        """List of services. Service represents the days of the week, as well as extra days, that a trip is valid."""
        return self.__base_url + self.__services

    def service_by_id_url(self, service_id: int):
        """Single service, which represents the days of the week, as well as extra days, that a trip is valid."""
        return self.service_url() + str(service_id)

    def shape_url(self, route_filter: str):
        """List of shapes. A route filter must be present for any shapes to be returned"""
        return self.__base_url + self.__shapes + route_filter

    def shape_by_id_url(self, shape_id: int):
        """Detail of a particular shape."""
        return self.__base_url + self.__shapes + str(shape_id)

    def stop_url(self):
        """List stops."""
        return self.__base_url + self.__stops

    def stop_by_id_url(self, stop_id: int):
        """Detail for a specific stop."""
        return self.stop_url() + str(stop_id)

    def trip_url(self, trip_filter: str):
        """List of trips, the journies of a particular vehicle through a set of stops on a primary route and zero or
        more alternative routes that can be filtered on. An id, route, route_pattern, or name filter must be present for
        any trips to be returned."""
        return self.__base_url + self.__trips + trip_filter

    def trip_by_id_url(self, trip_id: int):
        """Single trip - the journey of a particular vehicle through a set of stops"""
        return self.trip_url() + str(trip_id)

    def vehicle_url(self):
        """List of vehicles (buses, ferries, and trains)"""
        return self.__base_url + self.__vehicles

    def vehicle_by_id_url(self, vehicle_id: int):
        """Single vehicle (bus, ferry, or train)"""
        return self.vehicle_url() + str(vehicle_id)


load_dotenv()
MBTA_API_KEY = os.environ.get('MBTA_API_KEY', "No api key set")

session = requests.Session()
session.params = {}
session.params['api_key'] = MBTA_API_KEY

urls = URLs()
