from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http

scopes = ['https://www.googleapis.com/auth/drive.readonly']

credentials = ServiceAccountCredentials.from_json_keyfile_name('scripts/service_account_key - honestjung@gmail.com dolfinid-666ee9228acc.json', scopes)

http_auth = credentials.authorize(Http())
print(http_auth)
drive = build('drive', 'v3', http=http_auth)
print(drive)

results = drive.files().list(
    pageSize=10, fields="nextPageToken, files(id, name)").execute()
items = results.get('files', [])
print(items)

request = drive.files().list().execute()
files = request.get('items', [])
for f in files:
    print(f)