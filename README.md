# Job Search MCP Server

A Model Context Protocol (MCP) server for GitHub Copilot that provides comprehensive job search functionality. This system combines LinkedIn-style job simulation with real job data from The Muse Jobs API, plus intelligent fallback generation.

## 🚀 Features

### Multi-Platform Job Search
- **LinkedIn Simulation**: High-quality simulated LinkedIn job data with realistic company and salary information
- **The Muse Jobs API**: Live job data from real companies like Meta, Google, Atlassian, TikTok
- **Intelligent Fallbacks**: Market-accurate job generation when APIs are unavailable
- **Combined Search**: Aggregated results from multiple sources with deduplication

### GitHub Copilot Ready
- **MCP Compatible**: All functions work seamlessly with GitHub Copilot
- **Structured JSON**: Standardized response format for AI consumption
- **Async Support**: Real-time job searching capabilities
- **Error Handling**: Robust fallback mechanisms

## 📁 Project Structure

```
/
├── mcp_server.py              # Main MCP server with all job search tools
├── job_searcher.py            # The Muse API + realistic job generation
├── demo.py                    # Simple system demonstration
├── requirements.txt           # Python dependencies
└── job_search_results/        # Saved search results
```

# Job Search MCP Server

A Model Context Protocol (MCP) server for GitHub Copilot that provides comprehensive job search functionality.

## 🚀 Features

- **Multi-Platform Job Search**: LinkedIn simulation + The Muse API + intelligent fallbacks
- **GitHub Copilot Ready**: MCP compatible with structured JSON responses
- **Real Job Data**: Live data from companies like Meta, Google, Amazon, Netflix
- **Smart Fallbacks**: Market-accurate job generation when APIs are unavailable

## 📁 Project Structure

```
/
├── mcp_server.py              # Main MCP server with all job search tools
├── job_searcher.py            # The Muse API + realistic job generation
├── job_saver.py               # Utility for saving jobs in JSON format
├── demo.py                    # System demonstration with JSON format
├── requirements.txt           # Python dependencies
└── job_search_results/        # Saved search results (JSON files)
```

## 🛠 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Test the system and see new JSON format
python demo.py

# Start MCP server for GitHub Copilot
python mcp_server.py

# Test job saver utility
python job_saver.py
```

### Save Jobs to JSON Files

```python
from job_saver import save_jobs_to_json, validate_job_format

# Search and save jobs
result = search_combined_jobs("data scientist", "Texas", 30)
jobs = json.loads(result)["jobs"]

# Save with automatic filename
file_path = save_jobs_to_json(
    jobs, 
    {"keywords": "data scientist", "location": "Texas", "limit": 30}
)

# Save with custom filename  
file_path = save_jobs_to_json(
    jobs, 
    search_query,
    "texas_data_science_jobs.json"
)

# Validate job format
for job in jobs:
    if validate_job_format(job):
        print("✅ Valid format")
```

## 🔧 Usage with GitHub Copilot

### Available MCP Tools:
1. **`search_linkedin_jobs`** - LinkedIn-style job simulation
2. **`search_muse_jobs`** - The Muse API + realistic fallbacks  
3. **`search_combined_jobs`** - Combined platform search

### Example Usage:
```
"Find data science jobs in Texas"
→ Uses: search_combined_jobs("data scientist", "Texas", 30)

"Show remote Python developer positions"
→ Uses: search_muse_jobs("python developer", "Remote", 20)
```

## 📊 Job Data Format

All jobs are saved in a standardized JSON format that matches your specification:

```json
{
  "search_metadata": {
    "query": {"keywords": "data scientist", "location": "Texas", "limit": 30},
    "total_results": 25,
    "collected_at": "2025-11-08T17:36:35.678363",
    "source": "job_search_mcp_server"
  },
  "jobs": [
    {
      "company": "Meta",
      "position": "Senior Data Scientist",
      "apply_link": "https://linkedin.com/jobs/view/linkedin_1",
      "location": "Texas",
      "salary": "$120,000 - $180,000",
      "description": "We are seeking a talented Senior Data Scientist...",
      "requirements": "SQL, Python, Machine Learning, Statistics",
      "benefits": "Health insurance, 401k, Stock options, Flexible PTO",
      "job_type": "full_time",
      "experience_level": "senior_level",
      "posted_date": "2025-11-08",
      "deadline": null,
      "days_since_posted": 3,
      "remote_option": "onsite",
      "visa_sponsorship": true,
      "source": "linkedin/linkedin_1",
      "collection_method": "mcp_linkedin_simulation",
      "collected_at": "2025-11-08T17:36:35.678075",
      "field": "AI/ML",
      "company_type": "big_tech"
    }
  ]
}
```

### Field Mapping:
- **company**: Company name
- **position**: Job title/position
- **apply_link**: Direct application URL
- **location**: Job location (city, state, or "Remote")
- **salary**: Salary range or null
- **description**: Job description summary
- **requirements**: Required skills/qualifications
- **benefits**: Employee benefits offered
- **job_type**: "full_time", "part_time", "contract", etc.
- **experience_level**: "entry_level", "mid_level", "senior_level"
- **posted_date**: Date job was posted (YYYY-MM-DD)
- **deadline**: Application deadline (or null)
- **days_since_posted**: Days since job was posted
- **remote_option**: "remote", "onsite", "hybrid"
- **visa_sponsorship**: Boolean or null
- **source**: Data source identifier
- **collection_method**: How the data was collected
- **collected_at**: ISO timestamp of data collection
- **field**: Job category (AI/ML, Software Engineering, etc.)
- **company_type**: "big_tech", "startup", "enterprise", etc.

## ✅ Ready for Production

The system is production-ready and GitHub Copilot compatible! 🚀
