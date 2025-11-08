# LinkedIn Job Search MCP Server

A Model Context Protocol (MCP) server that provides LinkedIn job search functionality for GitHub Copilot integration.

## Quick Start

### 1. Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure LinkedIn credentials in .env
LINKEDIN_EMAIL=your-email@example.com
LINKEDIN_PASSWORD=your-password
```

### 2. Start Server

```bash
python start_http_server.py
```

Server runs at `http://localhost:8000/mcp`

### 3. Configure VS Code

Add to your VS Code `settings.json`:

```json
{
  "github.copilot.chat.experimental.mcp.servers": [
    {
      "name": "Linkedin Job Search",
      "transport": {
        "type": "http",
        "url": "http://localhost:8000/mcp"
      }
    }
  ]
}
```

### 4. Usage

In GitHub Copilot:
```
@agent Search for software engineer jobs in San Francisco
```

## Features

- **LinkedIn Job Search**: Search jobs by keywords and location
- **Structured JSON Output**: Standardized job data format
- **Auto File Saving**: Results saved to `job_search_results/`
- **GitHub Copilot Integration**: Seamless VS Code integration

## Available Tools

### `search_jobs`
- `keywords` (required): Job search terms
- `limit` (optional): Max results (default: 10)
- `offset` (optional): Skip results (default: 0)
- `location` (optional): Location filter

## File Structure

```
├── src/server/linkedin_mcp_client.py  # Main MCP server
├── copilot_runner.py                  # HTTP server runner  
├── start_http_server.py               # Startup script
├── job_search_results/                # Saved search results
└── requirements.txt                   # Dependencies
```

## Dependencies

- `fastmcp`: MCP server framework
- `linkedin-api`: LinkedIn API client
- `python-dotenv`: Environment variables
