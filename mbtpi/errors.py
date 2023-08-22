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


class BadRequestError(Exception):
    """Raised if response from MBTA API is the server cannot or will not process the request due to
    something that is perceived to be a client error."""

    def __init__(self, json):
        """Stores each value returned from the API as a field"""
        self.status = json["status"]
        if "source" in json:
            self.source = json["source"]["parameter"]
        self.detail = json["detail"]
        self.code = json["code"]

    def __str__(self):
        """Returns the error's status code and a summary of the problem"""
        return self.status + ": " + self.detail


class NotAcceptableError(Exception):
    """Raised if a request uses an invalid ‘accept’ header"""

    def __init__(self, json):
        """Stores each value returned from the API as a field"""
        self.status = json["status"]
        self.detail = json["detail"]
        self.code = json["code"]

    def __str__(self):
        """Returns the error's status code and a summary of the problem"""
        return self.status + ": " + self.detail


class NotFoundError(Exception):
    """Raised if a resource is not found"""

    def __init__(self, json):
        """Stores each value returned from the API as a field"""
        self.title = json["title"]
        self.status = json["status"]
        self.source = json["source"]["parameter"]
        self.code = json["code"]

    def __str__(self):
        """Returns the error's status code and a summary of the problem with the specific parameter"""
        return self.status + " " + self.title + ": " + self.source


class ForbiddenError(Exception):
    """Raised when the API key is invalid"""

    def __init__(self, json):
        """Stores each value returned from the API as a field"""
        self.status = json["status"]
        self.code = json["code"]

    def __str__(self):
        """Returns the error's status code and application specific error code"""
        return self.status + ": " + self.code


class TooManyRequestsError(Exception):
    """Raised when rate limited"""

    def __init__(self, json):
        """Stores each value returned from the API as a field"""
        self.status = json["status"]
        self.detail = json["detail"]
        self.code = json["code"]

    def __str__(self):
        """Returns the error's status code and a summary of the problem"""
        return self.status + ": " + self.detail
