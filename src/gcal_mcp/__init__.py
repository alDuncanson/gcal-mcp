"""Google Calendar MCP Server - Query upcoming calendar events."""

import datetime
import shutil
import subprocess

import google.auth
from google.auth.exceptions import DefaultCredentialsError
from fastmcp import FastMCP
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

mcp = FastMCP("Google Calendar")


def get_calendar_service():
    """Authenticate using Application Default Credentials and return Google Calendar service.

    Automatically prompts for authentication via gcloud if credentials are missing.
    """
    try:
        creds, _ = google.auth.default(scopes=SCOPES)
        return build("calendar", "v3", credentials=creds)
    except DefaultCredentialsError:
        gcloud_path = shutil.which("gcloud")
        if not gcloud_path:
            raise RuntimeError(
                "No Google credentials found and gcloud CLI is not installed.\n"
                "Install gcloud: https://cloud.google.com/sdk/docs/install\n"
                "Then run: gcloud auth application-default login "
                "--scopes=https://www.googleapis.com/auth/calendar.readonly,"
                "https://www.googleapis.com/auth/cloud-platform"
            )

        auth_scopes = [*SCOPES, "https://www.googleapis.com/auth/cloud-platform"]
        subprocess.run(
            [
                gcloud_path,
                "auth",
                "application-default",
                "login",
                f"--scopes={','.join(auth_scopes)}",
            ],
            check=True,
        )

        creds, _ = google.auth.default(scopes=SCOPES)
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
