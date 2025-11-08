# Quick Start Guide

## 1. Setup
```bash
# Install dependencies
./setup.sh

# Or manually:
python -m pip install -r requirements.txt

# Configure credentials
cp .env.example .env
# Edit .env with your LinkedIn email and password
```

## 2. Test LinkedIn Connection
```bash
python test_simple_linkedin.py
```

## 3. Start MCP Server
```bash
python main.py
```

## 4. Configure Claude Desktop
Add this to your Claude Desktop configuration:
```json
{
  "mcpServers": {
    "linkedin": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/path/to/your/jobly-linkedin-mcp-server",
      "env": {
        "LINKEDIN_EMAIL": "your_linkedin_email",
        "LINKEDIN_PASSWORD": "your_linkedin_password"
      }
    }
  }
}
```

## 5. Use with Claude
Once configured, you can ask Claude to:
- Search for jobs on LinkedIn
- Retrieve your LinkedIn feed posts
- Get profile information

Example prompts:
- "Search for software engineer jobs in San Francisco"
- "Show me my latest LinkedIn feed posts"
- "Get my LinkedIn profile information"
