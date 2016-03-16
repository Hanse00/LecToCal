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
import oauth2client.file


class CredentialsMissingError(Exception):
    """ Credentials must exist before they can be gotten. """


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


def _has_valid_credentials(credentials_store):
    store = oauth2client.file.Storage(credentials_store)
    credentials = store.get()
    return credentials is not None and not credentials.invalid


def _retreive_credentials(credentials_store):
    store = oauth2client.file.Storage(credentials_store)
    credentials = store.get()
    return credentials


def get_google_credentials(credentials_store):
    # Debugging message
    print("Getting the Google credentials at {}".format(credentials_store))

    if not _has_valid_credentials(credentials_store):
        raise CredentialsMissingError("No credentials found at: {}"
                                      .format(credentials_store))
    return _retreive_credentials(credentials_store)


def get_lectio_schedule(school_id, user_type, user_id):
    print("Getting schedule for user: {} {} at school: {}".format(user_type,
                                                                  user_id,
                                                                  school_id))
    return {"class": "math"}


def schedule_has_changed(google_credentials, calendar_name, schedule):
    print("Checking if the schedule: {} is different from calendar: {} "
          "for user with Google crendentials: {}".format(schedule,
                                                         calendar_name,
                                                         google_credentials))
    return True


def update_google_calendar_with_schedule(google_credentials,
                                         calendar_name,
                                         schedule):
    print("Updating calendar: {}, with data: {}, for user with "
          "crendentials: {}".format(calendar_name, schedule,
                                    google_credentials))


def main():
    arguments = get_arguments()
    google_credentials = get_google_credentials(arguments["credentials"])
    schedule = get_lectio_schedule(arguments["school_id"],
                                   arguments["user_type"],
                                   arguments["user_id"])
    if schedule_has_changed(google_credentials,
                            arguments["calendar"],
                            schedule):
        update_google_calendar_with_schedule(google_credentials,
                                             arguments["calendar"],
                                             schedule)

if __name__ == "__main__":
    main()
