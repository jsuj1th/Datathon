"""
Apify-based job scraper using Apify Actors
Much more reliable than manual scraping
"""

from typing import List, Optional
import os
from apify_client import ApifyClient
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.job import Job, JobType, RemoteOption, CollectionMethod


class ApifyJobScraper:
    """
    Job scraper using Apify Actors
    """

    # Actor IDs for different job sites
    ACTORS = {
        "linkedin": "curious_coder/linkedin-jobs-search-scraper",
        "indeed": "curious_coder/indeed-scraper",
        "wellfound": "radeance/wellfound-job-listings-scraper",
        "multi": "nextapi/job-search-engines"  # LinkedIn + Indeed + Glassdoor
    }

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Apify client

        Args:
            api_key: Apify API key (or set APIFY_API_TOKEN env var)
        """
        self.api_key = api_key or os.getenv("APIFY_API_TOKEN")

        if not self.api_key:
            raise ValueError(
                "Apify API key required. Either:\n"
                "  1. Pass api_key parameter\n"
                "  2. Set APIFY_API_TOKEN environment variable\n"
                "Get your key from: https://console.apify.com/account/integrations"
            )

        self.client = ApifyClient(self.api_key)

    def scrape_linkedin(
        self,
        search_query: str = "machine learning new grad",
        location: str = "United States",
        max_jobs: int = 100
    ) -> List[Job]:
        """
        Scrape jobs from LinkedIn using Apify

        Args:
            search_query: Job search keywords
            location: Job location
            max_jobs: Maximum number of jobs to collect

        Returns:
            List of Job objects
        """
        print(f"\n🔵 Scraping LinkedIn via Apify...")
        print(f"   Query: {search_query}")
        print(f"   Location: {location}")

        try:
            # Run LinkedIn Jobs Scraper
            run_input = {
                "queries": f"{search_query} {location}",
                "maxItems": max_jobs,
                "proxy": {
                    "useApifyProxy": True
                }
            }

            print("   🚀 Starting Apify actor...")
            run = self.client.actor(self.ACTORS["linkedin"]).call(run_input=run_input)

            # Get results
            jobs = []
            print("   📥 Fetching results...")

            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                try:
                    job = Job(
                        company=item.get("companyName", "")[:200],
                        position=item.get("title", "")[:200],
                        apply_link=item.get("link", item.get("url", "")),
                        location=item.get("location", "")[:200] if item.get("location") else None,
                        salary=item.get("salary", "")[:100] if item.get("salary") else None,
                        description=item.get("description", "")[:500] if item.get("description") else None,
                        job_type=JobType.NEW_GRAD,
                        remote_option=self._detect_remote(item.get("location", "")),
                        source="LinkedIn (Apify)",
                        collection_method=CollectionMethod.API,
                        field="AI/ML"
                    )
                    jobs.append(job)
                except Exception as e:
                    continue

            print(f"   ✅ Collected {len(jobs)} jobs from LinkedIn")
            return jobs

        except Exception as e:
            print(f"   ❌ Error: {e}")
            return []

    def scrape_indeed(
        self,
        search_query: str = "machine learning new grad",
        location: str = "United States",
        max_jobs: int = 100
    ) -> List[Job]:
        """
        Scrape jobs from Indeed using Apify

        Args:
            search_query: Job search keywords
            location: Job location
            max_jobs: Maximum number of jobs to collect

        Returns:
            List of Job objects
        """
        print(f"\n🔵 Scraping Indeed via Apify...")
        print(f"   Query: {search_query}")

        try:
            run_input = {
                "position": search_query,
                "location": location,
                "maxItems": max_jobs,
                "parseCompanyDetails": False,
                "saveOnlyUniqueItems": True,
                "proxy": {
                    "useApifyProxy": True
                }
            }

            print("   🚀 Starting Apify actor...")
            run = self.client.actor(self.ACTORS["indeed"]).call(run_input=run_input)

            jobs = []
            print("   📥 Fetching results...")

            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                try:
                    job = Job(
                        company=item.get("company", "")[:200],
                        position=item.get("positionName", item.get("title", ""))[:200],
                        apply_link=item.get("url", ""),
                        location=item.get("location", "")[:200] if item.get("location") else None,
                        salary=item.get("salary", "")[:100] if item.get("salary") else None,
                        description=item.get("description", "")[:500] if item.get("description") else None,
                        job_type=JobType.NEW_GRAD,
                        remote_option=self._detect_remote(item.get("location", "")),
                        source="Indeed (Apify)",
                        collection_method=CollectionMethod.API,
                        field="AI/ML"
                    )
                    jobs.append(job)
                except Exception as e:
                    continue

            print(f"   ✅ Collected {len(jobs)} jobs from Indeed")
            return jobs

        except Exception as e:
            print(f"   ❌ Error: {e}")
            return []

    def scrape_wellfound(
        self,
        search_query: str = "machine learning",
        max_jobs: int = 100
    ) -> List[Job]:
        """
        Scrape startup jobs from Wellfound using Apify

        Args:
            search_query: Job search keywords
            max_jobs: Maximum number of jobs to collect

        Returns:
            List of Job objects
        """
        print(f"\n🔵 Scraping Wellfound via Apify...")
        print(f"   Query: {search_query}")

        try:
            run_input = {
                "search": search_query,
                "maxItems": max_jobs,
                "proxy": {
                    "useApifyProxy": True
                }
            }

            print("   🚀 Starting Apify actor...")
            run = self.client.actor(self.ACTORS["wellfound"]).call(run_input=run_input)

            jobs = []
            print("   📥 Fetching results...")

            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                try:
                    job = Job(
                        company=item.get("companyName", item.get("company", ""))[:200],
                        position=item.get("title", item.get("role", ""))[:200],
                        apply_link=item.get("jobUrl", item.get("url", "")),
                        location=item.get("location", "")[:200] if item.get("location") else None,
                        salary=item.get("compensation", item.get("salary", ""))[:100] if item.get("compensation") or item.get("salary") else None,
                        description=item.get("description", "")[:500] if item.get("description") else None,
                        job_type=JobType.NEW_GRAD,
                        remote_option=self._detect_remote(item.get("location", "")),
                        source="Wellfound (Apify)",
                        collection_method=CollectionMethod.API,
                        field="AI/ML",
                        company_type="startup"
                    )
                    jobs.append(job)
                except Exception as e:
                    continue

            print(f"   ✅ Collected {len(jobs)} jobs from Wellfound")
            return jobs

        except Exception as e:
            print(f"   ❌ Error: {e}")
            return []

    def scrape_multi_platform(
        self,
        search_query: str = "machine learning new grad",
        location: str = "United States",
        max_jobs: int = 100
    ) -> List[Job]:
        """
        Scrape from multiple platforms (LinkedIn + Indeed + Glassdoor) simultaneously

        Args:
            search_query: Job search keywords
            location: Job location
            max_jobs: Maximum number of jobs per platform

        Returns:
            List of Job objects
        """
        print(f"\n🔵 Scraping Multiple Platforms via Apify...")
        print(f"   Query: {search_query}")
        print(f"   Platforms: LinkedIn, Indeed, Glassdoor")

        try:
            run_input = {
                "search": search_query,
                "location": location,
                "maxResults": max_jobs,
                "platforms": ["linkedin", "indeed", "glassdoor"]
            }

            print("   🚀 Starting Apify actor...")
            run = self.client.actor(self.ACTORS["multi"]).call(run_input=run_input)

            jobs = []
            print("   📥 Fetching results...")

            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                try:
                    source_platform = item.get("source", item.get("platform", "Unknown"))

                    job = Job(
                        company=item.get("company", item.get("companyName", ""))[:200],
                        position=item.get("title", item.get("jobTitle", ""))[:200],
                        apply_link=item.get("url", item.get("link", "")),
                        location=item.get("location", "")[:200] if item.get("location") else None,
                        salary=item.get("salary", "")[:100] if item.get("salary") else None,
                        description=item.get("description", "")[:500] if item.get("description") else None,
                        job_type=JobType.NEW_GRAD,
                        remote_option=self._detect_remote(item.get("location", "")),
                        source=f"{source_platform} (Apify Multi)",
                        collection_method=CollectionMethod.API,
                        field="AI/ML"
                    )
                    jobs.append(job)
                except Exception as e:
                    continue

            print(f"   ✅ Collected {len(jobs)} jobs from multiple platforms")
            return jobs

        except Exception as e:
            print(f"   ❌ Error: {e}")
            return []

    def scrape_all(
        self,
        search_query: str = "machine learning new grad 2026",
        location: str = "United States",
        max_jobs_per_source: int = 50
    ) -> List[Job]:
        """
        Scrape from all available sources

        Args:
            search_query: Job search keywords
            location: Job location
            max_jobs_per_source: Max jobs per source

        Returns:
            Combined list of Job objects
        """
        print("=" * 70)
        print("🚀 APIFY JOB SCRAPING - ALL SOURCES")
        print("=" * 70)

        all_jobs = []

        # LinkedIn
        linkedin_jobs = self.scrape_linkedin(search_query, location, max_jobs_per_source)
        all_jobs.extend(linkedin_jobs)

        # Indeed
        indeed_jobs = self.scrape_indeed(search_query, location, max_jobs_per_source)
        all_jobs.extend(indeed_jobs)

        # Wellfound
        wellfound_jobs = self.scrape_wellfound(search_query.replace(" new grad", ""), max_jobs_per_source)
        all_jobs.extend(wellfound_jobs)

        print(f"\n📊 Summary:")
        print(f"   LinkedIn: {len(linkedin_jobs)} jobs")
        print(f"   Indeed: {len(indeed_jobs)} jobs")
        print(f"   Wellfound: {len(wellfound_jobs)} jobs")
        print(f"   TOTAL: {len(all_jobs)} jobs")

        return all_jobs

    def _detect_remote(self, location: str) -> RemoteOption:
        """Detect remote work option from location string"""
        if not location:
            return RemoteOption.UNKNOWN

        location_lower = location.lower()

        if 'remote' in location_lower:
            if 'hybrid' in location_lower:
                return RemoteOption.HYBRID
            return RemoteOption.REMOTE
        elif 'hybrid' in location_lower:
            return RemoteOption.HYBRID
        else:
            return RemoteOption.ONSITE


# Example usage
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()

    # Check for API key
    api_key = os.getenv("APIFY_API_TOKEN")

    if not api_key:
        print("=" * 70)
        print("⚠️  APIFY API KEY REQUIRED")
        print("=" * 70)
        print()
        print("To use Apify scrapers:")
        print("1. Sign up at https://apify.com (free tier available)")
        print("2. Get API token from https://console.apify.com/account/integrations")
        print("3. Add to .env file:")
        print("   APIFY_API_TOKEN=your_token_here")
        print()
        print("Free tier includes:")
        print("  - $5 monthly credit")
        print("  - ~50-100 jobs can be scraped")
        print("  - Perfect for testing!")
        exit(1)

    # Initialize scraper
    scraper = ApifyJobScraper(api_key)

    # Test scraping
    print("Testing Apify scrapers...")
    print()

    # LinkedIn test (smaller batch)
    jobs = scraper.scrape_linkedin(
        search_query="machine learning new grad 2026",
        location="United States",
        max_jobs=20
    )

    if jobs:
        print("\n📋 Sample Jobs:")
        for i, job in enumerate(jobs[:5], 1):
            print(f"\n{i}. {job.company}")
            print(f"   Position: {job.position}")
            print(f"   Location: {job.location}")
            print(f"   Source: {job.source}")
