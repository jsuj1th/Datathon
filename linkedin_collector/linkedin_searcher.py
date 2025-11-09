#!/usr/bin/env python3
"""
Real LinkedIn Job Searcher
Uses linkedin-api to fetch REAL LinkedIn job postings
"""

import os
import logging
from typing import List, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import linkedin-api
try:
    from linkedin_api import Linkedin
    LINKEDIN_AVAILABLE = True
except ImportError:
    LINKEDIN_AVAILABLE = False
    logger.warning("linkedin-api not available. Install with: pip install linkedin-api")


class LinkedInJobSearcher:
    """Search for REAL jobs on LinkedIn using linkedin-api"""

    def __init__(self):
        self.api = None
        if LINKEDIN_AVAILABLE:
            try:
                email = os.getenv('LINKEDIN_EMAIL')
                password = os.getenv('LINKEDIN_PASSWORD')

                if email and password:
                    self.api = Linkedin(email, password)
                    logger.info("LinkedIn API initialized successfully")
                else:
                    logger.warning("LinkedIn credentials not found in .env file")
            except Exception as e:
                logger.error(f"Failed to initialize LinkedIn API: {e}")
                self.api = None

    def search_jobs(self, keywords: str, location: str = "", limit: int = 25) -> List[Dict[str, Any]]:
        """
        Search for REAL jobs on LinkedIn.

        Args:
            keywords: Job search keywords
            location: Location filter
            limit: Maximum number of jobs to return

        Returns:
            List of job dictionaries
        """
        if not self.api:
            logger.warning("LinkedIn API not initialized")
            return []

        try:
            logger.info(f"Searching LinkedIn for: {keywords} in {location}")

            # Search for jobs using linkedin-api
            jobs_raw = self.api.search_jobs(
                keywords=keywords,
                location_name=location if location else None,
                limit=limit
            )

            jobs = []
            for job_data in jobs_raw[:limit]:
                try:
                    # Extract job ID
                    job_id = job_data.get('trackingUrn', '').split(':')[-1]
                    if not job_id:
                        job_id = str(job_data.get('entityUrn', '')).split(':')[-1]

                    # Get full job details to get company info
                    try:
                        job_details = self.api.get_job(job_id)
                        company_name = job_details.get('companyDetails', {}).get('com.linkedin.voyager.deco.jobs.web.shared.WebCompactJobPostingCompany', {}).get('companyResolutionResult', {}).get('name', 'Unknown Company')
                        description = job_details.get('description', {}).get('text', 'No description available')
                        location_data = job_details.get('formattedLocation', '')
                    except:
                        # Fallback if detailed fetch fails
                        company_name = job_data.get('companyName', 'Unknown Company')
                        description = 'No description available'
                        location_data = ''

                    # Get job title
                    title = job_data.get('title', 'Unknown Title')

                    # Get location
                    location_str = location_data if location_data else job_data.get('formattedLocation', '')
                    if not location_str:
                        location_str = "Location not specified"

                    # Determine if remote
                    remote_option = "remote" if "remote" in location_str.lower() else "onsite"

                    # Get posting date (listed time ago)
                    listed_at = job_data.get('listedAt', 0)
                    if listed_at:
                        listed_date = datetime.fromtimestamp(listed_at / 1000).strftime('%Y-%m-%d')
                        days_ago = (datetime.now() - datetime.fromtimestamp(listed_at / 1000)).days
                    else:
                        listed_date = None
                        days_ago = None

                    # Construct LinkedIn job URL
                    apply_link = f"https://www.linkedin.com/jobs/view/{job_id}"

                    # Format job for our standard schema
                    formatted_job = {
                        "company": company_name,
                        "position": title,
                        "apply_link": apply_link,
                        "location": location_str,
                        "salary": None,  # LinkedIn API doesn't provide salary in search results
                        "description": description,
                        "requirements": None,
                        "benefits": None,
                        "job_type": "full_time",  # Default assumption
                        "experience_level": None,
                        "posted_date": listed_date,
                        "deadline": None,
                        "days_since_posted": days_ago,
                        "remote_option": remote_option,
                        "visa_sponsorship": None,
                        "source": f"linkedin/{job_id}",
                        "collection_method": "linkedin_api",
                        "collected_at": datetime.now().isoformat(),
                        "field": self._determine_field(keywords),
                        "company_type": "enterprise"  # Default
                    }

                    jobs.append(formatted_job)

                except Exception as e:
                    logger.warning(f"Failed to process job: {e}")
                    continue

            logger.info(f"Found {len(jobs)} jobs on LinkedIn")
            return jobs

        except Exception as e:
            logger.error(f"LinkedIn job search failed: {e}")
            return []

    def _determine_field(self, keywords: str) -> str:
        """Determine the field based on keywords."""
        keywords_lower = keywords.lower()

        if any(term in keywords_lower for term in ["data scientist", "machine learning", "ai", "artificial intelligence"]):
            return "AI/ML"
        elif any(term in keywords_lower for term in ["software engineer", "developer", "programmer", "backend", "frontend"]):
            return "Software Engineering"
        elif any(term in keywords_lower for term in ["data engineer", "data analyst", "analytics"]):
            return "Data Engineering"
        else:
            return "Technology"


# Test function
async def test_linkedin_search():
    """Test the LinkedIn job searcher."""
    print("🔍 Testing LinkedIn Job Searcher")
    print("=" * 50)

    searcher = LinkedInJobSearcher()

    if not searcher.api:
        print("❌ LinkedIn API not initialized")
        print("💡 Make sure LINKEDIN_EMAIL and LINKEDIN_PASSWORD are set in .env")
        return

    # Test search
    keywords = "software engineer"
    location = "San Francisco"

    print(f"\n🔍 Searching: '{keywords}' in '{location}'")
    print("-" * 40)

    jobs = searcher.search_jobs(keywords, location, limit=5)

    if jobs:
        print(f"✅ Found {len(jobs)} LinkedIn jobs!")
        for i, job in enumerate(jobs, 1):
            print(f"\n{i}. {job['position']} at {job['company']}")
            print(f"   📍 {job['location']}")
            print(f"   🔗 {job['apply_link']}")
            if job.get('days_since_posted'):
                print(f"   📅 Posted {job['days_since_posted']} days ago")
    else:
        print("❌ No jobs found")

    print("\n" + "=" * 50)
    print("Testing complete!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_linkedin_search())
