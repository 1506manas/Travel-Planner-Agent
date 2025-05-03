from phi.tools.python import PythonTools
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

class CalendarManagerTool(PythonTools):
    name = "calendar_manager"
    description = (
        "Add events to Google Calendar. "
        "Parameters: event_name (string), date, start_time, end_time."
        "The date and time should follow the format as %Y-%m-%d %H:%M only"
        "Create a new event and update the calendar for all different activities."
    )

    def __init__(self):
        super().__init__()
        self.creds = None
        self.service = None
        self.SCOPES = ['https://www.googleapis.com/auth/calendar']
        self.authenticate()

    def authenticate(self):
        """Authenticate and connect to Google Calendar API."""
        try:
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    self.creds = pickle.load(token)

            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.SCOPES)
                    self.creds = flow.run_local_server(port=0)

                with open('token.pickle', 'wb') as token:
                    pickle.dump(self.creds, token)

            self.service = build('calendar', 'v3', credentials=self.creds)
            self.log_debug("Authentication successful.")

        except Exception as e:
            self.log_debug(f"Authentication failed: {e}")
            raise Exception(f"Authentication failed: {e}")

    def run(self, event_name, date, start_time, end_time):
        """Add the events in the google calendar."""
        try:
            start_dt = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
            end_dt = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")

            event = {
                'summary': event_name,
                'start': {
                    'dateTime': start_dt.isoformat(),
                    'timeZone': 'IST',
                },
                'end': {
                    'dateTime': end_dt.isoformat(),
                    'timeZone': 'IST',
                },
            }

            self.log_debug(f"Creating event: {event}")

            created_event = self.service.events().insert(calendarId='primary', body=event).execute()
            event_link = created_event.get('htmlLink')
            self.log_debug(f"Event created successfully: {event_link}")
            return f"Event created: {event_link}"

        except Exception as e:
            self.log_debug(f"Failed to create event: {e}")
            return f"Failed to create event: {e}"

    def log_debug(self, message: str) -> None:
        """Log debug information into a text file."""
        log_file = "calendar_debug_log.txt"
        try:
            with open(log_file, "w", encoding="utf-8") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] {message}\n")
        except Exception:
            pass
