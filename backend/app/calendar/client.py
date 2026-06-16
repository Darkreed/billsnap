import os
from abc import ABC, abstractmethod
from datetime import date
from typing import Any

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.auth.credentials import TokenState

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
TOKEN_FILE = os.getenv("GOOGLE_TOKEN_FILE", "token.json")


class CalendarClient(ABC):
    @abstractmethod
    def create_event(self, title: str, due_date: date, description: str = "") -> str:
        """Create a calendar event. Returns the event ID."""

    @abstractmethod
    def delete_event(self, event_id: str) -> None:
        ...


class MockCalendarClient(CalendarClient):
    def create_event(self, title: str, due_date: date, description: str = "") -> str:
        print(f"[MockCalendar] Would create event: {title} on {due_date}")
        return "event-id-xxx"
    
    def delete_event(self, event_id: str) -> None:
        print(f"[MockCalendar] Would delete event: {event_id}")


class GoogleCalendarClient(CalendarClient):

    _service: Any

    def __init__(self):
        self._service = self._build_service()

    def _build_service(self):
        if not os.path.exists(TOKEN_FILE):
            raise RuntimeError("No token.json found. Run auth_google.py first.")
        
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        
        if creds.token_state == TokenState.STALE and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN_FILE, 'w') as tok:
                tok.write(creds.to_json())
        elif creds.token_state != TokenState.FRESH:
            raise RuntimeError("Invalid token. Re-run auth_google.py.")
        
        return build("calendar", "v3", credentials=creds)


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
        return response.get("id", "")

    def delete_event(self, event_id: str) -> None:
        self._service.events().delete(calendarId="primary", eventId=event_id).execute()