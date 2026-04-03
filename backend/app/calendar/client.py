import os
from abc import ABC, abstractmethod
from datetime import date
from typing import Any

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.auth.credentials import TokenState

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
TOKEN_FILE = os.getenv("GOOGLE_TOKEN_FILE", "token.json")


class CalendarClient(ABC):
    @abstractmethod
    def create_event(self, title: str, due_date: date, description: str = "") -> str:
        """Create a calendar event. Returns the event URL."""
        ...


class MockCalendarClient(CalendarClient):
    def create_event(self, title: str, due_date: date, description: str = "") -> str:
        print(f"[MockCalendar] Would create event: {title} on {due_date}")
        return "https://mock-calendar-event"


class GoogleCalendarClient(CalendarClient):

    _service: Any

    def __init__(self):
        self._service = self._build_service()

    def _build_service(self):
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        else:
            creds = None
        if not creds or creds.token_state != TokenState.FRESH:
            if creds and creds.token_state == TokenState.STALE and creds.refresh_token:
                creds.refresh(Request())
            else:
                creds = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE,SCOPES).run_local_server(port=0)
            with open(TOKEN_FILE,'w') as tok:
                tok.write(creds.to_json())
        
        return build("calendar","v3",credentials=creds)


    def create_event(self, title: str, due_date: date, description: str = "") -> str:
        event_det = { 
            "summary": title, 
            "description": description , 
            "start": { 
                "date": due_date.isoformat(), 
                "timeZone": "Asia/Tokyo" 
            }, 
            "end": { 
                "date": due_date.isoformat(), 
                "timeZone": "Asia/Tokyo" 
            }
        }
        
        response = self._service.events().insert(calendarId="primary", body=event_det).execute()
        return response.get("htmlLink", "")
