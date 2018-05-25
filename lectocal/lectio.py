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
import re
import requests
from lxml import html
from . import lesson


USER_TYPE = {"student": "elev", "teacher": "laerer"}
LESSON_STATUS = {None: "normal", "Ændret!": "changed", "Aflyst!": "cancelled"}


class UserDoesNotExistError(Exception):
    """ Attempted to get a non-existing user from Lectio. """


class IdNotFoundInLinkError(Exception):
    """ All lessons with a link should include an ID. """


class InvalidStatusError(Exception):
    """ Lesson status can only take the values Ændret!, Aflyst! and None. """


class InvalidTimeLineError(Exception):
    """ The line doesn't include any valid formatting of time. """


class InvalidLocationError(Exception):
    """ The line doesn't include any location. """


def _get_user_page(school_id, user_type, user_id, week=""):
    URL_TEMPLATE = "https://www.lectio.dk/lectio/{0}/" \
                   "SkemaNy.aspx?type={1}&{1}id={2}&week={3}"

    r = requests.get(URL_TEMPLATE.format(school_id,
                                         USER_TYPE[user_type],
                                         user_id,
                                         week),
                     allow_redirects=False)
    return r


def _get_lectio_weekformat_with_offset(offset):
    today = datetime.date.today()
    future_date = today + datetime.timedelta(weeks=offset)
    week_number = "{0:02d}".format(future_date.isocalendar()[1])
    year_number = str(future_date.isocalendar()[0])
    lectio_week = week_number + year_number
    return lectio_week


def _get_id_from_link(link):
    match = re.search("(?:absid|ProeveholdId|outboundCensorID)=(\d+)", link)
    if match is None:
        raise IdNotFoundInLinkError("Couldn't find id in link: {}".format(
                                    link))
    return match.group(1)

def _get_complete_link(link):
    return "https://www.lectio.dk" + link.split("&prevurl=", 1)[0]


def _is_status_line(line):
    match = re.search("Ændret!|Aflyst!", line)
    return match is not None


def _is_location_line(line):
    match = re.search("Lokaler?: ", line)
    return match is not None


def _is_time_line(line):
    # Search for one of the following formats:
    # 14/3-2016 Hele dagen
    # 14/3-2016 15:20 til 16:50
    # 8/4-2016 17:30 til 9/4-2016 01:00
    # 7/12-2015 10:00 til 11:30
    # 17/12-2015 10:00 til 11:30
    match = re.search("\d{1,2}/\d{1,2}-\d{4} (?:Hele dagen|\d{2}:\d{2} til "
                      "(?:\d{1,2}/\d{1,2}-\d{4} )?\d{2}:\d{2})", line)
    return match is not None


def _get_status_from_line(line):
    try:
        return LESSON_STATUS[line]
    except KeyError:
        raise InvalidStatusError("Line: '{}' has no valid status".format(line))


def _get_location_from_line(line):
    match = re.search("Lokaler?: (.*)", line)
    if match is None:
        raise InvalidLocationError("No location found in line: '{}'"
                                   .format(line))
    return match.group(1)


def _get_date_from_match(match):
    if match:
        return datetime.datetime.strptime(match, "%d/%m-%Y").date()
    else:
        return None


def _get_time_from_match(match):
    if match:
        return datetime.datetime.strptime(match, "%H:%M").time()
    else:
        return None


def _get_time_from_line(line):
    # Extract the following information in capture groups:
    # 1 - start date
    # 2 - start time
    # 3 - end date
    # 4 - end time
    match = re.search("(\d{1,2}/\d{1,2}-\d{4})(?: (\d{2}:\d{2}) til "
                      "(\d{1,2}/\d{1,2}-\d{4})? ?(\d{2}:\d{2}))?", line)
    if match is None:
        raise InvalidTimeLineError("No time found in line: '{}'".format(line))

    start_date = _get_date_from_match(match.group(1))
    start_time = _get_time_from_match(match.group(2))

    if start_time:
        start = datetime.datetime.combine(start_date, start_time)
    else:
        start = start_date

    end_date = _get_date_from_match(match.group(3))
    end_time = _get_time_from_match(match.group(4))

    if not end_date:
        end_date = start_date

    if end_time:
        end = datetime.datetime.combine(end_date, end_time)
    else:
        end = end_date
    return start, end


def _add_line_to_text(line, text):
    if text != "":
        text += "\n"
    text += line
    return text


def _add_section_to_summary(section, summary):
    if summary != "" and section != "":
        summary += " " + u"\u2022" + " "
    summary += section
    return summary


def _get_info_from_title(title):
    summary = description = ""
    status = start_time = end_time = location = None
    lines = title.splitlines()
    headerSection = True
    for line in lines:
        if headerSection:
            if line == '':
                headerSection = False
                continue
            if _is_status_line(line):
                status = _get_status_from_line(line)
            elif _is_time_line(line):
                start_time, end_time = _get_time_from_line(line)
            elif _is_location_line(line):
                location = _get_location_from_line(line)
            else:
                summary = _add_section_to_summary(line, summary)
        else:
            description = _add_line_to_text(line, description)
    return summary, status, start_time, end_time, location, description


def _parse_element_to_lesson(element):
    link = element.get("href")
    id = None
    if link:
        id = _get_id_from_link(link)
        link = _get_complete_link(link)
    summary, status, start_time, end_time, location, description = \
        _get_info_from_title(element.get("data-additionalinfo"))
    return lesson.Lesson(id, summary, status, start_time, end_time, location, description, link)


def _parse_page_to_lessons(page):
    tree = html.fromstring(page)
    # Find all a elements with class s2skemabrik in page
    lesson_elements = tree.xpath("//a[contains(concat("
                                 "' ', normalize-space(@class), ' '),"
                                 "' s2skemabrik ')]")
    lessons = []
    for element in lesson_elements:
        lessons.append(_parse_element_to_lesson(element))
    return lessons


def _retreive_week_schedule(school_id, user_type, user_id, week):
    r = _get_user_page(school_id, user_type, user_id, week)
    schedule = _parse_page_to_lessons(r.content)
    return schedule


def _filter_for_duplicates(schedule):
    filtered_schedule = []
    for lesson in schedule:
        if lesson not in filtered_schedule:
            filtered_schedule.append(lesson)
    return filtered_schedule


def _retreive_user_schedule(school_id, user_type, user_id, n_weeks):
    schedule = []
    for week_offset in range(n_weeks + 1):
        week = _get_lectio_weekformat_with_offset(week_offset)
        week_schedule = _retreive_week_schedule(school_id,
                                                user_type,
                                                user_id,
                                                week)
        schedule += week_schedule
    filtered_schedule = _filter_for_duplicates(schedule)
    return filtered_schedule


def _user_exists(school_id, user_type, user_id):
    r = _get_user_page(school_id, user_type, user_id)
    return r.status_code == requests.codes.ok


def get_schedule(school_id, user_type, user_id, n_weeks):
    if not _user_exists(school_id, user_type, user_id):
        raise UserDoesNotExistError("Couldn't find user - school: {}, "
                                    "type: {}, id: {} - in Lectio.".format(
                                        school_id, user_type, user_id))
    return _retreive_user_schedule(school_id, user_type, user_id, n_weeks)
