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

import lectio
import datetime
import apiclient.discovery
from httplib2 import Http
import pytz

SERVICE_NAME = "calendar"
SERVICE_VERSION = "v3"

DEFAULT_TIME_ZONE = pytz.timezone("Europe/Copenhagen")


class CalendarNotFoundError(object):
    """ To get the id of a calendar, the calendar must exist. """


def _get_calendar_service(google_credentials):
    return apiclient.discovery.build(SERVICE_NAME, SERVICE_VERSION,
                                     http=google_credentials.authorize(Http()))


def has_calendar(google_credentials, calendar_name):
    service = _get_calendar_service(google_credentials)
    page_token = None
    while True:
        calendar_list = service \
                        .calendarList() \
                        .list(pageToken=page_token) \
                        .execute()
        for calendar_entry in calendar_list['items']:
            if calendar_entry["summary"] == calendar_name:
                return True
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            return False


def create_calendar(google_credentials, calendar_name):
    calendar = {
        "summary": calendar_name,
        "timeZone": DEFAULT_TIME_ZONE.zone
    }

    service = _get_calendar_service(google_credentials)
    service.calendars().insert(body=calendar).execute()


def _get_calendar_id_for_name(google_credentials, calendar_name):
    service = _get_calendar_service(google_credentials)
    page_token = None
    while True:
        calendar_list = service \
                        .calendarList() \
                        .list(pageToken=page_token) \
                        .execute()
        for calendar_entry in calendar_list['items']:
            if calendar_entry["summary"] == calendar_name:
                return calendar_entry["id"]
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            raise CalendarNotFoundError("Calendar: {} not found"
                                        .format(calendar_name))


def _get_first_time_of_week():
    today = datetime.date.today()
    days_since_first_weekday = datetime.timedelta(days=today.weekday())
    first_day_this_week = today - days_since_first_weekday
    return datetime.datetime.combine(first_day_this_week, datetime.time.min)


def _get_last_time_in_n_weeks(n):
    today_n_weeks = datetime.date.today() + datetime.timedelta(weeks=n)
    days_to_week_end = datetime.timedelta(days=(6 - today_n_weeks.weekday()))
    last_day_n_weeks = today_n_weeks + days_to_week_end
    return datetime.datetime.combine(last_day_n_weeks, datetime.time.max)


def _get_events_in_date_range(service, calendar_id, start, end):
    all_events = []
    page_token = None
    while True:
        events = service \
                 .events() \
                 .list(calendarId=calendar_id,
                       pageToken=page_token,
                       timeMax=DEFAULT_TIME_ZONE.localize(end).isoformat(),
                       timeMin=DEFAULT_TIME_ZONE.localize(start).isoformat()) \
                 .execute()
        all_events += events["items"]
        page_token = events.get('nextPageToken')
        if not page_token:
            break
    return all_events


def _parse_event_to_lesson(event):
    id = event["id"]
    sumarry = event["summary"]
    if event["start"]["dateTime"]:
        start = datetime.datetime.strptime(event["start"]["dateTime"],
                                           "%Y-%m-%dT%H:%M")
    else:
        start = datetime.datetime.strptime(event["start"]["date"],
                                           "%Y-%m-%d").date()
    if event["end"]["dateTime"]:
        end = datetime.datetime.strptime(event["end"]["dateTime"],
                                         "%Y-%m-%dT%H:%M")
    else:
        end = datetime.datetime.strptime(event["end"]["date"],
                                         "%Y-%m-%d").date()
    return lectio.Lesson(id, summary, None, start, end)


def _parse_events_to_schedule(events):
    schedule = []
    for event in events:
        schedule.append(_parse_event_to_lesson(event))
    return schedule


def _get_schedule_from_calendar(google_credentials, calendar_name):
    service = _get_calendar_service(google_credentials)
    calendar_id = _get_calendar_id_for_name(google_credentials, calendar_name)
    start = _get_first_time_of_week()
    end = _get_last_time_in_n_weeks(3)
    events = _get_events_in_date_range(service, calendar_id, start, end)
    return _parse_events_to_schedule(events)


def _schedules_are_identical(schedule1, schedule2):
    # Check if all lessons in each schedule, have a corresponding
    # lesson in the other schedule
    return all(lesson in schedule1 for lesson in schedule2) and \
           all(lesson in schedule2 for lesson in schedule1)


def schedule_has_updated(google_credentials, calendar_name, schedule):
    # Debug message
    # print("Checking if the schedule: {} is different from calendar: {} "
    #       "for user with Google crendentials: {}".format(schedule,
    #                                                      calendar_name,
    #                                                      google_credentials))
    google_schedule = _get_schedule_from_calendar(google_credentials,
                                                  calendar_name)
    return not _schedules_are_identical(schedule, google_schedule)


def update_calendar_with_schedule(google_credentials,
                                  calendar_name,
                                  schedule):
    # print("Updating calendar: {}, with data: {}, for user with "
    #       "crendentials: {}".format(calendar_name, schedule,
    #                                 google_credentials))
    pass
