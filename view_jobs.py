"""
Simple CLI tool to view collected jobs
"""

import json
import sys
from datetime import datetime


def load_jobs(filepath="data/jobs_output.json"):
    """Load jobs from JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        print("   Run 'python main.py' first to collect jobs.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON file: {filepath}")
        sys.exit(1)


def print_job(job, index):
    """Pretty print a single job"""
    print(f"\n{'='*70}")
    print(f"Job #{index}")
    print(f"{'='*70}")
    print(f"🏢 Company: {job['company']}")
    print(f"💼 Position: {job['position']}")
    print(f"📍 Location: {job.get('location', 'Not specified')}")
    print(f"💰 Salary: {job.get('salary', 'Not specified')}")
    print(f"🏠 Remote: {job.get('remote_option', 'unknown')}")
    print(f"📅 Posted: {job.get('days_since_posted', 'N/A')} days ago" if job.get('days_since_posted') else "")
    print(f"🔗 Apply: {job['apply_link']}")
    print(f"📦 Source: {job['source']}")

    if job.get('description'):
        desc = job['description'][:200]
        print(f"\n📝 Description:\n   {desc}...")


def view_all(data):
    """View all jobs"""
    jobs = data['jobs']
    print(f"\n📊 Total Jobs: {len(jobs)}")
    print(f"📅 Collected: {data['collection_timestamp']}")
    print(f"📦 Sources: {', '.join(data['sources'][:5])}")

    for i, job in enumerate(jobs, 1):
        print_job(job, i)

        if i % 10 == 0:
            response = input(f"\n--- Showing {i}/{len(jobs)} jobs. Continue? (y/n/q to quit): ")
            if response.lower() in ['n', 'q']:
                break


def search_jobs(data, query):
    """Search jobs by keyword"""
    jobs = data['jobs']
    query_lower = query.lower()

    matches = [
        job for job in jobs
        if query_lower in job['company'].lower()
        or query_lower in job['position'].lower()
        or query_lower in job.get('location', '').lower()
    ]

    print(f"\n🔍 Found {len(matches)} jobs matching '{query}'")

    for i, job in enumerate(matches, 1):
        print_job(job, i)


def filter_by_location(data, location):
    """Filter jobs by location"""
    jobs = data['jobs']
    location_lower = location.lower()

    matches = [
        job for job in jobs
        if location_lower in job.get('location', '').lower()
    ]

    print(f"\n📍 Found {len(matches)} jobs in '{location}'")

    for i, job in enumerate(matches, 1):
        print_job(job, i)


def show_summary(data):
    """Show collection summary"""
    jobs = data['jobs']

    print("\n" + "=" * 70)
    print("📊 COLLECTION SUMMARY")
    print("=" * 70)

    print(f"\nTotal Jobs: {data['total_count']}")
    print(f"Collection Time: {data['collection_timestamp']}")

    # Count by source
    source_counts = {}
    for job in jobs:
        source = job['source']
        source_counts[source] = source_counts.get(source, 0) + 1

    print("\n📦 Jobs by Source:")
    for source, count in sorted(source_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {source}: {count}")

    # Count by location
    location_counts = {}
    for job in jobs:
        location = job.get('location', 'Unknown')
        location_counts[location] = location_counts.get(location, 0) + 1

    print("\n📍 Top 10 Locations:")
    for location, count in sorted(location_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"   • {location}: {count}")

    # Salary info
    with_salary = sum(1 for job in jobs if job.get('salary'))
    print(f"\n💰 Jobs with Salary Info: {with_salary} ({with_salary/len(jobs)*100:.1f}%)")

    # Remote options
    remote_counts = {}
    for job in jobs:
        remote = job.get('remote_option', 'unknown')
        remote_counts[remote] = remote_counts.get(remote, 0) + 1

    print("\n🏠 Remote Options:")
    for option, count in sorted(remote_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {option}: {count}")


def main():
    """Main CLI interface"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python view_jobs.py summary              - Show collection summary")
        print("  python view_jobs.py all                  - View all jobs")
        print("  python view_jobs.py search <query>       - Search jobs")
        print("  python view_jobs.py location <location>  - Filter by location")
        print("\nExamples:")
        print("  python view_jobs.py search Google")
        print("  python view_jobs.py location 'San Francisco'")
        sys.exit(0)

    command = sys.argv[1]
    data = load_jobs()

    if command == "summary":
        show_summary(data)

    elif command == "all":
        view_all(data)

    elif command == "search":
        if len(sys.argv) < 3:
            print("❌ Please provide a search query")
            sys.exit(1)
        query = sys.argv[2]
        search_jobs(data, query)

    elif command == "location":
        if len(sys.argv) < 3:
            print("❌ Please provide a location")
            sys.exit(1)
        location = sys.argv[2]
        filter_by_location(data, location)

    else:
        print(f"❌ Unknown command: {command}")
        print("   Use 'python view_jobs.py' to see usage")


if __name__ == "__main__":
    main()
