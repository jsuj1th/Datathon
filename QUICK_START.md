# ⚡ Quick Start Guide

## 🚀 Run the Complete Pipeline in 3 Steps

### Prerequisites
```bash
# Install dependencies
pip install -r requirements.txt

# Configure .env file with your API keys
# (See below for required keys)
```

---

## Step 1: Collect Jobs

### Option A: GitHub & Web Jobs (Recommended to run first)
```bash
cd github_collector
python3 main.py
```
**Output:** `../data/jobs_output.json`

### Option B: LinkedIn Jobs
```bash
cd linkedin_collector
python3 search_and_save.py
```
**Output:** `../data/linkedin_*.json`

### Run Both for Maximum Jobs!

---

## Step 2: Match & Email

```bash
cd /Users/sujithjulakanti/Desktop/Datathon
python3 run_pipeline.py
```

This will:
1. ✅ Load all jobs from `data/` folder
2. 🤖 Match with resume using Google Gemini AI
3. 📊 Rank and select top 50 matches
4. 📧 Send email via Gmail SMTP

---

## 🔑 Required Configuration

### `.env` File (in root directory)

```bash
# REQUIRED: For job matching
GEMINI_API_KEY=your_gemini_api_key_here

# REQUIRED: For email
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_16_char_app_password

# REQUIRED: For LinkedIn collector
LINKEDIN_EMAIL=your_linkedin@email.com
LINKEDIN_PASSWORD=your_linkedin_password

# OPTIONAL: For better GitHub results
GITHUB_PERSONAL_ACCESS_TOKEN=your_github_token

# OPTIONAL: For web scraping
FIRECRAWL_API_KEY=your_firecrawl_key
APIFY_API_TOKEN=your_apify_token
```

### How to Get Gmail App Password:
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" and your device
3. Copy the 16-character password (no spaces)
4. Paste into `.env` file

### How to Get Gemini API Key:
1. Go to https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key
4. Paste into `.env` file

---

## 📊 What Gets Collected

### GitHub Collector (`github_collector/main.py`)
- GitHub repositories with job postings
- Company career pages hosted on GitHub
- Job boards via Firecrawl/Apify scraping
- **Output:** `data/jobs_output.json`

### LinkedIn Collector (`linkedin_collector/search_and_save.py`)
- LinkedIn job listings
- Multiple searches based on `job_keywords.txt`
- **Output:** `data/linkedin_*.json` (one file per search)

### All Data Goes to `data/` Folder
- Centralized location
- Easy to process
- Easy to archive

---

## 📂 Directory Structure

```
Datathon/
├── .env                        # Your API keys (EDIT THIS)
├── config.yaml                 # Collection settings
├── search_keywords.txt         # GitHub search terms
│
├── collectors/                 # Collection modules
│   ├── github_discovery.py
│   ├── github_fetcher.py
│   ├── apify_scraper.py
│   └── firecrawl_scraper.py
│
├── github_collector/
│   └── main.py                 # RUN: GitHub & web collection
│
├── linkedin_collector/
│   ├── search_and_save.py      # RUN: LinkedIn collection
│   └── job_keywords.txt        # LinkedIn search terms (EDIT THIS)
│
├── data/                       # All collected jobs
│   ├── jobs_output.json        # GitHub & web jobs
│   └── linkedin_*.json         # LinkedIn jobs
│
├── matched_jobs/
│   └── top_50_matches.json     # AI-matched jobs
│
├── job_matcher.py              # AI matching engine
├── send_email_smtp.py          # Email sender
└── run_pipeline.py             # RUN: Match & email pipeline
```

---

## 🎯 Common Workflows

### Workflow 1: Quick Test (Use Existing Jobs)
```bash
# Skip collection, just match and email existing jobs
python3 run_pipeline.py
```

### Workflow 2: Fresh Collection + Matching
```bash
# Collect GitHub jobs
cd github_collector && python3 main.py && cd ..

# Collect LinkedIn jobs
cd linkedin_collector && python3 search_and_save.py && cd ..

# Match and email
python3 run_pipeline.py
```

### Workflow 3: Only GitHub Jobs
```bash
# Collect only GitHub jobs
cd github_collector && python3 main.py && cd ..

# Match and email
python3 run_pipeline.py
```

### Workflow 4: Only LinkedIn Jobs
```bash
# Collect only LinkedIn jobs
cd linkedin_collector && python3 search_and_save.py && cd ..

# Match and email
python3 run_pipeline.py
```

---

## 🔍 Customize Search Keywords

### For GitHub & Web Scraping
Edit `search_keywords.txt`:
```
machine learning new grad
AI engineer 2026
data scientist entry level
software engineer new grad
```

### For LinkedIn
Edit `linkedin_collector/job_keywords.txt`:
```
keyword | location | limit
machine learning engineer | Remote | 30
data scientist | San Francisco | 25
AI researcher | New York | 20
```

---

## 🐛 Troubleshooting

### No jobs collected?
- Check `.env` has correct API keys
- Verify internet connection
- Check `config.yaml` settings

### LinkedIn not working?
- Run: `playwright install chromium`
- Verify LinkedIn credentials in `.env`
- Check if LinkedIn account is locked

### Email not sending?
- Use Gmail App Password (not regular password)
- Enable 2FA on Gmail account
- Check recipient email in `.env`

### "Module not found" errors?
```bash
pip install -r requirements.txt
```

---

## 📧 What You'll Receive

**Email Contains:**
- Top 50 job matches ranked by relevance
- Company name, position, location
- Match score and reasoning
- Apply links
- Professional HTML formatting

**Example:**
```
🎯 Top 50 Job Matches for You!

1. Machine Learning Engineer - Google (95% Match)
   📍 Mountain View, CA | Remote OK
   💰 $150k-$200k
   🔗 Apply: https://...
   ✨ Why it matches: Strong alignment with your ML experience...

2. AI Research Scientist - OpenAI (92% Match)
   ...
```

---

## ✅ Verification Checklist

Before running:
- [ ] `.env` file configured with all required keys
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Playwright installed (for LinkedIn): `playwright install chromium`
- [ ] Keywords configured in `search_keywords.txt`
- [ ] LinkedIn keywords in `linkedin_collector/job_keywords.txt`

---

## 📚 Additional Documentation

- **CLEANUP_SUMMARY.md** - Details of repository reorganization
- **EXECUTION_FLOW.md** - Detailed end-to-end flow
- **README.md** - Complete project documentation
- **github_collector/README.md** - GitHub collector docs
- **linkedin_collector/README.md** - LinkedIn collector docs

---

## 🎉 That's It!

**3 Simple Steps:**
1. Collect jobs (GitHub and/or LinkedIn)
2. Run pipeline (match + email)
3. Check your inbox for top matches!

**Questions?** Check the detailed docs or `.env` configuration.

**Happy Job Hunting! 🚀**
