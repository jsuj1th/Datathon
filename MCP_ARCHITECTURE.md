# How the LinkedIn MCP Server Works

## Overview
Our LinkedIn MCP (Model Context Protocol) server enables Claude and other AI clients to interact with LinkedIn's job search and feed functionality through standardized tool calls.

## Architecture Components

### 1. MCP Server Framework
```python
import fastmcp
mcp = fastmcp.FastMCP("linkedin-mcp")
```
- Uses FastMCP library for easy MCP server creation
- Handles JSON-RPC communication protocol automatically
- Provides tool registration via decorators

### 2. Available Tools

#### Tool 1: `search_jobs`
```python
@mcp.tool
def search_jobs(keywords: str, limit: int = 3, offset: int = 0, location: str = '') -> str:
```
**Purpose**: Search for jobs on LinkedIn  
**Parameters**:
- `keywords`: Job search terms (e.g., "software engineer", "data scientist")
- `limit`: Number of results to return (default: 3)
- `offset`: Skip first N results (for pagination)
- `location`: Geographic filter (e.g., "San Francisco", "Remote")

**Returns**: Formatted string with job details including title, company, location, and description

#### Tool 2: `get_feed_posts`
```python
@mcp.tool
def get_feed_posts(limit: int = 10, offset: int = 0) -> str:
```
**Purpose**: Retrieve LinkedIn feed posts  
**Parameters**:
- `limit`: Number of posts to retrieve
- `offset`: Skip first N posts

**Returns**: Formatted string with post content and authors

#### Tool 3: `get_profile`
```python
@mcp.tool
def get_profile(public_id: Optional[str] = None) -> str:
```
**Purpose**: Get LinkedIn profile information  
**Parameters**:
- `public_id`: LinkedIn public ID (optional, gets own profile if None)

**Returns**: Profile details including name, headline, location, summary

### 3. Communication Protocol

The MCP server communicates using JSON-RPC over stdio:

#### Tool Discovery
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

#### Tool Execution
```json
{
  "jsonrpc": "2.0", 
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "search_jobs",
    "arguments": {
      "keywords": "python developer",
      "location": "remote",
      "limit": 5
    }
  }
}
```

## Integration Patterns for Multiple MCP Tools

### Pattern 1: Multiple Independent Servers (Recommended)

**File Structure:**
```
job-search-suite/
├── linkedin-mcp-server/
│   ├── main.py
│   └── src/server/linkedin_mcp_client.py
├── glassdoor-mcp-server/
│   ├── main.py
│   └── src/server/glassdoor_mcp_client.py
├── github-jobs-mcp-server/
│   ├── main.py
│   └── src/server/github_mcp_client.py
└── email-mcp-server/
    ├── main.py
    └── src/server/email_mcp_client.py
```

**Claude Desktop Config:**
```json
{
  "mcpServers": {
    "linkedin-jobs": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/path/to/linkedin-mcp-server"
    },
    "glassdoor-jobs": {
      "command": "python", 
      "args": ["main.py"],
      "cwd": "/path/to/glassdoor-mcp-server"
    },
    "github-jobs": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/path/to/github-jobs-mcp-server"
    },
    "email-notifications": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/path/to/email-mcp-server"
    }
  }
}
```

**Advantages:**
- ✅ Independent development and deployment
- ✅ Better error isolation
- ✅ Easier to maintain and debug
- ✅ Can use different dependencies per service
- ✅ Scalable architecture

### Pattern 2: Unified MCP Server

**File Structure:**
```
unified-job-mcp-server/
├── main.py
└── src/
    ├── tools/
    │   ├── linkedin_tools.py
    │   ├── glassdoor_tools.py
    │   ├── github_tools.py
    │   └── email_tools.py
    └── server/
        └── unified_mcp_client.py
```

**Implementation:**
```python
# src/server/unified_mcp_client.py
import fastmcp
from tools import linkedin_tools, glassdoor_tools, github_tools, email_tools

mcp = fastmcp.FastMCP("unified-job-server")

# Register all tools
linkedin_tools.register_tools(mcp)
glassdoor_tools.register_tools(mcp)
github_tools.register_tools(mcp)
email_tools.register_tools(mcp)
```

**Claude Desktop Config:**
```json
{
  "mcpServers": {
    "job-search-suite": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/path/to/unified-job-mcp-server"
    }
  }
}
```

## Current Working Example

### Starting the Server
```bash
# Navigate to the project directory
cd /Users/sujithjulakanti/Desktop/Datathon

# Start the MCP server
python main.py
```

### Testing the Server
```bash
# Test LinkedIn API directly
python test_simple_linkedin.py

# Test individual functions
python -c "
from src.server.linkedin_mcp_client import search_jobs_direct
print(search_jobs_direct('python developer', 'remote', 3))
"
```

### Using with Claude Desktop
1. Copy `claude_desktop_config.json` content to Claude Desktop settings
2. Update the `cwd` path to your actual project path
3. Set your LinkedIn credentials in `.env` file
4. Restart Claude Desktop

### Available Commands in Claude
Once connected, you can use these commands in Claude:

- **"Search for Python developer jobs in San Francisco"**
  - Calls: `search_jobs("python developer", 3, 0, "San Francisco")`

- **"Show me recent LinkedIn posts"** 
  - Calls: `get_feed_posts(10, 0)`

- **"Get my LinkedIn profile information"**
  - Calls: `get_profile()`

## Next Steps for Multi-Tool Integration

### 1. Create Additional MCP Servers
Based on our LinkedIn server template, create:
- `glassdoor-mcp-server` for company reviews and salary data
- `github-jobs-mcp-server` for tech job postings
- `indeed-mcp-server` for broader job search
- `email-mcp-server` for sending job digests

### 2. Standardize Tool Interfaces
Use consistent function signatures across servers:
```python
# Standard job search interface
@mcp.tool
def search_jobs(keywords: str, location: str = '', limit: int = 10) -> dict:
    return {
        "source": "platform_name",
        "jobs": [...],
        "total_count": int,
        "search_params": {...}
    }
```

### 3. Create Orchestration Tools
Add tools that coordinate multiple services:
```python
@mcp.tool
def search_all_platforms(keywords: str, location: str = '') -> str:
    """Search jobs across LinkedIn, Glassdoor, GitHub, and Indeed"""
    # Combine results from multiple platforms
```

## Benefits of This MCP Architecture

1. **Standardized Interface**: All tools use the same JSON-RPC protocol
2. **Type Safety**: FastMCP provides automatic type checking and validation
3. **Documentation**: Tool descriptions are automatically exposed to clients
4. **Error Handling**: Consistent error responses across all tools
5. **Scalability**: Easy to add new tools and platforms
6. **Client Agnostic**: Works with Claude, custom clients, or other MCP-compatible tools

This architecture makes it easy to build a comprehensive job search and application suite that Claude can orchestrate seamlessly.
