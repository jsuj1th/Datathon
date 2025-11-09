# 🚀 End-to-End Execution Flow

## Complete Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    AUTOMATED JOB APPLICATION PIPELINE                │
└─────────────────────────────────────────────────────────────────────┘

📋 PHASE 1: JOB COLLECTION
├─ GitHub Collector (github_collector/main.py)
│  ├─ Input: config.yaml, search_keywords.txt, .env
│  ├─ Process:
│  │  ├─ Search GitHub repos for job postings
│  │  ├─ Discover companies with career pages
│  │  ├─ Scrape job boards (Firecrawl/Apify)
│  │  └─ Deduplicate jobs
│  └─ Output: data/jobs_output.json
│
└─ LinkedIn Collector (linkedin_collector/search_and_save.py)
   ├─ Input: job_keywords.txt, .env
   ├─ Process:
   │  ├─ Search LinkedIn for each keyword
   │  ├─ Extract job details
   │  └─ Validate job format
   └─ Output: data/linkedin_*.json (multiple files)

                        ⬇️

📊 PHASE 2: JOB MATCHING
└─ Job Matcher (job_matcher.py)
   ├─ Input: All files in data/*.json
   ├─ Process:
   │  ├─ Load resume
   │  ├─ Load all job files
   │  ├─ Use Google Gemini AI for matching
   │  ├─ Calculate relevance scores
   │  └─ Rank jobs by best match
   └─ Output: matched_jobs/top_50_matches.json

                        ⬇️

📧 PHASE 3: EMAIL DELIVERY
└─ Email Sender (send_email_smtp.py)
   ├─ Input: matched_jobs/top_50_matches.json
   ├─ Process:
   │  ├─ Format jobs into HTML email
   │  ├─ Create professional layout
   │  └─ Send via Gmail SMTP
   └─ Output: Email sent to recipient

                        ⬇️

✅ COMPLETE!
```

---

## 📂 File Structure & Data Flow

```
Datathon/
├── .env                        🔑 API keys & credentials (ALL collectors use this)
├── config.yaml                 ⚙️  GitHub & web scraper settings
├── search_keywords.txt         🔍 Keywords for GitHub/web scraping
│
├── collectors/                 📚 Reusable collection modules
│   ├── github_discovery.py     → Used by github_collector/main.py
│   ├── github_fetcher.py       → Used by github_collector/main.py
│   ├── apify_scraper.py        → Used by github_collector/main.py
│   └── firecrawl_scraper.py    → Used by github_collector/main.py
│
├── github_collector/
│   ├── main.py                 🚀 RUN THIS: Orchestrates GitHub & web job collection
│   │                              Output → ../data/jobs_output.json
│   └── README.md
│
├── linkedin_collector/
│   ├── search_and_save.py      🚀 RUN THIS: LinkedIn job collection
│   │                              Output → ../data/linkedin_*.json
│   ├── job_saver.py            → Saves to ../data/ folder
│   ├── job_keywords.txt        → LinkedIn search terms
│   └── mcp_server.py           → LinkedIn search backend
│
├── data/                       💾 UNIFIED DATA FOLDER (all jobs here!)
│   ├── jobs_output.json        ← From GitHub collector
│   └── linkedin_*.json         ← From LinkedIn collector (multiple files)
│
├── job_matcher.py              🚀 RUN THIS: Match jobs with resume
│                                  Input  → data/*.json
│                                  Output → matched_jobs/top_50_matches.json
│
├── send_email_smtp.py          🚀 RUN THIS: Send email with matches
│                                  Input  → matched_jobs/top_50_matches.json
│
├── run_pipeline.py             🚀 RUN THIS: Execute complete pipeline
│                                  (Runs matcher + email sender)
│
└── matched_jobs/
    └── top_50_matches.json     ← Final output
```

---

## 🎯 Execution Steps

### OPTION 1: Run Complete Pipeline (Recommended)

```bash
# Step 1: Collect jobs (choose one or both)

# GitHub & Web Jobs
cd /Users/sujithjulakanti/Desktop/Datathon/github_collector
python3 main.py

# LinkedIn Jobs  
cd /Users/sujithjulakanti/Desktop/Datathon/linkedin_collector
python3 search_and_save.py

# Step 2: Match & Email (runs automatically)
cd /Users/sujithjulakanti/Desktop/Datathon
python3 run_pipeline.py
```

### OPTION 2: Run Step by Step

```bash
# From root directory: /Users/sujithjulakanti/Desktop/Datathon

# STEP 1a: Collect GitHub & Web Jobs
cd github_collector
python3 main.py
cd ..

# STEP 1b: Collect LinkedIn Jobs
cd linkedin_collector
python3 search_and_save.py
cd ..

# STEP 2: Match Jobs with Resume
python3 job_matcher.py

# STEP 3: Send Email
python3 send_email_smtp.py
```

---

## 📋 Detailed Step-by-Step Instructions

### STEP 1a: GitHub & Web Job Collection

```bash
cd /Users/sujithjulakanti/Desktop/Datathon/github_collector
python3 main.py
```

**What it does:**
1. Loads `config.yaml` from parent directory
2. Reads `search_keywords.txt` from parent directory  
3. Uses GitHub token from `.env`
4. Searches GitHub for job repositories
5. Fetches job details from discovered repos
6. Optionally scrapes job boards (Firecrawl/Apify)
7. Deduplicates jobs
8. Saves to `../data/jobs_output.json`

**Output file:** `data/jobs_output.json`

**Expected output:**
```
🚀 AUTOMATED JOB RETRIEVER - DATA COLLECTION PIPELINE
======================================================================
⏰ Started at: 2025-11-09 10:30:00

======================================================================
📚 PHASE 1: COLLECTING FROM GITHUB REPOSITORIES
======================================================================
🔍 Searching GitHub for: '2026 new grad jobs'
...
✅ Total jobs from GitHub: 234

======================================================================
🔥 PHASE 2: WEB SCRAPING
======================================================================
🔥 Using Firecrawl (LLM-powered extraction)
...

======================================================================
🧹 PHASE 3: DEDUPLICATION
======================================================================
📊 Original jobs: 456
🗑️  Duplicates removed: 23
✨ Unique jobs: 433

======================================================================
💾 PHASE 4: SAVING TO JSON
======================================================================
✅ Saved 433 jobs to ../data/jobs_output.json
📁 File size: 320.45 KB

✅ DATA COLLECTION COMPLETE!
```

---

### STEP 1b: LinkedIn Job Collection

```bash
cd /Users/sujithjulakanti/Desktop/Datathon/linkedin_collector
python3 search_and_save.py
```

**What it does:**
1. Reads search keywords from `job_keywords.txt`
2. Uses LinkedIn credentials from `../.env`
3. For each keyword:
   - Searches LinkedIn
   - Extracts job details
   - Validates job format
   - Saves to `../data/linkedin_{keyword}_{location}.json`

**Output files:** Multiple files in `data/`:
- `linkedin_machine_learning_remote.json`
- `linkedin_data_scientist_san_francisco.json`
- etc.

**Expected output:**
```
🚀 AUTOMATED JOB SEARCH AND SAVE
======================================================================

📖 Loading search keywords from job_keywords.txt...
✅ Loaded 3 search queries

======================================================================
Search 1/3
======================================================================
🔍 JOB SEARCH AND SAVE
======================================================================
Keywords: machine learning engineer
Location: Remote
Limit: 30

🚀 Searching for jobs...
✅ Found 28 jobs
📊 Sources: LinkedIn, TheMuse

💾 Saving to JSON file...

======================================================================
✅ JOB SEARCH COMPLETE!
======================================================================
📁 File: ../data/linkedin_machine_learning_engineer_remote.json
📊 Total Jobs: 28
🎯 Success!

...

🎉 ALL SEARCHES COMPLETE!
📁 Files saved in: /Users/sujithjulakanti/Desktop/Datathon/data
```

---

### STEP 2: Job Matching

```bash
cd /Users/sujithjulakanti/Desktop/Datathon
python3 job_matcher.py
```

**What it does:**
1. Loads your resume
2. Scans `data/` folder for all `.json` files
3. Loads jobs from:
   - `data/jobs_output.json` (GitHub jobs)
   - `data/linkedin_*.json` (LinkedIn jobs)
4. Uses Google Gemini AI to match each job with resume
5. Calculates relevance scores
6. Ranks jobs by best match
7. Saves top 50 to `matched_jobs/top_50_matches.json`

**Input:** All files in `data/` folder  
**Output:** `matched_jobs/top_50_matches.json`

**Expected output:**
```
🤖 AI-POWERED JOB MATCHER
======================================================================

📂 Loading jobs from data folder...
✅ Loaded 433 jobs from jobs_output.json
✅ Loaded 28 jobs from linkedin_machine_learning_engineer_remote.json
✅ Loaded 25 jobs from linkedin_data_scientist_san_francisco.json
📊 Total jobs to match: 486

🧠 Matching jobs with your resume using Gemini AI...
Processing job 1/486: Machine Learning Engineer at Google
Processing job 2/486: Data Scientist at Meta
...

✅ Matched 486 jobs
📊 Top 50 matches saved to matched_jobs/top_50_matches.json

🎯 Top 5 Matches:
1. Machine Learning Engineer - Google (Score: 95%)
2. AI Research Scientist - OpenAI (Score: 92%)
3. Data Scientist - Meta (Score: 89%)
4. ML Engineer - DeepMind (Score: 88%)
5. Research Engineer - Anthropic (Score: 87%)
```

---

### STEP 3: Email Delivery

```bash
cd /Users/sujithjulakanti/Desktop/Datathon
python3 send_email_smtp.py
```

**What it does:**
1. Loads `matched_jobs/top_50_matches.json`
2. Formats jobs into beautiful HTML email
3. Sends via Gmail SMTP to recipient

**Input:** `matched_jobs/top_50_matches.json`  
**Output:** Email sent

**Expected output:**
```
📧 SENDING JOB MATCHES VIA EMAIL
======================================================================

📂 Loading matched jobs...
✅ Loaded 50 jobs from matched_jobs/top_50_matches.json

📝 Formatting email...
✅ HTML email generated

📤 Sending email via Gmail SMTP...
✅ Email sent successfully to recipient@gmail.com

🎉 Done!
```

---

## 🔧 Configuration Requirements

### `.env` File (Root Directory)

```bash
# Required for Job Matching
GEMINI_API_KEY=AIzaSyBQMMCmSSqecWcObb58FEZPaERy9YRU3H0

# Required for Email
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_16_char_app_password

# Required for LinkedIn Collector
LINKEDIN_EMAIL=your_linkedin@email.com
LINKEDIN_PASSWORD=your_linkedin_password

# Optional: For GitHub Collector
GITHUB_PERSONAL_ACCESS_TOKEN=your_github_token

# Optional: For Web Scraping
FIRECRAWL_API_KEY=your_firecrawl_key
APIFY_API_TOKEN=your_apify_token
```

### `config.yaml` (Root Directory)

Used by GitHub collector:
- GitHub search keywords
- Web scraping targets
- Collection limits
- Output format

### `search_keywords.txt` (Root Directory)

Used by GitHub collector:
```
machine learning new grad
AI engineer 2026
data scientist entry level
```

### `linkedin_collector/job_keywords.txt`

Used by LinkedIn collector:
```
machine learning engineer | Remote | 30
data scientist | San Francisco | 25
AI researcher | New York | 20
```

---

## 🎯 Summary

**Execution Order:**
1. ✅ GitHub Collector → `data/jobs_output.json`
2. ✅ LinkedIn Collector → `data/linkedin_*.json`
3. ✅ Job Matcher → `matched_jobs/top_50_matches.json`
4. ✅ Email Sender → Email delivered

**Key Points:**
- All job data centralized in `data/` folder
- All collectors use single `.env` file
- Clear separation of concerns
- Easy to run step by step or complete pipeline
- No scattered files or configs

**Result:**
📧 Top 50 AI-matched jobs delivered to your inbox! 🎉
