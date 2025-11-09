#!/usr/bin/env python3
"""
Complete Job Search Pipeline
Interactive application that:
1. Asks for user query and preferences
2. Searches GitHub and LinkedIn for jobs
3. Matches jobs with resume using AI
4. Sends email with top matches
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
import logging

# Setup paths
sys.path.insert(0, str(Path(__file__).parent / "NewMCP Folder"))
sys.path.insert(0, str(Path(__file__).parent / "github_collector"))
sys.path.insert(0, str(Path(__file__).parent / "linkedin_collector"))

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def get_user_preferences():
    """Interactive function to get user preferences"""
    print_header("🎯 JOB SEARCH & MATCHING SYSTEM")
    
    print("\n👋 Welcome! Let's find your perfect job matches.\n")
    
    # 1. Job Query
    print("📝 STEP 1: What type of job are you looking for?")
    print("   Examples:")
    print("   - Machine Learning Engineer")
    print("   - Data Scientist")
    print("   - Software Engineer")
    print("   - AI Researcher")
    query = input("\n   Your job query: ").strip()
    
    if not query:
        print("   ❌ Job query is required!")
        sys.exit(1)
    
    # 2. Keywords
    print("\n🔍 STEP 2: Enter keywords to filter jobs (comma-separated)")
    print("   Examples: python, machine learning, tensorflow, nlp, computer vision")
    keywords_input = input("\n   Keywords: ").strip()
    
    keywords = []
    if keywords_input:
        keywords = [k.strip() for k in keywords_input.split(',') if k.strip()]
    else:
        # Extract keywords from query
        keywords = [word for word in query.lower().split() if len(word) > 3]
    
    # 3. Location
    print("\n📍 STEP 3: Where do you want to work?")
    print("   Examples: San Francisco, New York, Remote, Boston")
    location = input("\n   Location: ").strip()
    
    if not location:
        location = "Remote"
    
    # 4. Experience Level
    print("\n💼 STEP 4: What's your experience level?")
    print("   Options: entry, junior, mid, senior, lead")
    experience = input("\n   Experience level: ").strip().lower()
    
    if experience not in ['entry', 'junior', 'mid', 'senior', 'lead']:
        experience = 'mid'
    
    # 5. Number of results
    print("\n🎯 STEP 5: How many top matches do you want?")
    print("   (We'll search for more and rank the best ones)")
    top_n_input = input("\n   Number of top matches (default 20): ").strip()
    
    try:
        top_n = int(top_n_input) if top_n_input else 20
    except ValueError:
        top_n = 20
    
    # 6. Email
    print("\n📧 STEP 6: Where should we send the results?")
    default_email = os.getenv('RECIPIENT_EMAIL', '')
    if default_email:
        print(f"   (Press Enter to use: {default_email})")
    
    recipient_email = input("\n   Email address: ").strip()
    
    if not recipient_email and default_email:
        recipient_email = default_email
    
    if not recipient_email:
        print("   ❌ Email address is required!")
        sys.exit(1)
    
    # 7. Resume path
    print("\n📄 STEP 7: Path to your resume (PDF)")
    default_resume = "./NewMCP Folder/MCP_Servers/pdfDocs/Resume_NEW_ML_Pathakota_Pranavi_2.pdf"
    
    if Path(default_resume).exists():
        print(f"   (Press Enter to use default resume)")
        resume_path = input("\n   Resume path: ").strip()
        if not resume_path:
            resume_path = default_resume
    else:
        resume_path = input("\n   Resume path: ").strip()
    
    if not resume_path or not Path(resume_path).exists():
        print(f"   ❌ Resume file not found: {resume_path}")
        sys.exit(1)
    
    # Summary
    print_header("📋 SEARCH SUMMARY")
    print(f"\n   Job Query: {query}")
    print(f"   Keywords: {', '.join(keywords)}")
    print(f"   Location: {location}")
    print(f"   Experience: {experience}")
    print(f"   Top Matches: {top_n}")
    print(f"   Email: {recipient_email}")
    print(f"   Resume: {resume_path}")
    
    print("\n❓ Does this look correct?")
    confirm = input("   (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("   ❌ Search cancelled")
        sys.exit(0)
    
    return {
        'query': query,
        'keywords': keywords,
        'location': location,
        'experience': experience,
        'top_n': top_n,
        'recipient_email': recipient_email,
        'resume_path': resume_path
    }


def search_github_jobs(query, keywords, location, limit=50):
    """Search GitHub for jobs using Firecrawl"""
    print_header("🔎 SEARCHING GITHUB FOR JOBS")
    
    try:
        from github_collector.firecrawl_search import search_github_with_firecrawl
        
        print(f"\n   Query: {query}")
        print(f"   Keywords: {', '.join(keywords)}")
        print(f"   Location: {location}")
        print(f"   Limit: {limit}")
        
        jobs = search_github_with_firecrawl(
            keywords=query,
            location=location,
            limit=limit
        )
        
        print(f"\n   ✅ Found {len(jobs)} jobs on GitHub")
        
        # Save to data directory
        output_dir = Path(__file__).parent / "data"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"github_{query.replace(' ', '_').lower()}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({'jobs': jobs, 'source': 'github'}, f, indent=2)
        
        print(f"   💾 Saved to: {output_file}")
        
        return jobs
        
    except ImportError as e:
        print(f"\n   ⚠️  GitHub collector not available: {e}")
        import traceback
        traceback.print_exc()
        return []
    except Exception as e:
        print(f"\n   ⚠️  Error searching GitHub: {e}")
        import traceback
        traceback.print_exc()
        return []


def search_linkedin_jobs(query, keywords, location, limit=50):
    """Search LinkedIn for jobs"""
    print_header("🔎 SEARCHING LINKEDIN FOR JOBS")
    
    try:
        from linkedin_collector.job_searcher import JobSearcher
        import asyncio
        
        print(f"\n   Query: {query}")
        print(f"   Keywords: {', '.join(keywords)}")
        print(f"   Location: {location}")
        print(f"   Limit: {limit}")
        
        searcher = JobSearcher()
        
        # Combine query and keywords into search string
        search_keywords = f"{query} {' '.join(keywords)}"
        
        # Run async search
        jobs = asyncio.run(searcher.search_jobs(
            keywords=search_keywords,
            location=location,
            limit=limit
        ))
        
        print(f"\n   ✅ Found {len(jobs)} jobs on LinkedIn")
        
        # Save to data directory
        output_dir = Path(__file__).parent / "data"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"linkedin_{query.replace(' ', '_').lower()}_{location.replace(' ', '_').lower()}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({'jobs': jobs, 'source': 'linkedin'}, f, indent=2)
        
        print(f"   💾 Saved to: {output_file}")
        
        return jobs
        
    except ImportError as e:
        print(f"\n   ⚠️  LinkedIn collector not available: {e}")
        return []
    except Exception as e:
        print(f"\n   ⚠️  Error searching LinkedIn: {e}")
        import traceback
        traceback.print_exc()
        return []


def match_jobs_with_ai(resume_path, all_jobs, top_n=20):
    """Match jobs with resume using AI"""
    print_header("🤖 MATCHING JOBS WITH YOUR RESUME")
    
    try:
        # Import from NewMCP Folder explicitly
        sys.path.insert(0, str(Path(__file__).parent / "NewMCP Folder"))
        from job_matcher import JobMatcher
        
        # Initialize matcher
        matcher = JobMatcher()
        
        print(f"\n   Resume: {resume_path}")
        print(f"   Total jobs to analyze: {len(all_jobs)}")
        print(f"   Top matches to return: {top_n}")
        
        # Extract resume text
        print("\n   📄 Extracting resume text...")
        resume_text = matcher.extract_resume(resume_path)
        
        if not resume_text:
            print("   ❌ Failed to extract resume text")
            return []
        
        print(f"   ✅ Extracted {len(resume_text)} characters")
        
        # Match jobs
        print(f"\n   🧠 Analyzing {len(all_jobs)} jobs with AI...")
        print("   (This may take a minute...)")
        
        matched_jobs = matcher.match_jobs_with_llm(resume_text, all_jobs, top_n=top_n)
        
        print(f"\n   ✅ Found {len(matched_jobs)} top matches")
        
        # Save matched jobs
        output_dir = Path(__file__).parent / "matched_jobs"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / "top_matches.json"
        matcher.save_matched_jobs(matched_jobs, str(output_file))
        
        print(f"   💾 Saved to: {output_file}")
        
        return matched_jobs
        
    except Exception as e:
        print(f"\n   ❌ Error matching jobs: {e}")
        import traceback
        traceback.print_exc()
        return []


def send_email_results(recipient, matched_jobs):
    """Send email with matched jobs"""
    print_header("📧 SENDING EMAIL WITH RESULTS")
    
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from email.mime.application import MIMEApplication
        
        print(f"\n   Recipient: {recipient}")
        print(f"   Jobs to send: {len(matched_jobs)}")
        
        # Get email credentials
        smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        gmail_user = os.getenv('GMAIL_USER')
        gmail_password = os.getenv('GMAIL_APP_PASSWORD')
        
        if not gmail_user or not gmail_password:
            print("\n   ❌ Email credentials not found in .env file")
            print("   Please set GMAIL_USER and GMAIL_APP_PASSWORD")
            return False
        
        # Create email content
        sys.path.insert(0, str(Path(__file__).parent / "NewMCP Folder"))
        from job_matcher import JobMatcher
        matcher = JobMatcher()
        email_content = matcher.prepare_email_content(matched_jobs)
        
        # Create HTML version
        html_content = "<html><body style='font-family: Arial, sans-serif;'>"
        html_content += "<h2>🎯 Your Top Job Matches</h2>"
        
        for i, job in enumerate(matched_jobs, 1):
            html_content += f"<div style='margin: 20px 0; padding: 15px; border-left: 4px solid #4CAF50;'>"
            html_content += f"<h3>{i}. {job.get('position', 'Unknown Position')}</h3>"
            html_content += f"<p><strong>Company:</strong> {job.get('company', 'Unknown')}</p>"
            html_content += f"<p><strong>Location:</strong> {job.get('location', 'Unknown')}</p>"
            html_content += f"<p><strong>Match Score:</strong> {job.get('match_score', 0)}/100</p>"
            
            if job.get('match_reason'):
                html_content += f"<p><strong>Why it matches:</strong> {job.get('match_reason')}</p>"
            
            if job.get('description'):
                desc = job.get('description', '')[:200]
                html_content += f"<p><strong>Description:</strong> {desc}...</p>"
            
            if job.get('apply_link'):
                html_content += f"<p><a href='{job.get('apply_link')}' style='background: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;'>Apply Now</a></p>"
            
            html_content += "</div>"
        
        html_content += "<hr><p style='color: #666;'>🤖 Generated by AI Job Matcher</p>"
        html_content += "</body></html>"
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = gmail_user
        msg['To'] = recipient
        msg['Subject'] = f"🎯 Your Top {len(matched_jobs)} Job Matches - {matched_jobs[0].get('position', 'Jobs')}"
        
        # Attach both plain text and HTML
        msg.attach(MIMEText(email_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))
        
        # Attach JSON file
        json_data = json.dumps({'matched_jobs': matched_jobs}, indent=2)
        attachment = MIMEApplication(json_data, _subtype='json')
        attachment.add_header('Content-Disposition', 'attachment', filename='matched_jobs.json')
        msg.attach(attachment)
        
        # Send email
        print(f"\n   📡 Connecting to {smtp_host}:{smtp_port}...")
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        
        print("   🔐 Logging in...")
        server.login(gmail_user, gmail_password)
        
        print("   📨 Sending email...")
        server.send_message(msg)
        server.quit()
        
        print("\n   ✅ Email sent successfully!")
        return True
        
    except Exception as e:
        print(f"\n   ❌ Failed to send email: {e}")
        import traceback
        traceback.print_exc()
        return False


def display_results(matched_jobs):
    """Display results preview"""
    print_header("📊 TOP MATCHED JOBS")
    
    for i, job in enumerate(matched_jobs[:10], 1):
        print(f"\n{i}. {job.get('position', 'Unknown Position')}")
        print(f"   🏢 Company: {job.get('company', 'Unknown')}")
        print(f"   📍 Location: {job.get('location', 'Unknown')}")
        print(f"   ⭐ Match Score: {job.get('match_score', 0)}/100")
        
        if job.get('match_reason'):
            print(f"   💡 Why: {job.get('match_reason')}")
        
        if job.get('apply_link'):
            print(f"   🔗 Apply: {job.get('apply_link')}")
    
    if len(matched_jobs) > 10:
        print(f"\n... and {len(matched_jobs) - 10} more jobs (check your email)")


def main():
    """Main pipeline"""
    try:
        # Step 1: Get user preferences
        preferences = get_user_preferences()
        
        # Step 2: Search GitHub
        github_jobs = search_github_jobs(
            query=preferences['query'],
            keywords=preferences['keywords'],
            location=preferences['location'],
            limit=50
        )
        
        # Step 3: Search LinkedIn
        linkedin_jobs = search_linkedin_jobs(
            query=preferences['query'],
            keywords=preferences['keywords'],
            location=preferences['location'],
            limit=50
        )
        
        # Combine all jobs
        all_jobs = []
        
        if github_jobs:
            all_jobs.extend(github_jobs)
            print(f"\n✅ Added {len(github_jobs)} GitHub jobs")
        
        if linkedin_jobs:
            all_jobs.extend(linkedin_jobs)
            print(f"✅ Added {len(linkedin_jobs)} LinkedIn jobs")
        
        # Check if we have any jobs
        if not all_jobs:
            print_header("❌ NO JOBS FOUND FROM COLLECTORS")
            print("\n   Both GitHub and LinkedIn collectors returned 0 jobs.")
            print("   Please check:")
            print("   1. Your internet connection")
            print("   2. API keys in .env file")
            print("   3. The collector configurations")
            print("\n   You can also manually run the collectors:")
            print("   - GitHub: cd github_collector && python3 main.py")
            print("   - LinkedIn: cd linkedin_collector && python3 job_searcher.py")
            sys.exit(1)
        
        print(f"\n✅ Total jobs collected: {len(all_jobs)}")
        
        # Step 4: Match jobs with AI
        matched_jobs = match_jobs_with_ai(
            resume_path=preferences['resume_path'],
            all_jobs=all_jobs,
            top_n=preferences['top_n']
        )
        
        if not matched_jobs:
            print("\n❌ No matches found!")
            sys.exit(1)
        
        # Step 5: Display results
        display_results(matched_jobs)
        
        # Step 6: Send email
        send_success = send_email_results(
            recipient=preferences['recipient_email'],
            matched_jobs=matched_jobs
        )
        
        # Final summary
        print_header("✅ PROCESS COMPLETE")
        
        print(f"\n   📊 Total jobs analyzed: {len(all_jobs)}")
        print(f"   🎯 Top matches found: {len(matched_jobs)}")
        
        if send_success:
            print(f"   📧 Email sent to: {preferences['recipient_email']}")
        else:
            print(f"   ⚠️  Email not sent (check configuration)")
        
        print(f"\n   💾 Results saved in: matched_jobs/top_matches.json")
        
        print("\n" + "=" * 70)
        print("   Thank you for using the AI Job Matcher! 🚀")
        print("=" * 70 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Process cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
