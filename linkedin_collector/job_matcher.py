#!/usr/bin/env python3
"""
Job Matcher - LLM-based Resume to Job Matching System
Matches resume with collected jobs and ranks top 50 matches
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import PyPDF2
except ImportError:
    logger.warning("PyPDF2 not installed. Install with: pip install PyPDF2")
    PyPDF2 = None

try:
    import google.generativeai as genai
except ImportError:
    logger.warning("Google Generative AI not installed. Install with: pip install google-generativeai")
    genai = None


class JobMatcher:
    """Match resume with jobs using LLM"""

    def __init__(self, gemini_api_key: str = None):
        self.gemini_api_key = gemini_api_key or os.getenv('GEMINI_API_KEY')

        if self.gemini_api_key and genai:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            logger.info("✅ Gemini API initialized")
        else:
            self.model = None
            logger.warning("⚠️  Gemini API not available")

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF resume"""
        try:
            if not PyPDF2:
                return "PDF extraction not available - PyPDF2 not installed"

            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"

                logger.info(f"✅ Extracted {len(text)} characters from resume PDF")
                return text.strip()

        except Exception as e:
            logger.error(f"Error extracting PDF text: {e}")
            return ""

    def load_all_jobs(self, jobs_dir: str) -> List[Dict[str, Any]]:
        """Load all jobs from JSON files in directory"""
        try:
            jobs_path = Path(jobs_dir)
            all_jobs = []

            if not jobs_path.exists():
                logger.error(f"Jobs directory not found: {jobs_dir}")
                return []

            # Load all JSON files
            json_files = list(jobs_path.glob("*.json"))
            logger.info(f"Found {len(json_files)} JSON files")

            for json_file in json_files:
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                        # Extract jobs from the file
                        jobs = data.get('jobs', [])
                        all_jobs.extend(jobs)
                        logger.info(f"Loaded {len(jobs)} jobs from {json_file.name}")

                except Exception as e:
                    logger.warning(f"Failed to load {json_file.name}: {e}")
                    continue

            logger.info(f"✅ Total jobs loaded: {len(all_jobs)}")
            return all_jobs

        except Exception as e:
            logger.error(f"Error loading jobs: {e}")
            return []

    def match_jobs_with_llm(self, resume_text: str, jobs: List[Dict[str, Any]], top_n: int = 50) -> List[Dict[str, Any]]:
        """Use LLM to match resume with jobs and rank top N"""
        try:
            if not self.model:
                logger.error("Gemini model not available")
                return self._fallback_matching(resume_text, jobs, top_n)

            logger.info(f"🤖 Using Gemini to match {len(jobs)} jobs with resume")

            # Create job summaries for LLM (to reduce token usage)
            job_summaries = []
            for i, job in enumerate(jobs):
                summary = {
                    "index": i,
                    "company": job.get('company', 'Unknown'),
                    "position": job.get('position', 'Unknown'),
                    "location": job.get('location', 'Unknown'),
                    "description": job.get('description', '')[:300],  # First 300 chars
                    "requirements": job.get('requirements', ''),
                    "experience_level": job.get('experience_level', ''),
                    "field": job.get('field', '')
                }
                job_summaries.append(summary)

            # Split into batches to avoid token limits
            batch_size = 20
            all_matches = []

            for batch_num in range(0, len(job_summaries), batch_size):
                batch = job_summaries[batch_num:batch_num + batch_size]

                prompt = f"""You are an expert job matcher. Analyze this resume and rank these jobs by relevance.

RESUME:
{resume_text[:3000]}

JOBS TO RANK:
{json.dumps(batch, indent=2)}

TASK:
For each job, provide:
1. Match score (0-100, where 100 is perfect match)
2. Brief reason (one sentence)

Consider:
- Skills match
- Experience level
- Job field/domain
- Location preferences
- Job requirements

Respond in JSON format ONLY:
{{
  "matches": [
    {{
      "index": 0,
      "score": 85,
      "reason": "Strong Python and ML skills match, relevant experience"
    }},
    ...
  ]
}}
"""

                try:
                    response = self.model.generate_content(prompt)
                    result_text = response.text.strip()

                    # Extract JSON from response
                    if "```json" in result_text:
                        result_text = result_text.split("```json")[1].split("```")[0]
                    elif "```" in result_text:
                        result_text = result_text.split("```")[1].split("```")[0]

                    result = json.loads(result_text)
                    all_matches.extend(result.get('matches', []))

                    logger.info(f"✅ Processed batch {batch_num//batch_size + 1}")

                except Exception as e:
                    logger.warning(f"Failed to process batch: {e}")
                    continue

            # Sort by score and get top N
            all_matches.sort(key=lambda x: x.get('score', 0), reverse=True)
            top_matches = all_matches[:top_n]

            # Map back to original jobs
            matched_jobs = []
            for match in top_matches:
                idx = match['index']
                if idx < len(jobs):
                    job = jobs[idx].copy()
                    job['match_score'] = match.get('score', 0)
                    job['match_reason'] = match.get('reason', '')
                    matched_jobs.append(job)

            logger.info(f"✅ Matched top {len(matched_jobs)} jobs")
            return matched_jobs

        except Exception as e:
            logger.error(f"Error in LLM matching: {e}")
            return self._fallback_matching(resume_text, jobs, top_n)

    def _fallback_matching(self, resume_text: str, jobs: List[Dict[str, Any]], top_n: int) -> List[Dict[str, Any]]:
        """Simple keyword-based matching as fallback"""
        logger.info("Using fallback keyword matching")

        # Extract keywords from resume
        resume_lower = resume_text.lower()
        keywords = ['python', 'machine learning', 'ai', 'data', 'software', 'engineer', 'ml', 'deep learning']

        # Score each job
        scored_jobs = []
        for job in jobs:
            score = 0
            desc = job.get('description', '') or ''
            reqs = job.get('requirements', '') or ''
            description = (desc + ' ' + reqs).lower()

            for keyword in keywords:
                if keyword in resume_lower and keyword in description:
                    score += 10

            job_copy = job.copy()
            job_copy['match_score'] = score
            job_copy['match_reason'] = 'Keyword-based match (fallback)'
            scored_jobs.append(job_copy)

        # Sort and return top N
        scored_jobs.sort(key=lambda x: x.get('match_score', 0), reverse=True)
        return scored_jobs[:top_n]

    def save_matched_jobs(self, matched_jobs: List[Dict[str, Any]], output_file: str):
        """Save matched jobs to JSON file"""
        try:
            output_data = {
                "total_matches": len(matched_jobs),
                "matched_jobs": matched_jobs,
                "generated_at": __import__('datetime').datetime.now().isoformat()
            }

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)

            logger.info(f"✅ Saved matched jobs to {output_file}")

        except Exception as e:
            logger.error(f"Error saving matched jobs: {e}")

    def prepare_email_content(self, matched_jobs: List[Dict[str, Any]]) -> str:
        """Prepare email content with top matched jobs"""
        email_body = "🎯 Top Job Matches Based on Your Resume\n"
        email_body += "=" * 60 + "\n\n"

        for i, job in enumerate(matched_jobs, 1):
            email_body += f"{i}. {job.get('position', 'Unknown Position')}\n"
            email_body += f"   Company: {job.get('company', 'Unknown Company')}\n"
            email_body += f"   Location: {job.get('location', 'Unknown')}\n"
            email_body += f"   Match Score: {job.get('match_score', 0)}/100\n"

            if job.get('match_reason'):
                email_body += f"   Reason: {job['match_reason']}\n"

            email_body += f"   Apply: {job.get('apply_link', 'No link')}\n"
            email_body += "\n"

        email_body += "\n" + "=" * 60 + "\n"
        email_body += "🤖 Generated by Job Matcher AI\n"

        return email_body


def main():
    """Main function"""
    print("🎯 Job Matcher - Resume to Job Matching System")
    print("=" * 60)

    # Paths
    resume_pdf = "/Users/pranavi/Documents/Courses/Programming_LLMs/Project/MCP_Servers/pdfDocs/Resume_NEW_ML_Pathakota_Pranavi_2.pdf"
    jobs_dir = "/Users/pranavi/Documents/Courses/Programming_LLMs/Project/Datathon/job_search_results"
    output_file = "/Users/pranavi/Documents/Courses/Programming_LLMs/Project/Datathon/matched_jobs/top_50_matches.json"

    # Create output directory
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Initialize matcher
    matcher = JobMatcher()

    # Step 1: Extract resume text
    print("\n📄 Step 1: Extracting resume text...")
    resume_text = matcher.extract_text_from_pdf(resume_pdf)
    if not resume_text:
        print("❌ Failed to extract resume text")
        return
    print(f"✅ Extracted {len(resume_text)} characters")

    # Step 2: Load all jobs
    print("\n📊 Step 2: Loading collected jobs...")
    all_jobs = matcher.load_all_jobs(jobs_dir)
    if not all_jobs:
        print("❌ No jobs found")
        return
    print(f"✅ Loaded {len(all_jobs)} jobs")

    # Step 3: Match with LLM
    print("\n🤖 Step 3: Matching jobs with resume using LLM...")
    top_matches = matcher.match_jobs_with_llm(resume_text, all_jobs, top_n=50)
    print(f"✅ Found top {len(top_matches)} matches")

    # Step 4: Save results
    print("\n💾 Step 4: Saving matched jobs...")
    matcher.save_matched_jobs(top_matches, output_file)

    # Step 5: Display preview
    print("\n📋 Top 10 Matches Preview:")
    print("=" * 60)
    for i, job in enumerate(top_matches[:10], 1):
        print(f"{i}. {job.get('position')} at {job.get('company')}")
        print(f"   Score: {job.get('match_score')}/100 - {job.get('match_reason', 'N/A')[:50]}")
        print(f"   Link: {job.get('apply_link')}\n")

    # Step 6: Prepare email content
    print("\n📧 Step 6: Email content prepared")
    print("=" * 60)
    print(f"✅ Output saved to: {output_file}")
    print(f"✅ Ready to send via Gmail MCP!")

    return output_file


if __name__ == "__main__":
    main()
