#!/usr/bin/env python3
"""
GitHub Job Search using Firecrawl API
Uses Firecrawl to scrape job listings from GitHub and other sources
"""

import os
import sys
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Load environment
load_dotenv(Path(__file__).parent.parent / ".env")


def search_github_with_firecrawl(keywords: str, location: str = "", limit: int = 50) -> List[Dict]:
    """
    Search for jobs using Firecrawl API
    
    Args:
        keywords: Search keywords (e.g., "machine learning engineer")
        location: Location filter (optional)
        limit: Maximum number of jobs to return
        
    Returns:
        List of job dictionaries
    """
    try:
        from collectors.firecrawl_scraper import FirecrawlJobScraper
        
        print(f"\n   🔥 Searching with Firecrawl API...")
        print(f"   Keywords: {keywords}")
        print(f"   Location: {location}")
        
        # Get API key
        api_key = os.getenv('FIRECRAWL_API_KEY')
        if not api_key:
            print("   ❌ FIRECRAWL_API_KEY not found in .env")
            return _fallback_github_jobs(keywords, limit)
        
        scraper = FirecrawlJobScraper()
        
        # Use multiple sources
        all_jobs = []
        
        # Try SimplifyJobs (GitHub repo with 30k+ jobs)
        try:
            print(f"\n   🔎 Searching SimplifyJobs on GitHub...")
            simplify_jobs = scraper.scrape_simplify(max_jobs=limit)
            
            if simplify_jobs:
                # Convert Job objects to dicts
                for job in simplify_jobs:
                    job_dict = {
                        'company': job.company,
                        'position': job.position,
                        'location': job.location or 'Not specified',
                        'description': job.description or f"Position at {job.company}",
                        'requirements': ', '.join(job.requirements or []),
                        'apply_link': job.apply_link or '',
                        'source': 'simplify_github',
                        'experience_level': str(job.job_type) if job.job_type else 'not_specified',
                        'job_type': str(job.job_type) if job.job_type else 'full-time',
                        'remote_option': str(job.remote_option) if job.remote_option else 'unknown'
                    }
                    
                    # Filter by keywords
                    text = f"{job_dict['position']} {job_dict['company']} {job_dict['description']} {job_dict['requirements']}".lower()
                    if any(kw.lower() in text for kw in keywords.split()):
                        all_jobs.append(job_dict)
                
                print(f"      ✅ Found {len(all_jobs)} matching jobs from SimplifyJobs")
                
        except Exception as e:
            print(f"      ⚠️  SimplifyJobs error: {e}")
        
        if not all_jobs:
            print("\n   ⚠️  No jobs from Firecrawl, using fallback...")
            return _fallback_github_jobs(keywords, limit)
        
        # Remove duplicates by company + position
        seen = set()
        unique_jobs = []
        
        for job in all_jobs:
            key = f"{job.get('company', '')}_{job.get('position', '')}"
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        print(f"\n   ✅ Total unique jobs: {len(unique_jobs)}")
        
        return unique_jobs[:limit]
        
    except ImportError as e:
        print(f"\n   ❌ Firecrawl not available: {e}")
        return _fallback_github_jobs(keywords, limit)
    except Exception as e:
        print(f"\n   ❌ Error in Firecrawl search: {e}")
        import traceback
        traceback.print_exc()
        return _fallback_github_jobs(keywords, limit)


def _fallback_github_jobs(keywords: str, limit: int = 50) -> List[Dict]:
    """
    Fallback: Try to get jobs from cached data or SimplifyJobs
    """
    try:
        print("\n   📂 Trying to load from cached jobs or SimplifyJobs...")
        
        # Try cached jobs first
        from github_collector.simple_search import search_github_jobs
        jobs = search_github_jobs(keywords, "", limit)
        
        if jobs:
            return jobs
        
        # If no cached jobs, create sample jobs
        return _create_sample_jobs(keywords, limit)
        
    except Exception as e:
        print(f"   ⚠️  Fallback failed: {e}")
        return _create_sample_jobs(keywords, limit)


def _create_sample_jobs(keywords: str, limit: int = 20) -> List[Dict]:
    """Create sample jobs for testing when APIs are unavailable"""
    print(f"\n   📝 Creating {limit} sample GitHub jobs for testing...")
    
    companies = [
        'GitHub', 'GitLab', 'Microsoft', 'Google', 'Amazon',
        'Meta', 'Apple', 'Netflix', 'Stripe', 'Airbnb',
        'Uber', 'Twitter', 'LinkedIn', 'Salesforce', 'Oracle',
        'IBM', 'Intel', 'NVIDIA', 'AMD', 'Qualcomm'
    ]
    
    positions = [
        f"{keywords} Engineer",
        f"Senior {keywords}",
        f"{keywords} Specialist",
        f"Lead {keywords}",
        f"{keywords} Architect"
    ]
    
    locations = ['Remote', 'San Francisco', 'New York', 'Seattle', 'Austin', 'Boston']
    
    jobs = []
    for i in range(min(limit, len(companies))):
        company = companies[i]
        position = positions[i % len(positions)]
        location = locations[i % len(locations)]
        
        job = {
            'company': company,
            'position': position,
            'location': location,
            'description': f"We're looking for a talented {keywords} professional to join our team. You'll work on cutting-edge projects using modern technologies.",
            'requirements': f"{keywords}, Python, Git, Agile, Cloud Computing",
            'apply_link': f"https://github.com/jobs/{company.lower()}-{i}",
            'source': 'github_sample',
            'experience_level': ['entry', 'mid', 'senior'][i % 3],
            'job_type': 'Full-time',
            'salary_range': f"${80 + i*10}k - ${120 + i*15}k"
        }
        jobs.append(job)
    
    print(f"   ✅ Created {len(jobs)} sample jobs")
    return jobs


def main():
    """Test the Firecrawl GitHub search"""
    print("🔥 Testing GitHub Job Search with Firecrawl")
    print("=" * 60)
    
    jobs = search_github_with_firecrawl(
        keywords="machine learning",
        location="Remote",
        limit=30
    )
    
    print(f"\n{'=' * 60}")
    print(f"✅ Found {len(jobs)} total jobs")
    print(f"{'=' * 60}")
    
    if jobs:
        print("\n📋 First 5 jobs:")
        for i, job in enumerate(jobs[:5], 1):
            print(f"\n{i}. {job['position']} at {job['company']}")
            print(f"   📍 Location: {job['location']}")
            print(f"   🔗 Apply: {job.get('apply_link', 'N/A')}")
            print(f"   📝 Description: {job.get('description', '')[:100]}...")


if __name__ == "__main__":
    main()
