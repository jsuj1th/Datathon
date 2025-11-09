#!/usr/bin/env python3
"""
Main Job Search Application
Interactive tool to search for jobs, match with resume, and send results via email
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Any
import logging

# Add NewMCP Folder to path
sys.path.insert(0, str(Path(__file__).parent / "NewMCP Folder"))

from job_matcher import JobMatcher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class JobSearchApp:
    """Main application for job search and matching"""

    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.matcher = JobMatcher()
        self.resume_text = None
        self.matched_jobs = []

    def get_user_input(self) -> Dict[str, Any]:
        """Get user inputs interactively"""
        print("\n" + "=" * 70)
        print("🎯 AI-Powered Job Search & Matching System")
        print("=" * 70)
        print()

        user_data = {}

        # Get resume path
        print("📄 RESUME UPLOAD")
        print("-" * 70)
        default_resume = self.project_dir / "uploads"
        if default_resume.exists():
            pdf_files = list(default_resume.glob("*.pdf"))
            if pdf_files:
                print(f"Found resume: {pdf_files[0].name}")
                use_default = input("Use this resume? (y/n): ").strip().lower()
                if use_default == 'y':
                    user_data['resume_path'] = str(pdf_files[0])
                else:
                    user_data['resume_path'] = input("Enter path to your resume PDF: ").strip()
            else:
                user_data['resume_path'] = input("Enter path to your resume PDF: ").strip()
        else:
            user_data['resume_path'] = input("Enter path to your resume PDF: ").strip()

        print()

        # Get job search keywords
        print("🔍 JOB SEARCH KEYWORDS")
        print("-" * 70)
        print("Enter keywords for the jobs you're looking for (comma-separated)")
        print("Examples: Machine Learning, Data Science, AI Engineer, Python Developer")
        keywords_input = input("Keywords: ").strip()
        user_data['keywords'] = [k.strip() for k in keywords_input.split(',') if k.strip()]

        print()

        # Get location preference
        print("📍 LOCATION PREFERENCE")
        print("-" * 70)
        location = input("Preferred location (or 'Remote'): ").strip()
        user_data['location'] = location if location else "Remote"

        print()

        # Get number of matches
        print("📊 MATCH PREFERENCES")
        print("-" * 70)
        try:
            top_n = int(input("How many top matches to find? (default: 20): ").strip() or "20")
            user_data['top_n'] = top_n
        except ValueError:
            user_data['top_n'] = 20

        print()

        # Get email recipient
        print("📧 EMAIL DELIVERY")
        print("-" * 70)
        send_email = input("Would you like to email the results? (y/n): ").strip().lower()
        if send_email == 'y':
            recipient = input("Recipient email address: ").strip()
            user_data['recipient_email'] = recipient
        else:
            user_data['recipient_email'] = None

        print()
        print("=" * 70)
        print()

        return user_data

    def display_user_query_summary(self, user_data: Dict[str, Any]):
        """Display summary of user's search query"""
        print("\n📋 YOUR SEARCH QUERY")
        print("=" * 70)
        print(f"Resume: {Path(user_data['resume_path']).name}")
        print(f"Keywords: {', '.join(user_data['keywords'])}")
        print(f"Location: {user_data['location']}")
        print(f"Top Matches: {user_data['top_n']}")
        if user_data['recipient_email']:
            print(f"Email Results To: {user_data['recipient_email']}")
        print("=" * 70)
        print()

        confirm = input("Proceed with this search? (y/n): ").strip().lower()
        return confirm == 'y'

    def extract_resume(self, resume_path: str) -> bool:
        """Extract text from resume PDF"""
        print("\n📄 Extracting resume text...")
        try:
            self.resume_text = self.matcher.extract_resume(resume_path)
            if not self.resume_text:
                print("❌ Failed to extract resume text")
                return False
            print(f"✅ Extracted {len(self.resume_text)} characters from resume")
            return True
        except Exception as e:
            print(f"❌ Error extracting resume: {e}")
            return False

    def load_jobs(self) -> List[Dict[str, Any]]:
        """Load jobs from all available sources"""
        print("\n📊 Loading jobs from all sources...")
        
        jobs_dirs = [
            str(self.project_dir / "linkedin_collector" / "job_search_results"),
            str(self.project_dir / "data"),
            str(self.project_dir / "matched_jobs")
        ]

        all_jobs = self.matcher.load_all_jobs(jobs_dirs)
        
        if not all_jobs:
            print("❌ No jobs found in any source")
            print("\n💡 TIP: Run the job collectors first to gather job postings")
            return []
        
        print(f"✅ Loaded {len(all_jobs)} jobs from all sources")
        return all_jobs

    def filter_jobs_by_keywords(self, jobs: List[Dict[str, Any]], keywords: List[str]) -> List[Dict[str, Any]]:
        """Filter jobs by user-specified keywords"""
        if not keywords:
            return jobs

        print(f"\n🔍 Filtering jobs by keywords: {', '.join(keywords)}")
        
        filtered_jobs = []
        keywords_lower = [k.lower() for k in keywords]
        
        for job in jobs:
            # Check if any keyword appears in job title, description, or requirements
            job_text = (
                job.get('position', '') + ' ' +
                job.get('description', '') + ' ' +
                job.get('requirements', '') + ' ' +
                job.get('field', '')
            ).lower()
            
            if any(keyword in job_text for keyword in keywords_lower):
                filtered_jobs.append(job)
        
        print(f"✅ Found {len(filtered_jobs)} jobs matching your keywords")
        return filtered_jobs

    def match_jobs(self, jobs: List[Dict[str, Any]], top_n: int) -> List[Dict[str, Any]]:
        """Match jobs with resume using AI"""
        print(f"\n🤖 Matching {len(jobs)} jobs with your resume using AI...")
        print("   This may take a moment...")
        
        try:
            matched_jobs = self.matcher.match_jobs_with_llm(
                self.resume_text, 
                jobs, 
                top_n=top_n
            )
            
            print(f"✅ Found top {len(matched_jobs)} matches")
            self.matched_jobs = matched_jobs
            return matched_jobs
        
        except Exception as e:
            print(f"❌ Error during matching: {e}")
            return []

    def display_results(self, matched_jobs: List[Dict[str, Any]]):
        """Display matched job results"""
        if not matched_jobs:
            print("\n❌ No matches found")
            return

        print("\n" + "=" * 70)
        print(f"🎯 TOP {len(matched_jobs)} JOB MATCHES")
        print("=" * 70)
        print()

        for i, job in enumerate(matched_jobs[:10], 1):  # Show top 10
            print(f"{i}. {job.get('position', 'Unknown Position')}")
            print(f"   Company: {job.get('company', 'Unknown Company')}")
            print(f"   Location: {job.get('location', 'Unknown')}")
            print(f"   Match Score: {job.get('match_score', 0)}/100")
            
            reason = job.get('match_reason', '')
            if reason:
                # Truncate long reasons
                reason_display = reason[:100] + "..." if len(reason) > 100 else reason
                print(f"   Why: {reason_display}")
            
            apply_link = job.get('apply_link', 'N/A')
            if apply_link != 'N/A':
                print(f"   Apply: {apply_link}")
            
            print()

        if len(matched_jobs) > 10:
            print(f"   ... and {len(matched_jobs) - 10} more matches")
            print()

        print("=" * 70)

    def save_results(self, matched_jobs: List[Dict[str, Any]]) -> str:
        """Save matched jobs to JSON file"""
        print("\n💾 Saving results...")
        
        output_dir = self.project_dir / "matched_jobs"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / "latest_matches.json"
        
        try:
            self.matcher.save_matched_jobs(matched_jobs, str(output_file))
            print(f"✅ Results saved to: {output_file}")
            return str(output_file)
        except Exception as e:
            print(f"❌ Error saving results: {e}")
            return ""

    def send_email(self, recipient: str, matched_jobs: List[Dict[str, Any]]):
        """Send matched jobs via email"""
        print(f"\n📧 Sending results to {recipient}...")
        
        try:
            # Prepare email content
            email_content = self.matcher.prepare_email_content(matched_jobs)
            
            # Try to import and use email sender
            try:
                from send_email_smtp import send_job_email
                
                success = send_job_email(
                    recipient_email=recipient,
                    job_data=matched_jobs,
                    subject="Your AI-Matched Job Opportunities"
                )
                
                if success:
                    print(f"✅ Email sent successfully to {recipient}")
                else:
                    print(f"⚠️  Email sending failed. Results saved locally.")
                    
            except ImportError:
                print("⚠️  Email module not available. Results saved locally.")
                print("\n📄 Email Preview:")
                print("-" * 70)
                print(email_content[:500] + "..." if len(email_content) > 500 else email_content)
                
        except Exception as e:
            print(f"❌ Error sending email: {e}")

    def run(self):
        """Main application flow"""
        try:
            # Get user input
            user_data = self.get_user_input()
            
            # Display summary and confirm
            if not self.display_user_query_summary(user_data):
                print("\n❌ Search cancelled by user")
                return
            
            # Extract resume
            if not self.extract_resume(user_data['resume_path']):
                return
            
            # Load jobs
            all_jobs = self.load_jobs()
            if not all_jobs:
                return
            
            # Filter by keywords
            filtered_jobs = self.filter_jobs_by_keywords(all_jobs, user_data['keywords'])
            if not filtered_jobs:
                print("\n⚠️  No jobs found matching your keywords")
                return
            
            # Match jobs with resume
            matched_jobs = self.match_jobs(filtered_jobs, user_data['top_n'])
            if not matched_jobs:
                return
            
            # Display results
            self.display_results(matched_jobs)
            
            # Save results
            output_file = self.save_results(matched_jobs)
            
            # Send email if requested
            if user_data['recipient_email']:
                self.send_email(user_data['recipient_email'], matched_jobs)
            
            # Final summary
            print("\n" + "=" * 70)
            print("✅ JOB SEARCH COMPLETE!")
            print("=" * 70)
            print(f"📊 Found {len(matched_jobs)} matches")
            if output_file:
                print(f"💾 Saved to: {output_file}")
            if user_data['recipient_email']:
                print(f"📧 Emailed to: {user_data['recipient_email']}")
            print("=" * 70)
            print()
            
        except KeyboardInterrupt:
            print("\n\n❌ Search cancelled by user")
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            print(f"\n❌ An error occurred: {e}")


def main():
    """Entry point"""
    app = JobSearchApp()
    app.run()


if __name__ == "__main__":
    main()
