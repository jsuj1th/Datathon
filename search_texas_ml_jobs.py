#!/usr/bin/env python3
"""
Search for ML Engineer jobs in Texas using the job search APIs
"""

import os
import sys
import json
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent / "NewMCP Folder"))

from job_matcher import JobMatcher

def search_texas_ml_jobs():
    """Search for ML Engineer jobs in Texas"""
    
    print("\n" + "=" * 80)
    print("🔍 Searching for ML Engineer Jobs in Texas (Entry Level)")
    print("=" * 80)
    
    # Set API keys from config
    os.environ['GEMINI_API_KEY'] = "AIzaSyBQMMCmSSqecWcObb58FEZPaERy9YRU3H0"
    os.environ['FIRECRAWL_API_KEY'] = "fc-4b622c879b344861a2fcb26a23cb0b21"
    
    # Initialize job matcher
    matcher = JobMatcher()
    
    # Search parameters
    search_queries = [
        "Machine Learning Engineer Texas entry level",
        "ML Engineer Austin entry level",
        "AI Engineer Dallas junior",
        "Machine Learning Houston entry level",
    ]
    
    all_jobs = []
    
    for query in search_queries:
        print(f"\n🔎 Searching: {query}")
        print("-" * 80)
        
        try:
            # Use the job matcher's search functionality
            # Note: This will use LinkedIn-style simulated data
            result = matcher.search_jobs(
                keywords=query,
                location="Texas",
                limit=10
            )
            
            if isinstance(result, str):
                result = json.loads(result)
            
            jobs = result.get('jobs', [])
            print(f"   ✅ Found {len(jobs)} jobs")
            all_jobs.extend(jobs)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Remove duplicates based on job ID or URL
    unique_jobs = []
    seen_ids = set()
    
    for job in all_jobs:
        job_id = job.get('id') or job.get('url') or job.get('title', '')
        if job_id not in seen_ids:
            seen_ids.add(job_id)
            unique_jobs.append(job)
    
    print(f"\n" + "=" * 80)
    print(f"📊 Total unique jobs found: {len(unique_jobs)}")
    print("=" * 80)
    
    # Display jobs
    if unique_jobs:
        print("\n🎯 ML ENGINEER JOBS IN TEXAS (ENTRY LEVEL)")
        print("=" * 80)
        
        for i, job in enumerate(unique_jobs, 1):
            print(f"\n{i}. {job.get('title', 'N/A')}")
            print(f"   🏢 Company: {job.get('company', 'N/A')}")
            print(f"   📍 Location: {job.get('location', 'N/A')}")
            
            # Salary if available
            salary = job.get('salary_range') or job.get('salary')
            if salary:
                print(f"   💰 Salary: {salary}")
            
            # URL
            url = job.get('url', '') or job.get('apply_url', '')
            if url:
                print(f"   🔗 Apply: {url}")
            
            # Description preview
            desc = job.get('description', '')
            if desc:
                preview = desc[:250].replace('\n', ' ').strip()
                print(f"   📝 {preview}...")
            
            print("   " + "-" * 76)
        
        # Save results
        output_file = Path(__file__).parent / "data" / "texas_ml_jobs_search.json"
        output_file.parent.mkdir(exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump({
                'search_params': {
                    'keywords': 'Machine Learning Engineer',
                    'location': 'Texas',
                    'level': 'Entry Level'
                },
                'total_jobs': len(unique_jobs),
                'jobs': unique_jobs
            }, f, indent=2)
        
        print(f"\n💾 Results saved to: {output_file}")
        
        # Also create a simple text file for easy reading
        txt_file = Path(__file__).parent / "texas_ml_jobs_list.txt"
        with open(txt_file, 'w') as f:
            f.write("ML ENGINEER JOBS IN TEXAS (ENTRY LEVEL)\n")
            f.write("=" * 80 + "\n\n")
            
            for i, job in enumerate(unique_jobs, 1):
                f.write(f"{i}. {job.get('title', 'N/A')}\n")
                f.write(f"   Company: {job.get('company', 'N/A')}\n")
                f.write(f"   Location: {job.get('location', 'N/A')}\n")
                
                url = job.get('url', '') or job.get('apply_url', '')
                if url:
                    f.write(f"   Apply: {url}\n")
                
                f.write("\n" + "-" * 80 + "\n\n")
        
        print(f"📄 Text summary saved to: {txt_file}")
    else:
        print("\n❌ No jobs found. Try running the full pipeline with your APIs.")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    search_texas_ml_jobs()
