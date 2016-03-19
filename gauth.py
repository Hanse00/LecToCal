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

import oauth2client.file


class CredentialsMissingError(Exception):
    """ Credentials must exist before they can be gotten. """


def _has_valid_credentials(credentials_store):
    store = oauth2client.file.Storage(credentials_store)
    credentials = store.get()
    return credentials is not None and not credentials.invalid


def _retreive_credentials(credentials_store):
    store = oauth2client.file.Storage(credentials_store)
    credentials = store.get()
    return credentials


def get_credentials(credentials_store):
    # Debugging message
    print("Getting the Google credentials at {}".format(credentials_store))

    if not _has_valid_credentials(credentials_store):
        raise CredentialsMissingError("No credentials found at: {}"
                                      .format(credentials_store))
    return _retreive_credentials(credentials_store)
