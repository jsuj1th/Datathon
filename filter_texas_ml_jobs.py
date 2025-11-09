#!/usr/bin/env python3
"""
Filter and display ML Engineer jobs in Texas from existing data
"""

import json
from pathlib import Path

def filter_texas_ml_jobs():
    """Filter jobs for ML Engineer positions in Texas"""
    
    data_dir = Path(__file__).parent / "data"
    all_jobs = []
    
    # Load all job files
    for job_file in data_dir.glob("*.json"):
        try:
            with open(job_file) as f:
                data = json.load(f)
                if isinstance(data, list):
                    all_jobs.extend(data)
                elif isinstance(data, dict) and 'jobs' in data:
                    all_jobs.extend(data['jobs'])
        except Exception as e:
            print(f"Error reading {job_file.name}: {e}")
    
    print(f"\n📊 Total jobs loaded: {len(all_jobs)}")
    
    # Filter for ML Engineer jobs in Texas
    texas_ml_jobs = []
    texas_keywords = ['texas', 'tx', 'dallas', 'houston', 'austin', 'san antonio']
    ml_keywords = ['machine learning', 'ml engineer', 'ai engineer', 'deep learning']
    entry_keywords = ['entry level', 'junior', 'associate', '0-2 years', 'new grad', 'graduate']
    
    for job in all_jobs:
        # Get job fields (handling different formats)
        title = str(job.get('title', '') or job.get('job_title', '')).lower()
        location = str(job.get('location', '') or job.get('job_location', '')).lower()
        description = str(job.get('description', '') or job.get('job_description', '')).lower()
        company = job.get('company', '') or job.get('company_name', '')
        
        # Check if it's in Texas
        is_texas = any(keyword in location for keyword in texas_keywords)
        
        # Check if it's ML related
        is_ml = any(keyword in title or keyword in description[:500] for keyword in ml_keywords)
        
        # Check if it's entry level (prefer but not required)
        is_entry = any(keyword in title or keyword in description[:500] for keyword in entry_keywords)
        
        if is_texas and is_ml:
            job['is_entry_level'] = is_entry
            texas_ml_jobs.append(job)
    
    # Sort: entry level first
    texas_ml_jobs.sort(key=lambda x: (not x.get('is_entry_level', False), x.get('title', '')))
    
    print(f"🎯 Found {len(texas_ml_jobs)} ML Engineer jobs in Texas")
    print(f"   ({sum(1 for j in texas_ml_jobs if j.get('is_entry_level'))} are entry-level)\n")
    print("=" * 80)
    
    # Display jobs
    for i, job in enumerate(texas_ml_jobs[:20], 1):  # Show top 20
        print(f"\n{i}. {'⭐ ' if job.get('is_entry_level') else ''}{job.get('title', 'N/A')}")
        print(f"   🏢 Company: {job.get('company', job.get('company_name', 'N/A'))}")
        print(f"   📍 Location: {job.get('location', job.get('job_location', 'N/A'))}")
        
        # URL
        url = job.get('url', '') or job.get('apply_url', '') or job.get('job_url', '')
        if url:
            print(f"   🔗 Apply: {url}")
        
        # Description preview
        desc = job.get('description', '') or job.get('job_description', '')
        if desc:
            preview = desc[:200].replace('\n', ' ').strip()
            print(f"   📝 {preview}...")
        
        print("   " + "-" * 76)
    
    # Save filtered results
    output_file = Path(__file__).parent / "texas_ml_jobs.json"
    with open(output_file, 'w') as f:
        json.dump(texas_ml_jobs, f, indent=2)
    
    print(f"\n💾 Saved {len(texas_ml_jobs)} jobs to: {output_file.name}")
    print("\n" + "=" * 80)

if __name__ == "__main__":
    filter_texas_ml_jobs()
