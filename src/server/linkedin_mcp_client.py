#!/usr/bin/env python3
"""
LinkedIn MCP Server
A Model Context Protocol server that provides LinkedIn job search and feed capabilities.
Based on adhikasp/mcp-linkedin implementation.
"""

from linkedin_api import Linkedin
from fastmcp import FastMCP
import os
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("mcp-linkedin")

def get_client() -> Linkedin:
    """Get LinkedIn API client with credentials from environment variables."""
    email = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")
    
    if not email or not password:
        raise ValueError("LinkedIn credentials not found. Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD environment variables.")
    
    return Linkedin(email, password, debug=True)

@mcp.tool()
def get_feed_posts(limit: int = 10, offset: int = 0) -> str:
    """
    Retrieve LinkedIn feed posts.
    
    :param limit: Maximum number of posts to retrieve (default: 10)
    :param offset: Number of posts to skip (default: 0)
    :return: Feed post details as formatted string
    """
    client = get_client()
    try:
        post_urns = client.get_feed_posts(limit=limit, offset=offset)
    except Exception as e:
        logger.error(f"Error retrieving feed posts: {e}")
        return f"Error retrieving feed posts: {e}"
    
    posts = ""
    for urn in post_urns:
        posts += f"Post by {urn['author_name']}: {urn['content']}\n\n"

    return posts

@mcp.tool()
def search_jobs(keywords: str, limit: int = 3, offset: int = 0, location: str = '') -> str:
    """
    Search for jobs on LinkedIn.
    
    :param keywords: Job search keywords
    :param limit: Maximum number of job results (default: 3)
    :param offset: Number of jobs to skip (default: 0)
    :param location: Optional location filter
    :return: Job details as formatted string
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
        return f"Error searching jobs: {e}"
    
    job_results = ""
    for job in jobs:
        try:
            job_id = job["entityUrn"].split(":")[-1]
            job_data = client.get_job(job_id=job_id)

            job_title = job_data.get("title", "N/A")
            company_data = job_data.get("companyDetails", {}).get("com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany", {})
            company_name = company_data.get("companyResolutionResult", {}).get("name", "N/A")
            job_description = job_data.get("description", {}).get("text", "N/A")
            job_location = job_data.get("formattedLocation", "N/A")
            
            job_results += f"Job: {job_title} at {company_name} in {job_location}\n"
            job_results += f"Description: {job_description[:500]}...\n\n"
            
        except Exception as e:
            logger.warning(f"Error processing job {job.get('entityUrn', 'unknown')}: {e}")
            continue

    return job_results if job_results else "No jobs found matching the criteria."

@mcp.tool()
def get_profile(public_id: Optional[str] = None) -> str:
    """
    Get LinkedIn profile information.
    
    :param public_id: Public ID of the profile (if None, gets own profile)
    :return: Profile information as formatted string
    """
    client = get_client()
    try:
        if public_id:
            profile = client.get_profile(public_id)
        else:
            # Get own profile
            profile = client.get_profile()
        
        # Extract key information
        first_name = profile.get('firstName', 'N/A')
        last_name = profile.get('lastName', 'N/A')
        headline = profile.get('headline', 'N/A')
        location = profile.get('geoLocationName', 'N/A')
        summary = profile.get('summary', 'N/A')
        
        profile_info = f"Name: {first_name} {last_name}\n"
        profile_info += f"Headline: {headline}\n"
        profile_info += f"Location: {location}\n"
        profile_info += f"Summary: {summary}\n"
        
        return profile_info
        
    except Exception as e:
        logger.error(f"Error retrieving profile: {e}")
        return f"Error retrieving profile: {e}"

if __name__ == "__main__":
    # Test the server
    print("Testing LinkedIn MCP Server...")
    try:
        # Test job search
        result = search_jobs(keywords="software engineer", location="San Francisco", limit=2)
        print("Job search result:")
        print(result)
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure to set LINKEDIN_EMAIL and LINKEDIN_PASSWORD environment variables.")
