# GitHub Job Collector

This folder contains the main job collection orchestrator for GitHub and web-based sources.

## Purpose
Orchestrates job discovery from GitHub repositories, job boards, and career pages using multiple collectors.

## Files

- `main.py` - Main orchestrator for GitHub and web scraping job collection
- *(github_discovery.py and github_fetcher.py are now in ../collectors/)*

## Features

- Searches GitHub repositories for job postings
- Discovers companies with careers pages on GitHub
- Fetches job listings from GitHub-hosted career sites
- Web scraping via Firecrawl (LLM-powered) or Apify
- Deduplication and formatting
- Saves to unified data directory

## Usage

```bash
# From github_collector directory
python3 main.py

# Or from root directory
python3 github_collector/main.py
```

## Configuration

All configuration is in the main folder:
- `.env` - API keys and credentials (in root folder)
- `config.yaml` - Collection settings (in root folder)
- `search_keywords.txt` - Search terms (in root folder)

Required in `.env`:
```
GITHUB_PERSONAL_ACCESS_TOKEN=your_github_token
FIRECRAWL_API_KEY=your_firecrawl_key  # Optional but recommended
APIFY_API_TOKEN=your_apify_token      # Optional fallback
```

## Output Format

Jobs are saved to `../data/jobs_output.json` in JSON format:
```json
{
  "company": "Company Name",
  "position": "Job Title",
  "location": "Location",
  "description": "Job description",
  "apply_link": "https://..."
}
```

## Integration

All job collectors save to the same `data/` folder:
- GitHub jobs: `data/jobs_output.json`
- LinkedIn jobs: `data/linkedin_*.json`
- All files are in the main `data/` directory for easy access

## Next Steps

Future enhancements:
- Automatic job board discovery
- Company GitHub organization tracking
- Enhanced deduplication across all sources
