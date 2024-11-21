import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


JSON_CREDS = "credentials.json"

def generate_creds(service_token, scopes):
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists(service_token):
    creds = Credentials.from_authorized_user_file(service_token, scopes)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          JSON_CREDS, scopes
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(service_token, "w") as token:
      token.write(creds.to_json())
  return creds

def create_service(app, version, creds):
  try:
    if app == 'photoslibrary':
       return build(app, version, credentials=creds, static_discovery=False)
    return build(app, version, credentials=creds)  
  except HttpError as err:
        print(err)

  