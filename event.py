from __future__ import print_function
import datetime
import os.path
from uuid import uuid1
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def main():
  creds = None
  if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
  if not creds or not creds.valid:
    print("Token Invalid")
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
      creds = flow.run_local_server(port=8080)
      with open('token.json', 'w') as token:
        token.write(creds.to_json())
    
  service = build('calendar', 'v3', credentials=creds)


  event = {
    'start': {
      'dateTime': '2015-05-28T09:00:00-07:00',
      'timeZone': 'UTC+1',
    },

    'end': {
      'dateTime': '2015-05-28T17:00:00-07:00',
      'timeZone': 'UTC+1',
    },

    "conferenceData": {
      "createRequest": {"requestId": f"{uuid1().hex}", "conferenceSolutionKey": {"type": "hangoutsMeet"}}}
  }

  event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
  result = event.get('hangoutLink')
  calLink = event.get("htmlLink")
  eventId = event.get("id")
  print(result)
  print(calLink)
  service.events().delete(calendarId='primary', eventId=eventId).execute()
  return f'Google Meet Link: {result}'


if __name__ == "__main__":
  main()
