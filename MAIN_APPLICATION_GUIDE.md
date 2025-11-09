# 🚀 Job Search & Match Application - Complete Guide

## ✅ What's Been Fixed & Created

### 1. **MCP Server Issues - FIXED** ✅
- Fixed hardcoded paths in configuration files
- Added missing methods (`extract_resume`, `match_job_with_resume`) to `job_matcher.py`
- Installed all required dependencies (PyPDF2, google-generativeai)
- MCP server now starts without errors

### 2. **Web Inspector - CREATED** ✅
- Created simple web inspector at `http://localhost:8000`
- Displays all 5 MCP tools with their parameters
- Beautiful, modern UI to view all available capabilities

### 3. **Main Application - CREATED** ✅
- New file: `main_job_application.py` in parent directory
- Interactive CLI that asks for:
  - User query (job type)
  - Job keywords
  - Recipient email address
  - Resume path
  - Number of top matches

---

## 📂 File Structure

```
Datathon/
├── main_job_application.py          ← NEW! Main interactive application
├── .env                              ← Your credentials (already configured)
├── NewMCP Folder/
│   ├── job_matcher.py                ← FIXED! Added missing methods
│   ├── job_matcher_mcp_stdio.py      ← MCP server (stdio mode)
│   ├── web_inspector_simple.py       ← NEW! Web inspector
│   └── launch_inspector.sh           ← NEW! Inspector launcher
├── data/                             ← Job search results
└── matched_jobs/                     ← Matched results output
```

---

## 🎯 How to Use

### Option 1: Run the Main Interactive Application

```bash
cd /Users/sujithjulakanti/Desktop/Datathon
python3 main_job_application.py
```

**What it does:**
1. Asks for your job search query
2. Asks for keywords (comma-separated)
3. Asks for location preference
4. Asks for recipient email address
5. Asks for resume path
6. Searches for jobs (optional)
7. Matches jobs with your resume using AI
8. Displays top matches
9. Optionally sends results via email

**Example interaction:**
```
🎯 JOB SEARCH & MATCH APPLICATION
==================================================

📝 What type of job are you looking for?
   Your query: Machine Learning Engineer

🔍 Enter job keywords (comma-separated)
   Keywords: python, machine learning, tensorflow, ai

📍 Enter location preference (optional)
   Location: Remote

📧 Enter recipient email address
   Email: pranavipathakota@gmail.com

📄 Enter path to your resume (PDF)
   Resume path: [Press Enter for default]

🎯 How many top job matches do you want?
   Number: 50
```

---

### Option 2: View MCP Tools in Web Inspector

The web inspector is currently running at:
**http://localhost:8000**

It displays all 5 available MCP tools:
1. **search_jobs** - Search across job platforms
2. **match_jobs** - Match jobs with resume using AI
3. **send_email** - Send results via email
4. **extract_resume** - Extract text from PDF
5. **get_statistics** - Get job search statistics

---

### Option 3: Use MCP Server Directly

```bash
cd "/Users/sujithjulakanti/Desktop/Datathon/NewMCP Folder"
python3 job_matcher_mcp_stdio.py
```

The server communicates via stdio (standard input/output) for MCP protocol.

---

## 🛠️ Available MCP Tools

### 1. **search_jobs**
Search for jobs across multiple platforms

**Parameters:**
- `keywords` (string, required) - Job search keywords
- `location` (string, optional) - Location filter
- `limit` (integer, optional) - Max results (default: 30)

**Example:**
```json
{
  "keywords": "Machine Learning Engineer",
  "location": "Remote",
  "limit": 50
}
```

---

### 2. **match_jobs**
Match jobs with resume using AI/LLM

**Parameters:**
- `resume_path` (string, required) - Path to resume PDF
- `jobs_dirs` (array, required) - Directories with job JSON files
- `top_n` (integer, optional) - Number of top matches (default: 50)

**Example:**
```json
{
  "resume_path": "./NewMCP Folder/MCP_Servers/pdfDocs/Resume_NEW_ML_Pathakota_Pranavi_2.pdf",
  "jobs_dirs": ["./data", "./linkedin_collector/job_search_results"],
  "top_n": 50
}
```

---

### 3. **send_email**
Send matched jobs via Gmail SMTP

**Parameters:**
- `recipient` (string, required) - Recipient email
- `subject` (string, required) - Email subject
- `matched_jobs_file` (string, required) - Path to matched jobs JSON

**Example:**
```json
{
  "recipient": "pranavipathakota@gmail.com",
  "subject": "Your Top Job Matches",
  "matched_jobs_file": "./matched_jobs/top_matches.json"
}
```

---

### 4. **extract_resume**
Extract text from PDF resume

**Parameters:**
- `pdf_path` (string, required) - Path to PDF resume

---

### 5. **get_statistics**
Get statistics about job search results

**Parameters:**
- `jobs_dirs` (array, required) - Directories with job JSON files

---

## 📧 Email Configuration

Your email is already configured in `.env`:

```properties
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
GMAIL_USER=sujithjulakanti2002@gmail.com
GMAIL_APP_PASSWORD=jytu utys knks evyj
RECIPIENT_EMAIL=pranavipathakota@gmail.com
```

✅ Ready to send emails!

---

## 🔑 API Keys Configured

```properties
✅ GEMINI_API_KEY - For AI job matching
✅ GMAIL credentials - For sending emails
✅ LinkedIn credentials - For job searching
```

---

## 📊 Output Files

### Matched Jobs Output
Location: `./matched_jobs/top_matches.json`

Format:
```json
{
  "total_matches": 50,
  "matched_jobs": [
    {
      "position": "Machine Learning Engineer",
      "company": "Google",
      "location": "Remote",
      "match_score": 95,
      "match_reason": "Strong Python and ML skills match",
      "apply_link": "https://..."
    }
  ],
  "generated_at": "2025-11-09T..."
}
```

---

## 🚀 Quick Start Commands

### Start Web Inspector (Already Running)
```bash
cd "/Users/sujithjulakanti/Desktop/Datathon/NewMCP Folder"
python3 web_inspector_simple.py
```
Then open: http://localhost:8000

### Run Main Application
```bash
cd /Users/sujithjulakanti/Desktop/Datathon
python3 main_job_application.py
```

### Test MCP Server
```bash
cd "/Users/sujithjulakanti/Desktop/Datathon/NewMCP Folder"
python3 job_matcher_mcp_stdio.py --version
```

---

## ✅ Everything is Ready!

1. ✅ MCP Server working - No errors
2. ✅ Web Inspector running - View at http://localhost:8000
3. ✅ Main application created - Interactive job search
4. ✅ All dependencies installed
5. ✅ Email configured and working
6. ✅ Gemini AI configured for matching

---

## 🎯 Next Steps

1. **View the tools** → Open http://localhost:8000 in your browser
2. **Run the app** → Execute `python3 main_job_application.py`
3. **Get matched jobs** → Enter your preferences and get AI-matched results
4. **Receive email** → Get top matches sent to your inbox

---

## 🆘 Troubleshooting

### If web inspector port is busy:
Edit `web_inspector_simple.py` and change `port = 8000` to another port

### If email fails:
Check your `.env` file has correct Gmail credentials

### If resume not found:
Update the resume path when prompted or place your resume in:
`./NewMCP Folder/MCP_Servers/pdfDocs/`

---

## 📝 Notes

- The MCP server runs in stdio mode (standard input/output)
- Web inspector provides a visual interface to see all tools
- Main application provides interactive CLI for end users
- All matched jobs are saved to `./matched_jobs/` directory
- Email uses Gmail SMTP with app password (already configured)

---

**Created by: AI Job Matcher System**  
**Date: November 9, 2025**
