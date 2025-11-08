#!/usr/bin/env python3
"""
Advanced LinkedIn Job Search Test
Test different job search parameters to find working combinations.
"""

from linkedin_api import Linkedin
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

def test_advanced_job_search():
    """Test various job search parameters to find what works."""
    
    print("🔍 Advanced LinkedIn Job Search Testing...")
    print("=" * 60)
    
    # Check environment variables
    email = os.getenv('LINKEDIN_EMAIL')
    password = os.getenv('LINKEDIN_PASSWORD')
    
    if not email or not password:
        print("❌ ERROR: LinkedIn credentials not found!")
        return False
    
    try:
        # Initialize LinkedIn client
        print("🔗 Connecting to LinkedIn...")
        client = Linkedin(email, password, debug=True, refresh_cookies=True)
        print("✅ Successfully connected to LinkedIn")
        
        # Test different search parameters
        search_tests = [
            # Test 1: Simple keyword search, no location
            {
                "name": "Simple keyword search",
                "params": {"keywords": "python", "limit": 3}
            },
            # Test 2: Popular keywords with broader location
            {
                "name": "Popular tech job",
                "params": {"keywords": "software developer", "location_name": "United States", "limit": 3}
            },
            # Test 3: Remote jobs
            {
                "name": "Remote jobs",
                "params": {"keywords": "remote software", "limit": 3}
            },
            # Test 4: Entry level positions
            {
                "name": "Entry level",
                "params": {"keywords": "junior developer", "location_name": "California", "limit": 3}
            },
            # Test 5: Data jobs
            {
                "name": "Data jobs",
                "params": {"keywords": "data analyst", "location_name": "New York", "limit": 3}
            },
            # Test 6: Just location-based
            {
                "name": "Location only",
                "params": {"keywords": "engineer", "location_name": "San Francisco Bay Area", "limit": 5}
            }
        ]
        
        successful_searches = []
        
        for i, test in enumerate(search_tests, 1):
            print(f"\n📋 Test {i}: {test['name']}")
            print(f"   Parameters: {test['params']}")
            
            try:
                jobs = client.search_jobs(**test['params'])
                print(f"   ✅ Found {len(jobs)} jobs")
                
                if jobs:
                    successful_searches.append(test)
                    
                    # Try to get details for first job
                    first_job = jobs[0]
                    print(f"   📄 First job: {first_job.get('title', 'N/A')}")
                    
                    # Show some basic info from the search results
                    for j, job in enumerate(jobs[:2]):  # Show first 2 jobs
                        title = job.get('title', 'N/A')
                        company = job.get('companyName', 'N/A') 
                        location = job.get('location', 'N/A')
                        print(f"      {j+1}. {title} at {company} - {location}")
                
                # Add delay between searches to avoid rate limiting
                time.sleep(2)
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                time.sleep(3)  # Longer delay after error
        
        print(f"\n🎉 Testing completed!")
        print(f"✅ Successful searches: {len(successful_searches)}/{len(search_tests)}")
        
        if successful_searches:
            print("\n🔥 Working search parameters:")
            for test in successful_searches:
                print(f"   - {test['name']}: {test['params']}")
            return True
        else:
            print("\n❌ No successful job searches found")
            print("This might be due to:")
            print("1. LinkedIn rate limiting")
            print("2. Account restrictions")
            print("3. Geographic restrictions")
            print("4. LinkedIn API changes")
            return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_job_search_with_different_methods():
    """Test alternative job search approaches."""
    
    print("\n🔍 Testing alternative job search methods...")
    print("=" * 60)
    
    email = os.getenv('LINKEDIN_EMAIL')
    password = os.getenv('LINKEDIN_PASSWORD')
    
    try:
        client = Linkedin(email, password, debug=True)
        
        # Method 1: Try getting recent jobs without specific search
        print("\n📋 Method 1: Recent jobs (no specific search)")
        try:
            # Sometimes this works better than specific searches
            jobs = client.search_jobs(keywords="", limit=5)
            print(f"   ✅ Found {len(jobs)} recent jobs")
            
            if jobs:
                for i, job in enumerate(jobs[:3]):
                    print(f"   {i+1}. {job.get('title', 'N/A')} - {job.get('location', 'N/A')}")
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Method 2: Try with common job titles
        print("\n📋 Method 2: Common job titles")
        common_titles = ["analyst", "manager", "engineer", "developer", "specialist"]
        
        for title in common_titles:
            try:
                jobs = client.search_jobs(keywords=title, limit=2)
                if jobs:
                    print(f"   ✅ '{title}': Found {len(jobs)} jobs")
                    break
                else:
                    print(f"   ⚠️  '{title}': No jobs found")
            except Exception as e:
                print(f"   ❌ '{title}': Error - {e}")
                
            time.sleep(1)
        
        # Method 3: Try different location formats
        print("\n📋 Method 3: Different location formats")
        locations = ["", "US", "United States", "California", "CA", "Remote"]
        
        for location in locations:
            try:
                jobs = client.search_jobs(keywords="python", location_name=location, limit=2)
                print(f"   Location '{location}': {len(jobs)} jobs")
                if jobs:
                    break
            except Exception as e:
                print(f"   Location '{location}': Error - {e}")
                
            time.sleep(1)
            
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    print("LinkedIn Job Search Diagnostic Tool")
    print("=" * 60)
    
    # Run comprehensive tests
    success = test_advanced_job_search()
    
    if not success:
        print("\n🔧 Running alternative methods...")
        test_job_search_with_different_methods()
        
    print("\n💡 Tips for better job search results:")
    print("1. Try broader keywords (e.g., 'engineer' instead of 'senior software engineer')")
    print("2. Use location names that LinkedIn recognizes")
    print("3. Avoid special characters in search terms")
    print("4. Try searching without location first")
    print("5. Check if your LinkedIn account has geographic restrictions")
