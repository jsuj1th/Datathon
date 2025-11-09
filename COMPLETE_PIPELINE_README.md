# 🎯 Complete Job Search & Matching Pipeline

## Overview

This is a complete, interactive job search and matching system that:

1. **Takes user input** - Job query, keywords, location, etc.
2. **Searches multiple sources** - GitHub and LinkedIn job boards
3. **AI-powered matching** - Uses Google Gemini AI to match jobs with your resume
4. **Email delivery** - Sends top matches to your inbox

## 🚀 Quick Start

### Option 1: Run the Complete Pipeline (Recommended)

```bash
python3 main_complete_pipeline.py
```

This will guide you through:
- What job you're looking for
- Keywords to filter by
- Location preferences
- Experience level
- Where to send results

### Option 2: View MCP Tools Inspector

```bash
cd "NewMCP Folder"
python3 web_inspector_simple.py
```

Then open: http://localhost:8000

This shows all available MCP tools in a web interface.

## 📋 How It Works

### Step 1: User Input
The system asks you for:
- **Job Query**: e.g., "Machine Learning Engineer"
- **Keywords**: e.g., "python, tensorflow, nlp"
- **Location**: e.g., "Remote", "San Francisco"
- **Experience Level**: entry, junior, mid, senior, lead
- **Top Matches**: How many results you want
- **Email**: Where to send results
- **Resume**: Path to your PDF resume

### Step 2: Job Collection
Searches multiple sources:
- **GitHub Jobs** - From `github_collector/`
- **LinkedIn Jobs** - From `linkedin_collector/`

Jobs are filtered by your keywords and preferences.

### Step 3: AI Matching
Uses Google Gemini AI to:
- Extract skills from your resume
- Analyze each job description
- Calculate match scores (0-100)
- Provide reasons for each match

### Step 4: Email Delivery
Sends an HTML email with:
- Top matched jobs
- Match scores and reasons
- Direct apply links
- Attached JSON file with all data

## 📁 Output Structure

```
data/
  ├── github_machine_learning_engineer.json
  ├── linkedin_machine_learning_engineer_remote.json
  └── jobs_output.json

matched_jobs/
  └── top_matches.json
```

## 🔧 Configuration

All settings are in `.env`:

```env
# Email Configuration
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-app-password
RECIPIENT_EMAIL=recipient@gmail.com

# Google Gemini AI
GEMINI_API_KEY=your-gemini-api-key

# LinkedIn (Optional)
LINKEDIN_EMAIL=your-linkedin@email.com
LINKEDIN_PASSWORD=your-password
```

## 🛠️ MCP Tools Available

The MCP server provides these tools:

1. **search_jobs** - Search for jobs by keywords and location
2. **match_jobs** - Match jobs with resume using AI
3. **extract_resume** - Extract text from PDF resume
4. **send_email** - Send job matches via email
5. **get_statistics** - Get job search statistics

View all tools at: http://localhost:8000 (when web inspector is running)

## 📊 Example Workflow

```bash
# Run the complete pipeline
python3 main_complete_pipeline.py

# Answer the prompts:
Job query: Machine Learning Engineer
Keywords: python, tensorflow, pytorch, nlp
Location: Remote
Experience level: mid
Top matches: 20
Email: your-email@gmail.com
Resume: ./path/to/resume.pdf

# System will:
# ✅ Search GitHub (50 jobs)
# ✅ Search LinkedIn (50 jobs)
# ✅ Match 100 jobs with AI
# ✅ Return top 20 matches
# ✅ Send email with results
```

## 🎨 Web Inspector Features

The web inspector at `http://localhost:8000` shows:

- **All available MCP tools** with descriptions
- **Input parameters** for each tool
- **Return types** and schemas
- **Real-time server status**

## 🔍 Troubleshooting

### Email not sending?
- Check `GMAIL_USER` and `GMAIL_APP_PASSWORD` in `.env`
- Make sure you're using an App Password, not your regular password
- Enable "Less secure app access" if needed

### No jobs found?
- The collectors may need credentials
- Check that job data exists in `data/` directory
- Try running collectors separately first

### AI matching not working?
- Check `GEMINI_API_KEY` in `.env`
- Verify your Gemini API quota
- Falls back to keyword matching if AI unavailable

### Inspector not loading?
- Make sure port 8000 is not in use
- Try: `lsof -ti:8000 | xargs kill -9`
- Restart the inspector

## 📚 Component Files

- **main_complete_pipeline.py** - Complete interactive pipeline
- **main_job_application.py** - Alternative simpler version
- **NewMCP Folder/job_matcher.py** - AI matching logic
- **NewMCP Folder/job_matcher_mcp_server.py** - MCP server
- **NewMCP Folder/web_inspector_simple.py** - Web inspector
- **github_collector/main.py** - GitHub job collector
- **linkedin_collector/job_searcher.py** - LinkedIn job collector

## 🚦 Running Each Component Separately

### 1. Run GitHub Collector
```bash
cd github_collector
python3 main.py
```

### 2. Run LinkedIn Collector
```bash
cd linkedin_collector
python3 job_searcher.py
```

### 3. Run Job Matcher
```bash
cd "NewMCP Folder"
python3 job_matcher.py
```

### 4. Run MCP Server
```bash
cd "NewMCP Folder"
python3 job_matcher_mcp_stdio.py
```

### 5. View MCP Tools
```bash
cd "NewMCP Folder"
python3 web_inspector_simple.py
# Open http://localhost:8000
```

### 6. Run Complete Pipeline
```bash
python3 main_complete_pipeline.py
```

## ✨ Features

- ✅ Interactive command-line interface
- ✅ Multi-source job collection (GitHub + LinkedIn)
- ✅ AI-powered resume matching
- ✅ Smart keyword filtering
- ✅ Email delivery with HTML formatting
- ✅ Web-based MCP tool inspector
- ✅ JSON export of all results
- ✅ Comprehensive error handling
- ✅ Fallback mechanisms

## 🎯 Next Steps

1. **Configure your `.env` file** with credentials
2. **Run the web inspector** to see available tools
3. **Run the complete pipeline** to find jobs
4. **Check your email** for results!

## 📞 Support

If you encounter issues:
1. Check the `.env` configuration
2. Verify Python dependencies are installed
3. Check the MCP web inspector for tool status
4. Review error messages carefully

---

**Made with ❤️ by the AI Job Matcher Team**
