#!/usr/bin/env python3
"""
Temporary script to save California data science jobs
"""

import json
from job_saver import save_jobs_to_json
from datetime import datetime

# The complete job search results
job_data = {
  "search_query": {
    "keywords": "data science",
    "location": "California", 
    "limit": 30
  },
  "total_results": 26,
  "sources_used": [
    "linkedin",
    "aggregated"
  ],
  "jobs": [
    {
      "job_id": "linkedin_1",
      "title": "Senior Data Scientist",
      "company": "Meta",
      "location": "California",
      "description": "We are seeking a talented Senior Data Scientist to join our dynamic team. This role offers excellent opportunities for growth and impact.",
      "employment_type": "Full-time",
      "seniority_level": "Mid-Senior level",
      "posted_date": "2025-11-08",
      "apply_url": "https://linkedin.com/jobs/view/linkedin_1",
      "salary_range": "$120,000 - $180,000",
      "source": "linkedin",
      "skills_required": ["SQL", "Python", "Machine Learning", "Statistics"]
    },
    {
      "job_id": "linkedin_2",
      "title": "Data Scientist II",
      "company": "Google",
      "location": "California",
      "description": "We are seeking a talented Data Scientist II to join our dynamic team. This role offers excellent opportunities for growth and impact.",
      "employment_type": "Full-time",
      "seniority_level": "Mid-Senior level",
      "posted_date": "2025-11-08",
      "apply_url": "https://linkedin.com/jobs/view/linkedin_2",
      "salary_range": "$90,000 - $140,000",
      "source": "linkedin",
      "skills_required": ["SQL", "Python", "Machine Learning", "Statistics"]
    },
    {
      "job_id": "linkedin_3",
      "title": "ML Engineer",
      "company": "Netflix",
      "location": "California",
      "description": "We are seeking a talented ML Engineer to join our dynamic team. This role offers excellent opportunities for growth and impact.",
      "employment_type": "Full-time",
      "seniority_level": "Mid-Senior level",
      "posted_date": "2025-11-08",
      "apply_url": "https://linkedin.com/jobs/view/linkedin_3",
      "salary_range": "$90,000 - $140,000",
      "source": "linkedin",
      "skills_required": ["SQL", "Python", "Machine Learning", "Statistics"]
    },
    {
      "job_id": "linkedin_4",
      "title": "Data Engineer",
      "company": "Spotify",
      "location": "California",
      "description": "We are seeking a talented Data Engineer to join our dynamic team. This role offers excellent opportunities for growth and impact.",
      "employment_type": "Full-time",
      "seniority_level": "Mid-Senior level",
      "posted_date": "2025-11-08",
      "apply_url": "https://linkedin.com/jobs/view/linkedin_4",
      "salary_range": "$90,000 - $140,000",
      "source": "linkedin",
      "skills_required": ["SQL", "Python", "Machine Learning", "Statistics"]
    },
    {
      "job_id": "linkedin_5",
      "title": "Senior Data Scientist",
      "company": "Palantir",
      "location": "California",
      "description": "We are seeking a talented Senior Data Scientist to join our dynamic team. This role offers excellent opportunities for growth and impact.",
      "employment_type": "Full-time",
      "seniority_level": "Mid-Senior level",
      "posted_date": "2025-11-08",
      "apply_url": "https://linkedin.com/jobs/view/linkedin_5",
      "salary_range": "$120,000 - $180,000",
      "source": "linkedin",
      "skills_required": ["SQL", "Python", "Machine Learning", "Statistics"]
    },
    {
      "job_id": "linkedin_6",
      "title": "Data Scientist II",
      "company": "DataBricks",
      "location": "California",
      "description": "We are seeking a talented Data Scientist II to join our dynamic team. This role offers excellent opportunities for growth and impact.",
      "employment_type": "Full-time",
      "seniority_level": "Mid-Senior level",
      "posted_date": "2025-11-08",
      "apply_url": "https://linkedin.com/jobs/view/linkedin_6",
      "salary_range": "$90,000 - $140,000",
      "source": "linkedin",
      "skills_required": ["SQL", "Python", "Machine Learning", "Statistics"]
    },
    {
      "job_id": "linkedin_7",
      "title": "ML Engineer",
      "company": "Snowflake",
      "location": "California",
      "description": "We are seeking a talented ML Engineer to join our dynamic team. This role offers excellent opportunities for growth and impact.",
      "employment_type": "Full-time",
      "seniority_level": "Mid-Senior level",
      "posted_date": "2025-11-08",
      "apply_url": "https://linkedin.com/jobs/view/linkedin_7",
      "salary_range": "$90,000 - $140,000",
      "source": "linkedin",
      "skills_required": ["SQL", "Python", "Machine Learning", "Statistics"]
    },
    {
      "job_id": "linkedin_8",
      "title": "Data Engineer",
      "company": "Meta",
      "location": "California",
      "description": "We are seeking a talented Data Engineer to join our dynamic team. This role offers excellent opportunities for growth and impact.",
      "employment_type": "Full-time",
      "seniority_level": "Mid-Senior level",
      "posted_date": "2025-11-08",
      "apply_url": "https://linkedin.com/jobs/view/linkedin_8",
      "salary_range": "$90,000 - $140,000",
      "source": "linkedin",
      "skills_required": ["SQL", "Python", "Machine Learning", "Statistics"]
    },
    {
      "job_id": "linkedin_9",
      "title": "Senior Data Scientist",
      "company": "Google",
      "location": "California",
      "description": "We are seeking a talented Senior Data Scientist to join our dynamic team. This role offers excellent opportunities for growth and impact.",
      "employment_type": "Full-time",
      "seniority_level": "Mid-Senior level",
      "posted_date": "2025-11-08",
      "apply_url": "https://linkedin.com/jobs/view/linkedin_9",
      "salary_range": "$120,000 - $180,000",
      "source": "linkedin",
      "skills_required": ["SQL", "Python", "Machine Learning", "Statistics"]
    },
    {
      "job_id": "linkedin_10",
      "title": "Data Scientist II",
      "company": "Netflix",
      "location": "California",
      "description": "We are seeking a talented Data Scientist II to join our dynamic team. This role offers excellent opportunities for growth and impact.",
      "employment_type": "Full-time",
      "seniority_level": "Mid-Senior level",
      "posted_date": "2025-11-08",
      "apply_url": "https://linkedin.com/jobs/view/linkedin_10",
      "salary_range": "$90,000 - $140,000",
      "source": "linkedin",
      "skills_required": ["SQL", "Python", "Machine Learning", "Statistics"]
    },
    {
      "job_id": "linkedin_11",
      "title": "ML Engineer",
      "company": "Spotify",
      "location": "California",
      "description": "We are seeking a talented ML Engineer to join our dynamic team. This role offers excellent opportunities for growth and impact.",
      "employment_type": "Full-time",
      "seniority_level": "Mid-Senior level",
      "posted_date": "2025-11-08",
      "apply_url": "https://linkedin.com/jobs/view/linkedin_11",
      "salary_range": "$90,000 - $140,000",
      "source": "linkedin",
      "skills_required": ["SQL", "Python", "Machine Learning", "Statistics"]
    },
    {
      "job_id": "linkedin_12",
      "title": "Data Engineer",
      "company": "Palantir",
      "location": "California",
      "description": "We are seeking a talented Data Engineer to join our dynamic team. This role offers excellent opportunities for growth and impact.",
      "employment_type": "Full-time",
      "seniority_level": "Mid-Senior level",
      "posted_date": "2025-11-08",
      "apply_url": "https://linkedin.com/jobs/view/linkedin_12",
      "salary_range": "$90,000 - $140,000",
      "source": "linkedin",
      "skills_required": ["SQL", "Python", "Machine Learning", "Statistics"]
    },
    {
      "job_id": "linkedin_13",
      "title": "Senior Data Scientist",
      "company": "DataBricks",
      "location": "California",
      "description": "We are seeking a talented Senior Data Scientist to join our dynamic team. This role offers excellent opportunities for growth and impact.",
      "employment_type": "Full-time",
      "seniority_level": "Mid-Senior level",
      "posted_date": "2025-11-08",
      "apply_url": "https://linkedin.com/jobs/view/linkedin_13",
      "salary_range": "$120,000 - $180,000",
      "source": "linkedin",
      "skills_required": ["SQL", "Python", "Machine Learning", "Statistics"]
    },
    {
      "job_id": "linkedin_14",
      "title": "Data Scientist II",
      "company": "Snowflake",
      "location": "California",
      "description": "We are seeking a talented Data Scientist II to join our dynamic team. This role offers excellent opportunities for growth and impact.",
      "employment_type": "Full-time",
      "seniority_level": "Mid-Senior level",
      "posted_date": "2025-11-08",
      "apply_url": "https://linkedin.com/jobs/view/linkedin_14",
      "salary_range": "$90,000 - $140,000",
      "source": "linkedin",
      "skills_required": ["SQL", "Python", "Machine Learning", "Statistics"]
    },
    {
      "job_id": "linkedin_15",
      "title": "ML Engineer",
      "company": "Meta",
      "location": "California",
      "description": "We are seeking a talented ML Engineer to join our dynamic team. This role offers excellent opportunities for growth and impact.",
      "employment_type": "Full-time",
      "seniority_level": "Mid-Senior level",
      "posted_date": "2025-11-08",
      "apply_url": "https://linkedin.com/jobs/view/linkedin_15",
      "salary_range": "$90,000 - $140,000",
      "source": "linkedin",
      "skills_required": ["SQL", "Python", "Machine Learning", "Statistics"]
    },
    {
      "title": "Analyst",
      "company": "CloudSoft",
      "location": "California",
      "link": "https://jobs.example.com/cloudsoft/analyst-1",
      "description": "We are looking for a talented Analyst to join our team. Required skills: Programming, Problem Solving, Team Collaboration. Salary: $80,000 - $150,000.",
      "source": "aggregated",
      "salary": "$80,000 - $150,000",
      "posted_date": "2025-11-04"
    },
    {
      "title": "Analyst", 
      "company": "TechCorp",
      "location": "California",
      "link": "https://jobs.example.com/techcorp/analyst-2",
      "description": "We are looking for a talented Analyst to join our team. Required skills: Team Collaboration, Problem Solving, Programming. Salary: $80,000 - $150,000.",
      "source": "aggregated",
      "salary": "$80,000 - $150,000",
      "posted_date": "2025-10-31"
    },
    {
      "title": "Developer",
      "company": "InnovateCo",
      "location": "California",
      "link": "https://jobs.example.com/innovateco/developer-3",
      "description": "We are looking for a talented Developer to join our team. Required skills: Problem Solving, Team Collaboration, Programming. Salary: $80,000 - $150,000.",
      "source": "aggregated",
      "salary": "$80,000 - $150,000",
      "posted_date": "2025-10-20"
    },
    {
      "title": "Analyst",
      "company": "InnovateCo",
      "location": "California",
      "link": "https://jobs.example.com/innovateco/analyst-4",
      "description": "We are looking for a talented Analyst to join our team. Required skills: Problem Solving, Team Collaboration, Programming. Salary: $80,000 - $150,000.",
      "source": "aggregated",
      "salary": "$80,000 - $150,000",
      "posted_date": "2025-10-18"
    },
    {
      "title": "Developer",
      "company": "DataTech",
      "location": "California",
      "link": "https://jobs.example.com/datatech/developer-6",
      "description": "We are looking for a talented Developer to join our team. Required skills: Programming, Problem Solving, Team Collaboration. Salary: $80,000 - $150,000.",
      "source": "aggregated",
      "salary": "$80,000 - $150,000",
      "posted_date": "2025-10-12"
    },
    {
      "title": "Developer",
      "company": "CloudSoft",
      "location": "California",
      "link": "https://jobs.example.com/cloudsoft/developer-7",
      "description": "We are looking for a talented Developer to join our team. Required skills: Problem Solving, Programming, Team Collaboration. Salary: $80,000 - $150,000.",
      "source": "aggregated",
      "salary": "$80,000 - $150,000",
      "posted_date": "2025-11-05"
    },
    {
      "title": "Engineer",
      "company": "CloudSoft",
      "location": "California",
      "link": "https://jobs.example.com/cloudsoft/engineer-8",
      "description": "We are looking for a talented Engineer to join our team. Required skills: Problem Solving, Team Collaboration, Programming. Salary: $80,000 - $150,000.",
      "source": "aggregated",
      "salary": "$80,000 - $150,000",
      "posted_date": "2025-10-15"
    },
    {
      "title": "Software Developer",
      "company": "DataTech",
      "location": "California",
      "link": "https://jobs.example.com/datatech/software-developer-9",
      "description": "We are looking for a talented Software Developer to join our team. Required skills: Team Collaboration, Problem Solving, Programming. Salary: $80,000 - $150,000.",
      "source": "aggregated",
      "salary": "$80,000 - $150,000",
      "posted_date": "2025-11-03"
    },
    {
      "title": "Software Developer",
      "company": "InnovateCo",
      "location": "California",
      "link": "https://jobs.example.com/innovateco/software-developer-11",
      "description": "We are looking for a talented Software Developer to join our team. Required skills: Team Collaboration, Problem Solving, Programming. Salary: $80,000 - $150,000.",
      "source": "aggregated",
      "salary": "$80,000 - $150,000",
      "posted_date": "2025-10-27"
    },
    {
      "title": "Software Developer",
      "company": "CloudSoft",
      "location": "California",
      "link": "https://jobs.example.com/cloudsoft/software-developer-13",
      "description": "We are looking for a talented Software Developer to join our team. Required skills: Programming, Team Collaboration, Problem Solving. Salary: $80,000 - $150,000.",
      "source": "aggregated",
      "salary": "$80,000 - $150,000",
      "posted_date": "2025-10-21"
    },
    {
      "title": "Engineer",
      "company": "TechCorp",
      "location": "California",
      "link": "https://jobs.example.com/techcorp/engineer-14",
      "description": "We are looking for a talented Engineer to join our team. Required skills: Problem Solving, Programming, Team Collaboration. Salary: $80,000 - $150,000.",
      "source": "aggregated",
      "salary": "$80,000 - $150,000",
      "posted_date": "2025-10-10"
    }
  ]
}

# Convert to the format expected by job_saver
formatted_jobs = []
for job in job_data['jobs']:
    formatted_job = {
        'company': job.get('company', 'Unknown'),
        'position': job.get('title', 'Unknown'),
        'apply_link': job.get('apply_url', job.get('link', '')),
        'location': job.get('location', 'California'),
        'salary': job.get('salary_range', job.get('salary', '')),
        'description': job.get('description', ''),
        'requirements': ', '.join(job.get('skills_required', [])) if job.get('skills_required') else '',
        'benefits': '',
        'job_type': 'full_time',
        'experience_level': job.get('seniority_level', 'mid_level').replace('-', '_').replace(' ', '_').lower() if job.get('seniority_level') else 'mid_level',
        'posted_date': job.get('posted_date', '2025-11-08'),
        'deadline': None,
        'days_since_posted': 0,
        'remote_option': 'unknown',
        'visa_sponsorship': None,
        'source': job.get('source', 'combined_search'),
        'collection_method': 'mcp_combined_search',
        'collected_at': datetime.now().isoformat(),
        'field': 'Data Science',
        'company_type': 'unknown'
    }
    formatted_jobs.append(formatted_job)

# Save all jobs
file_path = save_jobs_to_json(formatted_jobs, job_data['search_query'])
print(f"Successfully saved {len(formatted_jobs)} jobs to: {file_path}")
