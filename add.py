# Copyright 2016 Philip Hansen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import gauth

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

CLIENT_SECRET = "client_secret.json"

SERVICE_NAME = "calendar"
SERVICE_VERSION = "v3"

EVENT = {
    "summary": "Test Event",
    "start": {"dateTime": "2016-03-11T17:00:00+01:00"},
    "end": {"dateTime": "2016-03-11T18:00:00+01:00"}
}


def get_calendar_service(credentials):
    return build(SERVICE_NAME,
                 SERVICE_VERSION,
                 http=credentials.authorize(Http()))


def add_to_calendar(credentials, event):
    calendar = get_calendar_service(credentials)
    response = calendar.events().insert(calendarId="primary",
                                        body=EVENT).execute()
    return response


def main():
    credentials = gauth.get_credentials()
    response = add_to_calendar(credentials, EVENT)
    print("Event added with link: {}".format(response["htmlLink"]))

if __name__ == "__main__":
    main()
