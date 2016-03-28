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

import pkg_resources
import argparse
import oauth2client.file
import oauth2client.client
import oauth2client.tools


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
    if not _has_valid_credentials(credentials_store):
        raise CredentialsMissingError("No credentials found at: {}"
                                      .format(credentials_store))
    return _retreive_credentials(credentials_store)


def _get_arguments():
    parser = argparse.ArgumentParser(description="Generate Google OAuth "
                                     "credentials for user.",
                                     parents=[oauth2client.tools.argparser])
    parser.add_argument("-c", "--credentials",
                        type=str,
                        default="storage.json",
                        help="File location for saving generated credentials. "
                        "(default: storage.json)")
    parser.add_argument("-s", "--scopes",
                        type=str,
                        nargs="+",
                        default=["https://www.googleapis.com/auth/calendar"],
                        help="OAuth scopes to request for the given user. "
                        "(default: https://www.googleapis.com/auth/calendar)")
    return parser.parse_args()


def _get_client_secret_path():
    return pkg_resources.resource_filename(__name__, "client_secret.json")


def generate_credentials(client_secret, credentials_storage, scopes, flags):
    store = oauth2client.file.Storage(credentials_storage)
    flow = oauth2client.client.flow_from_clientsecrets(client_secret, scopes)
    oauth2client.tools.run_flow(flow, store, flags)


def main():
    arguments = _get_arguments()
    generate_credentials(_get_client_secret_path(),
                         arguments.credentials,
                         arguments.scopes,
                         arguments)

if __name__ == '__main__':
    main()
