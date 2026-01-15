"""Google Calendar MCP Server - Query upcoming calendar events."""

import datetime
import json
from pathlib import Path

from fastmcp import FastMCP
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

TOKEN_PATH = Path.home() / ".config" / "gcal-mcp" / "token.json"

CLIENT_CONFIG = {
    "installed": {
        "client_id": "894785146012-rih2k2gtd97l3aqlvibgcmeipp30tl24.apps.googleusercontent.com",
        "client_secret": "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",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": ["http://localhost"],
    }
}

mcp = FastMCP("Google Calendar")


def get_calendar_service():
    """Authenticate using OAuth and return Google Calendar service.

    Uses saved credentials from token.json if available, otherwise
    initiates OAuth flow via local server.
    """
    creds = None

    if TOKEN_PATH.exists():
        try:
            token_data = json.loads(TOKEN_PATH.read_text())
            creds = Credentials.from_authorized_user_info(token_data, SCOPES)
        except (json.JSONDecodeError, ValueError):
            pass

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            from google.auth.transport.requests import Request

            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(CLIENT_CONFIG, SCOPES)
            creds = flow.run_local_server(port=0)

        TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
        TOKEN_PATH.write_text(creds.to_json())

    return build("calendar", "v3", credentials=creds)


@mcp.tool
def get_upcoming_events(max_results: int = 10, calendar_id: str = "primary") -> str:
    """Get upcoming calendar events.

    Args:
        max_results: Maximum number of events to return (default: 10)
        calendar_id: Calendar ID to query (default: "primary")

    Returns:
        Formatted list of upcoming events with start time and title
    """
    try:
        service = get_calendar_service()
        now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()

        events_result = (
            service.events()
            .list(
                calendarId=calendar_id,
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            return "No upcoming events found."

        lines = []
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            summary = event.get("summary", "(No title)")
            lines.append(f"• {start}: {summary}")

        return "\n".join(lines)

    except HttpError as error:
        return f"Error fetching events: {error}"


@mcp.tool
def get_events_for_date(date: str, calendar_id: str = "primary") -> str:
    """Get calendar events for a specific date.

    Args:
        date: Date in YYYY-MM-DD format
        calendar_id: Calendar ID to query (default: "primary")

    Returns:
        Formatted list of events for that date
    """
    try:
        service = get_calendar_service()

        start_of_day = datetime.datetime.fromisoformat(date).replace(
            hour=0, minute=0, second=0, tzinfo=datetime.timezone.utc
        )
        end_of_day = start_of_day + datetime.timedelta(days=1)

        events_result = (
            service.events()
            .list(
                calendarId=calendar_id,
                timeMin=start_of_day.isoformat(),
                timeMax=end_of_day.isoformat(),
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            return f"No events found for {date}."

        lines = [f"Events for {date}:"]
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            summary = event.get("summary", "(No title)")
            lines.append(f"• {start}: {summary}")

        return "\n".join(lines)

    except HttpError as error:
        return f"Error fetching events: {error}"


@mcp.tool
def search_events(
    query: str, max_results: int = 10, calendar_id: str = "primary"
) -> str:
    """Search calendar events by keyword.

    Args:
        query: Search term to find in event titles/descriptions
        max_results: Maximum number of events to return (default: 10)
        calendar_id: Calendar ID to query (default: "primary")

    Returns:
        Matching events with start time and title
    """
    try:
        service = get_calendar_service()
        now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()

        events_result = (
            service.events()
            .list(
                calendarId=calendar_id,
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
                q=query,
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            return f"No events found matching '{query}'."

        lines = [f"Events matching '{query}':"]
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            summary = event.get("summary", "(No title)")
            lines.append(f"• {start}: {summary}")

        return "\n".join(lines)

    except HttpError as error:
        return f"Error searching events: {error}"


@mcp.tool
def list_calendars() -> str:
    """List all available calendars.

    Returns:
        List of calendar names and IDs
    """
    try:
        service = get_calendar_service()
        calendars_result = service.calendarList().list().execute()
        calendars = calendars_result.get("items", [])

        if not calendars:
            return "No calendars found."

        lines = ["Available calendars:"]
        for cal in calendars:
            name = cal.get("summary", "(No name)")
            cal_id = cal.get("id")
            primary = " (primary)" if cal.get("primary") else ""
            lines.append(f"• {name}{primary}\n  ID: {cal_id}")

        return "\n".join(lines)

    except HttpError as error:
        return f"Error listing calendars: {error}"


def main():
    """Entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
