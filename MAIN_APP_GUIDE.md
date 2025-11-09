# Job Search Application - User Guide

## Quick Start

### Option 1: Interactive Job Search (Recommended for Users)

Run the main application that guides you through the job search process:

```bash
python3 main_job_search.py
```

This will:
1. ✅ Ask for your resume (PDF)
2. ✅ Ask for job keywords (e.g., "Machine Learning", "Data Science")
3. ✅ Ask for location preferences
4. ✅ Ask how many matches you want
5. ✅ Ask for recipient email address (optional)
6. ✅ Search and match jobs using AI
7. ✅ Display and save results
8. ✅ Email results (if requested)

### Option 2: MCP Web Inspector (For Developers/Testing)

Launch the MCP server in a web interface to test individual tools:

```bash
cd "NewMCP Folder"
./launch_mcp_inspector.sh
```

This will open http://localhost:5173 where you can:
- Browse all 4 MCP tools
- Test tools interactively
- View request/response logs

---

## Main Application Features

### 1. Resume Upload
- Automatically finds PDFs in the `uploads/` folder
- Or specify a custom path to your resume

### 2. Keyword-Based Search
- Enter comma-separated keywords
- Examples: "Machine Learning, AI, Python"
- Filters jobs matching your interests

### 3. AI-Powered Matching
- Uses Google Gemini AI to analyze job fit
- Provides match scores (0-100)
- Gives detailed reasons for each match

### 4. Results Delivery
- View top matches in terminal
- Save to JSON file
- Optional email delivery

---

## Example Usage

```
🎯 AI-Powered Job Search & Matching System
======================================================================

📄 RESUME UPLOAD
----------------------------------------------------------------------
Found resume: my_resume.pdf
Use this resume? (y/n): y

🔍 JOB SEARCH KEYWORDS
----------------------------------------------------------------------
Enter keywords for the jobs you're looking for (comma-separated)
Examples: Machine Learning, Data Science, AI Engineer, Python Developer
Keywords: Machine Learning, AI, Deep Learning

📍 LOCATION PREFERENCE
----------------------------------------------------------------------
Preferred location (or 'Remote'): Remote

📊 MATCH PREFERENCES
----------------------------------------------------------------------
How many top matches to find? (default: 20): 20

📧 EMAIL DELIVERY
----------------------------------------------------------------------
Would you like to email the results? (y/n): y
Recipient email address: user@example.com
```

---

## MCP Tools Available

### 1. `get_job_statistics`
Get statistics about collected jobs

### 2. `collect_jobs`
Collect jobs from all sources (LinkedIn, GitHub, job boards)

### 3. `extract_resume`
Extract text from resume PDF
- **Input**: `resume_path` (string)

### 4. `match_jobs`
Match jobs with resume using AI
- **Input**: 
  - `resume_path` (string, optional)
  - `top_n` (number, default: 10)

---

## Directory Structure

```
Datathon/
├── main_job_search.py          # Main interactive application
├── uploads/                     # Place your resume PDFs here
├── matched_jobs/               # Output folder for results
│   └── latest_matches.json
├── data/                       # Job data from various sources
├── linkedin_collector/         # LinkedIn job search results
└── NewMCP Folder/              # MCP server implementation
    ├── job_matcher.py
    ├── job_matcher_mcp_stdio.py
    ├── launch_mcp_inspector.sh
    └── mcp-server-config.json
```

---

## Requirements

Install dependencies:

```bash
pip install PyPDF2 google-generativeai python-dotenv
```

Set up environment variables:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

---

## Tips

1. **First time?** Place your resume PDF in the `uploads/` folder
2. **No jobs?** Run the job collectors first to gather postings
3. **Testing?** Use the MCP Inspector to test individual components
4. **Email issues?** Results are always saved locally in `matched_jobs/`

---

## Troubleshooting

### "No jobs found"
- Run the LinkedIn collector: `cd linkedin_collector && python3 search_and_save.py`
- Check that `data/` folder has JSON files

### "Failed to extract resume"
- Ensure resume is a valid PDF
- Check file path is correct

### "Email sending failed"
- Results are still saved locally
- Check email configuration in `send_email_smtp.py`

---

## Support

For issues or questions, check:
- `QUICK_START.md` - Getting started guide
- `EXECUTION_FLOW.md` - System architecture
- `NewMCP Folder/WEB_INSPECTOR_GUIDE.md` - MCP testing guide
