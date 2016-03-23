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

import argparse
import gauth
import lectio
import lesson
import gcalendar


def get_arguments():
    parser = argparse.ArgumentParser(description="Scrapes a Lectio schedule "
                                     "and syncs it to Google Calendar.")
    parser.add_argument("school_id",
                        type=int,
                        help="ID of the school user belongs to in Lectio")
    parser.add_argument("user_type",
                        choices=["student", "teacher"],
                        help="User type in Lectio (options: student, teacher)")
    parser.add_argument("user_id",
                        type=int,
                        help="User's ID in Lectio")
    parser.add_argument("--credentials",
                        default="storage.json",
                        help="Path to the file storing the Google "
                        "OAuth credentials (default: storage.json)")
    parser.add_argument("--calendar",
                        default="Lectio",
                        help="Name to use for the calendar inside "
                        "Google Calendar (default: Lectio)")

    arguments = vars(parser.parse_args())
    return arguments


def main():
    arguments = get_arguments()
    google_credentials = gauth.get_credentials(arguments["credentials"])
    if not gcalendar.has_calendar(google_credentials, arguments["calendar"]):
        gcalendar.create_calendar(google_credentials, arguments["calendar"])
    lectio_schedule = lectio.get_schedule(arguments["school_id"],
                                          arguments["user_type"],
                                          arguments["user_id"])
    google_schedule = gcalendar.get_schedule(google_credentials,
                                             arguments["calendar"])
    if not lesson.schedules_are_identical(lectio_schedule, google_schedule):
        print("Schedule needs updating")
        gcalendar.update_calendar_with_schedule(google_credentials,
                                                arguments["calendar"],
                                                google_schedule,
                                                lectio_schedule)
        print("Schedule updated!")
    else:
        print("Schedule does not need updating")

if __name__ == "__main__":
    main()
