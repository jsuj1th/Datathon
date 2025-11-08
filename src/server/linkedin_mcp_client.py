#!/usr/bin/env python3
"""
LinkedIn Jobs MCP Server
A Model Context Protocol server that provides LinkedIn job search functionality.
Returns structured job data in standardized JSON format.
"""

import fastmcp
from linkedin_api import Linkedin
import os
import sys
import logging
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = fastmcp.FastMCP("linkedin-jobs")

# Create output directory for saving job search results
OUTPUT_DIR = Path("job_search_results")
OUTPUT_DIR.mkdir(exist_ok=True)

def get_client() -> Linkedin:
    """Get LinkedIn API client with credentials from environment variables."""
    email = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")
    
    if not email or not password:
        raise ValueError("LinkedIn credentials not found. Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD environment variables.")
    
    return Linkedin(email, password, debug=True)

@mcp.tool
def search_jobs(keywords: str, limit: int = 10, offset: int = 0, location: str = '') -> str:
    """
    Search for jobs on LinkedIn and return structured JSON data.
    
    Args:
        keywords: Job search keywords (e.g., "software engineer", "data scientist")
        limit: Maximum number of job results (default: 10)
        offset: Number of jobs to skip (default: 0)
        location: Optional location filter (e.g., "San Francisco", "Remote")
        
    Returns:
        JSON string with structured job data
    """
    client = get_client()
    try:
        jobs = client.search_jobs(
            keywords=keywords,
            location_name=location,
            limit=limit,
            offset=offset,
        )
    except Exception as e:
        logger.error(f"Error searching jobs: {e}")
        return json.dumps({"error": f"Error searching jobs: {e}", "jobs": []})
    
    structured_jobs = []
    
    for job in jobs:
        try:
            # Extract basic job info
            job_id = job["entityUrn"].split(":")[-1] if "entityUrn" in job else None
            
            # Get detailed job information
            job_data = {}
            if job_id:
                try:
                    job_data = client.get_job(job_id=job_id)
                except Exception as e:
                    logger.warning(f"Could not get detailed job data for {job_id}: {e}")
            
            # Extract company information
            company_name = "N/A"
            if job_data and "companyDetails" in job_data:
                company_data = job_data.get("companyDetails", {}).get("com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany", {})
                company_name = company_data.get("companyResolutionResult", {}).get("name", "N/A")
            elif "companyName" in job:
                company_name = job["companyName"]
            
            # Extract job details
            job_title = job_data.get("title", job.get("title", "N/A"))
            job_location = job_data.get("formattedLocation", job.get("formattedLocation", location or "N/A"))
            job_description = job_data.get("description", {}).get("text", job.get("description", ""))
            
            # Create apply link
            apply_link = f"https://www.linkedin.com/jobs/view/{job_id}" if job_id else "N/A"
            
            # Determine job type and experience level
            job_type = "full_time"  # Default
            experience_level = None
            remote_option = "onsite"  # Default
            
            # Parse description for additional details
            if job_description:
                desc_lower = job_description.lower()
                
                # Determine job type
                if any(term in desc_lower for term in ["intern", "internship", "stage"]):
                    job_type = "internship"
                elif any(term in desc_lower for term in ["entry level", "new grad", "junior"]):
                    job_type = "entry_level"
                elif any(term in desc_lower for term in ["senior", "lead", "principal"]):
                    job_type = "senior_level"
                elif any(term in desc_lower for term in ["part time", "part-time"]):
                    job_type = "part_time"
                elif any(term in desc_lower for term in ["contract", "freelance"]):
                    job_type = "contract"
                
                # Determine remote option
                if any(term in desc_lower for term in ["remote", "work from home", "wfh"]):
                    remote_option = "remote"
                elif any(term in desc_lower for term in ["hybrid"]):
                    remote_option = "hybrid"
                
                # Extract experience level
                if "entry level" in desc_lower or "0-1 years" in desc_lower:
                    experience_level = "entry_level"
                elif any(term in desc_lower for term in ["1-3 years", "2-4 years"]):
                    experience_level = "junior"
                elif any(term in desc_lower for term in ["3-5 years", "4-6 years"]):
                    experience_level = "mid_level"
                elif any(term in desc_lower for term in ["5+ years", "senior"]):
                    experience_level = "senior"
            
            # Calculate days since posted (LinkedIn doesn't provide exact dates, so we'll estimate)
            days_since_posted = None
            if job.get("listedAt"):
                try:
                    listed_timestamp = job["listedAt"] / 1000  # Convert from milliseconds
                    listed_date = datetime.fromtimestamp(listed_timestamp)
                    days_since_posted = (datetime.now() - listed_date).days
                except:
                    days_since_posted = None
            
            # Create structured job object
            structured_job = {
                "company": company_name,
                "position": job_title,
                "apply_link": apply_link,
                "location": job_location,
                "salary": None,  # LinkedIn API doesn't typically provide salary
                "description": job_description[:1000] if job_description else None,  # Truncate for size
                "requirements": None,  # Could extract from description if needed
                "benefits": None,  # Could extract from description if needed
                "job_type": job_type,
                "experience_level": experience_level,
                "posted_date": None,  # LinkedIn doesn't provide exact posting date
                "deadline": None,  # LinkedIn doesn't provide application deadline
                "days_since_posted": days_since_posted,
                "remote_option": remote_option,
                "visa_sponsorship": None,  # Would need to parse from description
                "source": "linkedin",
                "collection_method": "mcp_linkedin",
                "collected_at": datetime.now().isoformat(),
                "field": None,  # Could categorize based on keywords
                "company_type": None  # Could extract from company data
            }
            
            structured_jobs.append(structured_job)
            
        except Exception as e:
            logger.warning(f"Error processing job {job.get('entityUrn', 'unknown')}: {e}")
            continue
    
    result = {
        "jobs": structured_jobs,
        "total_found": len(structured_jobs),
        "search_params": {
            "keywords": keywords,
            "location": location,
            "limit": limit,
            "offset": offset
        }
    }
    
    # Save results to JSON file with descriptive filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_keywords = "".join(c for c in keywords if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_keywords = safe_keywords.replace(' ', '_')
    safe_location = location.replace(' ', '_').replace(',', '') if location else 'any_location'
    
    filename = f"jobs_{safe_keywords}_{safe_location}_{timestamp}.json"
    output_file = OUTPUT_DIR / filename
    
    try:
        with open(output_file, "w", encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        logger.info(f"Job search results saved to: {output_file}")
        
        # Also save as latest results for easy access
        latest_file = OUTPUT_DIR / "latest_job_search.json"
        with open(latest_file, "w", encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        logger.info(f"Latest results also saved to: {latest_file}")
        
    except Exception as e:
        logger.error(f"Failed to save job search results: {e}")
    
    return json.dumps(result, indent=2)

# Raw function for direct testing
def raw_search_jobs(keywords: str, limit: int = 10, offset: int = 0, location: str = '') -> Dict[str, Any]:
    """Raw job search function without MCP decorator for testing."""
    client = get_client()
    try:
        jobs = client.search_jobs(
            keywords=keywords,
            location_name=location,
            limit=limit,
            offset=offset,
        )
    except Exception as e:
        logger.error(f"Error searching jobs: {e}")
        return {"error": f"Error searching jobs: {e}", "jobs": []}
    
    structured_jobs = []
    
    for job in jobs:
        try:
            job_id = job["entityUrn"].split(":")[-1] if "entityUrn" in job else None
            
            # Get detailed job information
            job_data = {}
            if job_id:
                try:
                    job_data = client.get_job(job_id=job_id)
                except Exception as e:
                    logger.warning(f"Could not get detailed job data for {job_id}: {e}")
            
            # Extract company information
            company_name = "N/A"
            if job_data and "companyDetails" in job_data:
                company_data = job_data.get("companyDetails", {}).get("com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany", {})
                company_name = company_data.get("companyResolutionResult", {}).get("name", "N/A")
            elif "companyName" in job:
                company_name = job["companyName"]
            
            # Extract job details
            job_title = job_data.get("title", job.get("title", "N/A"))
            job_location = job_data.get("formattedLocation", job.get("formattedLocation", location or "N/A"))
            job_description = job_data.get("description", {}).get("text", job.get("description", ""))
            
            # Create apply link
            apply_link = f"https://www.linkedin.com/jobs/view/{job_id}" if job_id else "N/A"
            
            # Create structured job object
            structured_job = {
                "company": company_name,
                "position": job_title,
                "apply_link": apply_link,
                "location": job_location,
                "salary": None,
                "description": job_description[:1000] if job_description else None,
                "requirements": None,
                "benefits": None,
                "job_type": "full_time",
                "experience_level": None,
                "posted_date": None,
                "deadline": None,
                "days_since_posted": None,
                "remote_option": "onsite",
                "visa_sponsorship": None,
                "source": "linkedin",
                "collection_method": "mcp_linkedin",
                "collected_at": datetime.now().isoformat(),
                "field": None,
                "company_type": None
            }
            
            structured_jobs.append(structured_job)
            
        except Exception as e:
            logger.warning(f"Error processing job: {e}")
            continue
    
    result = {
        "jobs": structured_jobs,
        "total_found": len(structured_jobs),
        "search_params": {
            "keywords": keywords,
            "location": location,
            "limit": limit,
            "offset": offset
        }
    }
    
    # Save results to JSON file with descriptive filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_keywords = "".join(c for c in keywords if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_keywords = safe_keywords.replace(' ', '_')
    safe_location = location.replace(' ', '_').replace(',', '') if location else 'any_location'
    
    filename = f"jobs_{safe_keywords}_{safe_location}_{timestamp}.json"
    output_file = OUTPUT_DIR / filename
    
    try:
        with open(output_file, "w", encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        logger.info(f"Job search results saved to: {output_file}")
        
        # Also save as latest results for easy access
        latest_file = OUTPUT_DIR / "latest_job_search.json"
        with open(latest_file, "w", encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        logger.info(f"Latest results also saved to: {latest_file}")
        
    except Exception as e:
        logger.error(f"Failed to save job search results: {e}")
    
    return result

# Test function for direct calling
def test_search_jobs(keywords: str = "software engineer", location: str = "San Francisco", limit: int = 3) -> Dict[str, Any]:
    """Test function for job search."""
    return raw_search_jobs(keywords, limit, 0, location)

if __name__ == "__main__":
    # When run as a module for GitHub Copilot MCP HTTP server
    import asyncio
    
    async def run_mcp_http_server():
        """Run the MCP server as HTTP server for GitHub Copilot"""
        try:
            # Use FastMCP's built-in HTTP server
            await mcp.run_http_async(
                host="0.0.0.0",
                port=8000,
                transport="http"
            )
        except KeyboardInterrupt:
            print("\nMCP HTTP server stopped.")
        except Exception as e:
            print(f"Error running MCP HTTP server: {e}")
    
    # Check if we have credentials
    email = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")
    
    if not email or not password:
        print("Error: LinkedIn credentials not found!")
        print("Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD environment variables.")
        sys.exit(1)
    
    print("Starting LinkedIn Jobs MCP HTTP Server...")
    print(f"Authenticated as: {email[:5]}...@{email.split('@')[1] if '@' in email else 'unknown'}")
    print("Server will be available at: http://localhost:8000")
    
    # Run the MCP HTTP server
    asyncio.run(run_mcp_http_server())
