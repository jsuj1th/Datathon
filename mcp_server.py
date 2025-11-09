#!/usr/bin/env python3
"""
Jobs MCP Server
A Model Context Protocol server that provides LinkedIn simulation and The Muse Jobs API integration.
"""

import asyncio
import json
import logging
import os
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    import fastmcp
    from fastmcp import mcp
except ImportError:
    # For testing without fastmcp
    class MockMCP:
        def tool(self, func):
            return func
    mcp = MockMCP()

# Import job searcher
try:
    from job_searcher import JobSearcher, search_jobs_enhanced
    JOB_SEARCHER_AVAILABLE = True
except ImportError:
    JOB_SEARCHER_AVAILABLE = False
    logging.warning("Job searcher not available")

# Import PDF parser
try:
    from pdf_parser import PDFParser
    PDF_PARSER_AVAILABLE = True
except ImportError:
    PDF_PARSER_AVAILABLE = False
    logging.warning("PDF parser not available")

# Import keyword generator
try:
    from keyword_generator import KeywordGenerator
    KEYWORD_GENERATOR_AVAILABLE = True
except ImportError:
    KEYWORD_GENERATOR_AVAILABLE = False
    logging.warning("Keyword generator not available")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP app
app = fastmcp.FastMCP("Jobs MCP Server")

def search_linkedin_jobs(keywords: str, limit: int = 10, offset: int = 0, location: str = '') -> str:
    """
    Search for jobs on LinkedIn (simulated with realistic data).
    
    Args:
        keywords: Job search keywords (e.g., "software engineer", "data scientist")
        limit: Maximum number of job results (default: 10)
        offset: Number of jobs to skip (default: 0)
        location: Optional location filter (e.g., "San Francisco", "Remote")
        
    Returns:
        JSON string with structured LinkedIn-style job data
    """
    try:
        logger.info(f"LinkedIn search: {keywords} in {location}, limit={limit}")
        
        # Simulate LinkedIn job data structure
        jobs = []
        
        # Define job templates based on keywords
        if "software" in keywords.lower() or "engineer" in keywords.lower():
            companies = ["Google", "Meta", "Apple", "Microsoft", "Amazon", "Netflix", "Uber", "Airbnb"]
            titles = ["Senior Software Engineer", "Software Engineer II", "Full Stack Engineer", "Backend Engineer"]
        elif "data" in keywords.lower() or "scientist" in keywords.lower():
            companies = ["Meta", "Google", "Netflix", "Spotify", "Palantir", "DataBricks", "Snowflake"]
            titles = ["Senior Data Scientist", "Data Scientist II", "ML Engineer", "Data Engineer"]
        else:
            companies = ["TechCorp", "InnovateCo", "StartupXYZ", "BigTech Inc"]
            titles = ["Engineer", "Developer", "Analyst", "Specialist"]
        
        # Generate realistic job listings
        for i in range(min(limit, 20)):
            job_id = f"linkedin_{i + offset + 1}"
            title = titles[i % len(titles)]
            company = companies[i % len(companies)]
            job_location = location if location else ["San Francisco, CA", "New York, NY", "Remote", "Seattle, WA"][i % 4]
            
            # Determine experience level and job type
            experience_level = "senior_level" if "senior" in title.lower() else "mid_level"
            remote_option = "remote" if job_location == "Remote" else "onsite"
            
            # Calculate days since posted
            days_ago = random.randint(1, 7)  # LinkedIn jobs are usually recent
            
            job = {
                "company": company,
                "position": title,
                "apply_link": f"https://linkedin.com/jobs/view/{job_id}",
                "location": job_location,
                "salary": "$120,000 - $180,000" if "senior" in title.lower() else "$90,000 - $140,000",
                "description": f"We are seeking a talented {title} to join our dynamic team. This role offers excellent opportunities for growth and impact.",
                "requirements": ", ".join(["Python", "JavaScript", "AWS", "Docker"] if "software" in keywords.lower() else ["SQL", "Python", "Machine Learning", "Statistics"]),
                "benefits": "Health insurance, 401k, Stock options, Flexible PTO, Remote work",
                "job_type": "full_time",
                "experience_level": experience_level,
                "posted_date": datetime.now().strftime("%Y-%m-%d"),
                "deadline": None,
                "days_since_posted": days_ago,
                "remote_option": remote_option,
                "visa_sponsorship": True,
                "source": f"linkedin/{job_id}",
                "collection_method": "mcp_linkedin_simulation",
                "collected_at": datetime.now().isoformat(),
                "field": "Software Engineering" if "software" in keywords.lower() or "engineer" in keywords.lower() else "AI/ML" if "data" in keywords.lower() else "Technology",
                "company_type": "big_tech" if company in ["Google", "Meta", "Apple", "Microsoft", "Amazon", "Netflix"] else "startup"
            }
            
            jobs.append(job)
        
        result = {
            "search_query": {
                "keywords": keywords,
                "location": location,
                "limit": limit,
                "offset": offset
            },
            "total_results": len(jobs),
            "jobs": jobs,
            "source": "linkedin_simulation",
            "generated_at": datetime.now().isoformat()
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"LinkedIn job search failed: {e}")
        return json.dumps({
            "error": str(e),
            "jobs": []
        }, indent=2)

async def search_muse_jobs(keywords: str, location: str = "", limit: int = 25) -> str:
    """
    Search for jobs using The Muse API and realistic fallbacks.
    
    Args:
        keywords: Job search keywords (e.g., "software engineer", "data scientist")
        location: Optional location filter (e.g., "San Francisco", "Remote")
        limit: Maximum number of job results (default: 25)
        
    Returns:
        JSON string with structured job data from The Muse and fallbacks
    """
    try:
        if not JOB_SEARCHER_AVAILABLE:
            return json.dumps({
                "error": "Job searcher not available",
                "jobs": []
            }, indent=2)
        
        logger.info(f"Muse search: {keywords} in {location}, limit={limit}")
        
        # Use job searcher for The Muse API and fallbacks
        return await search_jobs_enhanced(keywords, location, limit)
        
    except Exception as e:
        logger.error(f"Muse job search failed: {e}")
        return json.dumps({
            "error": str(e),
            "jobs": []
        }, indent=2)

async def search_combined_jobs(keywords: str, location: str = "", limit: int = 30) -> str:
    """
    Search for jobs across multiple platforms (LinkedIn simulation + The Muse).
    
    Args:
        keywords: Job search keywords (e.g., "software engineer", "data scientist") 
        location: Optional location filter (e.g., "San Francisco", "Remote")
        limit: Maximum number of job results total (default: 30)
        
    Returns:
        JSON string with combined job data from multiple sources
    """
    try:
        logger.info(f"Combined search: {keywords} in {location}, limit={limit}")
        
        all_jobs = []
        sources_used = []
        
        # Split limit between sources
        linkedin_limit = limit // 2
        muse_limit = limit - linkedin_limit
        
        # Get LinkedIn jobs (simulated)
        try:
            linkedin_result = search_linkedin_jobs(keywords, linkedin_limit, 0, location)
            linkedin_data = json.loads(linkedin_result)
            if linkedin_data.get("jobs"):
                all_jobs.extend(linkedin_data["jobs"])
                sources_used.append("linkedin")
        except Exception as e:
            logger.warning(f"LinkedIn search failed in combined: {e}")
        
        # Get The Muse jobs
        if JOB_SEARCHER_AVAILABLE:
            try:
                muse_result = await search_muse_jobs(keywords, location, muse_limit)
                muse_data = json.loads(muse_result)
                if muse_data.get("jobs"):
                    all_jobs.extend(muse_data["jobs"])
                    sources_used.extend(muse_data.get("sources", ["muse"]))
            except Exception as e:
                logger.warning(f"Muse search failed in combined: {e}")
        
        # Remove duplicates based on title and company
        seen = set()
        unique_jobs = []
        for job in all_jobs:
            key = (job.get("title", "").lower(), job.get("company", "").lower())
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        # Limit final results
        unique_jobs = unique_jobs[:limit]
        
        result = {
            "search_query": {
                "keywords": keywords,
                "location": location,
                "limit": limit
            },
            "total_results": len(unique_jobs),
            "sources_used": list(set(sources_used)),
            "jobs": unique_jobs,
            "generated_at": datetime.now().isoformat()
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Combined job search failed: {e}")
        return json.dumps({
            "error": str(e),
            "jobs": []
        }, indent=2)

# Backward compatibility aliases
def bb7_search_jobs(keywords: str, limit: int = 10, offset: int = 0, location: str = '') -> str:
    """
    Legacy LinkedIn job search (alias for search_linkedin_jobs).
    """
    return search_linkedin_jobs(keywords, limit, offset, location)

# Register tools with the MCP app
app.tool()(search_linkedin_jobs)
app.tool()(search_muse_jobs)
app.tool()(search_combined_jobs)
app.tool()(bb7_search_jobs)

@mcp.tool
def parse_pdf_document(file_path: str, method: str = "auto", save_result: bool = True) -> str:
    """
    Parse a PDF document and extract structured information.
    
    Args:
        file_path: Path to the PDF file to parse
        method: Parsing method ('pypdf2', 'pdfplumber', 'pymupdf', 'auto')
        save_result: Whether to save the parsed result to a JSON file
        
    Returns:
        JSON string with parsed PDF data including text, metadata, and structured information
    """
    if not PDF_PARSER_AVAILABLE:
        return json.dumps({
            "error": "PDF parser not available. Install with: pip install PyPDF2 pdfplumber PyMuPDF"
        })
    
    try:
        parser = PDFParser()
        result = parser.parse_pdf(file_path, method)
        
        if save_result:
            output_file = parser.save_parsed_data(result)
            result["saved_to"] = output_file
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Failed to parse PDF: {str(e)}",
            "file_path": file_path
        })

@mcp.tool
def extract_pdf_text(file_path: str, method: str = "auto") -> str:
    """
    Extract only the text content from a PDF file.
    
    Args:
        file_path: Path to the PDF file
        method: Parsing method ('pypdf2', 'pdfplumber', 'pymupdf', 'auto')
        
    Returns:
        Raw text content from the PDF
    """
    if not PDF_PARSER_AVAILABLE:
        return "PDF parser not available. Install with: pip install PyPDF2 pdfplumber PyMuPDF"
    
    try:
        parser = PDFParser()
        text = parser.extract_text_only(file_path, method)
        return text
        
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"

@mcp.tool
def batch_parse_pdfs(directory_path: str, pattern: str = "*.pdf", save_results: bool = True) -> str:
    """
    Parse multiple PDF files in a directory.
    
    Args:
        directory_path: Path to directory containing PDF files
        pattern: File pattern to match (default: "*.pdf")
        save_results: Whether to save individual parsed results
        
    Returns:
        JSON string with results from all parsed PDFs
    """
    if not PDF_PARSER_AVAILABLE:
        return json.dumps({
            "error": "PDF parser not available. Install with: pip install PyPDF2 pdfplumber PyMuPDF"
        })
    
    try:
        parser = PDFParser()
        results = parser.batch_parse_pdfs(directory_path, pattern)
        
        if save_results:
            # Save a summary of all results
            summary = {
                "batch_info": {
                    "directory": directory_path,
                    "pattern": pattern,
                    "total_files": len(results),
                    "processed_at": datetime.now().isoformat()
                },
                "results": results
            }
            
            # Save batch summary
            output_dir = Path(__file__).parent / "parsed_pdfs"
            output_dir.mkdir(exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            batch_file = output_dir / f"batch_results_{timestamp}.json"
            
            with open(batch_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            return json.dumps({
                **summary,
                "batch_results_saved_to": str(batch_file)
            }, indent=2)
        
        return json.dumps({
            "batch_info": {
                "directory": directory_path,
                "pattern": pattern,
                "total_files": len(results),
                "processed_at": datetime.now().isoformat()
            },
            "results": results
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Failed to batch parse PDFs: {str(e)}",
            "directory": directory_path
        })

@mcp.tool
def extract_job_keywords_from_pdf(file_path: str) -> str:
    """
    Extract job-relevant keywords from a PDF using AI analysis.
    
    Args:
        file_path: Path to the PDF file to analyze
        
    Returns:
        JSON string with AI-extracted keywords and job-relevant information
    """
    if not PDF_PARSER_AVAILABLE:
        return json.dumps({
            "error": "PDF parser not available. Install with: pip install PyPDF2 pdfplumber PyMuPDF"
        })
    
    try:
        parser = PDFParser()
        result = parser.extract_job_keywords(file_path)
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Failed to extract keywords: {str(e)}",
            "file_path": file_path
        })

@mcp.tool
def generate_keywords_from_text(text: str, context: str = "general") -> str:
    """
    Generate job-relevant keywords from text using Gemini AI.
    
    Args:
        text: Input text to analyze
        context: Context type ('job_description', 'resume', 'cover_letter', 'general')
        
    Returns:
        JSON string with extracted keywords and analysis
    """
    if not KEYWORD_GENERATOR_AVAILABLE:
        return json.dumps({
            "error": "Keyword generator not available. Check Gemini AI setup."
        })
    
    try:
        generator = KeywordGenerator()
        result = generator.generate_keywords_from_text(text, context)
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Failed to generate keywords: {str(e)}"
        })

@mcp.tool
def generate_keywords_from_pdf(file_path: str, context: str = "auto") -> str:
    """
    Generate keywords from a PDF file using Gemini AI.
    
    Args:
        file_path: Path to PDF file
        context: Context type ('job_description', 'resume', 'cover_letter', 'auto')
        
    Returns:
        JSON string with extracted keywords and file analysis
    """
    if not KEYWORD_GENERATOR_AVAILABLE:
        return json.dumps({
            "error": "Keyword generator not available. Check Gemini AI setup."
        })
    
    try:
        generator = KeywordGenerator()
        result = generator.generate_keywords_from_pdf(file_path, context)
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Failed to generate keywords from PDF: {str(e)}",
            "file_path": file_path
        })

@mcp.tool
def generate_job_match_keywords(job_description: str, resume_text: str) -> str:
    """
    Generate keywords for job matching by comparing job description with resume.
    
    Args:
        job_description: Text of job description
        resume_text: Text of resume/CV
        
    Returns:
        JSON string with matching analysis and keyword recommendations
    """
    if not KEYWORD_GENERATOR_AVAILABLE:
        return json.dumps({
            "error": "Keyword generator not available. Check Gemini AI setup."
        })
    
    try:
        generator = KeywordGenerator()
        result = generator.generate_job_match_keywords(job_description, resume_text)
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Failed to analyze job match: {str(e)}"
        })

@mcp.tool
def generate_industry_keywords(industry: str, role: str = "") -> str:
    """
    Generate industry-specific keywords and terms.
    
    Args:
        industry: Industry name (e.g., "technology", "healthcare", "finance")
        role: Optional specific role (e.g., "software engineer", "data scientist")
        
    Returns:
        JSON string with industry-specific keywords
    """
    if not KEYWORD_GENERATOR_AVAILABLE:
        return json.dumps({
            "error": "Keyword generator not available. Check Gemini AI setup."
        })
    
    try:
        generator = KeywordGenerator()
        result = generator.generate_industry_keywords(industry, role)
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Failed to generate industry keywords: {str(e)}"
        })

@mcp.tool
def optimize_keywords_for_ats(text: str, target_job: str = "") -> str:
    """
    Optimize keywords for ATS (Applicant Tracking Systems).
    
    Args:
        text: Text to optimize (resume, cover letter, etc.)
        target_job: Target job title or description
        
    Returns:
        JSON string with ATS optimization recommendations
    """
    if not KEYWORD_GENERATOR_AVAILABLE:
        return json.dumps({
            "error": "Keyword generator not available. Check Gemini AI setup."
        })
    
    try:
        generator = KeywordGenerator()
        result = generator.optimize_keywords_for_ats(text, target_job)
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Failed to optimize for ATS: {str(e)}"
        })

# Test function for when run as script
async def test_mcp_server():
    """Test the MCP server functionality."""
    print("🚀 Testing Jobs MCP Server")
    print("=" * 50)
    
    test_cases = [
        ("software engineer", "San Francisco"),
        ("data scientist", "New York"),  
        ("python developer", "Remote")
    ]
    
    for keywords, location in test_cases:
        print(f"\n🔍 Testing: '{keywords}' in '{location}'")
        print("-" * 40)
        
        # Test LinkedIn search
        print("📊 LinkedIn Search:")
        linkedin_result = search_linkedin_jobs(keywords, 3, 0, location)
        linkedin_data = json.loads(linkedin_result)
        print(f"   Found {linkedin_data.get('total_results', 0)} LinkedIn jobs")
        
        # Test Muse search  
        if JOB_SEARCHER_AVAILABLE:
            print("🔍 Muse Search:")
            muse_result = await search_muse_jobs(keywords, location, 3)
            muse_data = json.loads(muse_result)
            print(f"   Found {muse_data.get('total_jobs', 0)} Muse jobs")
        
        # Test combined search
        print("🌐 Combined Search:")
        combined_result = await search_combined_jobs(keywords, location, 5)
        combined_data = json.loads(combined_result)
        print(f"   Found {combined_data.get('total_results', 0)} total jobs")
        print(f"   Sources: {', '.join(combined_data.get('sources_used', []))}")
    
    print("\n" + "=" * 50)
    print("✅ Testing complete!")

def main():
    """Main function to run the server."""
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Run tests
        asyncio.run(test_mcp_server())
    else:
        # Run the MCP server over HTTP
        print("🚀 Starting Jobs MCP Server over HTTP...")
        print("Available tools:")
        print("  Job Search:")
        print("    - search_linkedin_jobs")
        print("    - search_muse_jobs") 
        print("    - search_combined_jobs")
        print("    - bb7_search_jobs (legacy)")
        print("  PDF Processing:")
        print("    - parse_pdf_document")
        print("    - extract_pdf_text")
        print("    - batch_parse_pdfs")
        print("    - extract_job_keywords_from_pdf (AI-powered)")
        print("  Keyword Generation (AI-powered):")
        print("    - generate_keywords_from_text")
        print("    - generate_keywords_from_pdf")
        print("    - generate_job_match_keywords")
        print("    - generate_industry_keywords")
        print("    - optimize_keywords_for_ats")
        print("    - extract_job_keywords_from_pdf")
        print("  Keyword Generation:")
        print("    - generate_keywords_from_text")
        print("    - generate_keywords_from_pdf")
        print("    - generate_job_match_keywords")
        print("    - generate_industry_keywords")
        print("    - optimize_keywords_for_ats")
        print("🌐 Server will be available at: http://localhost:8080/mcp")
        
        try:
            app.run(transport="http", port=8080, host="localhost")
        except KeyboardInterrupt:
            print("\n👋 Server stopped")

if __name__ == "__main__":
    main()
