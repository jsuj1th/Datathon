# 🎯 Automated Job Matcher & Email System

An intelligent end-to-end job application pipeline that collects jobs from multiple sources, matches them with your resume using AI, and emails the top matches.

## ✨ Features

- **Multi-Source Job Collection**: Automatically collects jobs from LinkedIn, GitHub, and web sources
- **AI-Powered Matching**: Uses Google Gemini AI to match jobs with your resume
- **Smart Ranking**: Ranks jobs by relevance with detailed match reasoning
- **Automated Email Delivery**: Sends top 50 job matches via Gmail SMTP
- **Complete Automation**: Organized pipeline with centralized configuration

## 📁 Project Structure

```
Datathon/
├── .env                         # 🔑 Single environment file (API keys & credentials)
├── config.yaml                  # ⚙️ Collection settings
├── search_keywords.txt          # 🔍 Search terms for job collection
├── requirements.txt             # 📦 Python dependencies
│
├── collectors/                  # 📚 Job collection modules
│   ├── github_discovery.py      # Discover GitHub job repos
│   ├── github_fetcher.py        # Fetch jobs from GitHub
│   ├── apify_scraper.py         # Apify web scraper
│   └── firecrawl_scraper.py     # Firecrawl LLM scraper
│
├── github_collector/            # 🐙 GitHub job collection orchestrator
│   ├── main.py                  # Main orchestrator for GitHub & web scraping
│   └── README.md                # GitHub collector docs
│
├── linkedin_collector/          # 💼 LinkedIn job collection
│   ├── search_and_save.py       # LinkedIn job search & save
│   ├── job_saver.py             # Job saving utility
│   ├── mcp_server.py            # LinkedIn MCP server
│   ├── job_keywords.txt         # LinkedIn search keywords
│   └── README.md                # LinkedIn collector docs
│
├── data/                        # 💾 Unified data directory
│   ├── jobs_output.json         # GitHub & web scraper jobs
│   └── linkedin_*.json          # LinkedIn job files
│
├── models/                      # 📋 Data models
│   └── job.py                   # Job data structure
│
├── matched_jobs/                # 🎯 AI matching results
│   └── top_50_matches.json      # Top 50 ranked jobs
│
├── job_matcher.py              # 🤖 AI job matching engine
├── send_email_smtp.py          # 📧 Gmail email sender
├── run_pipeline.py             # 🚀 Main automation pipeline
└── view_jobs.py                # 👀 View collected jobs
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright for LinkedIn scraping (if needed)
playwright install chromium
```

### 2. Configure Environment Variables

Edit `.env` file in the root directory with your credentials:

```bash
# Gemini API Key (REQUIRED for job matching)
GEMINI_API_KEY=your_gemini_api_key_here

# Gmail SMTP (REQUIRED for email sending)
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_16_char_app_password

# LinkedIn Credentials (for LinkedIn collector)
LINKEDIN_EMAIL=your_linkedin_email
LINKEDIN_PASSWORD=your_linkedin_password

# Optional: For additional sources
GITHUB_PERSONAL_ACCESS_TOKEN=your_github_token
FIRECRAWL_API_KEY=your_firecrawl_key
APIFY_API_TOKEN=your_apify_token
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

## 📊 End-to-End Flow

### Complete Pipeline Flow:

```
1. JOB COLLECTION
   ├── GitHub Collector (github_collector/main.py)
   │   ├── Searches GitHub repos for job postings
   │   ├── Web scraping (Firecrawl/Apify)
   │   └── Saves to: data/jobs_output.json
   │
   └── LinkedIn Collector (linkedin_collector/search_and_save.py)
       ├── Searches LinkedIn for jobs
       └── Saves to: data/linkedin_*.json

2. JOB MATCHING (job_matcher.py)
   ├── Loads all jobs from data/ folder
   ├── Uses Google Gemini AI for matching
   ├── Ranks jobs by relevance
   └── Saves to: matched_jobs/top_50_matches.json

3. EMAIL DELIVERY (send_email_smtp.py)
   └── Sends top 50 matches via Gmail SMTP
```

## 🎯 How to Run

### Option 1: Run Complete Pipeline (Recommended)

```bash
# From root directory
python3 run_pipeline.py
```

This will:
1. ✅ Load jobs from all sources in `data/` folder
2. 🤖 Match jobs with your resume using AI
3. 📊 Rank and select top 50 matches
4. 📧 Send email with job details

### Option 2: Run Individual Components

#### Collect GitHub & Web Jobs:
```bash
cd github_collector
python3 main.py
```
Output: `../data/jobs_output.json`

#### Collect LinkedIn Jobs:
```bash
cd linkedin_collector
python3 search_and_save.py
```
Output: `../data/linkedin_*.json`

#### Match Jobs with Resume:
```bash
python3 job_matcher.py
```
Input: All JSON files in `data/`
Output: `matched_jobs/top_50_matches.json`

#### Send Email:
```bash
python3 send_email_smtp.py
```
Input: `matched_jobs/top_50_matches.json`

## 📝 Configuration Files

### `.env` (Root Directory)
Single source of truth for all API keys and credentials. Used by all collectors.

### `config.yaml` (Root Directory)
Job collection settings:
- GitHub search keywords
- Web scraping targets
- Collection limits
- Output format settings

### `search_keywords.txt` (Root Directory)
Search terms for GitHub & web scraping job collection.

### `linkedin_collector/job_keywords.txt`
Search terms for LinkedIn job collection in format:
```
keyword | location | limit
machine learning engineer | Remote | 30
data scientist | San Francisco | 25
```

## 📂 Data Organization

All job data is centralized in the `data/` folder:
- `jobs_output.json` - GitHub and web scraper jobs
- `linkedin_*.json` - LinkedIn job files (multiple files possible)

This centralized approach makes it easy to:
- Process all jobs together
- Deduplicate across sources
- Archive or version control job data

## 🔧 Customization

### Add More Job Sources

Edit `config.yaml` to add new web scraping targets:
```yaml
web_scraping:
  sites:
    - name: "YourJobBoard"
      url: "https://yourjobboard.com/jobs"
      enabled: true
```

### Modify Search Keywords

Edit `search_keywords.txt` for GitHub/web scraping:
```
machine learning new grad
AI engineer 2026
data scientist entry level
```

Edit `linkedin_collector/job_keywords.txt` for LinkedIn:
```
machine learning | Remote | 30
AI engineer | San Francisco | 25
```

## 🐛 Troubleshooting

### Jobs not collecting?
- Check `.env` file has correct API keys
- Verify `config.yaml` settings
- Check network connectivity

### LinkedIn not working?
- Ensure LinkedIn credentials in `.env`
- Run `playwright install chromium`
- Check LinkedIn hasn't blocked your account

### Email not sending?
- Verify Gmail app password (not regular password)
- Check recipient email in `.env`
- Ensure 2FA is enabled on Gmail account

## 📄 License

This project is for educational and personal use.

## 🤝 Contributing

Feel free to submit issues or pull requests to improve the pipeline!
