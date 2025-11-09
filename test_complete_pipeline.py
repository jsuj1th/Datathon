#!/usr/bin/env python3
"""Quick test of complete pipeline components"""

import sys
from pathlib import Path

print("Testing Complete Pipeline Components")
print("=" * 60)

# Test 1: GitHub Firecrawl Import
print("\n1. Testing GitHub Firecrawl import...")
try:
    from github_collector.firecrawl_search import search_github_with_firecrawl
    print("   ✅ GitHub Firecrawl import successful")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 2: JobMatcher from NewMCP Folder
print("\n2. Testing JobMatcher from NewMCP Folder...")
try:
    sys.path.insert(0, str(Path(__file__).parent / "NewMCP Folder"))
    from job_matcher import JobMatcher
    
    matcher = JobMatcher()
    
    # Check for extract_resume method
    if hasattr(matcher, 'extract_resume'):
        print("   ✅ JobMatcher has extract_resume method")
    else:
        print("   ❌ JobMatcher missing extract_resume method")
        
    # Check for match_job_with_resume method
    if hasattr(matcher, 'match_job_with_resume'):
        print("   ✅ JobMatcher has match_job_with_resume method")
    else:
        print("   ❌ JobMatcher missing match_job_with_resume method")
        
    # Check for match_jobs_with_llm method
    if hasattr(matcher, 'match_jobs_with_llm'):
        print("   ✅ JobMatcher has match_jobs_with_llm method")
    else:
        print("   ❌ JobMatcher missing match_jobs_with_llm method")
        
    # Check for prepare_email_content method
    if hasattr(matcher, 'prepare_email_content'):
        print("   ✅ JobMatcher has prepare_email_content method")
    else:
        print("   ❌ JobMatcher missing prepare_email_content method")
        
except Exception as e:
    print(f"   ❌ Failed: {e}")
    import traceback
    traceback.print_exc()

# Test 3: LinkedIn Searcher
print("\n3. Testing LinkedIn Searcher...")
try:
    from linkedin_collector.job_searcher import JobSearcher
    searcher = JobSearcher()
    print("   ✅ LinkedIn JobSearcher import successful")
except Exception as e:
    print(f"   ❌ Failed: {e}")

print("\n" + "=" * 60)
print("✅ Component testing complete!")
