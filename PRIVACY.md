# Privacy Policy

**Last updated:** January 18, 2026

## Overview

gcal-mcp is an open-source Model Context Protocol (MCP) server that provides read-only access to your Google Calendar. This privacy policy explains how the application handles your data.

## Data Collection

**We do not collect, store, or transmit any of your data to external servers.**

- All calendar data is accessed directly from Google's API and displayed locally
- No analytics, tracking, or telemetry is included
- No user data is shared with third parties

## Data Storage

- OAuth credentials are stored locally on your machine at `~/.config/gcal-mcp/token.json`
- No calendar data is cached or persisted

## Google API Access

This application requests read-only access to your Google Calendar (`calendar.readonly` scope). It can:

- View your calendar events
- Search for events by keyword

It cannot:

- Create, modify, or delete events
- Access other Google services

## Open Source

This project is open source. You can review the code at: https://github.com/alDuncanson/gcal-mcp

## Contact

For questions or concerns, please open an issue on the GitHub repository.
