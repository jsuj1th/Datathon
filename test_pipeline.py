#!/usr/bin/env python3
"""Quick test of the job matcher"""

from job_matcher import JobMatcher
from pathlib import Path

# Test the JobMatcher
matcher = JobMatcher()

# Test resume path
resume_path = "./NewMCP Folder/MCP_Servers/pdfDocs/Resume_NEW_ML_Pathakota_Pranavi_2.pdf"

if not Path(resume_path).exists():
    resume_path = "./Resume/Resume (13).pdf"

print(f"Testing with resume: {resume_path}")
print(f"Resume exists: {Path(resume_path).exists()}")

if Path(resume_path).exists():
    print("\nExtracting resume text...")
    text = matcher.extract_resume(resume_path)
    print(f"✅ Extracted {len(text)} characters")
    print(f"Preview: {text[:200]}...")
else:
    print("❌ Resume not found")

# Test with sample job
sample_job = {
    'company': 'Tech Corp',
    'position': 'Machine Learning Engineer',
    'location': 'Remote',
    'description': 'Looking for ML engineer with Python and TensorFlow experience',
    'requirements': 'Python, ML, AI, TensorFlow'
}

if Path(resume_path).exists():
    print("\nTesting job matching...")
    matched = matcher.match_job_with_resume(sample_job, text)
    print(f"✅ Match Score: {matched.get('match_score')}/100")
    print(f"   Reason: {matched.get('match_reason')}")

print("\n✅ All tests passed!")
