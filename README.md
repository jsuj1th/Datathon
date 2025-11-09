# 🎯 Automated Job Matcher & Email System

An intelligent end-to-end job application pipeline that collects jobs from multiple sources, matches them with your resume using AI, and emails the top matches.

## ✨ Features

- **Multi-Source Job Collection**: Automatically collects jobs from LinkedIn and GitHub repositories
- **AI-Powered Matching**: Uses Google Gemini AI to match jobs with your resume
- **Smart Ranking**: Ranks jobs by relevance with detailed match reasoning
- **Automated Email Delivery**: Sends top 50 job matches via Gmail SMTP
- **Complete Automation**: One command runs the entire pipeline

## 📁 Project Structure

```
Project/
├── linkedin_collector/          # LinkedIn job collection
│   ├── linkedin_searcher.py     # LinkedIn job search
│   ├── search_and_save.py       # Save LinkedIn jobs
│   └── job_search_results/      # LinkedIn job data
│
├── github_collector/            # GitHub job collection
│   ├── github_discovery.py      # Discover job repos
│   └── github_fetcher.py        # Fetch GitHub jobs
│
├── data/                        # Additional job sources
│   └── jobs_output.json         # Jobs from various sources
│
├── matched_jobs/                # AI matching results
│   └── top_50_matches.json      # Top 50 ranked jobs
│
├── models/                      # Data models
│   └── job.py                   # Job data structure
│
├── collectors/                  # Legacy collectors
│
├── job_matcher.py              # AI job matching engine
├── send_email_smtp.py          # Gmail email sender
├── run_pipeline.py             # Main automation pipeline
├── view_jobs.py                # View collected jobs
├── main.py                     # Alternative job collector
└── .env                        # Configuration (API keys)
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright for web scraping (if needed)
playwright install chromium
```

### 2. Configure Environment Variables

Edit `.env` file with your credentials:

```bash
# Gemini API Key (REQUIRED for job matching)
GEMINI_API_KEY=your_gemini_api_key_here

# Gmail SMTP (REQUIRED for email sending)
GMAIL_USER=your_email@gmail.com
GMAIL_APP_PASSWORD=your_16_char_app_password
RECIPIENT_EMAIL=recipient@gmail.com
```

#### Get Gmail App Password:
1. Go to https://myaccount.google.com/apppasswords
2. Create password for "Mail"
3. Copy the 16-character password (remove spaces)
4. Add to `.env` file

#### Get Gemini API Key:
1. Go to https://aistudio.google.com/app/apikey
2. Create API key
3. Add to `.env` file

### 3. Run the Complete Pipeline

```bash
python3 run_pipeline.py
```

This will:
1. ✅ Load jobs from LinkedIn and other sources (521 jobs)
2. 🤖 Match jobs with your resume using AI
3. 📊 Rank and select top 50 matches
4. 📧 Send email with job details

## 📋 Pipeline Components

### 1. Job Collection

**LinkedIn Collector** (`linkedin_collector/`)
- Searches LinkedIn for relevant jobs
- Saves to `linkedin_collector/job_search_results/`

```bash
cd linkedin_collector
python3 search_and_save.py
```

**GitHub Collector** (`github_collector/`)
- Discovers job repositories on GitHub
- Fetches jobs from markdown tables

```bash
cd github_collector
python3 github_discovery.py
```

**Other Sources** (`data/`)
- Jobs from additional sources stored in `data/jobs_output.json`

### 2. AI Job Matching

**Job Matcher** (`job_matcher.py`)
- Loads jobs from all sources
- Extracts resume from PDF
- Uses Gemini AI to:
  - Calculate match scores (0-100)
  - Provide match reasoning
  - Rank jobs by relevance

```bash
python3 job_matcher.py
```

Output: `matched_jobs/top_50_matches.json`

### 3. Email Delivery

**SMTP Email Sender** (`send_email_smtp.py`)
- Sends top matches via Gmail
- Formats jobs in readable email
- Includes apply links and match scores

```bash
python3 send_email_smtp.py
```

## 🔧 Individual Component Usage

### View Collected Jobs

```bash
python3 view_jobs.py
```

Shows statistics:
- Total jobs collected
- Jobs by source
- Sample job listings

### Run Job Matcher Only

```bash
python3 job_matcher.py
```

Outputs:
- Console: Match scores and reasoning
- File: `matched_jobs/top_50_matches.json`

### Test Email Sending

```bash
python3 send_email_smtp.py
```

Requires:
- `matched_jobs/top_50_matches.json` to exist
- Gmail credentials in `.env`

## 📊 Output Format

### Matched Jobs (`matched_jobs/top_50_matches.json`)

```json
{
  "matched_jobs": [
    {
      "company": "Google",
      "position": "Machine Learning Engineer",
      "location": "Mountain View, CA",
      "match_score": 95,
      "match_reason": "Strong alignment with your ML background...",
      "apply_link": "https://...",
      "source": "LinkedIn"
    }
  ],
  "total_matched": 50,
  "resume_summary": "...",
  "matched_at": "2025-11-09T10:30:00"
}
```

### Email Format

```
🎯 Top Job Matches Based on Your Resume
======================================================================

1. Machine Learning Engineer
   Company: Google
   Location: Mountain View, CA
   Match Score: 95/100
   Why: Strong alignment with your ML background and experience...
   Apply: https://...

[... 49 more jobs ...]
```

## 🔑 Configuration

### Resume Location

Update in `job_matcher.py` (line 135):
```python
resume_file = str(project_dir / "YourResume.pdf")
```

### Job Sources

Add/modify sources in collectors:
- LinkedIn: `linkedin_collector/linkedin_searcher.py`
- GitHub: `github_collector/github_discovery.py`
- Other: Add JSON files to `data/`

### Email Settings

Configure in `.env`:
```bash
GMAIL_USER=sender@gmail.com
RECIPIENT_EMAIL=receiver@gmail.com
```

### AI Model

Change model in `job_matcher.py` (line 35):
```python
self.model = genai.GenerativeModel("gemini-2.0-flash-exp")
```

## 🛠️ Troubleshooting

### "No matched jobs found"
- Check if `matched_jobs/top_50_matches.json` exists
- Run `python3 job_matcher.py` first

### Email not sending
- Verify Gmail App Password is correct (16 chars, no spaces)
- Check 2-Factor Authentication is enabled
- Check spam folder for received emails

### "GEMINI_API_KEY not found"
- Add your Gemini API key to `.env` file
- Get key at: https://aistudio.google.com/app/apikey

### Job collection fails
- Check internet connection
- Verify API tokens in `.env`
- Check rate limits for LinkedIn/GitHub

## 📈 Pipeline Flow

```
┌─────────────────────────────────────────────────┐
│  1. JOB COLLECTION                              │
│  ─────────────────                              │
│  • LinkedIn Collector → job_search_results/     │
│  • GitHub Collector   → data/jobs_output.json   │
│  • Other Sources      → data/                   │
└─────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────┐
│  2. AI JOB MATCHING (job_matcher.py)            │
│  ────────────────────────────────                │
│  • Load 521 jobs from all sources               │
│  • Extract resume from PDF                      │
│  • Gemini AI analyzes each job                  │
│  • Calculate match scores (0-100)               │
│  • Generate match reasoning                     │
│  • Rank and select top 50                       │
└─────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────┐
│  3. EMAIL DELIVERY (send_email_smtp.py)         │
│  ───────────────────────────────────             │
│  • Load top 50 matches                          │
│  • Format email with job details                │
│  • Send via Gmail SMTP                          │
│  • ✅ Check your inbox!                         │
└─────────────────────────────────────────────────┘
```

## 🎓 Educational Purpose

This project is part of **CSCE 689: Programming LLMs** course, demonstrating:
- LLM integration (Google Gemini)
- Web scraping and data collection
- Automated workflows
- Email automation
- Real-world AI applications

## 📝 Files Overview

| File | Purpose | When to Use |
|------|---------|-------------|
| `run_pipeline.py` | Complete automation | Run entire pipeline |
| `job_matcher.py` | AI matching engine | Match jobs with resume |
| `send_email_smtp.py` | Email sender | Send matched jobs |
| `view_jobs.py` | View collected jobs | Check collected data |
| `main.py` | Alternative collector | Collect from web sources |

## 🚦 Status

✅ **Job Collection**: Working (521 jobs collected)
✅ **AI Matching**: Working (Gemini 2.0 Flash)
✅ **Email Sending**: Working (Gmail SMTP)
✅ **Full Pipeline**: Ready to use

## 🤝 Contributing

Feel free to:
- Add new job sources
- Improve AI matching prompts
- Enhance email formatting
- Add new features

## 📄 License

Educational project for CSCE 689: Programming LLMs
