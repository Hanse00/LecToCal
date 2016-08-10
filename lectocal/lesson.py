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

import copy
import hashlib
import datetime

STATUS_COLORS = {"normal": "10", "changed": "5", "cancelled": "11"}


class Lesson(object):
    def __init__(self, id, summary, status, start, end, location, description, link):
        self.summary = summary
        self.status = status or "normal"
        self.start = start
        self.end = end
        self.location = location
        self.description = description
        self.link = link

        if id is None:
            self.id = self._gen_id()
        else:
            self.id = id

    def to_gcalendar_format(self):
        TEMPLATE = {
            "summary": None,
            "id": None,
            "colorId": None,
            "start": {
                "timeZone": "Europe/Copenhagen"
            },
            "end": {
                "timeZone": "Europe/Copenhagen"
            },
            "location": None,
            "description": None,
            "source": {}

        }

        formatted = copy.deepcopy(TEMPLATE)
        formatted["summary"] = self.summary
        formatted["id"] = self.id
        formatted["colorId"] = STATUS_COLORS[self.status]
        if type(self.start) == datetime.datetime:
            formatted["start"]["dateTime"] = self.start.isoformat()
        else:
            formatted["start"]["date"] = self.start.isoformat()
        if type(self.end) == datetime.datetime:
            formatted["end"]["dateTime"] = self.end.isoformat()
        else:
            formatted["end"]["date"] = self.end.isoformat()
        formatted["location"] = self.location
        formatted["description"] = self.description
        if self.link is not None:
            formatted["source"]["url"] = self.link
        return formatted

    def _gen_id(self):
        lesson_string = str(self.summary) + str(self.status) + \
                        str(self.start) + str(self.end) + \
                        str(self.location) + str(self.description) + \
                        str(self.link)
        hasher = hashlib.sha256()
        hasher.update(bytes(lesson_string, "utf8"))
        hash_value = hasher.hexdigest()
        return hash_value

    def __eq__(self, other):
        if type(self) == type(other):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str({"id": self.id, "summary": self.summary,
                    "status": self.status, "start": self.start,
                    "end": self.end, "location": self.location,
                    "description": self.description, "link": self.link})


def schedules_are_identical(schedule1, schedule2):
    return all(lesson in schedule1 for lesson in schedule2) and \
           all(lesson in schedule2 for lesson in schedule1)
