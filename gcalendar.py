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
import copy
from datetime import datetime
from pytz import timezone
from apiclient.discovery import build
from httplib2 import Http

SERVICE_NAME = "calendar"
SERVICE_VERSION = "v3"


class Event(object):
    JSON_TEMPLATE = {
        "summary": None,
        "start": {"dateTime": None},
        "end": {"dateTime": None}
    }

    def __init__(self, summary, start, end):
        self.json = copy.deepcopy(self.JSON_TEMPLATE)

        self.json["summary"] = summary
        self.json["start"]["dateTime"] = start.isoformat()
        self.json["end"]["dateTime"] = end.isoformat()


def get_calendar_service(credentials):
    return build(SERVICE_NAME,
                 SERVICE_VERSION,
                 http=credentials.authorize(Http()))


def add_to_calendar(credentials, event):
    calendar = get_calendar_service(credentials)
    response = calendar.events().insert(calendarId="primary",
                                        body=event).execute()
    return response


def main():
    local_time = timezone("Europe/Copenhagen")
    start_time = local_time.localize(datetime(2016, 3, 13, 17))
    end_time = local_time.localize(datetime(2016, 3, 13, 18))
    event = Event("Test Event", start_time, end_time)

    print(event.json)

    credentials = gauth.get_credentials()
    response = add_to_calendar(credentials, event.json)
    print("Event added with link: {}".format(response["htmlLink"]))

if __name__ == "__main__":
    main()
