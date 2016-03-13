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

import pprint

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


def add_to_calendar(service, event, calendar_id="primary"):
    response = service.events() \
                      .insert(calendarId=calendar_id, body=event) \
                      .execute()
    return response


def get_calendars(service):
    page_token = None
    calendar_list = []
    while True:
        response = service.calendarList() \
                          .list(pageToken=page_token) \
                          .execute()
        calendar_list += response["items"]
        page_token = response.get('nextPageToken')
        if not page_token:
            break
    return calendar_list


def main():
    credentials = gauth.get_credentials()
    calendar_service = get_calendar_service(credentials)

    pprint.pprint(get_calendars(calendar_service))

    # local_time = timezone("Europe/Copenhagen")
    # start_time = local_time.localize(datetime(2016, 3, 13, 17))
    # end_time = local_time.localize(datetime(2016, 3, 13, 18))
    # event = Event("Test Event", start_time, end_time)

    # print(event.json)

    # response = add_to_calendar(calendar_service, event.json)
    # print("Event added with link: {}".format(response["htmlLink"]))

if __name__ == "__main__":
    main()
