# 🎯 System Overview & Quick Access

## 🌐 MCP Tools Inspector

**Currently Running at:** http://localhost:8000

The web inspector shows all available MCP tools with:
- Tool names and descriptions
- Input parameters and types
- Return values and schemas
- Live server status

### Available MCP Tools:

1. **search_jobs** - Search for jobs by keywords and location
   - Inputs: query, location, limit
   - Returns: List of job objects

2. **match_jobs** - Match jobs with resume using AI
   - Inputs: resume_path, jobs_data, top_n
   - Returns: Ranked list of matched jobs

3. **extract_resume** - Extract text from PDF resume
   - Inputs: pdf_path
   - Returns: Extracted text string

4. **send_email** - Send job matches via email
   - Inputs: recipient, matched_jobs
   - Returns: Success status

5. **get_statistics** - Get job search statistics
   - Inputs: jobs_data
   - Returns: Statistics object

---

## 🚀 Complete Pipeline Flow

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: User Input                                         │
│  ────────────────────────────────────────────────────────  │
│  • Job query (e.g., "Machine Learning Engineer")            │
│  • Keywords (e.g., "python, tensorflow, nlp")              │
│  • Location (e.g., "Remote", "San Francisco")              │
│  • Experience level (entry/mid/senior)                      │
│  • Email address for results                                │
│  • Path to resume PDF                                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: Job Collection                                     │
│  ────────────────────────────────────────────────────────  │
│  GitHub Collector → Searches GitHub Jobs                    │
│  LinkedIn Collector → Searches LinkedIn Jobs                │
│                                                             │
│  Filters applied:                                           │
│  ✓ Keywords match                                           │
│  ✓ Location match                                           │
│  ✓ Experience level                                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: AI-Powered Matching                                │
│  ────────────────────────────────────────────────────────  │
│  • Extract resume text from PDF                             │
│  • Extract skills and experience from resume                │
│  • Analyze each job description                             │
│  • Calculate match score (0-100)                            │
│  • Generate match reason for each job                       │
│  • Rank jobs by relevance                                   │
│                                                             │
│  Uses: Google Gemini AI (gemini-2.5-flash)                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: Results & Email                                    │
│  ────────────────────────────────────────────────────────  │
│  • Display top matches in terminal                          │
│  • Save results to JSON file                                │
│  • Send HTML email with:                                    │
│    - Top matched jobs                                       │
│    - Match scores and reasons                               │
│    - Apply links                                            │
│    - Attached JSON file                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 File Structure

```
Datathon/
├── main_complete_pipeline.py        ← RUN THIS! Complete interactive pipeline
├── launch_menu.sh                   ← Easy launcher menu
├── COMPLETE_PIPELINE_README.md      ← Full documentation
│
├── NewMCP Folder/
│   ├── job_matcher.py               ← AI matching logic
│   ├── job_matcher_mcp_server.py    ← MCP server implementation
│   ├── job_matcher_mcp_stdio.py     ← MCP STDIO interface
│   ├── web_inspector_simple.py      ← Web UI for MCP tools
│   └── mcp-server-config.json       ← MCP configuration
│
├── github_collector/
│   └── main.py                      ← GitHub job collector
│
├── linkedin_collector/
│   └── job_searcher.py              ← LinkedIn job collector
│
├── data/                            ← Collected jobs
│   ├── github_*.json
│   └── linkedin_*.json
│
└── matched_jobs/                    ← AI-matched results
    └── top_matches.json
```

---

## ⚡ Quick Commands

### Run the Complete Pipeline
```bash
python3 main_complete_pipeline.py
```

### View MCP Tools Inspector
```bash
cd "NewMCP Folder"
python3 web_inspector_simple.py
# Then open: http://localhost:8000
```

### Use the Menu Launcher
```bash
./launch_menu.sh
```

---

## 🎯 What Each Component Does

### 1. **main_complete_pipeline.py** (THE MAIN FILE)
   - Interactive prompts for user input
   - Orchestrates all components
   - Calls GitHub and LinkedIn collectors
   - Uses AI to match jobs with resume
   - Sends email with results

### 2. **Web Inspector** (http://localhost:8000)
   - Visual interface to see all MCP tools
   - Shows tool parameters and return types
   - Real-time server status
   - Great for debugging and understanding available tools

### 3. **GitHub Collector**
   - Searches GitHub Jobs API
   - Filters by keywords and location
   - Returns structured job data

### 4. **LinkedIn Collector**
   - Searches LinkedIn Jobs
   - Filters by keywords, location, experience
   - Returns structured job data

### 5. **Job Matcher (AI)**
   - Extracts text from resume PDF
   - Uses Google Gemini AI to analyze
   - Matches jobs with resume
   - Ranks by relevance (0-100 score)
   - Provides match reasons

### 6. **Email Sender**
   - Creates HTML email
   - Includes top matches
   - Attaches JSON file
   - Sends via Gmail SMTP

---

## 🔧 Configuration Required

Edit `.env` file with your credentials:

```env
# Email (Required for sending results)
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-char-app-password
RECIPIENT_EMAIL=where-to-send@gmail.com

# AI (Required for matching)
GEMINI_API_KEY=your-gemini-api-key

# LinkedIn (Optional - for LinkedIn collector)
LINKEDIN_EMAIL=your-linkedin@email.com
LINKEDIN_PASSWORD=your-password
```

---

## 📊 Example Usage

```bash
$ python3 main_complete_pipeline.py

╔════════════════════════════════════════════════════════════╗
  🎯 JOB SEARCH & MATCHING SYSTEM
╚════════════════════════════════════════════════════════════╝

👋 Welcome! Let's find your perfect job matches.

📝 STEP 1: What type of job are you looking for?
   Examples:
   - Machine Learning Engineer
   - Data Scientist
   - Software Engineer

   Your job query: Machine Learning Engineer

🔍 STEP 2: Enter keywords to filter jobs (comma-separated)
   Examples: python, machine learning, tensorflow, nlp

   Keywords: python, tensorflow, pytorch, nlp, computer vision

📍 STEP 3: Where do you want to work?
   Examples: San Francisco, New York, Remote, Boston

   Location: Remote

... (continues with more prompts)

✅ Searching GitHub... Found 45 jobs
✅ Searching LinkedIn... Found 52 jobs
🤖 Matching 97 jobs with AI...
✅ Top 20 matches found
📧 Email sent successfully!
```

---

## 🎨 Web Inspector Features

When you open http://localhost:8000, you'll see:

- **Tool List**: All 5 MCP tools with descriptions
- **Parameters**: Required and optional inputs for each tool
- **Return Types**: What data each tool returns
- **Examples**: Sample inputs and outputs
- **Server Status**: Real-time connection status

This helps you understand what the MCP server can do!

---

## ✅ Checklist

Before running the pipeline:

- [ ] `.env` file configured with API keys
- [ ] Gmail App Password created
- [ ] Resume PDF available
- [ ] Python dependencies installed
- [ ] MCP server can start (test with web inspector)

---

## 🆘 Troubleshooting

**Q: Web inspector not loading?**
A: Make sure port 8000 is free. Kill any process using it:
```bash
lsof -ti:8000 | xargs kill -9
```

**Q: No jobs found?**
A: Jobs are saved in `data/` directory. Even if collectors fail, existing jobs will be used.

**Q: Email not sending?**
A: Check `GMAIL_USER` and `GMAIL_APP_PASSWORD` in `.env`. Use App Password, not regular password.

**Q: AI matching not working?**
A: Check `GEMINI_API_KEY` in `.env`. System will fall back to keyword matching.

---

**Ready to find your perfect job? Run:**
```bash
python3 main_complete_pipeline.py
```

Or use the menu:
```bash
./launch_menu.sh
```
