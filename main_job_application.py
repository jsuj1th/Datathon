#!/usr/bin/env python3
"""
Main Job Search Application
Interactive tool that asks for user query, recipient email, and job keywords
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent / "NewMCP Folder"))

# Load environment variables
load_dotenv()

from job_matcher import JobMatcher


def get_user_input():
    """Get user inputs interactively"""
    print("=" * 70)
    print("🎯 JOB SEARCH & MATCH APPLICATION")
    print("=" * 70)
    print()
    
    # Get user query
    print("📝 What type of job are you looking for?")
    print("   (e.g., 'Machine Learning Engineer', 'Data Scientist')")
    user_query = input("   Your query: ").strip()
    
    if not user_query:
        print("❌ Query cannot be empty!")
        sys.exit(1)
    
    print()
    
    # Get job keywords
    print("🔍 Enter job keywords (comma-separated)")
    print("   (e.g., 'python, machine learning, ai, tensorflow')")
    keywords_input = input("   Keywords: ").strip()
    
    keywords = [k.strip() for k in keywords_input.split(',') if k.strip()]
    if not keywords:
        keywords = user_query.split()
    
    print()
    
    # Get location
    print("📍 Enter location preference (optional)")
    print("   (e.g., 'San Francisco', 'Remote', 'New York')")
    location = input("   Location: ").strip()
    
    if not location:
        location = "Remote"
    
    print()
    
    # Get recipient email
    print("📧 Enter recipient email address")
    default_email = os.getenv('RECIPIENT_EMAIL', '')
    if default_email:
        print(f"   (Press Enter to use: {default_email})")
    
    recipient_email = input("   Email: ").strip()
    
    if not recipient_email:
        recipient_email = default_email
    
    if not recipient_email:
        print("❌ Email address is required!")
        sys.exit(1)
    
    print()
    
    # Get resume path
    print("📄 Enter path to your resume (PDF)")
    default_resume = "./NewMCP Folder/MCP_Servers/pdfDocs/Resume_NEW_ML_Pathakota_Pranavi_2.pdf"
    print(f"   (Press Enter to use: {default_resume})")
    resume_path = input("   Resume path: ").strip()
    
    if not resume_path:
        resume_path = default_resume
    
    print()
    
    # Get number of top matches
    print("🎯 How many top job matches do you want?")
    print("   (Default: 50)")
    top_n_input = input("   Number: ").strip()
    
    try:
        top_n = int(top_n_input) if top_n_input else 50
    except ValueError:
        top_n = 50
    
    print()
    print("=" * 70)
    
    return {
        'query': user_query,
        'keywords': keywords,
        'location': location,
        'recipient_email': recipient_email,
        'resume_path': resume_path,
        'top_n': top_n
    }


def search_jobs(query, location, limit=30):
    """Search for jobs using the job search tools"""
    print("\n🔎 STEP 1: Searching for jobs...")
    print(f"   Query: {query}")
    print(f"   Location: {location}")
    print(f"   Limit: {limit}")
    
    try:
        # Import job search module
        from bb7_search_combined_jobs import search_combined_jobs
        
        # Search for jobs
        results = search_combined_jobs(keywords=query, location=location, limit=limit)
        
        # Parse results
        if isinstance(results, str):
            results = json.loads(results)
        
        jobs = results.get('jobs', [])
        print(f"✅ Found {len(jobs)} jobs")
        
        # Save to file
        output_dir = Path(__file__).parent / "data"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"jobs_{query.replace(' ', '_').lower()}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({'jobs': jobs}, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved jobs to {output_file}")
        return str(output_file)
        
    except ImportError:
        print("⚠️  Job search module not available, using existing jobs...")
        return None
    except Exception as e:
        print(f"⚠️  Error searching jobs: {e}")
        print("   Using existing jobs from data directory...")
        return None


def match_jobs_with_resume(resume_path, keywords, top_n=50):
    """Match jobs with resume"""
    print("\n🤖 STEP 2: Matching jobs with your resume...")
    print(f"   Resume: {resume_path}")
    print(f"   Top matches: {top_n}")
    
    # Initialize job matcher
    matcher = JobMatcher()
    
    # Extract resume text
    print("\n   Extracting resume text...")
    resume_text = matcher.extract_resume(resume_path)
    
    if not resume_text:
        print("   ❌ Failed to extract resume text")
        return None
    
    print(f"   ✅ Extracted {len(resume_text)} characters")
    
    # Load jobs
    print("\n   Loading jobs from data directory...")
    jobs_dirs = [
        str(Path(__file__).parent / "data"),
        str(Path(__file__).parent / "linkedin_collector" / "job_search_results")
    ]
    
    all_jobs = matcher.load_all_jobs(jobs_dirs)
    
    if not all_jobs:
        print("   ❌ No jobs found")
        return None
    
    print(f"   ✅ Loaded {len(all_jobs)} jobs")
    
    # Match jobs
    print(f"\n   Matching jobs with AI (using keywords: {', '.join(keywords[:3])}...)...")
    matched_jobs = matcher.match_jobs_with_llm(resume_text, all_jobs, top_n=top_n)
    
    print(f"   ✅ Matched {len(matched_jobs)} jobs")
    
    # Save matched jobs
    output_dir = Path(__file__).parent / "matched_jobs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "top_matches.json"
    matcher.save_matched_jobs(matched_jobs, str(output_file))
    
    print(f"   ✅ Saved to {output_file}")
    
    return str(output_file), matched_jobs


def send_email(recipient, matched_jobs_file, matched_jobs):
    """Send email with matched jobs"""
    print("\n📧 STEP 3: Sending email with matched jobs...")
    print(f"   Recipient: {recipient}")
    
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        # Get email credentials from .env
        smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        gmail_user = os.getenv('GMAIL_USER')
        gmail_password = os.getenv('GMAIL_APP_PASSWORD')
        
        if not gmail_user or not gmail_password:
            print("   ❌ Email credentials not found in .env file")
            return False
        
        # Create email content
        matcher = JobMatcher()
        email_content = matcher.prepare_email_content(matched_jobs)
        
        # Create email
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = recipient
        msg['Subject'] = f"🎯 Your Top {len(matched_jobs)} Job Matches"
        
        msg.attach(MIMEText(email_content, 'plain'))
        
        # Send email
        print(f"   Connecting to {smtp_host}:{smtp_port}...")
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        
        print("   Logging in...")
        server.login(gmail_user, gmail_password)
        
        print("   Sending email...")
        server.send_message(msg)
        server.quit()
        
        print("   ✅ Email sent successfully!")
        return True
        
    except Exception as e:
        print(f"   ❌ Failed to send email: {e}")
        return False


def display_summary(matched_jobs):
    """Display summary of matched jobs"""
    print("\n" + "=" * 70)
    print("📊 TOP MATCHED JOBS SUMMARY")
    print("=" * 70)
    
    for i, job in enumerate(matched_jobs[:10], 1):
        print(f"\n{i}. {job.get('position', 'Unknown Position')}")
        print(f"   Company: {job.get('company', 'Unknown')}")
        print(f"   Location: {job.get('location', 'Unknown')}")
        print(f"   Match Score: {job.get('match_score', 0)}/100")
        
        if job.get('match_reason'):
            print(f"   Reason: {job.get('match_reason')}")
        
        if job.get('apply_link'):
            print(f"   Apply: {job.get('apply_link')}")
    
    if len(matched_jobs) > 10:
        print(f"\n... and {len(matched_jobs) - 10} more jobs")
    
    print("\n" + "=" * 70)


def main():
    """Main function"""
    try:
        # Get user inputs
        user_data = get_user_input()
        
        # Search for jobs (optional - uses existing if search fails)
        search_jobs(
            query=user_data['query'],
            location=user_data['location'],
            limit=100
        )
        
        # Match jobs with resume
        result = match_jobs_with_resume(
            resume_path=user_data['resume_path'],
            keywords=user_data['keywords'],
            top_n=user_data['top_n']
        )
        
        if not result:
            print("\n❌ Job matching failed")
            sys.exit(1)
        
        matched_jobs_file, matched_jobs = result
        
        # Display summary
        display_summary(matched_jobs)
        
        # Ask if user wants to send email
        print("\n📧 Would you like to send these results via email?")
        send_choice = input("   (y/n): ").strip().lower()
        
        if send_choice == 'y':
            send_email(
                recipient=user_data['recipient_email'],
                matched_jobs_file=matched_jobs_file,
                matched_jobs=matched_jobs
            )
        else:
            print("   ℹ️  Email not sent")
        
        print("\n✅ Process completed successfully!")
        print(f"📁 Results saved to: {matched_jobs_file}")
        print("\n" + "=" * 70)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Process cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
