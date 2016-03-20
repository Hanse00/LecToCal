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

import datetime
import requests


class UserDoesNotExistError(Exception):
    """ Attempted to get a non-existing user from Lectio. """


class Lesson(object):
    def __init__(self, id, summary, status, start_time, end_time):
        self.id = id
        self.summary = summary
        self.status = status
        self.start_time = start_time
        self.end_time = end_time

    def __eq__(self, other):
        if type(self) == type(other):
            if self.id is None and other.id is None:
                if self.summary == other.summary:
                    return True
            elif self.id == other.id:
                return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)


def _get_user_page(school_id, user_type, user_id, week=""):
    URL_TEMPLATE = "http://www.lectio.dk/lectio/{0}/" \
                   "SkemaNy.aspx?type={1}&{1}id={2}&week={3}"
    USER_TYPE = {"student": "elev", "teacher": "laerer"}

    r = requests.get(URL_TEMPLATE.format(school_id,
                                         USER_TYPE[user_type],
                                         user_id,
                                         ""),
                     allow_redirects=False)
    return r


def _get_lectio_weekformat_with_offset(offset):
    today = datetime.date(2015, 12, 20)
    future_date = today + datetime.timedelta(weeks=offset)
    week_number = "{0:02d}".format(future_date.isocalendar()[1])
    year_number = str(future_date.isocalendar()[0])
    lectio_week = week_number + year_number
    return lectio_week


def _get_week_schedule(school_id, user_type, user_id, week):
    pass



def _filter_for_duplicates(schedule):
    filtered_schedule = []
    for lesson in schedule:
        if lesson not in filtered_schedule:
            filtered_schedule += lesson
    return filtered_schedule


def _retreive_user_schedule(school_id, user_type, user_id):
    schedule = []
    for week_offset in range(4):
        week = _get_lectio_weekformat_with_offset(week_offset)
        week_schedule = _get_week_schedule(school_id, user_type, user_id, week)
        schedule += week_schedule
    filtered_schedule = _filter_for_duplicates(schedule)
    return filtered_schedule


def _user_exists(school_id, user_type, user_id):
    r = _get_user_page(school_id, user_type, user_id)
    return r.status_code == requests.codes.ok


def get_schedule(school_id, user_type, user_id):
    # Debugging message
    print("Getting schedule for user: {} {} at school: {}".format(user_type,
                                                                  user_id,
                                                                  school_id))
    if not _user_exists(school_id, user_type, user_id):
        raise UserDoesNotExistError("Couldn't find user - school: {}, "
                                    "type: {}, id: {} - in Lectio.".format(
                                        school_id, user_type, user_id))
    return _retreive_user_schedule(school_id, user_type, user_id)
