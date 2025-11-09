#!/usr/bin/env python3
"""
Search and Save Jobs
A simple script to search for jobs and save them to JSON format.
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from mcp_server import search_combined_jobs, search_linkedin_jobs, search_muse_jobs
from job_saver import save_jobs_to_json, validate_job_format


def load_keywords_from_file(filepath: str = "job_keywords.txt"):
    """
    Load search keywords from a pipe-delimited text file.

    Format: keyword | location | limit
    Example: machine learning engineer | Remote | 30

    Args:
        filepath: Path to the keywords file

    Returns:
        List of dictionaries with keywords, location, and limit
    """
    keywords_list = []
    file_path = Path(__file__).parent / filepath

    if not file_path.exists():
        print(f"⚠️  Keywords file not found: {file_path}")
        return []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue

            # Parse pipe-delimited format
            parts = [p.strip() for p in line.split('|')]

            if len(parts) < 1:
                print(f"⚠️  Skipping invalid line {line_num}: {line}")
                continue

            keyword_entry = {
                "keywords": parts[0],
                "location": parts[1] if len(parts) > 1 else "",
                "limit": int(parts[2]) if len(parts) > 2 else 30
            }

            keywords_list.append(keyword_entry)

    return keywords_list


async def search_and_save(keywords: str, location: str = "", limit: int = 30, output_filename: str = None):
    """
    Search for jobs and save them to JSON file.

    Args:
        keywords: Job search keywords (e.g., "data scientist", "software engineer")
        location: Job location (e.g., "San Francisco", "Remote")
        limit: Maximum number of jobs to retrieve
        output_filename: Optional custom filename for the JSON file
    """
    print("=" * 70)
    print("🔍 JOB SEARCH AND SAVE")
    print("=" * 70)
    print(f"Keywords: {keywords}")
    print(f"Location: {location or 'Any'}")
    print(f"Limit: {limit}")
    print()

    # Search for jobs
    print("🚀 Searching for jobs...")
    result_json = await search_combined_jobs(keywords, location, limit)
    result = json.loads(result_json)

    # Extract jobs
    jobs = result.get("jobs", [])
    search_query = result.get("search_query", {
        "keywords": keywords,
        "location": location,
        "limit": limit
    })

    print(f"✅ Found {len(jobs)} jobs")
    print(f"📊 Sources: {', '.join(result.get('sources_used', []))}")
    print()

    # Show sample jobs
    if jobs:
        print("📋 Sample Jobs:")
        for i, job in enumerate(jobs[:5], 1):
            print(f"\n{i}. {job.get('position')} at {job.get('company')}")
            print(f"   Location: {job.get('location')}")
            print(f"   Salary: {job.get('salary', 'Not specified')}")
            print(f"   Source: {job.get('source')}")

        if len(jobs) > 5:
            print(f"\n... and {len(jobs) - 5} more jobs")

    print()
    print("=" * 70)

    # Validate jobs
    print("🔍 Validating job format...")
    valid_jobs = []
    invalid_count = 0

    for job in jobs:
        if validate_job_format(job):
            valid_jobs.append(job)
        else:
            invalid_count += 1

    print(f"✅ Valid jobs: {len(valid_jobs)}")
    if invalid_count > 0:
        print(f"⚠️  Invalid jobs: {invalid_count}")
    print()

    # Save to JSON
    print("💾 Saving to JSON file...")
    file_path = save_jobs_to_json(valid_jobs, search_query, output_filename)

    print()
    print("=" * 70)
    print("✅ JOB SEARCH COMPLETE!")
    print("=" * 70)
    print(f"📁 File: {file_path}")
    print(f"📊 Total Jobs: {len(valid_jobs)}")
    print(f"🎯 Success!")

    return file_path


async def main():
    """Main function that loads searches from keywords file."""
    print("\n" + "=" * 70)
    print("🚀 AUTOMATED JOB SEARCH AND SAVE")
    print("=" * 70)
    print()

    # Allow command line arguments for single search
    if len(sys.argv) > 1:
        keywords = sys.argv[1]
        location = sys.argv[2] if len(sys.argv) > 2 else ""
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        filename = sys.argv[4] if len(sys.argv) > 4 else None

        await search_and_save(keywords, location, limit, filename)
    else:
        # Load searches from job_keywords.txt
        print("📖 Loading search keywords from job_keywords.txt...")
        searches = load_keywords_from_file("job_keywords.txt")

        if not searches:
            print("❌ No keywords found in job_keywords.txt")
            print("💡 Add keywords in format: keyword | location | limit")
            print("💡 Example: machine learning engineer | Remote | 30")
            return

        print(f"✅ Loaded {len(searches)} search queries")
        print("(Use: python search_and_save.py 'keywords' 'location' limit filename for single search)")
        print()

        for i, search in enumerate(searches, 1):
            print(f"\n{'='*70}")
            print(f"Search {i}/{len(searches)}")
            print(f"{'='*70}")

            # Generate filename from keywords and location
            keywords_slug = search["keywords"].lower().replace(" ", "_")[:30]
            location_slug = search["location"].lower().replace(" ", "_")[:15] if search["location"] else "any"
            filename = f"{keywords_slug}_{location_slug}.json"

            await search_and_save(
                search["keywords"],
                search["location"],
                search["limit"],
                filename
            )

            if i < len(searches):
                print("\n⏳ Waiting 2 seconds before next search...")
                await asyncio.sleep(2)

    print("\n" + "=" * 70)
    print("🎉 ALL SEARCHES COMPLETE!")
    print("=" * 70)
    print(f"📁 Files saved in: {Path(__file__).parent / 'job_search_results'}")
    print()


if __name__ == "__main__":
    asyncio.run(main())
