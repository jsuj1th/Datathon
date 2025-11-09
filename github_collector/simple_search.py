#!/usr/bin/env python3
"""
Simple GitHub Job Search
Wrapper for easy integration with main pipeline
"""

import asyncio
import sys
from pathlib import Path
from typing import List, Dict
import json

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from collectors.github_discovery import GitHubRepoDiscovery
from collectors.github_fetcher import GitHubJobFetcher
from models.job import Job
import os
from dotenv import load_dotenv

# Load environment
load_dotenv(Path(__file__).parent.parent / ".env")


def search_github_jobs(keywords: str, location: str = "", limit: int = 50) -> List[Dict]:
    """
    Simple function to search GitHub for jobs
    
    Args:
        keywords: Search keywords (e.g., "machine learning engineer")
        location: Location filter (optional)
        limit: Maximum number of jobs to return
        
    Returns:
        List of job dictionaries
    """
    try:
        print(f"\n   🔍 Searching GitHub repositories...")
        print(f"   Keywords: {keywords}")
        
        # Check if we have cached jobs from previous runs
        data_dir = Path(__file__).parent.parent / "data"
        jobs_output = data_dir / "jobs_output.json"
        
        if jobs_output.exists():
            print(f"   📂 Loading cached GitHub jobs from {jobs_output}")
            with open(jobs_output, 'r', encoding='utf-8') as f:
                data = json.load(f)
                cached_jobs = data.get('jobs', [])
                
                if cached_jobs:
                    print(f"   ✅ Found {len(cached_jobs)} cached jobs")
                    
                    # Convert to dict format if needed
                    job_dicts = []
                    for job in cached_jobs:
                        if isinstance(job, dict):
                            job_dicts.append(job)
                        else:
                            # Convert Job object to dict
                            job_dict = {
                                'company': getattr(job, 'company', ''),
                                'position': getattr(job, 'position', ''),
                                'location': getattr(job, 'location', ''),
                                'description': getattr(job, 'description', ''),
                                'requirements': '',
                                'apply_link': getattr(job, 'application_url', ''),
                                'source': 'GitHub',
                            }
                            job_dicts.append(job_dict)
                    
                    # Filter by keywords
                    if keywords:
                        keywords_lower = keywords.lower()
                        filtered_jobs = []
                        
                        for job in job_dicts:
                            search_text = f"{job.get('position', '')} {job.get('company', '')} {job.get('description', '')}".lower()
                            
                            if keywords_lower in search_text or any(kw.strip().lower() in search_text for kw in keywords.split()):
                                filtered_jobs.append(job)
                        
                        job_dicts = filtered_jobs
                        print(f"   🔍 Filtered to {len(job_dicts)} jobs matching '{keywords}'")
                    
                    # Filter by location if specified
                    if location and location.lower() != "remote" and location:
                        location_lower = location.lower()
                        filtered_jobs = []
                        
                        for job in job_dicts:
                            job_location = job.get('location', '').lower()
                            
                            if location_lower in job_location or 'remote' in job_location:
                                filtered_jobs.append(job)
                        
                        job_dicts = filtered_jobs
                        print(f"   📍 Filtered to {len(job_dicts)} jobs in '{location}' or remote")
                    
                    # Limit results
                    job_dicts = job_dicts[:limit]
                    
                    print(f"   ✅ Returning {len(job_dicts)} GitHub jobs from cache")
                    return job_dicts
        
        # If no cached jobs, try to collect fresh ones (but use rate limit protection)
        print(f"   📡 No cached jobs found, collecting fresh jobs...")
        print(f"   ⚠️  Note: GitHub API has rate limits, using simplified search")
        
        # Use a simple direct fetch from known repositories
        fetcher = GitHubJobFetcher(os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"))
        
        # Try to fetch from SimplifyJobs directly (no API needed, just markdown)
        known_urls = [
            "https://raw.githubusercontent.com/SimplifyJobs/New-Grad-Positions/dev/README.md",
            "https://raw.githubusercontent.com/SimplifyJobs/Summer2025-Internships/dev/README.md",
        ]
        
        all_jobs = []
        for url in known_urls:
            try:
                print(f"   📥 Fetching from {url.split('/')[-3]}...")
                markdown = fetcher.fetch_markdown_from_url(url)
                if markdown:
                    jobs = fetcher.parse_markdown_table(markdown, url.split('/')[-3], "Software/ML")
                    all_jobs.extend(jobs)
                    print(f"      ✅ Got {len(jobs)} jobs")
            except Exception as e:
                print(f"      ⚠️  Failed: {e}")
                continue
        
        print(f"   📊 Collected {len(all_jobs)} total jobs from GitHub")
        
        # Convert to dict format
        job_dicts = []
        for job in all_jobs:
            job_dict = {
                'company': job.company,
                'position': job.position,
                'location': job.location,
                'description': job.description or '',
                'requirements': '',
                'apply_link': job.application_url,
                'source': 'GitHub',
                'field': job.field,
                'job_type': job.job_type.value if hasattr(job.job_type, 'value') else str(job.job_type),
                'remote_option': job.remote_option.value if hasattr(job.remote_option, 'value') else str(job.remote_option),
                'salary_range': job.salary_range,
                'posted_date': job.posted_date.isoformat() if job.posted_date else None
            }
            job_dicts.append(job_dict)
        
        # Filter by keywords
        if keywords:
            keywords_lower = keywords.lower()
            filtered_jobs = []
            
            for job in job_dicts:
                search_text = f"{job.get('position', '')} {job.get('company', '')} {job.get('description', '')}".lower()
                
                if keywords_lower in search_text or any(kw.strip().lower() in search_text for kw in keywords.split()):
                    filtered_jobs.append(job)
            
            job_dicts = filtered_jobs
            print(f"   🔍 Filtered to {len(job_dicts)} jobs matching '{keywords}'")
        
        # Filter by location if specified
        if location and location.lower() != "remote":
            location_lower = location.lower()
            filtered_jobs = []
            
            for job in job_dicts:
                job_location = job.get('location', '').lower()
                
                if location_lower in job_location or 'remote' in job_location:
                    filtered_jobs.append(job)
            
            job_dicts = filtered_jobs
            print(f"   📍 Filtered to {len(job_dicts)} jobs in '{location}' or remote")
        
        # Limit results
        job_dicts = job_dicts[:limit]
        
        print(f"   ✅ Returning {len(job_dicts)} GitHub jobs")
        
        return job_dicts
        
    except Exception as e:
        print(f"   ❌ Error searching GitHub: {e}")
        import traceback
        traceback.print_exc()
        return []


def main():
    """Test the GitHub search"""
    print("🔍 Testing GitHub Job Search")
    
    jobs = search_github_jobs(
        keywords="machine learning engineer",
        location="Remote",
        limit=20
    )
    
    print(f"\n✅ Found {len(jobs)} jobs")
    
    if jobs:
        print("\nFirst 3 jobs:")
        for i, job in enumerate(jobs[:3], 1):
            print(f"\n{i}. {job['position']} at {job['company']}")
            print(f"   Location: {job['location']}")
            print(f"   Apply: {job['apply_link']}")


if __name__ == "__main__":
    main()
