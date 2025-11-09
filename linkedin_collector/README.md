# LinkedIn Job Collector

This folder contains all LinkedIn-related job collection and searching functionality.

## Purpose
Collects job listings from LinkedIn using various methods (MCP server, API, web scraping).

## Files

- `job_searcher.py` - Main LinkedIn job searcher
- `linkedin_searcher.py` - LinkedIn-specific search implementation
- `job_saver.py` - Save jobs to JSON format
- `search_and_save.py` - Combined search and save workflow
- `demo.py` - Demo script for LinkedIn integration
- `mcp_server.py` - LinkedIn MCP server implementation

## Output

- `job_search_results/` - Collected jobs in JSON format
  - `ai_researcher_new_york.json`
  - `data_scientist_san_francisco.json`
  - `deep_learning_engineer_remote.json`
  - `linkedin_real_test.json`
  - `machine_learning_engineer_remote.json`

## Usage

```bash
# From linkedin_collector directory
python3 linkedin_searcher.py

# Or use the combined workflow
python3 search_and_save.py
```

## Configuration

Set LinkedIn credentials in `.env`:
```
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
```

## Integration

This collector is part of the main job matching pipeline. Jobs collected here are:
1. Saved to `job_search_results/`
2. Loaded by `job_matcher.py` in the main directory
3. Ranked and matched with your resume
4. Sent via email

## Documentation

See the main project documentation for full pipeline details.
