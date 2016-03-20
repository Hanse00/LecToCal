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


def schedule_has_updated(google_credentials, calendar_name, schedule):
    # print("Checking if the schedule: {} is different from calendar: {} "
    #       "for user with Google crendentials: {}".format(schedule,
    #                                                      calendar_name,
    #                                                      google_credentials))
    return True


def update_calendar_with_schedule(google_credentials,
                                  calendar_name,
                                  schedule):
    # print("Updating calendar: {}, with data: {}, for user with "
    #       "crendentials: {}".format(calendar_name, schedule,
    #                                 google_credentials))
    pass
