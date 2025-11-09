#!/usr/bin/env python3
"""
Jobs MCP Server
A Model Context Protocol server that provides LinkedIn simulation and The Muse Jobs API integration.
"""

import asyncio
import json
import logging
import os
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    import fastmcp
    from fastmcp import mcp
except ImportError:
    # For testing without fastmcp
    class MockMCP:
        def tool(self, func):
            return func
    mcp = MockMCP()

# Import job searcher
try:
    from job_searcher import JobSearcher, search_jobs_enhanced
    JOB_SEARCHER_AVAILABLE = True
except ImportError:
    JOB_SEARCHER_AVAILABLE = False
    logging.warning("Job searcher not available")

# Import LinkedIn searcher
try:
    from linkedin_searcher import LinkedInJobSearcher
    LINKEDIN_SEARCHER_AVAILABLE = True
    linkedin_searcher = LinkedInJobSearcher()
except ImportError:
    LINKEDIN_SEARCHER_AVAILABLE = False
    linkedin_searcher = None
    logging.warning("LinkedIn searcher not available")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP app
app = fastmcp.FastMCP("Jobs MCP Server")

def search_linkedin_jobs(keywords: str, limit: int = 10, offset: int = 0, location: str = '') -> str:
    """
    Search for jobs on LinkedIn (simulated with realistic data).
    
    Args:
        keywords: Job search keywords (e.g., "software engineer", "data scientist")
        limit: Maximum number of job results (default: 10)
        offset: Number of jobs to skip (default: 0)
        location: Optional location filter (e.g., "San Francisco", "Remote")
        
    Returns:
        JSON string with structured LinkedIn-style job data
    """
    try:
        logger.info(f"LinkedIn search: {keywords} in {location}, limit={limit}")
        
        # Simulate LinkedIn job data structure
        jobs = []
        
        # Define job templates based on keywords
        if "software" in keywords.lower() or "engineer" in keywords.lower():
            companies = ["Google", "Meta", "Apple", "Microsoft", "Amazon", "Netflix", "Uber", "Airbnb"]
            titles = ["Senior Software Engineer", "Software Engineer II", "Full Stack Engineer", "Backend Engineer"]
        elif "data" in keywords.lower() or "scientist" in keywords.lower():
            companies = ["Meta", "Google", "Netflix", "Spotify", "Palantir", "DataBricks", "Snowflake"]
            titles = ["Senior Data Scientist", "Data Scientist II", "ML Engineer", "Data Engineer"]
        else:
            companies = ["TechCorp", "InnovateCo", "StartupXYZ", "BigTech Inc"]
            titles = ["Engineer", "Developer", "Analyst", "Specialist"]
        
        # Generate realistic job listings with actual LinkedIn-style links
        for i in range(min(limit, 20)):
            # Generate realistic LinkedIn job ID (10 digits)
            linkedin_job_id = random.randint(3000000000, 3999999999)
            title = titles[i % len(titles)]
            company = companies[i % len(companies)]
            job_location = location if location else ["San Francisco, CA", "New York, NY", "Remote", "Seattle, WA"][i % 4]

            # Determine experience level and job type
            experience_level = "senior_level" if "senior" in title.lower() else "mid_level"
            remote_option = "remote" if job_location == "Remote" else "onsite"

            # Calculate days since posted
            days_ago = random.randint(1, 7)  # LinkedIn jobs are usually recent

            # Create realistic LinkedIn apply link
            company_slug = company.lower().replace(" ", "-")
            title_slug = title.lower().replace(" ", "-").replace(",", "")
            apply_link = f"https://www.linkedin.com/jobs/view/{linkedin_job_id}?refId=search&position={i+1}"

            job = {
                "company": company,
                "position": title,
                "apply_link": apply_link,
                "location": job_location,
                "salary": "$120,000 - $180,000" if "senior" in title.lower() else "$90,000 - $140,000",
                "description": f"We are seeking a talented {title} to join our dynamic team. This role offers excellent opportunities for growth and impact.",
                "requirements": ", ".join(["Python", "JavaScript", "AWS", "Docker"] if "software" in keywords.lower() else ["SQL", "Python", "Machine Learning", "Statistics"]),
                "benefits": "Health insurance, 401k, Stock options, Flexible PTO, Remote work",
                "job_type": "full_time",
                "experience_level": experience_level,
                "posted_date": datetime.now().strftime("%Y-%m-%d"),
                "deadline": None,
                "days_since_posted": days_ago,
                "remote_option": remote_option,
                "visa_sponsorship": True,
                "source": f"linkedin/{linkedin_job_id}",
                "collection_method": "mcp_linkedin_simulation",
                "collected_at": datetime.now().isoformat(),
                "field": "Software Engineering" if "software" in keywords.lower() or "engineer" in keywords.lower() else "AI/ML" if "data" in keywords.lower() else "Technology",
                "company_type": "big_tech" if company in ["Google", "Meta", "Apple", "Microsoft", "Amazon", "Netflix"] else "startup"
            }
            
            jobs.append(job)
        
        result = {
            "search_query": {
                "keywords": keywords,
                "location": location,
                "limit": limit,
                "offset": offset
            },
            "total_results": len(jobs),
            "jobs": jobs,
            "source": "linkedin_simulation",
            "generated_at": datetime.now().isoformat()
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"LinkedIn job search failed: {e}")
        return json.dumps({
            "error": str(e),
            "jobs": []
        }, indent=2)

async def search_muse_jobs(keywords: str, location: str = "", limit: int = 25) -> str:
    """
    Search for jobs using The Muse API and realistic fallbacks.
    
    Args:
        keywords: Job search keywords (e.g., "software engineer", "data scientist")
        location: Optional location filter (e.g., "San Francisco", "Remote")
        limit: Maximum number of job results (default: 25)
        
    Returns:
        JSON string with structured job data from The Muse and fallbacks
    """
    try:
        if not JOB_SEARCHER_AVAILABLE:
            return json.dumps({
                "error": "Job searcher not available",
                "jobs": []
            }, indent=2)
        
        logger.info(f"Muse search: {keywords} in {location}, limit={limit}")
        
        # Use job searcher for The Muse API and fallbacks
        return await search_jobs_enhanced(keywords, location, limit)
        
    except Exception as e:
        logger.error(f"Muse job search failed: {e}")
        return json.dumps({
            "error": str(e),
            "jobs": []
        }, indent=2)

async def search_combined_jobs(keywords: str, location: str = "", limit: int = 30) -> str:
    """
    Search for jobs from REAL sources (LinkedIn API + The Muse API).

    Args:
        keywords: Job search keywords (e.g., "software engineer", "data scientist")
        location: Optional location filter (e.g., "San Francisco", "Remote")
        limit: Maximum number of job results total (default: 30)

    Returns:
        JSON string with real job data from LinkedIn and The Muse
    """
    try:
        logger.info(f"Real job search: {keywords} in {location}, limit={limit}")

        all_jobs = []
        sources_used = []

        # Split limit between sources
        linkedin_limit = limit // 2
        muse_limit = limit - linkedin_limit

        # Get REAL LinkedIn jobs
        if LINKEDIN_SEARCHER_AVAILABLE and linkedin_searcher and linkedin_searcher.api:
            try:
                logger.info(f"Fetching {linkedin_limit} jobs from LinkedIn API")
                linkedin_jobs = linkedin_searcher.search_jobs(keywords, location, linkedin_limit)
                if linkedin_jobs:
                    all_jobs.extend(linkedin_jobs)
                    sources_used.append("linkedin")
                    logger.info(f"Got {len(linkedin_jobs)} jobs from LinkedIn")
            except Exception as e:
                logger.warning(f"LinkedIn search failed: {e}")

        # Get REAL jobs from The Muse API
        if JOB_SEARCHER_AVAILABLE:
            try:
                muse_result = await search_muse_jobs(keywords, location, muse_limit)
                muse_data = json.loads(muse_result)
                if muse_data.get("jobs"):
                    all_jobs.extend(muse_data["jobs"])
                    sources_used.extend(muse_data.get("sources", ["muse"]))
            except Exception as e:
                logger.warning(f"The Muse search failed: {e}")
        
        # Remove duplicates based on title and company
        seen = set()
        unique_jobs = []
        for job in all_jobs:
            key = (job.get("title", "").lower(), job.get("company", "").lower())
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        # Limit final results
        unique_jobs = unique_jobs[:limit]
        
        result = {
            "search_query": {
                "keywords": keywords,
                "location": location,
                "limit": limit
            },
            "total_results": len(unique_jobs),
            "sources_used": list(set(sources_used)),
            "jobs": unique_jobs,
            "generated_at": datetime.now().isoformat()
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Combined job search failed: {e}")
        return json.dumps({
            "error": str(e),
            "jobs": []
        }, indent=2)

# Backward compatibility aliases
def bb7_search_jobs(keywords: str, limit: int = 10, offset: int = 0, location: str = '') -> str:
    """
    Legacy LinkedIn job search (alias for search_linkedin_jobs).
    """
    return search_linkedin_jobs(keywords, limit, offset, location)

# Register tools with the MCP app
app.tool()(search_linkedin_jobs)
app.tool()(search_muse_jobs)
app.tool()(search_combined_jobs)
app.tool()(bb7_search_jobs)

# Test function for when run as script
async def test_mcp_server():
    """Test the MCP server functionality."""
    print("🚀 Testing Jobs MCP Server")
    print("=" * 50)
    
    test_cases = [
        ("software engineer", "San Francisco"),
        ("data scientist", "New York"),  
        ("python developer", "Remote")
    ]
    
    for keywords, location in test_cases:
        print(f"\n🔍 Testing: '{keywords}' in '{location}'")
        print("-" * 40)
        
        # Test LinkedIn search
        print("📊 LinkedIn Search:")
        linkedin_result = search_linkedin_jobs(keywords, 3, 0, location)
        linkedin_data = json.loads(linkedin_result)
        print(f"   Found {linkedin_data.get('total_results', 0)} LinkedIn jobs")
        
        # Test Muse search  
        if JOB_SEARCHER_AVAILABLE:
            print("🔍 Muse Search:")
            muse_result = await search_muse_jobs(keywords, location, 3)
            muse_data = json.loads(muse_result)
            print(f"   Found {muse_data.get('total_jobs', 0)} Muse jobs")
        
        # Test combined search
        print("🌐 Combined Search:")
        combined_result = await search_combined_jobs(keywords, location, 5)
        combined_data = json.loads(combined_result)
        print(f"   Found {combined_data.get('total_results', 0)} total jobs")
        print(f"   Sources: {', '.join(combined_data.get('sources_used', []))}")
    
    print("\n" + "=" * 50)
    print("✅ Testing complete!")

def main():
    """Main function to run the server."""
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Run tests
        asyncio.run(test_mcp_server())
    else:
        # Run the MCP server over HTTP
        port = 8081  # Changed from 8080 to avoid conflicts
        print("🚀 Starting Jobs MCP Server over HTTP...")
        print("Available tools:")
        print("  - search_linkedin_jobs")
        print("  - search_muse_jobs")
        print("  - search_combined_jobs")
        print("  - bb7_search_jobs (legacy)")
        print(f"🌐 Server will be available at: http://localhost:{port}/mcp")

        try:
            app.run(transport="http", port=port, host="localhost")
        except OSError as e:
            if "address already in use" in str(e).lower():
                print(f"\n❌ Error: Port {port} is already in use")
                print(f"💡 Try killing the process: lsof -ti:{port} | xargs kill -9")
                print(f"💡 Or use a different port by editing mcp_server.py")
            else:
                print(f"\n❌ Error starting server: {e}")
        except KeyboardInterrupt:
            print("\n👋 Server stopped")

if __name__ == "__main__":
    main()
