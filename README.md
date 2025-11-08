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

## ⚡ Quick Start

### 1. Start the HTTP Server
```bash
python start_http_server.py
```

### 2. Configure GitHub Copilot  
Add this MCP server:
- **Name**: `linkedin-jobs`
- **Transport**: `HTTP`
- **URL**: `http://localhost:8000/mcp`

### 3. Search Jobs with GitHub Copilot
Ask GitHub Copilot: *"Find software engineer jobs in San Francisco"*

## ✨ Features

✅ **LinkedIn Integration** - Search real LinkedIn job postings  
✅ **Structured JSON Data** - Company, position, location, salary, etc.  
✅ **GitHub Copilot Ready** - HTTP MCP server for seamless integration  
✅ **Flexible Search** - Keywords, location, experience level filters  
✅ **Rich Metadata** - Job type, remote options, posting dates  

## 📊 Example Output

```json
{
  "jobs": [
    {
      "company": "Google",
      "position": "Software Engineer", 
      "apply_link": "https://linkedin.com/jobs/view/123456",
      "location": "San Francisco, CA",
      "job_type": "full_time",
      "experience_level": "mid_level",
      "remote_option": "hybrid",
      "source": "linkedin"
    }
  ],
  "total_found": 25,
  "search_params": {
    "keywords": "software engineer",
    "location": "San Francisco"
  }
}
```

## 🛠️ Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up LinkedIn credentials  
cp .env.example .env
# Edit .env with your LinkedIn email/password

# Start the server
python start_http_server.py
```

## 🔧 Available Tool

### `search_jobs`
Search LinkedIn for jobs with structured output.

**Parameters:**
- `keywords` (required): Job search terms (e.g., "python developer")
- `location` (optional): Geographic filter (e.g., "San Francisco", "Remote") 
- `limit` (optional): Number of results (default: 10, max: 25)
- `offset` (optional): Pagination offset (default: 0)

## 📖 Documentation

- 🎉 [Setup Complete Guide](SETUP_COMPLETE.md) - You're all set!
- 🚀 [Quick Start HTTP](QUICKSTART_HTTP.md) - HTTP server guide  
- 🔧 [HTTP Server Setup](HTTP_SERVER_SETUP.md) - Detailed HTTP setup
- 📋 [GitHub Copilot Setup](GITHUB_COPILOT_SETUP.md) - Copilot integration

## 🛠️ Requirements

- Python 3.8+
- LinkedIn account credentials
- GitHub Copilot

## 🚨 Troubleshooting

**Server won't start?**
- Check port 8000 is available: `lsof -i :8000`
- Verify LinkedIn credentials in `.env` file
- Run: `pip install -r requirements.txt`

**GitHub Copilot can't connect?**
- Ensure server runs at `http://localhost:8000/mcp`
- Check firewall settings
- Restart GitHub Copilot after adding server

**LinkedIn authentication errors?**
- Double-check email/password in `.env`
- LinkedIn may rate-limit API requests

---

Built with [FastMCP](https://github.com/jlowin/fastmcp) for seamless MCP integration 🎉
