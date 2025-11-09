"""
GitHub Job Fetcher using REST API (fallback if MCP not available)
Can also be integrated with MCP GitHub server
"""

import requests
import re
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.job import Job, JobType, RemoteOption, CollectionMethod


class GitHubJobFetcher:
    """
    Fetch and parse job postings from GitHub markdown files
    """

    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token
        self.headers = {}
        if github_token:
            self.headers["Authorization"] = f"token {github_token}"

    def fetch_markdown_from_url(self, url: str) -> str:
        """
        Fetch markdown content from a URL

        Args:
            url: Raw markdown file URL (e.g., raw.githubusercontent.com)

        Returns:
            Markdown content as string
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching {url}: {e}")
            return ""

    def parse_markdown_table(
        self,
        markdown_content: str,
        source_name: str,
        field: str = "AI/ML"
    ) -> List[Job]:
        """
        Parse markdown table into Job objects

        Expected format:
        | Company | Position | Location | Salary | Link | Age |

        Args:
            markdown_content: Raw markdown text
            source_name: Name of the source repository
            field: Job field/domain

        Returns:
            List of Job objects
        """
        jobs = []

        # Split by lines and find table rows
        lines = markdown_content.split('\n')

        # Find tables by looking for pipe-separated rows
        in_table = False
        headers = []

        for line in lines:
            # Check if this is a table row
            if not line.strip().startswith('|'):
                in_table = False
                continue

            # Split by pipes
            cells = [cell.strip() for cell in line.split('|')[1:-1]]

            if not cells:
                continue

            # Check if this is a header row
            if not in_table and cells:
                # This might be a header
                headers = [h.lower().strip() for h in cells]
                in_table = True
                continue

            # Check if this is a separator row (---)
            if all('---' in cell or cell == '' for cell in cells):
                continue

            # This is a data row
            if in_table and len(cells) >= 3:
                try:
                    job = self._parse_table_row(cells, headers, source_name, field)
                    if job:
                        jobs.append(job)
                except Exception as e:
                    # Skip rows that can't be parsed
                    continue

        print(f"  📊 Parsed {len(jobs)} jobs from {source_name}")
        return jobs

    def _parse_table_row(
        self,
        cells: List[str],
        headers: List[str],
        source_name: str,
        field: str
    ) -> Optional[Job]:
        """
        Parse a single table row into a Job object

        Args:
            cells: Table cells
            headers: Table headers
            source_name: Source repository name
            field: Job field

        Returns:
            Job object or None if parsing fails
        """
        # Create a mapping of headers to cell values
        row_data = {}
        for i, header in enumerate(headers):
            if i < len(cells):
                row_data[header] = cells[i]

        # Extract company (clean HTML/markdown)
        company = self._clean_text(row_data.get('company', ''))
        if not company:
            return None

        # Extract position
        position = self._clean_text(row_data.get('position', ''))
        if not position:
            return None

        # Extract location
        location = self._clean_text(row_data.get('location', ''))

        # Extract salary
        salary = self._clean_text(row_data.get('salary', ''))

        # Extract application link
        apply_link = self._extract_url(row_data.get('posting', '') or row_data.get('link', ''))
        if not apply_link or not apply_link.startswith('http'):
            return None

        # Extract days since posted
        age_str = row_data.get('age', '') or row_data.get('posted', '')
        days_posted = self._parse_age(age_str)

        # Determine remote option from location
        remote_option = self._detect_remote_option(location)

        # Determine if it's for new grad
        job_type = JobType.NEW_GRAD if 'new grad' in position.lower() or 'new grad' in source_name.lower() else JobType.ENTRY_LEVEL

        # Create Job object
        job = Job(
            company=company,
            position=position,
            apply_link=apply_link,
            location=location if location else None,
            salary=salary if salary else None,
            job_type=job_type,
            remote_option=remote_option,
            days_since_posted=days_posted,
            source=source_name,
            collection_method=CollectionMethod.MCP_GITHUB,
            field=field
        )

        return job

    def _clean_text(self, text: str) -> str:
        """Remove HTML tags and markdown formatting"""
        if not text:
            return ""

        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)

        # Remove markdown bold (**text**)
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)

        # Remove markdown links [text](url)
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)

        # Remove extra whitespace
        text = ' '.join(text.split())

        return text.strip()

    def _extract_url(self, html_or_markdown: str) -> str:
        """Extract URL from HTML or markdown link"""
        if not html_or_markdown:
            return ""

        # Try to find href in HTML
        href_match = re.search(r'href=["\']([^"\']+)["\']', html_or_markdown)
        if href_match:
            return href_match.group(1)

        # Try markdown link format [text](url)
        md_match = re.search(r'\]\(([^)]+)\)', html_or_markdown)
        if md_match:
            return md_match.group(1)

        # If it's already a URL
        if html_or_markdown.startswith('http'):
            return html_or_markdown

        return ""

    def _parse_age(self, age_str: str) -> Optional[int]:
        """Parse age string like '6d' or '2 weeks' to days"""
        if not age_str:
            return None

        # Match patterns like '6d', '2w', '1m'
        match = re.search(r'(\d+)\s*([dwmy])', age_str.lower())
        if match:
            num = int(match.group(1))
            unit = match.group(2)

            if unit == 'd':
                return num
            elif unit == 'w':
                return num * 7
            elif unit == 'm':
                return num * 30
            elif unit == 'y':
                return num * 365

        return None

    def _detect_remote_option(self, location: str) -> RemoteOption:
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
        elif location_lower in ['anywhere', 'global', 'worldwide']:
            return RemoteOption.REMOTE
        else:
            return RemoteOption.ONSITE

    def fetch_jobs_from_source(self, source: Dict) -> List[Job]:
        """
        Fetch jobs from a discovered GitHub source

        Args:
            source: Source dictionary from GitHubRepoDiscovery

        Returns:
            List of Job objects
        """
        url = source.get('download_url')
        if not url:
            return []

        print(f"\n📥 Fetching jobs from {source['owner']}/{source['repo']}/{source['file_name']}...")

        markdown_content = self.fetch_markdown_from_url(url)
        if not markdown_content:
            return []

        source_name = f"{source['owner']}/{source['repo']}"
        jobs = self.parse_markdown_table(markdown_content, source_name)

        return jobs


# Example usage
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()

    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    fetcher = GitHubJobFetcher(token)

    # Example: Fetch from a known source
    test_source = {
        "owner": "speedyapply",
        "repo": "2026-AI-College-Jobs",
        "file_name": "NEW_GRAD_USA.md",
        "download_url": "https://raw.githubusercontent.com/speedyapply/2026-AI-College-Jobs/main/NEW_GRAD_USA.md"
    }

    jobs = fetcher.fetch_jobs_from_source(test_source)
    print(f"\n✅ Total jobs fetched: {len(jobs)}")

    # Print first 3 jobs as examples
    for i, job in enumerate(jobs[:3], 1):
        print(f"\n{i}. {job.company} - {job.position}")
        print(f"   Location: {job.location}")
        print(f"   Salary: {job.salary}")
        print(f"   Link: {job.apply_link}")
