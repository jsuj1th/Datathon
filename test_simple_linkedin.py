#!/usr/bin/env python3
"""
Simple LinkedIn API Test
Test LinkedIn API functionality without MCP decorators.
"""

from linkedin_api import Linkedin
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_linkedin_api():
    """Test basic LinkedIn API functionality."""
    
    print("🔍 Testing LinkedIn API functionality...")
    print("=" * 50)
    
    # Check environment variables
    email = os.getenv('LINKEDIN_EMAIL')
    password = os.getenv('LINKEDIN_PASSWORD')
    
    if not email or not password:
        print("❌ ERROR: LinkedIn credentials not found!")
        print("Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in your .env file")
        return False
    
    print("✅ LinkedIn credentials found")
    print(f"   Email: {email[:5]}...@{email.split('@')[1] if '@' in email else 'unknown'}")
    
    try:
        # Initialize LinkedIn client
        print("\n🔗 Connecting to LinkedIn...")
        client = Linkedin(email, password, debug=False)
        print("✅ Successfully connected to LinkedIn")
        
        # Test job search
        print("\n📋 Testing job search...")
        jobs = client.search_jobs(
            keywords="software engineer",
            location_name="San Francisco",
            limit=2,
            offset=0
        )
        print(f"✅ Found {len(jobs)} jobs")
        
        # Show first job details
        if jobs:
            first_job = jobs[0]
            print(f"   First job ID: {first_job.get('entityUrn', 'N/A')}")
            
            # Try to get detailed job information
            try:
                job_id = first_job["entityUrn"].split(":")[-1]
                job_details = client.get_job(job_id=job_id)
                job_title = job_details.get("title", "N/A")
                print(f"   Job title: {job_title}")
            except Exception as e:
                print(f"   ⚠️  Could not get job details: {e}")
        
        # Test feed posts
        print("\n📰 Testing feed posts...")
        try:
            posts = client.get_feed_posts(limit=2, offset=0)
            print(f"✅ Retrieved {len(posts)} feed posts")
        except Exception as e:
            print(f"⚠️  Could not get feed posts: {e}")
        
        # Test profile
        print("\n👤 Testing profile retrieval...")
        try:
            profile = client.get_profile()
            first_name = profile.get('firstName', 'N/A')
            last_name = profile.get('lastName', 'N/A')
            print(f"✅ Retrieved profile: {first_name} {last_name}")
        except Exception as e:
            print(f"⚠️  Could not get profile: {e}")
        
        print("\n🎉 LinkedIn API test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check your LinkedIn email and password")
        print("2. Make sure you can log into LinkedIn manually")
        print("3. Try using a different IP/network if rate limited")
        return False

if __name__ == "__main__":
    success = test_linkedin_api()
    
    if success:
        print("\n✅ LinkedIn API is working!")
        print("You can now use the MCP server.")
    else:
        print("\n❌ LinkedIn API test failed.")
        print("Please check your credentials and try again.")
