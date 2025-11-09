#!/usr/bin/env python3
"""
Quick script to search for ML Engineer jobs in Texas
"""

import json
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))

# Try to use the job search components
try:
    from job_matcher import JobMatcher
    
    # Initialize job matcher
    matcher = JobMatcher()
    
    print("🔍 Searching for ML Engineer jobs in Texas (entry level)...")
    print("=" * 60)
    
    # Search parameters
    search_params = {
        "keywords": "Machine Learning Engineer entry level",
        "location": "Texas",
        "limit": 20
    }
    
    print(f"\nSearch Parameters:")
    print(f"  Keywords: {search_params['keywords']}")
    print(f"  Location: {search_params['location']}")
    print(f"  Limit: {search_params['limit']}")
    print("\n" + "=" * 60)
    
    # Note: The actual job search would need API credentials
    # For now, let's check what data we already have
    data_dir = Path(__file__).parent / "data"
    
    print("\n📁 Checking existing job data files...")
    if data_dir.exists():
        job_files = list(data_dir.glob("*.json"))
        if job_files:
            print(f"\nFound {len(job_files)} job data files:")
            for file in job_files:
                print(f"  - {file.name}")
                try:
                    with open(file) as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            print(f"    Contains {len(data)} jobs")
                        elif isinstance(data, dict) and 'jobs' in data:
                            print(f"    Contains {len(data['jobs'])} jobs")
                except Exception as e:
                    print(f"    Error reading: {e}")
        else:
            print("  No job data files found")
    
    # Check matched jobs
    matched_dir = Path(__file__).parent / "matched_jobs"
    if matched_dir.exists():
        matched_files = list(matched_dir.glob("*.json"))
        if matched_files:
            print(f"\n📊 Found {len(matched_files)} matched job files:")
            for file in matched_files:
                print(f"  - {file.name}")
    
    print("\n" + "=" * 60)
    print("\n💡 To search for new jobs, you'll need to:")
    print("1. Ensure your API keys are set in environment variables")
    print("2. Run the complete pipeline: python main_complete_pipeline.py")
    print("3. Or use the MCP server once Claude Desktop connection is fixed")
    
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("\n💡 Try installing requirements:")
    print("   pip install -r requirements.txt")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
