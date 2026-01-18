# AGENTS.md

## Commands
- **Run server**: `uv run gcal-mcp` or `uv run python -m gcal_mcp`
- **Lint**: `uv run ruff check src/`
- **Format**: `uv run ruff format src/`
- **Build**: `uv build`

## Architecture
- **Single-module MCP server** using FastMCP framework (`fastmcp<3`)
- All code lives in `src/gcal_mcp/__init__.py`
- Exposes 3 tools: `get_upcoming_events`, `get_events_for_date`, `search_events`
- OAuth credentials stored at `~/.config/gcal-mcp/token.json`
- Uses Google Calendar API v3 (read-only scope)

## Code Style
- Python 3.11+ with type hints
- Ruff for linting and formatting
- Imports: stdlib → third-party → local (alphabetized within groups)
- Functions use docstrings with Args/Returns sections
- Error handling: catch `HttpError`, return user-friendly error strings
- Use `datetime.timezone.utc` for timezone-aware datetimes
- Entry point defined in `pyproject.toml` as `gcal-mcp = "gcal_mcp:main"`
