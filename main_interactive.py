#!/usr/bin/env python3
"""
Interactive Job Search and Matcher
Main entry point for the job search application with MCP server integration
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add NewMCP Folder to path
sys.path.insert(0, str(Path(__file__).parent / "NewMCP Folder"))

from job_matcher import JobMatcher


def print_banner():
    """Print application banner"""
    print("\n" + "="*60)
    print("🎯  INTERACTIVE JOB SEARCH & MATCHER")
    print("="*60 + "\n")


def get_user_input():
    """Get user input for job search"""
    print("📝 Please provide the following information:\n")
    
    # Get resume path
    resume_path = input("📄 Resume path (default: ./data/resume.pdf): ").strip()
    if not resume_path:
        resume_path = "./data/resume.pdf"
    
    # Verify resume exists
    if not os.path.exists(resume_path):
        print(f"⚠️  Warning: Resume file not found at {resume_path}")
        create_sample = input("Would you like to continue anyway? (y/n): ").strip().lower()
        if create_sample != 'y':
            sys.exit(0)
    
    # Get job search keywords
    print("\n🔍 Job Search Keywords:")
    print("Enter job titles/keywords (comma-separated)")
    print("Examples: 'Data Scientist, Machine Learning Engineer, AI Researcher'")
    keywords_input = input("Keywords: ").strip()
    
    if not keywords_input:
        keywords_input = "Software Engineer, Data Scientist, Machine Learning Engineer"
        print(f"Using default: {keywords_input}")
    
    keywords = [k.strip() for k in keywords_input.split(',')]
    
    # Get location preferences
    print("\n📍 Location Preferences:")
    print("Enter locations (comma-separated)")
    print("Examples: 'San Francisco, New York, Remote'")
    locations_input = input("Locations: ").strip()
    
    if not locations_input:
        locations_input = "Remote, San Francisco, New York"
        print(f"Using default: {locations_input}")
    
    locations = [l.strip() for l in locations_input.split(',')]
    
    # Get recipient email
    print("\n📧 Email Configuration:")
    recipient_email = input(f"Recipient email (default: {os.getenv('RECIPIENT_EMAIL', 'your@email.com')}): ").strip()
    if not recipient_email:
        recipient_email = os.getenv('RECIPIENT_EMAIL', '')
    
    if not recipient_email:
        print("⚠️  No recipient email provided. Email notifications will be skipped.")
    
    # Get additional query/preferences
    print("\n💭 Additional Requirements (optional):")
    print("Enter any specific requirements, preferences, or questions")
    print("Examples: 'Full-time only', 'Remote preferred', 'Salary > $100k'")
    user_query = input("Additional requirements: ").strip()
    
    return {
        'resume_path': resume_path,
        'keywords': keywords,
        'locations': locations,
        'recipient_email': recipient_email,
        'user_query': user_query
    }


def search_jobs(keywords, locations):
    """Search for jobs using the configured job search tools"""
    logger.info("🔍 Starting job search...")
    
    all_jobs = []
    
    try:
        # Import job search modules
        sys.path.insert(0, str(Path(__file__).parent / "linkedin_collector"))
        from job_searcher import JobSearcher
        
        searcher = JobSearcher()
        
        for keyword in keywords:
            for location in locations:
                logger.info(f"Searching for '{keyword}' in '{location}'...")
                try:
                    jobs = searcher.search_jobs(keyword, location, max_results=50)
                    all_jobs.extend(jobs)
                    logger.info(f"Found {len(jobs)} jobs for '{keyword}' in '{location}'")
                except Exception as e:
                    logger.error(f"Error searching for '{keyword}' in '{location}': {e}")
        
        logger.info(f"✅ Total jobs found: {len(all_jobs)}")
        return all_jobs
        
    except Exception as e:
        logger.error(f"Error during job search: {e}")
        return []


def match_jobs_with_resume(resume_path, jobs):
    """Match jobs with resume using JobMatcher"""
    logger.info("🎯 Matching jobs with resume...")
    
    try:
        matcher = JobMatcher()
        
        # Extract resume text
        resume_text = matcher.extract_resume(resume_path)
        logger.info(f"Resume extracted: {len(resume_text)} characters")
        
        # Match jobs
        matched_jobs = []
        for i, job in enumerate(jobs, 1):
            logger.info(f"Matching job {i}/{len(jobs)}: {job.get('title', 'Unknown')}")
            
            match_result = matcher.match_job_with_resume(resume_text, job)
            
            if match_result:
                matched_jobs.append({
                    **job,
                    'match_score': match_result.get('match_score', 0),
                    'match_analysis': match_result.get('analysis', ''),
                    'strengths': match_result.get('strengths', []),
                    'gaps': match_result.get('gaps', [])
                })
        
        # Sort by match score
        matched_jobs.sort(key=lambda x: x.get('match_score', 0), reverse=True)
        
        logger.info(f"✅ Matched {len(matched_jobs)} jobs")
        return matched_jobs[:50]  # Return top 50
        
    except Exception as e:
        logger.error(f"Error matching jobs: {e}")
        return jobs[:50]  # Return top 50 unmatched if error


def save_results(matched_jobs, output_path="./matched_jobs/interactive_results.json"):
    """Save matched jobs to file"""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(matched_jobs, f, indent=2)
        
        logger.info(f"✅ Results saved to {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error saving results: {e}")
        return None


def send_email(recipient_email, matched_jobs):
    """Send email with matched jobs"""
    if not recipient_email:
        logger.warning("No recipient email provided. Skipping email notification.")
        return False
    
    try:
        from send_email_smtp import send_job_email
        
        # Prepare email content
        top_jobs = matched_jobs[:10]  # Send top 10
        
        send_job_email(
            recipient=recipient_email,
            jobs=top_jobs,
            subject="🎯 Your Matched Job Opportunities"
        )
        
        logger.info(f"✅ Email sent to {recipient_email}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False


def display_summary(matched_jobs, user_data):
    """Display summary of results"""
    print("\n" + "="*60)
    print("📊 SEARCH SUMMARY")
    print("="*60)
    
    print(f"\n📝 Resume: {user_data['resume_path']}")
    print(f"🔍 Keywords: {', '.join(user_data['keywords'])}")
    print(f"📍 Locations: {', '.join(user_data['locations'])}")
    
    if user_data['user_query']:
        print(f"💭 Additional Requirements: {user_data['user_query']}")
    
    print(f"\n📈 Total Matched Jobs: {len(matched_jobs)}")
    
    if matched_jobs:
        print("\n🎯 Top 5 Matches:\n")
        
        for i, job in enumerate(matched_jobs[:5], 1):
            print(f"{i}. {job.get('title', 'Unknown Title')}")
            print(f"   Company: {job.get('company', 'Unknown Company')}")
            print(f"   Location: {job.get('location', 'Unknown Location')}")
            
            if 'match_score' in job:
                print(f"   Match Score: {job['match_score']}/100")
            
            if 'link' in job:
                print(f"   Link: {job['link']}")
            
            print()
    
    print("="*60 + "\n")


def main():
    """Main function"""
    try:
        print_banner()
        
        # Get user input
        user_data = get_user_input()
        
        print("\n" + "="*60)
        print("🚀 Starting Job Search Pipeline...")
        print("="*60 + "\n")
        
        # Step 1: Search for jobs
        jobs = search_jobs(user_data['keywords'], user_data['locations'])
        
        if not jobs:
            logger.warning("No jobs found. Please try different keywords or locations.")
            return
        
        # Step 2: Match jobs with resume
        matched_jobs = match_jobs_with_resume(user_data['resume_path'], jobs)
        
        # Step 3: Save results
        output_path = save_results(matched_jobs)
        
        # Step 4: Send email
        if user_data['recipient_email']:
            send_email(user_data['recipient_email'], matched_jobs)
        
        # Step 5: Display summary
        display_summary(matched_jobs, user_data)
        
        print("✅ Job search completed successfully!")
        
        if output_path:
            print(f"\n📁 Full results saved to: {output_path}")
        
        print("\n💡 Tip: You can view detailed results in the output file.")
        print("💡 Tip: Use the MCP server for programmatic access to these tools.\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error in main: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
