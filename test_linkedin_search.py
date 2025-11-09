#!/usr/bin/env python3
"""Test LinkedIn search"""

import asyncio
import sys
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent / "linkedin_collector"))

from job_searcher import JobSearcher

async def test():
    searcher = JobSearcher()
    
    print("🔍 Testing LinkedIn/Muse Job Search...")
    print("=" * 60)
    
    # Test search
    jobs = await searcher.search_jobs(
        keywords="machine learning engineer python",
        location="Remote",
        limit=10
    )
    
    print(f"\n✅ Found {len(jobs)} jobs")
    
    if jobs:
        print(f"\nFirst 3 jobs:")
        for i, job in enumerate(jobs[:3], 1):
            print(f"\n{i}. {job.get('position', 'Unknown')}")
            print(f"   Company: {job.get('company', 'Unknown')}")
            print(f"   Location: {job.get('location', 'Unknown')}")
            if job.get('apply_link'):
                print(f"   Link: {job.get('apply_link')}")
    
    return jobs

if __name__ == "__main__":
    jobs = asyncio.run(test())
    print(f"\n✅ Test complete! Got {len(jobs)} jobs")
