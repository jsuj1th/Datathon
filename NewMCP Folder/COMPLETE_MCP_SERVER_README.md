# 🎯 Complete Job Search MCP Server

## Overview

This is a comprehensive MCP (Model Context Protocol) server that provides complete job search functionality through a set of tools. It allows you to search jobs, match them with your resume using AI, filter by criteria, and send results via email - all through standardized MCP tool calls.

## 🚀 Features

### 7 Powerful MCP Tools:

1. **`search_jobs_complete`** - Complete pipeline (search + match + rank)
2. **`search_github_jobs`** - Search GitHub for jobs
3. **`search_linkedin_jobs`** - Search LinkedIn/The Muse for jobs
4. **`match_jobs_with_resume`** - AI-powered resume matching
5. **`extract_resume_text`** - Extract text from PDF resume
6. **`send_job_email`** - Send results via email
7. **`filter_jobs_by_criteria`** - Filter jobs by experience, location, keywords

## 📋 Tool Details

### 1. `search_jobs_complete` - The Main Tool ⭐

**Complete job search pipeline that does everything:**
- Searches GitHub and LinkedIn
- Filters by experience level
- Matches with your resume using AI
- Returns top ranked results

**Inputs:**
```json
{
  "keywords": "Machine Learning Engineer",
  "location": "Remote",
  "experience_level": "mid",  // entry, junior, mid, senior, lead
  "resume_path": "./Resume/Resume.pdf",
  "top_n": 20,
  "search_limit": 50
}
```

**Output:**
```json
{
  "success": true,
  "search_params": {...},
  "jobs_found": {
    "github": 50,
    "linkedin": 45,
    "total": 95
  },
  "matched_jobs": [
    {
      "company": "OpenAI",
      "position": "ML Engineer",
      "match_score": 95,
      "match_reason": "Strong Python and ML skills",
      ...
    },
    ...
  ]
}
```

---

### 2. `search_github_jobs`

Search GitHub for jobs using Firecrawl or cached data.

**Inputs:**
```json
{
  "keywords": "Data Scientist",
  "location": "San Francisco",
  "limit": 50
}
```

---

### 3. `search_linkedin_jobs`

Search LinkedIn/The Muse for jobs.

**Inputs:**
```json
{
  "keywords": "Software Engineer",
  "location": "Remote",
  "limit": 50
}
```

---

### 4. `match_jobs_with_resume`

Match jobs with your resume using Google Gemini AI.

**Inputs:**
```json
{
  "resume_path": "./Resume/Resume.pdf",
  "jobs": [...],  // Array of job objects
  "top_n": 20
}
```

**Output:**
- Jobs ranked by AI match score (0-100)
- Match reasons for each job
- Skills alignment

---

### 5. `extract_resume_text`

Extract text from PDF resume.

**Inputs:**
```json
{
  "resume_path": "./Resume/Resume.pdf"
}
```

**Output:**
```json
{
  "success": true,
  "characters": 1234,
  "preview": "First 500 chars...",
  "full_text": "Complete resume text..."
}
```

---

### 6. `send_job_email`

Send matched jobs via email.

**Inputs:**
```json
{
  "recipient_email": "user@example.com",
  "matched_jobs": [...],
  "subject": "Your Top Job Matches"
}
```

---

### 7. `filter_jobs_by_criteria`

Filter jobs by multiple criteria.

**Inputs:**
```json
{
  "jobs": [...],
  "experience_level": "mid",
  "location": "Remote",
  "keywords": ["python", "ai"],
  "min_match_score": 70
}
```

---

## 🛠️ Running the Server

### Method 1: Direct STDIO Mode
```bash
cd "NewMCP Folder"
python3 complete_job_search_mcp_server.py
```

### Method 2: Via MCP Inspector
```bash
cd "NewMCP Folder"
python3 web_inspector_simple.py
# Open http://localhost:8000
```

### Method 3: From MCP Client
Configure your MCP client with:
```json
{
  "command": "python3",
  "args": [
    "/path/to/complete_job_search_mcp_server.py"
  ],
  "env": {
    "GEMINI_API_KEY": "your-api-key"
  }
}
```

---

## 💡 Usage Examples

### Example 1: Complete Job Search
```json
// Tool: search_jobs_complete
{
  "keywords": "Machine Learning Engineer",
  "location": "Remote",
  "experience_level": "mid",
  "resume_path": "./Resume/Resume.pdf",
  "top_n": 20
}
```

This single call will:
1. Search GitHub (50 jobs)
2. Search LinkedIn (50 jobs)
3. Filter by "mid" experience
4. Match with your resume using AI
5. Return top 20 ranked matches

### Example 2: Search Then Match
```json
// Step 1: Search GitHub
// Tool: search_github_jobs
{
  "keywords": "Data Scientist",
  "limit": 30
}

// Step 2: Match with resume
// Tool: match_jobs_with_resume
{
  "resume_path": "./Resume/Resume.pdf",
  "jobs": [...jobs from step 1...],
  "top_n": 10
}

// Step 3: Send email
// Tool: send_job_email
{
  "recipient_email": "user@example.com",
  "matched_jobs": [...matched jobs...]
}
```

### Example 3: Filter and Refine
```json
// Tool: filter_jobs_by_criteria
{
  "jobs": [...all jobs...],
  "experience_level": "senior",
  "location": "San Francisco",
  "keywords": ["python", "tensorflow"],
  "min_match_score": 80
}
```

---

## 🔧 Configuration

Set these environment variables in `.env`:

```env
# Required for AI matching
GEMINI_API_KEY=your-gemini-api-key

# Required for email
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password

# Optional for enhanced search
FIRECRAWL_API_KEY=your-firecrawl-key
LINKEDIN_EMAIL=your-linkedin-email
LINKEDIN_PASSWORD=your-linkedin-password
```

---

## 📊 Tool Comparison

| Tool | GitHub | LinkedIn | AI Match | Email | Filters |
|------|--------|----------|----------|-------|---------|
| `search_jobs_complete` | ✅ | ✅ | ✅ | ❌ | ✅ |
| `search_github_jobs` | ✅ | ❌ | ❌ | ❌ | ❌ |
| `search_linkedin_jobs` | ❌ | ✅ | ❌ | ❌ | ❌ |
| `match_jobs_with_resume` | ❌ | ❌ | ✅ | ❌ | ❌ |
| `send_job_email` | ❌ | ❌ | ❌ | ✅ | ❌ |
| `filter_jobs_by_criteria` | ❌ | ❌ | ❌ | ❌ | ✅ |

**Recommendation:** Use `search_jobs_complete` for most cases as it does everything in one call!

---

## 🎯 Typical Workflow

### For End Users:
1. Call `search_jobs_complete` with your preferences
2. Get back ranked, matched jobs
3. Optionally call `send_job_email` to email results

### For Advanced Use:
1. Call `search_github_jobs` and `search_linkedin_jobs` separately
2. Combine results
3. Call `filter_jobs_by_criteria` to refine
4. Call `match_jobs_with_resume` to rank
5. Call `send_job_email` to share

---

## 🌐 Accessing via Web Inspector

1. Start the inspector:
```bash
cd "NewMCP Folder"
python3 web_inspector_simple.py
```

2. Open http://localhost:8000

3. You'll see all 7 tools with:
   - Descriptions
   - Input schemas
   - Required/optional parameters
   - Return types

---

## 📝 Response Format

All tools return consistent JSON:

```json
{
  "success": true/false,
  "error": "error message if failed",
  ...tool-specific data...
}
```

---

## 🔍 Error Handling

The server handles:
- ✅ Missing API keys (falls back to cached data)
- ✅ Invalid resume paths
- ✅ Network timeouts
- ✅ API rate limits
- ✅ Invalid inputs

All errors return structured JSON with details.

---

## 🚦 Testing

### Test the complete pipeline:
```bash
python3 complete_job_search_mcp_server.py --test
```

### Test individual tools:
Use the web inspector at http://localhost:8000

---

## 📚 Integration Examples

### Python Client:
```python
from mcp import Client

client = Client("complete-job-search")

result = await client.call_tool(
    "search_jobs_complete",
    {
        "keywords": "ML Engineer",
        "resume_path": "./Resume.pdf",
        "experience_level": "mid"
    }
)
```

### Claude Desktop:
Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "job-search": {
      "command": "python3",
      "args": ["path/to/complete_job_search_mcp_server.py"]
    }
  }
}
```

---

## ✨ Key Benefits

1. **Unified Interface** - One MCP server for all job search needs
2. **AI-Powered** - Uses Google Gemini for intelligent matching
3. **Multi-Source** - Searches GitHub and LinkedIn simultaneously
4. **Flexible** - Use complete pipeline or individual tools
5. **Standardized** - Follows MCP protocol for interoperability
6. **Error Resilient** - Falls back gracefully when APIs fail
7. **Filterable** - Filter by experience, location, keywords, scores

---

## 🎓 Learn More

- **MCP Protocol**: https://modelcontextprotocol.io
- **Web Inspector**: http://localhost:8000 (when running)
- **Main Pipeline**: `../main_complete_pipeline.py`
- **System Overview**: `../SYSTEM_OVERVIEW.md`

---

**Ready to search for jobs via MCP? Start the server and call `search_jobs_complete`!** 🚀
