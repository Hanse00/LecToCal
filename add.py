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

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = "https://www.googleapis.com/auth/calendar"
CREDENTIALS_STORAGE = "storage.json"
CLIENT_SECRET = "client_secret.json"

def get_credentials():
	store = file.Storage(CREDENTIALS_STORAGE)
	credentials = store.get()

	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPES)
		credentials = tools.run_flow(flow, store)
	return credentials

print(get_credentials())
