"""
GitHub Repository Discovery
Dynamically searches for job posting repositories on GitHub
"""

import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import time


class GitHubRepoDiscovery:
    """
    Discover job posting repositories on GitHub using search API
    """

    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        if github_token:
            self.headers["Authorization"] = f"token {github_token}"

    def search_job_repositories(
        self,
        keywords: List[str],
        min_stars: int = 50,
        updated_within_days: int = 30
    ) -> List[Dict]:
        """
        Search for job posting repositories on GitHub

        Args:
            keywords: Search keywords (e.g., ["2026 new grad jobs"])
            min_stars: Minimum stars required
            updated_within_days: Only repos updated within this timeframe

        Returns:
            List of repository information
        """
        all_repos = []

        for keyword in keywords:
            print(f"🔍 Searching GitHub for: '{keyword}'")

            # Calculate date threshold
            date_threshold = datetime.now() - timedelta(days=updated_within_days)
            date_str = date_threshold.strftime("%Y-%m-%d")

            # Build search query
            query = f"{keyword} stars:>={min_stars} pushed:>={date_str}"

            # Search repositories
            search_url = f"{self.base_url}/search/repositories"
            params = {
                "q": query,
                "sort": "updated",
                "order": "desc",
                "per_page": 10
            }

            try:
                response = requests.get(search_url, headers=self.headers, params=params)
                response.raise_for_status()
                data = response.json()

                repos = data.get("items", [])
                print(f"  ✅ Found {len(repos)} repositories")

                for repo in repos:
                    repo_info = {
                        "owner": repo["owner"]["login"],
                        "name": repo["name"],
                        "full_name": repo["full_name"],
                        "description": repo.get("description", ""),
                        "stars": repo["stargazers_count"],
                        "url": repo["html_url"],
                        "updated_at": repo["updated_at"],
                        "default_branch": repo["default_branch"]
                    }
                    all_repos.append(repo_info)

                # Rate limiting courtesy delay
                time.sleep(1)

            except requests.exceptions.RequestException as e:
                print(f"  ❌ Error searching for '{keyword}': {e}")
                continue

        # Remove duplicates
        unique_repos = {repo["full_name"]: repo for repo in all_repos}
        result = list(unique_repos.values())

        print(f"\n📦 Total unique repositories found: {len(result)}")
        return result

    def find_job_files(self, owner: str, repo: str, branch: str = "main") -> List[Dict]:
        """
        Find potential job posting files in a repository

        Args:
            owner: Repository owner
            repo: Repository name
            branch: Branch to search (default: main)

        Returns:
            List of file information
        """
        # Common patterns for job posting files
        patterns = [
            "README.md",
            "NEW_GRAD",
            "NEWGRAD",
            "JOBS",
            "INTERNSHIP",
            "POSITIONS"
        ]

        job_files = []

        # Get repository contents
        contents_url = f"{self.base_url}/repos/{owner}/{repo}/contents"

        try:
            response = requests.get(contents_url, headers=self.headers)
            response.raise_for_status()
            contents = response.json()

            # Filter files matching patterns
            for item in contents:
                if item["type"] == "file":
                    file_name = item["name"].upper()

                    # Check if filename matches any pattern
                    if any(pattern in file_name for pattern in patterns):
                        job_files.append({
                            "name": item["name"],
                            "path": item["path"],
                            "download_url": item["download_url"],
                            "size": item["size"]
                        })

            if job_files:
                print(f"  📄 Found {len(job_files)} potential job files in {owner}/{repo}")

        except requests.exceptions.RequestException as e:
            print(f"  ⚠️  Could not access {owner}/{repo}: {e}")

        return job_files

    def discover_all_sources(
        self,
        search_keywords: List[str],
        min_stars: int = 50,
        updated_within_days: int = 30
    ) -> List[Dict]:
        """
        Complete discovery pipeline: search repos and find job files

        Returns:
            List of discovered sources with file information
        """
        print("=" * 60)
        print("🚀 Starting GitHub Job Repository Discovery")
        print("=" * 60)

        # Step 1: Search for repositories
        repos = self.search_job_repositories(search_keywords, min_stars, updated_within_days)

        # Step 2: Find job files in each repository
        sources = []
        for repo in repos:
            owner = repo["owner"]
            name = repo["name"]
            branch = repo["default_branch"]

            print(f"\n🔎 Analyzing {repo['full_name']}...")

            # Try to find job files
            job_files = self.find_job_files(owner, name, branch)

            if job_files:
                for file_info in job_files:
                    sources.append({
                        "owner": owner,
                        "repo": name,
                        "file_path": file_info["path"],
                        "file_name": file_info["name"],
                        "download_url": file_info["download_url"],
                        "repo_stars": repo["stars"],
                        "repo_description": repo["description"],
                        "repo_url": repo["url"]
                    })

            # Rate limiting courtesy delay
            time.sleep(1)

        print("\n" + "=" * 60)
        print(f"✨ Discovery Complete: {len(sources)} job sources found")
        print("=" * 60)

        return sources


# Example usage
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()

    token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    discoverer = GitHubRepoDiscovery(token)

    # Search keywords from config
    keywords = [
        "2026 new grad jobs",
        "2026 AI ML jobs",
        "2026 software engineer new grad"
    ]

    sources = discoverer.discover_all_sources(
        search_keywords=keywords,
        min_stars=50,
        updated_within_days=30
    )

    # Print discovered sources
    print("\n📋 Discovered Sources:")
    for i, source in enumerate(sources, 1):
        print(f"\n{i}. {source['owner']}/{source['repo']}")
        print(f"   File: {source['file_name']}")
        print(f"   ⭐ Stars: {source['repo_stars']}")
        print(f"   📝 {source['repo_description'][:80]}...")
