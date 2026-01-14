# gcal-mcp

An MCP server that provides tools to query Google Calendar events.

## Installation

```bash
pip install gcal-mcp
```

Or with uv:

```bash
uv pip install gcal-mcp
```

## Setup

### 1. Create Google Cloud credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the [Google Calendar API](https://console.cloud.google.com/flows/enableapi?apiid=calendar-json.googleapis.com)
4. Go to **APIs & Services > Credentials**
5. Click **Create Credentials > OAuth client ID**
6. Select **Desktop app** as the application type
7. Download the JSON file and save it as `credentials.json` in `~/.config/gcal-mcp/`

### 2. Authenticate (first run)

On the first run, a browser window will open for Google OAuth authentication:

```bash
gcal-mcp
```

This creates a `token.json` file in `~/.config/gcal-mcp/` for future use.

## Configuration

By default, credentials are stored in `~/.config/gcal-mcp/`. You can override this with the `GCAL_MCP_CONFIG_DIR` environment variable:

```bash
export GCAL_MCP_CONFIG_DIR=/path/to/your/config
```

## Tools

| Tool | Description |
|------|-------------|
| `get_upcoming_events` | Get the next N upcoming events |
| `get_events_for_date` | Get events for a specific date (YYYY-MM-DD) |
| `search_events` | Search events by keyword |
| `list_calendars` | List all available calendars |

## Usage with Amp/Claude

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "gcal": {
      "command": "gcal-mcp"
    }
  }
}
```

Or if using uvx:

```json
{
  "mcpServers": {
    "gcal": {
      "command": "uvx",
      "args": ["gcal-mcp"]
    }
  }
}
```

## Example queries

- "What meetings do I have today?"
- "Show me my next 5 calendar events"
- "Do I have any events with 'standup' in the title?"
- "What's on my calendar for 2025-01-15?"

## Development

```bash
git clone https://github.com/alDuncanson/gcal-mcp
cd gcal-mcp
uv sync
uv run gcal-mcp
```
