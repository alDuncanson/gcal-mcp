# gcal-mcp

[![PyPI](https://img.shields.io/pypi/v/gcal-mcp)](https://pypi.org/project/gcal-mcp/)
[![CI](https://github.com/alDuncanson/gcal-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/alDuncanson/gcal-mcp/actions/workflows/ci.yml)
[![Release](https://github.com/alDuncanson/gcal-mcp/actions/workflows/release.yml/badge.svg)](https://github.com/alDuncanson/gcal-mcp/actions/workflows/release.yml)

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server for
Google Calendar that uses OAuth 2.0 with PKCE for secure authentication.

### Bring your own Oauth client

To use your own OAuth client credentials:

```bash
gcal-mcp --credentials /path/to/credentials.json
```
