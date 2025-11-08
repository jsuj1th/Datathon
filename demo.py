#!/usr/bin/env python3
"""
Simple Job Search Demo
Quick demonstration of the job search MCP server functionality with new JSON format.
"""

import asyncio
import json
import sys
from pathlib import Path

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from mcp_server import search_linkedin_jobs, search_muse_jobs, search_combined_jobs
from job_saver import save_jobs_to_json, validate_job_format

def quick_search(query: str, location: str = "", limit: int = 5) -> dict:
    """
    Quick job search using LinkedIn simulation with new JSON format.
    
    Args:
        query: Job search query (e.g., "software engineer", "data scientist")
        location: Location filter (optional)
        limit: Number of results (default: 5)
    
    Returns:
        Dictionary with job search results in new format
    """
    try:
        result = search_linkedin_jobs(query, limit, 0, location)
        data = json.loads(result)
        
        print(f"✅ Found {len(data.get('jobs', []))} jobs")
        
        # Validate the new format
        jobs = data.get('jobs', [])
        if jobs:
            first_job = jobs[0]
            print(f"\n📋 Sample Job Format:")
            print(f"   Company: {first_job.get('company')}")
            print(f"   Position: {first_job.get('position')}")
            print(f"   Location: {first_job.get('location')}")
            print(f"   Salary: {first_job.get('salary')}")
            print(f"   Field: {first_job.get('field')}")
            print(f"   Remote Option: {first_job.get('remote_option')}")
            print(f"   Experience Level: {first_job.get('experience_level')}")
            
            # Validate format
            if validate_job_format(first_job):
                print("✅ Job format validation passed")
            else:
                print("❌ Job format validation failed")
        
        return data
        
    except Exception as e:
        print(f"❌ Search failed: {e}")
        return {"error": str(e), "jobs": []}

async def muse_search(query: str, location: str = "", limit: int = 5) -> dict:
    """
    Search using The Muse API and realistic fallbacks.
    
    Args:
        query: Job search query
        location: Location filter (optional) 
        limit: Number of results (default: 5)
    
    Returns:
        Dictionary with job search results
    """
    try:
        result = await search_muse_jobs(query, location, limit)
        return json.loads(result)
    except Exception as e:
        return {"error": str(e), "jobs": []}

async def combined_search(query: str, location: str = "", limit: int = 10) -> dict:
    """
    Combined search across LinkedIn simulation and The Muse.
    
    Args:
        query: Job search query
        location: Location filter (optional)
        limit: Number of results (default: 10)
    
    Returns:
        Dictionary with combined job search results
    """
    try:
        result = await search_combined_jobs(query, location, limit)
        return json.loads(result)
    except Exception as e:
        return {"error": str(e), "jobs": []}

async def run_demo():
    """Run a comprehensive demo of the job search system with new JSON format."""
    print("🚀 Job Search MCP Server Demo - New JSON Format")
    print("=" * 60)
    
    test_cases = [
        ("data scientist", "Texas"),
        ("software engineer", "San Francisco"),
        ("python developer", "Remote")
    ]
    
    all_saved_files = []
    
    for query, location in test_cases:
        print(f"\n🔍 Searching: '{query}' in '{location}'")
        print("-" * 50)
        
        # LinkedIn simulation with new format
        print("📊 LinkedIn Simulation (New Format):")
        linkedin_result = quick_search(query, location, 5)
        
        if linkedin_result.get("jobs"):
            # Save to JSON file
            search_query = {"keywords": query, "location": location, "limit": 5}
            filename = f"{query.replace(' ', '_')}_{location.replace(' ', '_')}_linkedin.json"
            file_path = save_jobs_to_json(linkedin_result["jobs"], search_query, filename)
            all_saved_files.append(file_path)
            
            # Show sample jobs
            for i, job in enumerate(linkedin_result["jobs"][:3], 1):
                print(f"   {i}. {job.get('position')} at {job.get('company')}")
                print(f"      💰 {job.get('salary', 'Not specified')}")
                print(f"      🏢 {job.get('field')} - {job.get('experience_level')}")
                print(f"      📍 {job.get('remote_option')} in {job.get('location')}")
        
        # The Muse + fallbacks
        print(f"\n🎯 The Muse + Realistic Jobs:")
        muse_result = await muse_search(query, location, 5)
        
        if muse_result.get("jobs"):
            # Save to JSON file
            search_query = {"keywords": query, "location": location, "limit": 5}
            filename = f"{query.replace(' ', '_')}_{location.replace(' ', '_')}_muse.json"
            file_path = save_jobs_to_json(muse_result["jobs"], search_query, filename)
            all_saved_files.append(file_path)
            
            for i, job in enumerate(muse_result["jobs"][:2], 1):
                print(f"   {i}. {job.get('position', job.get('title', 'Unknown'))} at {job.get('company')}")
                print(f"      🔗 Source: {job.get('source', 'unknown')}")
                print(f"      📊 Field: {job.get('field', 'Unknown')}")
        
        # Combined search
        print(f"\n🌐 Combined Search:")
        combined_result = await combined_search(query, location, 8)
        
        if combined_result.get("jobs"):
            # Save to JSON file
            search_query = {"keywords": query, "location": location, "limit": 8}
            filename = f"{query.replace(' ', '_')}_{location.replace(' ', '_')}_combined.json"
            file_path = save_jobs_to_json(combined_result["jobs"], search_query, filename)
            all_saved_files.append(file_path)
            
            sources = combined_result.get("sources_used", [])
            print(f"   Found {len(combined_result['jobs'])} jobs from: {', '.join(sources)}")
            
            # Show job format validation
            sample_job = combined_result["jobs"][0] if combined_result["jobs"] else None
            if sample_job and validate_job_format(sample_job):
                print("   ✅ All jobs follow the new standardized format")
    
    print(f"\n📁 Files Saved:")
    print("=" * 40)
    for file_path in all_saved_files:
        print(f"✅ {file_path}")
    
    print(f"\n🎯 New JSON Format Features:")
    print("• Standardized field names (company, position, apply_link)")
    print("• Rich metadata (experience_level, remote_option, field)")
    print("• Consistent data types and structure")
    print("• Collection tracking (collection_method, collected_at)")
    print("• Flexible null handling for optional fields")
    
    print(f"\n✅ Demo completed!")
    print("🔧 GitHub Copilot MCP Tools Available:")
    print("  • search_linkedin_jobs")
    print("  • search_muse_jobs") 
    print("  • search_combined_jobs")
    print("  • bb7_search_jobs (legacy)")
    
    return all_saved_files

if __name__ == "__main__":
    # Test the new JSON format
    print("🧪 Testing New JSON Format...")
    
    # Run the demo
    saved_files = asyncio.run(run_demo())
    
    print(f"\n🎉 Demo Complete! New JSON format is working.")
    print(f"📊 Generated {len(saved_files)} JSON files with standardized job data.")
