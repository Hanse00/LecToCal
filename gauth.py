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

import prompter
from oauth2client import file, client, tools

DEFAULT_CREDENTIALS_STORE = "storage.json"
DEFAULT_CLIENT_SECRET_STORE = "client_secret.json"


class CredentialsMissingError(Exception):
    """ Credentials must exist before they can be gotten. """


def has_valid_credentials(store_location=DEFAULT_CREDENTIALS_STORE):
    store = file.Storage(store_location)
    credentials = store.get()

    return credentials is not None and not credentials.invalid


def get_credentials(store_location=DEFAULT_CREDENTIALS_STORE):
    store = file.Storage(store_location)
    credentials = store.get()

    if not credentials:
        raise CredentialsMissingError()

    return credentials


def authenticate_user(scopes, store_location=DEFAULT_CREDENTIALS_STORE,
                      client_secret=DEFAULT_CLIENT_SECRET_STORE):
    confirm = False
    store = file.Storage(store_location)
    credentials = store.get()

    if credentials:
        prompt = "Credentials already exist, do you want to overwrite?"
        # Not used here as prompter will return whether or not "No"
        # was entered, giving us the inverse of confirmation.
        confirm = not prompter.yesno(prompt, default='no')
        if not confirm:
            return

    flow = client.flow_from_clientsecrets(client_secret, scopes)
    credentials = tools.run_flow(flow, store)

if __name__ == "__main__":
    authenticate_user(["profile",
                       "email",
                       "https://www.googleapis.com/auth/calendar"])
    print(get_credentials())
