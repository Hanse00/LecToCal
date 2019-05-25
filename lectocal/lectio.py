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
import pickle
import re
import requests
from lxml import html
from . import lesson


USER_TYPE = {"student": "elev", "teacher": "laerer"}
LESSON_STATUS = {None: "normal", "Ændret!": "changed", "Aflyst!": "cancelled"}


class CannotLoginToLectioError(Exception):
    """ Could not login to Lectio (using cookie or login provided). """


class IdNotFoundInLinkError(Exception):
    """ All lessons with a link should include an ID. """


class InvalidStatusError(Exception):
    """ Lesson status can only take the values Ændret!, Aflyst! and None. """


class InvalidTimeLineError(Exception):
    """ The line doesn't include any valid formatting of time. """


class InvalidLocationError(Exception):
    """ The line doesn't include any location. """


def _get_user_page(school_id, user_type, user_id, week = "", login = "", password = ""):
    URL_TEMPLATE = "https://www.lectio.dk/lectio/{0}/" \
                   "SkemaNy.aspx?type={1}&{1}id={2}&week={3}"
                   
    LOGIN_URL = "https://www.lectio.dk/lectio/{0}/login.aspx".format(school_id)
    
    # Start requests session
    s = requests.Session()
    
    if(login != ""):
        # Get eventvalidation key
        result = s.get(LOGIN_URL)
        tree = html.fromstring(result.text)
        authenticity_token = list(set(tree.xpath("//input[@name='__EVENTVALIDATION']/@value")))[0]

        # Create payload
        payload = {
            "m$Content$username2": login,
            "m$Content$password2": password,
            "m$Content$passwordHidden": password,
            "__EVENTVALIDATION": authenticity_token,
            "__EVENTTARGET": "m$Content$submitbtn2",
            "__EVENTARGUMENT": "",
            "LectioPostbackId": ""
        }

        # Perform login
        result = s.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))
        
        # Save cookies to file
        with open('cookie.txt', 'wb') as f:
            pickle.dump(s.cookies, f)
        
    else:
        # Load cookies from file
        with open('cookie.txt', 'rb') as f:
            s.cookies.update(pickle.load(f))
        
    # Scrape url and save cookies to file
    r = s.get(URL_TEMPLATE.format(school_id,
                                  USER_TYPE[user_type],
                                  user_id,
                                  week),
                     allow_redirects=False)
    with open('cookie.txt', 'wb') as f:
        pickle.dump(s.cookies, f)
        
    return r


def _get_lectio_weekformat_with_offset(offset):
    today = datetime.date.today()
    future_date = today + datetime.timedelta(weeks=offset)
    week_number = "{0:02d}".format(future_date.isocalendar()[1])
    year_number = str(future_date.isocalendar()[0])
    lectio_week = week_number + year_number
    return lectio_week


def _get_id_from_link(link):
    match = re.search(r"(?:absid|ProeveholdId|outboundCensorID|aftaleid)=(\d+)", link)
    if match is None:
        return None
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
    match = re.search(r"\d{1,2}/\d{1,2}-\d{4} (?:Hele dagen|\d{2}:\d{2} til "
                      r"(?:\d{1,2}/\d{1,2}-\d{4} )?\d{2}:\d{2})", line)
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
    match = re.search(r"(\d{1,2}/\d{1,2}-\d{4})(?: (\d{2}:\d{2}) til "
                      r"(\d{1,2}/\d{1,2}-\d{4})? ?(\d{2}:\d{2}))?", line)
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


def _retreive_week_schedule(school_id, user_type, user_id, week, login = "", password = ""):
    r = _get_user_page(school_id, user_type, user_id, week, login = "", password = "")
    schedule = _parse_page_to_lessons(r.content)
    return schedule


def _filter_for_duplicates(schedule):
    filtered_schedule = []
    for lesson in schedule:
        if lesson not in filtered_schedule:
            filtered_schedule.append(lesson)
    return filtered_schedule


def _retreive_user_schedule(school_id, user_type, user_id, n_weeks, login = "", password = ""):
    schedule = []
    for week_offset in range(n_weeks + 1):
        week = _get_lectio_weekformat_with_offset(week_offset)
        week_schedule = _retreive_week_schedule(school_id,
                                                user_type,
                                                user_id,
                                                week, 
                                                login = "", 
                                                password = "")
        schedule += week_schedule
    filtered_schedule = _filter_for_duplicates(schedule)
    return filtered_schedule


def _can_login(school_id, user_type, user_id, login = "", password = ""):
    r = _get_user_page(school_id, user_type, user_id, "", login, password)
    return r.status_code == requests.codes.ok


def get_schedule(school_id, user_type, user_id, n_weeks, login = "", password = ""):
    if not _can_login(school_id, user_type, user_id, login, password):
        raise CannotLoginToLectioError(
            "Couldn't login user - school: {}, type: {}, id: {}, login: {} "
            "- in Lectio.".format(school_id, user_type, user_id, login))
    return _retreive_user_schedule(school_id, user_type, user_id, n_weeks, login = "", password = "")
