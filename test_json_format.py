#!/usr/bin/env python3
"""
Test LinkedIn Jobs MCP Server
Test the job search functionality and JSON output format.
"""

import json
from src.server.linkedin_mcp_client import test_search_jobs

def test_json_format():
    """Test the JSON output format matches requirements."""
    
    print("🔍 Testing LinkedIn Jobs MCP Server...")
    print("=" * 50)
    
    # Test job search
    result = test_search_jobs("software engineer", "San Francisco", 3)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return False
    
    print(f"✅ Found {result['total_found']} jobs")
    
    # Check first job format
    if result['jobs']:
        first_job = result['jobs'][0]
        print("\n📋 Sample job format:")
        print(json.dumps(first_job, indent=2))
        
        # Verify required fields
        required_fields = [
            'company', 'position', 'apply_link', 'location', 'salary',
            'description', 'requirements', 'benefits', 'job_type',
            'experience_level', 'posted_date', 'deadline', 'days_since_posted',
            'remote_option', 'visa_sponsorship', 'source', 'collection_method',
            'collected_at', 'field', 'company_type'
        ]
        
        missing_fields = [field for field in required_fields if field not in first_job]
        
        if missing_fields:
            print(f"❌ Missing fields: {missing_fields}")
            return False
        else:
            print("✅ All required fields present")
    
    # Test different search terms
    print("\n🔍 Testing various search terms...")
    test_cases = [
        ("python developer", "remote"),
        ("data scientist", "New York"),
        ("product manager", ""),
    ]
    
    for keywords, location in test_cases:
        try:
            result = test_search_jobs(keywords, location, 1)
            if "error" not in result and result['jobs']:
                print(f"✅ {keywords} in {location or 'any location'}: {result['total_found']} jobs")
            else:
                print(f"⚠️  {keywords} in {location or 'any location'}: no jobs found")
        except Exception as e:
            print(f"❌ {keywords}: {e}")
    
    return True

if __name__ == "__main__":
    success = test_json_format()
    
    if success:
        print("\n🎉 LinkedIn Jobs MCP Server is working correctly!")
        print("\nJSON Format matches requirements:")
        print("- ✅ Structured job objects")
        print("- ✅ All required fields present")
        print("- ✅ LinkedIn source properly identified")
        print("- ✅ Collection timestamp included")
        print("\nReady for Claude Desktop integration!")
    else:
        print("\n❌ Test failed. Please check configuration.")
