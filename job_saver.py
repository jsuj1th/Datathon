#!/usr/bin/env python3
"""
Job Saver Utility
Saves job search results in the specified JSON format.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

def save_jobs_to_json(jobs: List[Dict[str, Any]], search_query: Dict[str, Any], filename: str = None) -> str:
    """
    Save jobs to JSON file in the specified format.
    
    Args:
        jobs: List of job dictionaries
        search_query: The search query parameters
        filename: Optional custom filename
        
    Returns:
        Path to the saved file
    """
    # Create results directory if it doesn't exist
    results_dir = Path(__file__).parent / "job_search_results"
    results_dir.mkdir(exist_ok=True)
    
    # Generate filename if not provided
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        keywords_clean = search_query.get("keywords", "jobs").replace(" ", "_").lower()
        location_clean = search_query.get("location", "").replace(" ", "_").lower()
        location_part = f"_{location_clean}" if location_clean else ""
        filename = f"{keywords_clean}{location_part}_{timestamp}.json"
    
    # Ensure .json extension
    if not filename.endswith('.json'):
        filename += '.json'
    
    # Prepare the data structure
    job_data = {
        "search_metadata": {
            "query": search_query,
            "total_results": len(jobs),
            "collected_at": datetime.now().isoformat(),
            "source": "job_search_mcp_server"
        },
        "jobs": jobs
    }
    
    # Save to file
    file_path = results_dir / filename
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(job_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved {len(jobs)} jobs to: {file_path}")
    return str(file_path)

def load_jobs_from_json(filename: str) -> Dict[str, Any]:
    """
    Load jobs from JSON file.
    
    Args:
        filename: Path to the JSON file
        
    Returns:
        Dictionary containing search metadata and jobs
    """
    file_path = Path(filename)
    if not file_path.exists():
        # Try in results directory
        results_dir = Path(__file__).parent / "job_search_results"
        file_path = results_dir / filename
    
    if not file_path.exists():
        raise FileNotFoundError(f"Job file not found: {filename}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def validate_job_format(job: Dict[str, Any]) -> bool:
    """
    Validate that a job dictionary matches the required format.
    
    Args:
        job: Job dictionary to validate
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = [
        "company", "position", "apply_link", "location", "source",
        "collection_method", "collected_at", "field"
    ]
    
    for field in required_fields:
        if field not in job:
            print(f"❌ Missing required field: {field}")
            return False
    
    return True

if __name__ == "__main__":
    # Test the job saver
    sample_jobs = [
        {
            "company": "Test Company",
            "position": "Software Engineer",
            "apply_link": "https://example.com/apply/123",
            "location": "San Francisco, CA",
            "salary": "$120,000 - $150,000",
            "description": "Great opportunity for a software engineer",
            "requirements": "Python, JavaScript, SQL",
            "benefits": "Health insurance, 401k, PTO",
            "job_type": "full_time",
            "experience_level": "mid_level",
            "posted_date": "2025-11-08",
            "deadline": None,
            "days_since_posted": 3,
            "remote_option": "hybrid",
            "visa_sponsorship": True,
            "source": "test_source",
            "collection_method": "mcp_test",
            "collected_at": datetime.now().isoformat(),
            "field": "Software Engineering",
            "company_type": "startup"
        }
    ]
    
    sample_query = {
        "keywords": "software engineer",
        "location": "San Francisco",
        "limit": 10
    }
    
    # Test saving
    file_path = save_jobs_to_json(sample_jobs, sample_query, "test_jobs.json")
    
    # Test loading
    loaded_data = load_jobs_from_json(file_path)
    print(f"✅ Loaded {len(loaded_data['jobs'])} jobs from file")
    
    # Test validation
    for job in loaded_data['jobs']:
        if validate_job_format(job):
            print("✅ Job format is valid")
        else:
            print("❌ Job format is invalid")
