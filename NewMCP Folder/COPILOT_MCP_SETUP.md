# MCP HTTP Server for GitHub Copilot

## 🎯 Overview

This HTTP server wraps your job search MCP server so it works with GitHub Copilot in VS Code. Copilot requires HTTP-based MCP servers, while your original server uses STDIO.

## ✅ Server is Now Running!

The server is running at: **http://localhost:8080**

- **MCP Endpoint**: http://localhost:8080/mcp
- **Health Check**: http://localhost:8080/health
- **Web Interface**: http://localhost:8080 (open in browser)

## 🔧 Configuration for GitHub Copilot

### Option 1: VS Code Settings (Recommended)

1. Open VS Code Settings (Cmd + ,)
2. Search for "MCP" or "Model Context Protocol"
3. Add the server configuration:

```json
{
  "github.copilot.mcp.servers": {
    "job-search": {
      "url": "http://localhost:8080/mcp",
      "name": "Job Search Server"
    }
  }
}
```

### Option 2: Workspace Settings

Create or edit `.vscode/settings.json` in your workspace:

```json
{
  "github.copilot.mcp.servers": {
    "job-search": {
      "url": "http://localhost:8080/mcp",
      "name": "ML Job Search - Texas"
    }
  }
}
```

### Option 3: User Settings File

Edit your user settings file directly:
- Mac: `~/Library/Application Support/Code/User/settings.json`
- Windows: `%APPDATA%\Code\User\settings.json`
- Linux: `~/.config/Code/User/settings.json`

Add the MCP configuration there.

## 🚀 How to Use

### 1. Keep the Server Running

The server needs to be running for Copilot to access it. It's currently running in the background.

To start it manually later:
```bash
cd "/Users/sujithjulakanti/Desktop/Datathon/NewMCP Folder"
./start_http_server.sh
```

Or run directly:
```bash
python3 simple_mcp_http_server.py
```

### 2. Use with GitHub Copilot

Once configured, you can ask Copilot natural language questions like:

- "Search for ML Engineer jobs in Texas"
- "Find entry-level machine learning positions"
- "Show me AI engineer jobs in Austin"

Copilot will use the MCP server to fetch real job data!

### 3. Test the Server

Open http://localhost:8080 in your browser to see the web interface and confirm it's working.

Or test the health endpoint:
```bash
curl http://localhost:8080/health
```

## 📊 Available Data

The server currently has **15 entry-level ML Engineer jobs in Texas** including positions at:
- Dell Technologies (Austin)
- Tesla (Austin)
- Oracle (Austin)
- Indeed (Austin)
- Charles Schwab (Dallas)
- American Airlines (Dallas)
- AT&T (Dallas)
- And more!

## 🛠️ Troubleshooting

### Server Not Responding

1. Check if the server is running:
   ```bash
   curl http://localhost:8080/health
   ```

2. If not running, start it:
   ```bash
   cd "/Users/sujithjulakanti/Desktop/Datathon/NewMCP Folder"
   python3 simple_mcp_http_server.py
   ```

### Port Already in Use

If port 8080 is already in use, edit `simple_mcp_http_server.py` and change the port:
```python
server = SimpleJobSearchServer(host='localhost', port=8081)  # Use 8081 instead
```

Then update your Copilot configuration to use the new port.

### Copilot Not Finding the Server

1. Make sure the server is running
2. Reload VS Code (Cmd + Shift + P → "Reload Window")
3. Check the Copilot logs in VS Code Output panel

## 📝 Files Created

- `simple_mcp_http_server.py` - Main HTTP server
- `start_http_server.sh` - Convenient startup script
- `mcp_http_server.py` - Advanced version (not needed for basic use)
- `COPILOT_MCP_SETUP.md` - This file

## 🔄 Updating Job Data

To get fresh job listings:
```bash
cd /Users/sujithjulakanti/Desktop/Datathon
python3 get_texas_ml_jobs.py
```

The server will automatically use the updated data.

## ⚠️ Important Notes

1. **Keep the server running** - The HTTP server must be running for Copilot to access it
2. **Local only** - The server runs on localhost and is not accessible from outside your computer
3. **API Keys** - The server uses the API keys from your environment variables

## 🎉 Success!

Your MCP server is now compatible with GitHub Copilot! You can ask Copilot to search for jobs and it will use your custom job search functionality.

---

**Current Status**: ✅ Server Running on http://localhost:8080
**Job Data**: ✅ 15 ML Engineer jobs in Texas loaded
**Ready for**: GitHub Copilot integration
