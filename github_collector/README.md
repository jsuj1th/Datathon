# GitHub Job Collector

This folder contains GitHub-based job discovery and collection functionality.

## Purpose
Discovers and fetches job listings from GitHub repositories, job boards, and career pages hosted on GitHub.

## Files

- `github_discovery.py` - Discover job listings on GitHub
- `github_fetcher.py` - Fetch job details from discovered sources

## Features

- Searches GitHub repositories for job postings
- Discovers companies with careers pages on GitHub
- Fetches job listings from GitHub-hosted career sites
- Extracts structured job data

## Usage

```bash
# From github_collector directory

# Discover job sources
python3 github_discovery.py

# Fetch job listings
python3 github_fetcher.py
```

## Configuration

Set GitHub token in main `.env`:
```
GITHUB_PERSONAL_ACCESS_TOKEN=your_github_token
```

## Output Format

Jobs are saved in JSON format compatible with the main matcher:
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

Jobs from GitHub can be:
1. Saved to the main data directory
2. Combined with LinkedIn jobs
3. Processed by the job matcher pipeline

## Next Steps

Future enhancements:
- Automatic job board discovery
- Company GitHub organization tracking
- Pull request to add jobs feature
