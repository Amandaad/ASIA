from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
from app.config import settings

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def calendar_service():
    if not settings.google_calendar_id:
        raise RuntimeError("GOOGLE_CALENDAR_ID não configurado")
    creds = service_account.Credentials.from_service_account_file(
        settings.google_service_account_file, scopes=SCOPES
    )
    return build("calendar", "v3", credentials=creds, cache_discovery=False)

def check_slot(start: datetime, duration_minutes: int):
    service = calendar_service()
    end = start + timedelta(minutes=duration_minutes)
    result = service.events().list(
        calendarId=settings.google_calendar_id,
        timeMin=start.isoformat(),
        timeMax=end.isoformat(),
        singleEvents=True
    ).execute()
    return len(result.get("items", [])) == 0

def create_event(summary: str, start: datetime, duration_minutes: int, description: str):
    service = calendar_service()
    end = start + timedelta(minutes=duration_minutes)
    event = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start.isoformat(), "timeZone": settings.timezone},
        "end": {"dateTime": end.isoformat(), "timeZone": settings.timezone},
    }
    return service.events().insert(calendarId=settings.google_calendar_id, body=event).execute()
