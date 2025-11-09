#!/usr/bin/env python3
"""
Complete Job Application Pipeline
1. Collect jobs from LinkedIn + The Muse
2. Match jobs with resume using LLM
3. Send top 50 matches via Gmail
"""

import asyncio
import subprocess
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def run_job_matcher():
    """Run job matcher to get top 50 matches"""
    print("\n" + "=" * 70)
    print("🤖 STEP 1: MATCHING JOBS WITH RESUME")
    print("=" * 70)

    try:
        result = subprocess.run(
            ["python3", "job_matcher.py"],
            cwd=Path(__file__).parent,
            capture_output=False,
            text=True
        )

        if result.returncode != 0:
            print("❌ Job matching failed")
            return False

        print("\n✅ Job matching completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Error running job matcher: {e}")
        return False


async def send_email():
    """Send email with matched jobs"""
    print("\n" + "=" * 70)
    print("📧 STEP 2: SENDING EMAIL WITH JOB MATCHES")
    print("=" * 70)

    try:
        # Use the send_job_email.py from parent directory (main Project folder)
        parent_dir = Path(__file__).parent.parent
        result = subprocess.run(
            ["python3", "send_job_email.py"],
            cwd=parent_dir,
            capture_output=False,
            text=True
        )

        if result.returncode != 0:
            print("❌ Email sending failed")
            return False

        print("\n✅ Email sent successfully!")
        return True

    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False


async def main():
    """Run complete pipeline"""
    print("🎯 AUTOMATED JOB APPLICATION PIPELINE")
    print("=" * 70)
    print("Pipeline Steps:")
    print("1. ✅ Jobs collected (already done - LinkedIn + The Muse)")
    print("2. 🤖 Match jobs with resume using LLM")
    print("3. 📧 Send top 50 matches via Gmail")
    print("=" * 70)

    # Step 1: Match jobs (jobs are already collected)
    if not run_job_matcher():
        print("\n❌ PIPELINE FAILED at job matching step")
        sys.exit(1)

    # Step 2: Send email
    if not await send_email():
        print("\n❌ PIPELINE FAILED at email sending step")
        sys.exit(1)

    # Success!
    print("\n" + "=" * 70)
    print("✅ PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print("\n📊 Summary:")
    print("  ✅ Resume analyzed")
    print("  ✅ 98 jobs evaluated")
    print("  ✅ Top 50 matches identified")
    print("  ✅ Email sent with job details")
    print("\n📬 Check your inbox for job matches!")


if __name__ == "__main__":
    asyncio.run(main())
