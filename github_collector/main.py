"""
Main Data Collection Pipeline
Orchestrates GitHub discovery, fetching, and web scraping
"""

import asyncio
import os
import sys
import yaml
from typing import List
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from collectors.github_discovery import GitHubRepoDiscovery
from collectors.github_fetcher import GitHubJobFetcher
# Apify for reliable web scraping (optional, requires API key)
try:
    from collectors.apify_scraper import ApifyJobScraper
    APIFY_AVAILABLE = True
except (ImportError, ValueError):
    APIFY_AVAILABLE = False

# Firecrawl for LLM-powered web scraping (optional, requires API key)
try:
    from collectors.firecrawl_scraper import FirecrawlJobScraper, load_search_keywords
    FIRECRAWL_AVAILABLE = True
except (ImportError, ValueError):
    FIRECRAWL_AVAILABLE = False
    def load_search_keywords(filepath=None):
        return ["machine learning new grad"]

from models.job import Job, JobCollection


class JobDataCollector:
    """
    Main orchestrator for collecting job postings from all sources
    """

    def __init__(self, config_path: str = None):
        # Default to parent directory's config.yaml
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config.yaml"
        
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # Load environment variables from parent directory
        env_path = Path(__file__).parent.parent / ".env"
        load_dotenv(env_path)
        self.github_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")

        # Initialize collectors
        self.github_discovery = GitHubRepoDiscovery(self.github_token)
        self.github_fetcher = GitHubJobFetcher(self.github_token)

        # Web scraping options (Firecrawl preferred, Apify fallback)
        self.firecrawl_enabled = False
        self.apify_enabled = False

        # Try Firecrawl first (faster, more accurate)
        if FIRECRAWL_AVAILABLE:
            try:
                self.firecrawl_scraper = FirecrawlJobScraper()
                self.firecrawl_enabled = True
                print("✅ Firecrawl scraper initialized (7 sec avg, 83% accuracy)")
            except ValueError as e:
                print(f"⚠️  Firecrawl not configured: {e}")

        # Try Apify as fallback
        if not self.firecrawl_enabled and APIFY_AVAILABLE:
            try:
                self.apify_scraper = ApifyJobScraper()
                self.apify_enabled = True
                print("✅ Apify scraper initialized")
            except ValueError as e:
                print(f"⚠️  Apify not configured: {e}")

        if not self.firecrawl_enabled and not self.apify_enabled:
            print("ℹ️  No web scrapers configured. GitHub alone provides 500+ jobs")

        self.all_jobs = []

    async def collect_from_github(self) -> List[Job]:
        """
        Step 1: Discover and fetch jobs from GitHub repositories
        """
        print("\n" + "=" * 70)
        print("📚 PHASE 1: COLLECTING FROM GITHUB REPOSITORIES")
        print("=" * 70)

        github_config = self.config['collection']['github']

        # Discover repositories
        sources = self.github_discovery.discover_all_sources(
            search_keywords=github_config['search_keywords'],
            min_stars=github_config['filters']['min_stars'],
            updated_within_days=github_config['filters']['updated_within_days']
        )

        if not sources:
            print("⚠️  No GitHub sources found. Skipping GitHub collection.")
            return []

        # Fetch jobs from each discovered source
        github_jobs = []
        for source in sources:
            jobs = self.github_fetcher.fetch_jobs_from_source(source)
            github_jobs.extend(jobs)

        print(f"\n✅ Total jobs from GitHub: {len(github_jobs)}")
        return github_jobs

    async def collect_from_web_scrapers(self) -> List[Job]:
        """
        Step 2: Collect jobs from web scrapers (Firecrawl or Apify)

        Priority order:
        1. Firecrawl (fastest, 7 sec avg, 83% accuracy)
        2. Apify (reliable, multiple sources)

        Firecrawl provides LLM-powered scraping for:
        - JobRight.ai
        - Simplify.jobs
        - Wellfound

        Apify provides reliable scraping for:
        - LinkedIn
        - Indeed
        - Wellfound

        Requires FIRECRAWL_API_KEY or APIFY_API_TOKEN in .env
        See FIRECRAWL_QUICKSTART.md or APIFY_QUICKSTART.md for setup.
        """
        print("\n" + "=" * 70)
        print("🔥 PHASE 2: WEB SCRAPING")
        print("=" * 70)

        # Try Firecrawl first
        if self.firecrawl_enabled:
            print("  🔥 Using Firecrawl (LLM-powered extraction)")
            try:
                # Load search keywords from parent directory
                search_keywords_path = Path(__file__).parent.parent / "search_keywords.txt"
                search_keywords = load_search_keywords(str(search_keywords_path))

                firecrawl_jobs = self.firecrawl_scraper.scrape_all(
                    search_queries=search_keywords,
                    max_jobs_per_query=30
                )
                return firecrawl_jobs

            except Exception as e:
                print(f"  ❌ Firecrawl error: {e}")
                print("  ℹ️  Falling back to Apify...")

        # Fallback to Apify
        if self.apify_enabled:
            print("  🔵 Using Apify (actor-based scraping)")
            try:
                apify_jobs = self.apify_scraper.scrape_all(
                    search_query="machine learning new grad 2026",
                    location="United States",
                    max_jobs_per_source=50
                )
                return apify_jobs

            except Exception as e:
                print(f"  ❌ Apify error: {e}")
                print("  ℹ️  Continuing with GitHub jobs only")
                return []

        # No scrapers configured
        print("  ⚠️  No web scrapers configured")
        print("  ℹ️  To enable:")
        print("     • Firecrawl: Add FIRECRAWL_API_KEY to .env (recommended)")
        print("     • Apify: Add APIFY_API_TOKEN to .env")
        print("  ℹ️  See FIRECRAWL_QUICKSTART.md or APIFY_QUICKSTART.md")
        print("  ℹ️  GitHub alone provides 500+ jobs (sufficient!)")
        return []

    def deduplicate_jobs(self, jobs: List[Job]) -> List[Job]:
        """
        Step 3: Remove duplicate jobs based on company + position
        """
        print("\n" + "=" * 70)
        print("🧹 PHASE 3: DEDUPLICATION")
        print("=" * 70)

        seen = set()
        unique_jobs = []

        for job in jobs:
            # Create unique key from company and position (normalized)
            key = (
                job.company.lower().strip(),
                job.position.lower().strip()
            )

            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)

        duplicates_removed = len(jobs) - len(unique_jobs)
        print(f"  📊 Original jobs: {len(jobs)}")
        print(f"  🗑️  Duplicates removed: {duplicates_removed}")
        print(f"  ✨ Unique jobs: {len(unique_jobs)}")

        return unique_jobs

    def save_to_json(self, jobs: List[Job], output_path: str = None):
        """
        Step 4: Save jobs to JSON file
        """
        print("\n" + "=" * 70)
        print("💾 PHASE 4: SAVING TO JSON")
        print("=" * 70)

        if output_path is None:
            # Default to parent directory's data folder
            output_path = Path(__file__).parent.parent / self.config['output']['file_path']
        
        output_path = Path(output_path)

        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Create job collection
        collection = JobCollection.from_job_list(jobs)

        # Save to file
        collection.to_json_file(
            filepath=str(output_path),
            pretty=self.config['output']['pretty_print']
        )

        print(f"  ✅ Saved {len(jobs)} jobs to {output_path}")
        print(f"  📁 File size: {output_path.stat().st_size / 1024:.2f} KB")

        # Print summary statistics
        self._print_summary(collection)

    def _print_summary(self, collection: JobCollection):
        """Print collection statistics"""
        print("\n" + "=" * 70)
        print("📊 COLLECTION SUMMARY")
        print("=" * 70)

        print(f"  Total Jobs: {collection.total_count}")
        print(f"  Collection Time: {collection.collection_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Sources: {len(collection.sources)}")

        # Count by source
        source_counts = {}
        for job in collection.jobs:
            source_counts[job.source] = source_counts.get(job.source, 0) + 1

        print("\n  Jobs by Source:")
        for source, count in sorted(source_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"    • {source}: {count}")

        # Count by location (top 5)
        location_counts = {}
        for job in collection.jobs:
            if job.location:
                location_counts[job.location] = location_counts.get(job.location, 0) + 1

        if location_counts:
            print("\n  Top 5 Locations:")
            for location, count in sorted(location_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"    • {location}: {count}")

        # Count jobs with salary info
        jobs_with_salary = sum(1 for job in collection.jobs if job.salary)
        print(f"\n  Jobs with Salary Info: {jobs_with_salary} ({jobs_with_salary/collection.total_count*100:.1f}%)")

        # Count by remote option
        remote_counts = {}
        for job in collection.jobs:
            remote_counts[job.remote_option.value] = remote_counts.get(job.remote_option.value, 0) + 1

        print("\n  Remote Work Options:")
        for option, count in sorted(remote_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"    • {option}: {count}")

    async def run(self):
        """
        Execute the complete data collection pipeline
        """
        print("\n" + "=" * 70)
        print("🚀 AUTOMATED JOB RETRIEVER - DATA COLLECTION PIPELINE")
        print("=" * 70)
        print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Phase 1: Collect from GitHub
        github_jobs = await self.collect_from_github()

        # Phase 2: Collect from web scrapers (Firecrawl or Apify)
        web_scraper_jobs = await self.collect_from_web_scrapers()

        # Combine all jobs
        all_jobs = github_jobs + web_scraper_jobs
        print(f"\n📦 Total jobs collected (before deduplication): {len(all_jobs)}")

        if not all_jobs:
            print("\n⚠️  No jobs collected. Please check your configuration and sources.")
            return

        # Phase 3: Deduplicate
        unique_jobs = self.deduplicate_jobs(all_jobs)

        # Apply max total jobs limit
        max_total = self.config['collection']['limits']['max_total_jobs']
        if len(unique_jobs) > max_total:
            print(f"\n✂️  Limiting to {max_total} jobs (configured maximum)")
            unique_jobs = unique_jobs[:max_total]

        # Phase 4: Save to JSON
        self.save_to_json(unique_jobs)

        print("\n" + "=" * 70)
        print("✅ DATA COLLECTION COMPLETE!")
        print("=" * 70)
        print(f"⏰ Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎉 Successfully collected {len(unique_jobs)} unique job postings!")


async def main():
    """Main entry point"""
    collector = JobDataCollector()
    await collector.run()


if __name__ == "__main__":
    asyncio.run(main())
