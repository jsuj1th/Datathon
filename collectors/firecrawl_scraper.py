"""
Firecrawl-based job scraper
Fastest MCP scraper (7 seconds average, 83% accuracy)
"""

from typing import List, Optional, Dict
import os
import sys
import json

try:
    from firecrawl import FirecrawlApp
except ImportError:
    try:
        # Try alternative import
        from firecrawl.firecrawl import FirecrawlApp
    except ImportError:
        raise ImportError(
            "Firecrawl not installed. Install with: pip install firecrawl-py"
        )

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.job import Job, JobType, RemoteOption, CollectionMethod


def load_search_keywords(filepath: str = "search_keywords.txt") -> List[str]:
    """
    Load search keywords from a text file

    Args:
        filepath: Path to the keywords file

    Returns:
        List of search keywords (non-empty, non-comment lines)
    """
    keywords = []

    # Try project root first, then same directory as script
    if not os.path.isabs(filepath):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = os.path.join(project_root, filepath)

    if not os.path.exists(filepath):
        print(f"⚠️  Keywords file not found: {filepath}")
        print(f"   Using default keywords")
        return ["machine learning new grad", "artificial intelligence", "data science"]

    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith('#'):
                    keywords.append(line)

        print(f"✅ Loaded {len(keywords)} search keywords from {filepath}")
        return keywords
    except Exception as e:
        print(f"❌ Error loading keywords file: {e}")
        print(f"   Using default keywords")
        return ["machine learning new grad", "artificial intelligence", "data science"]


class FirecrawlJobScraper:
    """
    Job scraper using Firecrawl API
    Converts websites to LLM-ready markdown/structured data
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Firecrawl client

        Args:
            api_key: Firecrawl API key (or set FIRECRAWL_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("FIRECRAWL_API_KEY")

        if not self.api_key:
            raise ValueError(
                "Firecrawl API key required. Either:\n"
                "  1. Pass api_key parameter\n"
                "  2. Set FIRECRAWL_API_KEY environment variable\n"
                "Get your key from: https://www.firecrawl.dev/app/api-keys"
            )

        self.app = FirecrawlApp(api_key=self.api_key)

    def scrape_url(self, url: str) -> Dict:
        """
        Scrape a single URL and convert to markdown

        Args:
            url: URL to scrape

        Returns:
            Scraped data with markdown content
        """
        try:
            # Use v2 API: scrape() method
            result = self.app.scrape(url, formats=['markdown', 'html'])
            return result
        except Exception as e:
            print(f"   ❌ Error scraping {url}: {e}")
            return {}

    def extract_structured_data(self, url: str, schema: Dict, use_prompt: bool = False) -> Dict:
        """
        Extract structured data from URL using LLM

        Args:
            url: URL to scrape
            schema: JSON schema for extraction
            use_prompt: Whether to use prompt-based extraction instead of schema

        Returns:
            Extracted data matching the schema
        """
        try:
            if use_prompt:
                # Use prompt-based extraction for better results
                prompt = """
                Extract all job postings from this page. For each job, extract:
                - company: The company name
                - position: The job title/position
                - location: Where the job is located
                - salary: Salary information (if available)
                - url: The application or job posting URL

                Return a JSON object with a "jobs" array containing these job objects.
                """
                result = self.app.extract(
                    urls=[url],
                    prompt=prompt,
                    schema=schema,
                    timeout=90
                )
            else:
                # Use v2 API: extract() method with schema only
                result = self.app.extract(
                    urls=[url],
                    schema=schema,
                    timeout=60
                )

            # Return the data field from the result
            if hasattr(result, 'data'):
                return result.data
            elif isinstance(result, dict):
                return result.get('data', result)
            return result
        except Exception as e:
            print(f"   ❌ Error extracting from {url}: {e}")
            import traceback
            traceback.print_exc()
            return {}

    def scrape_jobright(
        self,
        search_query: str = "machine learning",
        max_jobs: int = 50
    ) -> List[Job]:
        """
        Scrape JobRight.ai using Firecrawl

        Args:
            search_query: Job search keywords
            max_jobs: Maximum number of jobs

        Returns:
            List of Job objects
        """
        print(f"\n🔥 Scraping JobRight.ai via Firecrawl...")
        print(f"   Query: {search_query}")

        jobs = []

        try:
            url = f"https://www.jobright.ai/jobs?q={search_query.replace(' ', '+')}"
            print(f"   📍 URL: {url}")

            # Define schema for job extraction
            job_schema = {
                "type": "object",
                "properties": {
                    "jobs": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "company": {"type": "string"},
                                "position": {"type": "string"},
                                "location": {"type": "string"},
                                "salary": {"type": "string"},
                                "url": {"type": "string"}
                            }
                        }
                    }
                }
            }

            print("   🚀 Extracting job data with LLM...")
            result = self.extract_structured_data(url, job_schema, use_prompt=True)

            # Parse results
            if result and 'jobs' in result:
                for item in result['jobs'][:max_jobs]:
                    try:
                        location = item.get('location', '')
                        remote = self._detect_remote(location)

                        job = Job(
                            company=item.get('company', '')[:200],
                            position=item.get('position', '')[:200],
                            apply_link=item.get('url', ''),
                            location=location[:200] if location else None,
                            salary=item.get('salary', '')[:100] if item.get('salary') else None,
                            job_type=JobType.NEW_GRAD,
                            remote_option=remote,
                            source="JobRight.ai (Firecrawl)",
                            collection_method=CollectionMethod.API,
                            field="AI/ML"
                        )
                        jobs.append(job)
                    except Exception as e:
                        continue

            print(f"   ✅ Collected {len(jobs)} jobs from JobRight.ai")

        except Exception as e:
            print(f"   ❌ Error: {e}")

        return jobs

    def scrape_simplify(self, max_jobs: int = 50) -> List[Job]:
        """
        Scrape Simplify.jobs using Firecrawl

        Args:
            max_jobs: Maximum number of jobs

        Returns:
            List of Job objects
        """
        print(f"\n🔥 Scraping Simplify.jobs via Firecrawl...")

        jobs = []

        try:
            url = "https://simplify.jobs/l/New-Grad-Data-Science-AI-ML"
            print(f"   📍 URL: {url}")

            job_schema = {
                "type": "object",
                "properties": {
                    "jobs": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "company": {"type": "string"},
                                "title": {"type": "string"},
                                "location": {"type": "string"},
                                "salary": {"type": "string"},
                                "link": {"type": "string"}
                            }
                        }
                    }
                }
            }

            print("   🚀 Extracting job data with LLM...")
            result = self.extract_structured_data(url, job_schema, use_prompt=True)

            if result and 'jobs' in result:
                for item in result['jobs'][:max_jobs]:
                    try:
                        location = item.get('location', '')
                        remote = self._detect_remote(location)

                        job = Job(
                            company=item.get('company', '')[:200],
                            position=item.get('title', '')[:200],
                            apply_link=item.get('link', ''),
                            location=location[:200] if location else None,
                            salary=item.get('salary', '')[:100] if item.get('salary') else None,
                            job_type=JobType.NEW_GRAD,
                            remote_option=remote,
                            source="Simplify.jobs (Firecrawl)",
                            collection_method=CollectionMethod.API,
                            field="AI/ML"
                        )
                        jobs.append(job)
                    except Exception as e:
                        continue

            print(f"   ✅ Collected {len(jobs)} jobs from Simplify.jobs")

        except Exception as e:
            print(f"   ❌ Error: {e}")

        return jobs

    def scrape_wellfound(
        self,
        search_query: str = "machine learning",
        max_jobs: int = 50
    ) -> List[Job]:
        """
        Scrape Wellfound using Firecrawl

        Args:
            search_query: Job search keywords
            max_jobs: Maximum number of jobs

        Returns:
            List of Job objects
        """
        print(f"\n🔥 Scraping Wellfound via Firecrawl...")
        print(f"   Query: {search_query}")

        jobs = []

        try:
            url = f"https://wellfound.com/jobs?search={search_query.replace(' ', '%20')}"
            print(f"   📍 URL: {url}")

            job_schema = {
                "type": "object",
                "properties": {
                    "jobs": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "company": {"type": "string"},
                                "role": {"type": "string"},
                                "location": {"type": "string"},
                                "salary": {"type": "string"},
                                "url": {"type": "string"}
                            }
                        }
                    }
                }
            }

            print("   🚀 Extracting job data with LLM...")
            result = self.extract_structured_data(url, job_schema, use_prompt=True)

            if result and 'jobs' in result:
                for item in result['jobs'][:max_jobs]:
                    try:
                        location = item.get('location', '')
                        remote = self._detect_remote(location)

                        job = Job(
                            company=item.get('company', '')[:200],
                            position=item.get('role', '')[:200],
                            apply_link=item.get('url', ''),
                            location=location[:200] if location else None,
                            salary=item.get('salary', '')[:100] if item.get('salary') else None,
                            job_type=JobType.NEW_GRAD,
                            remote_option=remote,
                            source="Wellfound (Firecrawl)",
                            collection_method=CollectionMethod.API,
                            field="AI/ML",
                            company_type="startup"
                        )
                        jobs.append(job)
                    except Exception as e:
                        continue

            print(f"   ✅ Collected {len(jobs)} jobs from Wellfound")

        except Exception as e:
            print(f"   ❌ Error: {e}")

        return jobs

    def scrape_all(
        self,
        search_queries: List[str] = None,
        max_jobs_per_query: int = 30
    ) -> List[Job]:
        """
        Scrape all job sites with multiple search queries

        Args:
            search_queries: List of search keywords to try
            max_jobs_per_query: Max jobs per query per site

        Returns:
            Combined list of jobs
        """
        if search_queries is None:
            search_queries = ["machine learning new grad"]

        print("=" * 70)
        print("🔥 FIRECRAWL JOB SCRAPING - ALL SOURCES")
        print("=" * 70)
        print(f"   Search Queries: {len(search_queries)}")
        for i, query in enumerate(search_queries, 1):
            print(f"   {i}. {query}")

        all_jobs = []
        jobright_total = 0
        simplify_total = 0
        wellfound_total = 0

        # Scrape each query
        for query_num, search_query in enumerate(search_queries, 1):
            print(f"\n{'='*70}")
            print(f"Query {query_num}/{len(search_queries)}: '{search_query}'")
            print(f"{'='*70}")

            # JobRight.ai
            jobright_jobs = self.scrape_jobright(search_query, max_jobs_per_query)
            all_jobs.extend(jobright_jobs)
            jobright_total += len(jobright_jobs)

            # Simplify.jobs (doesn't need search query - uses fixed URL)
            if query_num == 1:  # Only scrape Simplify once
                simplify_jobs = self.scrape_simplify(max_jobs_per_query * len(search_queries))
                all_jobs.extend(simplify_jobs)
                simplify_total = len(simplify_jobs)

            # Wellfound
            wellfound_jobs = self.scrape_wellfound(search_query, max_jobs_per_query)
            all_jobs.extend(wellfound_jobs)
            wellfound_total += len(wellfound_jobs)

        print(f"\n{'='*70}")
        print(f"📊 FINAL SUMMARY")
        print(f"{'='*70}")
        print(f"   JobRight.ai: {jobright_total} jobs")
        print(f"   Simplify.jobs: {simplify_total} jobs")
        print(f"   Wellfound: {wellfound_total} jobs")
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
    api_key = os.getenv("FIRECRAWL_API_KEY")

    if not api_key:
        print("=" * 70)
        print("⚠️  FIRECRAWL API KEY REQUIRED")
        print("=" * 70)
        print()
        print("To use Firecrawl:")
        print("1. Sign up at https://www.firecrawl.dev (free tier available)")
        print("2. Get API key from https://www.firecrawl.dev/app/api-keys")
        print("3. Add to .env file:")
        print("   FIRECRAWL_API_KEY=fc-your_key_here")
        print()
        print("Free tier includes:")
        print("  - 500 credits/month")
        print("  - Perfect for testing!")
        print()
        print("Advantages:")
        print("  ✅ Fastest MCP scraper (7 sec average)")
        print("  ✅ 83% accuracy rate")
        print("  ✅ LLM-powered extraction")
        print("  ✅ Handles JavaScript sites")
        exit(1)

    # Initialize scraper
    scraper = FirecrawlJobScraper(api_key)

    # Test scraping
    print("Testing Firecrawl scraper...")
    print()

    # JobRight.ai test
    jobs = scraper.scrape_jobright(
        search_query="machine learning",
        max_jobs=10
    )

    if jobs:
        print("\n📋 Sample Jobs:")
        for i, job in enumerate(jobs[:5], 1):
            print(f"\n{i}. {job.company}")
            print(f"   Position: {job.position}")
            print(f"   Location: {job.location}")
            print(f"   Source: {job.source}")
    else:
        print("\n⚠️  No jobs found. Trying a simpler scrape...")

        # Fallback: Try simple scrape
        url = "https://www.jobright.ai/jobs?q=machine+learning"
        result = scraper.scrape_url(url)

        if result:
            print(f"✅ Page scraped successfully!")
            # Handle both dict and object responses
            markdown = ""
            if hasattr(result, 'markdown'):
                markdown = result.markdown
            elif isinstance(result, dict):
                markdown = result.get('markdown', '')

            if markdown:
                print(f"   Content length: {len(markdown)} chars")
                print("\nFirst 500 characters:")
                print(markdown[:500])
            else:
                print(f"   Result type: {type(result)}")
                print(f"   Result keys: {dir(result) if hasattr(result, '__dir__') else result.keys() if isinstance(result, dict) else 'N/A'}")
