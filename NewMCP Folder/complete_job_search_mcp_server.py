#!/usr/bin/env python3
"""
Complete Job Search MCP Server
Provides comprehensive job search tools via MCP protocol
"""

import json
import sys
import os
from pathlib import Path
from typing import Any, Sequence
import asyncio
import logging

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Import MCP SDK
from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
import mcp.server.stdio

# Import job search components
from job_matcher import JobMatcher
from dotenv import load_dotenv

# Load environment
load_dotenv(parent_dir / ".env")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

# Initialize MCP Server
app = Server("complete-job-search-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available job search tools"""
    return [
        Tool(
            name="search_jobs_complete",
            description=(
                "Complete job search pipeline that searches GitHub and LinkedIn, "
                "matches with resume, and returns ranked results. "
                "This is the main tool that orchestrates everything."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "string",
                        "description": "Job search keywords (e.g., 'Machine Learning Engineer', 'Data Scientist')"
                    },
                    "location": {
                        "type": "string",
                        "description": "Location preference (e.g., 'Remote', 'San Francisco', 'New York')",
                        "default": "Remote"
                    },
                    "experience_level": {
                        "type": "string",
                        "description": "Experience level: entry, junior, mid, senior, lead",
                        "enum": ["entry", "junior", "mid", "senior", "lead"],
                        "default": "mid"
                    },
                    "resume_path": {
                        "type": "string",
                        "description": "Path to resume PDF file"
                    },
                    "top_n": {
                        "type": "number",
                        "description": "Number of top matches to return",
                        "default": 20
                    },
                    "search_limit": {
                        "type": "number",
                        "description": "Number of jobs to search from each source",
                        "default": 50
                    }
                },
                "required": ["keywords", "resume_path"]
            }
        ),
        Tool(
            name="search_github_jobs",
            description="Search for jobs on GitHub using keywords and filters",
            inputSchema={
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "string",
                        "description": "Job search keywords"
                    },
                    "location": {
                        "type": "string",
                        "description": "Location filter (optional)",
                        "default": ""
                    },
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of jobs to return",
                        "default": 50
                    }
                },
                "required": ["keywords"]
            }
        ),
        Tool(
            name="search_linkedin_jobs",
            description="Search for jobs on LinkedIn/The Muse using keywords and location",
            inputSchema={
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "string",
                        "description": "Job search keywords"
                    },
                    "location": {
                        "type": "string",
                        "description": "Location filter",
                        "default": "Remote"
                    },
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of jobs to return",
                        "default": 50
                    }
                },
                "required": ["keywords"]
            }
        ),
        Tool(
            name="match_jobs_with_resume",
            description="Match a list of jobs with resume using AI and return ranked results",
            inputSchema={
                "type": "object",
                "properties": {
                    "resume_path": {
                        "type": "string",
                        "description": "Path to resume PDF file"
                    },
                    "jobs": {
                        "type": "array",
                        "description": "Array of job objects to match",
                        "items": {
                            "type": "object"
                        }
                    },
                    "top_n": {
                        "type": "number",
                        "description": "Number of top matches to return",
                        "default": 20
                    }
                },
                "required": ["resume_path", "jobs"]
            }
        ),
        Tool(
            name="extract_resume_text",
            description="Extract text content from a PDF resume",
            inputSchema={
                "type": "object",
                "properties": {
                    "resume_path": {
                        "type": "string",
                        "description": "Path to resume PDF file"
                    }
                },
                "required": ["resume_path"]
            }
        ),
        Tool(
            name="send_job_email",
            description="Send matched jobs via email to recipient",
            inputSchema={
                "type": "object",
                "properties": {
                    "recipient_email": {
                        "type": "string",
                        "description": "Recipient email address"
                    },
                    "matched_jobs": {
                        "type": "array",
                        "description": "Array of matched job objects",
                        "items": {
                            "type": "object"
                        }
                    },
                    "subject": {
                        "type": "string",
                        "description": "Email subject line",
                        "default": "Your Top Job Matches"
                    }
                },
                "required": ["recipient_email", "matched_jobs"]
            }
        ),
        Tool(
            name="filter_jobs_by_criteria",
            description="Filter jobs by experience level, location, keywords, etc.",
            inputSchema={
                "type": "object",
                "properties": {
                    "jobs": {
                        "type": "array",
                        "description": "Array of job objects to filter",
                        "items": {
                            "type": "object"
                        }
                    },
                    "experience_level": {
                        "type": "string",
                        "description": "Experience level filter",
                        "enum": ["entry", "junior", "mid", "senior", "lead"]
                    },
                    "location": {
                        "type": "string",
                        "description": "Location filter (partial match)"
                    },
                    "keywords": {
                        "type": "array",
                        "description": "Keywords that must appear in job (any match)",
                        "items": {
                            "type": "string"
                        }
                    },
                    "min_match_score": {
                        "type": "number",
                        "description": "Minimum match score (0-100)",
                        "default": 0
                    }
                },
                "required": ["jobs"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls"""
    
    try:
        if name == "search_jobs_complete":
            return await search_jobs_complete(arguments)
        
        elif name == "search_github_jobs":
            return await search_github_jobs_tool(arguments)
        
        elif name == "search_linkedin_jobs":
            return await search_linkedin_jobs_tool(arguments)
        
        elif name == "match_jobs_with_resume":
            return await match_jobs_with_resume_tool(arguments)
        
        elif name == "extract_resume_text":
            return await extract_resume_text_tool(arguments)
        
        elif name == "send_job_email":
            return await send_job_email_tool(arguments)
        
        elif name == "filter_jobs_by_criteria":
            return await filter_jobs_by_criteria_tool(arguments)
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except Exception as e:
        logger.error(f"Error in tool {name}: {e}", exc_info=True)
        return [TextContent(
            type="text",
            text=json.dumps({
                "success": False,
                "error": str(e),
                "tool": name
            }, indent=2)
        )]


async def search_jobs_complete(args: dict) -> Sequence[TextContent]:
    """Complete job search pipeline"""
    keywords = args.get("keywords")
    location = args.get("location", "Remote")
    experience_level = args.get("experience_level", "mid")
    resume_path = args.get("resume_path")
    top_n = args.get("top_n", 20)
    search_limit = args.get("search_limit", 50)
    
    logger.info(f"🎯 Complete job search: {keywords} @ {location} ({experience_level})")
    
    result = {
        "success": False,
        "search_params": {
            "keywords": keywords,
            "location": location,
            "experience_level": experience_level,
            "top_n": top_n
        },
        "jobs_found": {
            "github": 0,
            "linkedin": 0,
            "total": 0
        },
        "matched_jobs": []
    }
    
    try:
        all_jobs = []
        
        # Step 1: Search GitHub
        logger.info("🔎 Searching GitHub...")
        try:
            from github_collector.firecrawl_search import search_github_with_firecrawl
            github_jobs = search_github_with_firecrawl(keywords, location, search_limit)
            all_jobs.extend(github_jobs)
            result["jobs_found"]["github"] = len(github_jobs)
            logger.info(f"✅ Found {len(github_jobs)} GitHub jobs")
        except Exception as e:
            logger.warning(f"⚠️ GitHub search failed: {e}")
        
        # Step 2: Search LinkedIn
        logger.info("🔎 Searching LinkedIn...")
        try:
            from linkedin_collector.job_searcher import JobSearcher
            searcher = JobSearcher()
            linkedin_jobs = await searcher.search_jobs(
                keywords=keywords,
                location=location,
                limit=search_limit
            )
            all_jobs.extend(linkedin_jobs)
            result["jobs_found"]["linkedin"] = len(linkedin_jobs)
            logger.info(f"✅ Found {len(linkedin_jobs)} LinkedIn jobs")
        except Exception as e:
            logger.warning(f"⚠️ LinkedIn search failed: {e}")
        
        result["jobs_found"]["total"] = len(all_jobs)
        
        if not all_jobs:
            result["error"] = "No jobs found from any source"
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        # Step 3: Filter by experience level
        filtered_jobs = []
        for job in all_jobs:
            job_exp = str(job.get('experience_level', '')).lower()
            if experience_level.lower() in job_exp or job_exp == 'not_specified' or not job_exp:
                filtered_jobs.append(job)
        
        if not filtered_jobs:
            filtered_jobs = all_jobs  # Use all if filter too restrictive
        
        logger.info(f"📊 Filtered to {len(filtered_jobs)} jobs matching {experience_level} level")
        
        # Step 4: Match with resume using AI
        logger.info("🤖 Matching with resume using AI...")
        matcher = JobMatcher()
        
        # Extract resume
        resume_text = matcher.extract_resume(resume_path)
        if not resume_text:
            result["error"] = "Failed to extract resume text"
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        
        # Match jobs
        matched_jobs = matcher.match_jobs_with_llm(resume_text, filtered_jobs, top_n=top_n)
        
        result["success"] = True
        result["matched_jobs"] = matched_jobs
        result["top_match_score"] = matched_jobs[0].get("match_score", 0) if matched_jobs else 0
        
        logger.info(f"✅ Complete! Found {len(matched_jobs)} top matches")
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    except Exception as e:
        result["error"] = str(e)
        logger.error(f"❌ Error in complete search: {e}", exc_info=True)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def search_github_jobs_tool(args: dict) -> Sequence[TextContent]:
    """Search GitHub for jobs"""
    keywords = args.get("keywords")
    location = args.get("location", "")
    limit = args.get("limit", 50)
    
    try:
        from github_collector.firecrawl_search import search_github_with_firecrawl
        jobs = search_github_with_firecrawl(keywords, location, limit)
        
        return [TextContent(type="text", text=json.dumps({
            "success": True,
            "source": "github",
            "jobs_found": len(jobs),
            "jobs": jobs
        }, indent=2))]
    
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2))]


async def search_linkedin_jobs_tool(args: dict) -> Sequence[TextContent]:
    """Search LinkedIn for jobs"""
    keywords = args.get("keywords")
    location = args.get("location", "Remote")
    limit = args.get("limit", 50)
    
    try:
        from linkedin_collector.job_searcher import JobSearcher
        searcher = JobSearcher()
        jobs = await searcher.search_jobs(keywords=keywords, location=location, limit=limit)
        
        return [TextContent(type="text", text=json.dumps({
            "success": True,
            "source": "linkedin",
            "jobs_found": len(jobs),
            "jobs": jobs
        }, indent=2))]
    
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2))]


async def match_jobs_with_resume_tool(args: dict) -> Sequence[TextContent]:
    """Match jobs with resume"""
    resume_path = args.get("resume_path")
    jobs = args.get("jobs", [])
    top_n = args.get("top_n", 20)
    
    try:
        matcher = JobMatcher()
        resume_text = matcher.extract_resume(resume_path)
        
        if not resume_text:
            return [TextContent(type="text", text=json.dumps({
                "success": False,
                "error": "Failed to extract resume text"
            }, indent=2))]
        
        matched_jobs = matcher.match_jobs_with_llm(resume_text, jobs, top_n=top_n)
        
        return [TextContent(type="text", text=json.dumps({
            "success": True,
            "jobs_analyzed": len(jobs),
            "matches_found": len(matched_jobs),
            "matched_jobs": matched_jobs
        }, indent=2))]
    
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2))]


async def extract_resume_text_tool(args: dict) -> Sequence[TextContent]:
    """Extract text from resume"""
    resume_path = args.get("resume_path")
    
    try:
        matcher = JobMatcher()
        text = matcher.extract_resume(resume_path)
        
        return [TextContent(type="text", text=json.dumps({
            "success": True,
            "characters": len(text),
            "preview": text[:500],
            "full_text": text
        }, indent=2))]
    
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2))]


async def send_job_email_tool(args: dict) -> Sequence[TextContent]:
    """Send jobs via email"""
    recipient_email = args.get("recipient_email")
    matched_jobs = args.get("matched_jobs", [])
    subject = args.get("subject", f"Your Top {len(matched_jobs)} Job Matches")
    
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from email.mime.application import MIMEApplication
        
        smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        gmail_user = os.getenv('GMAIL_USER')
        gmail_password = os.getenv('GMAIL_APP_PASSWORD')
        
        if not gmail_user or not gmail_password:
            return [TextContent(type="text", text=json.dumps({
                "success": False,
                "error": "Email credentials not configured"
            }, indent=2))]
        
        # Create email content
        matcher = JobMatcher()
        email_content = matcher.prepare_email_content(matched_jobs)
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(email_content, 'plain'))
        
        # Attach JSON
        json_data = json.dumps({'matched_jobs': matched_jobs}, indent=2)
        attachment = MIMEApplication(json_data, _subtype='json')
        attachment.add_header('Content-Disposition', 'attachment', filename='matched_jobs.json')
        msg.attach(attachment)
        
        # Send
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.send_message(msg)
        server.quit()
        
        return [TextContent(type="text", text=json.dumps({
            "success": True,
            "recipient": recipient_email,
            "jobs_sent": len(matched_jobs)
        }, indent=2))]
    
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2))]


async def filter_jobs_by_criteria_tool(args: dict) -> Sequence[TextContent]:
    """Filter jobs by various criteria"""
    jobs = args.get("jobs", [])
    experience_level = args.get("experience_level")
    location = args.get("location")
    keywords = args.get("keywords", [])
    min_match_score = args.get("min_match_score", 0)
    
    try:
        filtered = []
        
        for job in jobs:
            # Check experience level
            if experience_level:
                job_exp = str(job.get('experience_level', '')).lower()
                if experience_level.lower() not in job_exp and job_exp != 'not_specified':
                    continue
            
            # Check location
            if location:
                job_loc = str(job.get('location', '')).lower()
                if location.lower() not in job_loc:
                    continue
            
            # Check keywords
            if keywords:
                job_text = f"{job.get('position', '')} {job.get('description', '')} {job.get('requirements', '')}".lower()
                if not any(kw.lower() in job_text for kw in keywords):
                    continue
            
            # Check match score
            if min_match_score > 0:
                score = job.get('match_score', 0)
                if score < min_match_score:
                    continue
            
            filtered.append(job)
        
        return [TextContent(type="text", text=json.dumps({
            "success": True,
            "original_count": len(jobs),
            "filtered_count": len(filtered),
            "jobs": filtered
        }, indent=2))]
    
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2))]


async def main():
    """Run the MCP server"""
    logger.info("🚀 Complete Job Search MCP Server starting...")
    logger.info("📡 Waiting for MCP requests on stdin...")
    
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
