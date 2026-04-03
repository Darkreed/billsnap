import os
from app.calendar.client import CalendarClient, GoogleCalendarClient, MockCalendarClient


def get_calendar_client() -> CalendarClient:
    if os.environ.get("GOOGLE_CREDENTIALS_FILE"):
        return GoogleCalendarClient()
    return MockCalendarClient()
