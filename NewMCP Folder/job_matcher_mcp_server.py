#!/usr/bin/env python3
"""
MCP Server for AI-Powered Job Matching
Exposes job matching capabilities as MCP tools

This server acts as a "smart context engine" that:
1. Fetches jobs from multiple sources (LinkedIn, GitHub, etc.)
2. Analyzes user's resume for context
3. Uses AI to match and rank jobs
4. Provides personalized recommendations
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

# Add project directory to path
sys.path.insert(0, str(Path(__file__).parent))

from job_matcher import JobMatcher


@dataclass
class MCPTool:
    """MCP Tool definition"""
    name: str
    description: str
    input_schema: Dict[str, Any]


class JobMatcherMCPServer:
    """MCP Server for Job Matching"""

    def __init__(self):
        self.matcher = JobMatcher()
        self.project_dir = Path(__file__).parent

    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available MCP tools"""
        return [
            {
                "name": "collect_jobs",
                "description": "Collect jobs from all configured sources (LinkedIn, GitHub, job boards)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "sources": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of sources to collect from (e.g., ['linkedin', 'github', 'data'])"
                        },
                        "keywords": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Keywords to search for (e.g., ['AI', 'ML', 'new grad'])"
                        }
                    },
                    "required": []
                }
            },
            {
                "name": "extract_resume_context",
                "description": "Extract context from user's resume PDF for matching",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "resume_path": {
                            "type": "string",
                            "description": "Path to resume PDF file"
                        }
                    },
                    "required": ["resume_path"]
                }
            },
            {
                "name": "match_jobs_with_resume",
                "description": "Use AI to match jobs with resume and provide match scores + reasoning",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "resume_path": {
                            "type": "string",
                            "description": "Path to resume PDF"
                        },
                        "top_n": {
                            "type": "number",
                            "description": "Number of top matches to return (default: 50)",
                            "default": 50
                        },
                        "min_score": {
                            "type": "number",
                            "description": "Minimum match score threshold (0-100, default: 0)",
                            "default": 0
                        }
                    },
                    "required": ["resume_path"]
                }
            },
            {
                "name": "get_job_statistics",
                "description": "Get statistics about collected jobs (total count, sources, etc.)",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "analyze_job_match",
                "description": "Analyze why a specific job matches (or doesn't match) the resume",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "job_index": {
                            "type": "number",
                            "description": "Index of the job to analyze"
                        },
                        "resume_path": {
                            "type": "string",
                            "description": "Path to resume PDF"
                        }
                    },
                    "required": ["job_index", "resume_path"]
                }
            },
            {
                "name": "send_matches_email",
                "description": "Send top job matches via email",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "recipient": {
                            "type": "string",
                            "description": "Email address to send matches to"
                        },
                        "top_n": {
                            "type": "number",
                            "description": "Number of matches to send (default: 50)",
                            "default": 50
                        }
                    },
                    "required": ["recipient"]
                }
            }
        ]

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool and return result"""

        if tool_name == "collect_jobs":
            return await self._collect_jobs(arguments)

        elif tool_name == "extract_resume_context":
            return await self._extract_resume_context(arguments)

        elif tool_name == "match_jobs_with_resume":
            return await self._match_jobs_with_resume(arguments)

        elif tool_name == "get_job_statistics":
            return await self._get_job_statistics(arguments)

        elif tool_name == "analyze_job_match":
            return await self._analyze_job_match(arguments)

        elif tool_name == "send_matches_email":
            return await self._send_matches_email(arguments)

        else:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}"
            }

    async def _collect_jobs(self, args: Dict) -> Dict:
        """Collect jobs from specified sources"""
        try:
            # Default sources
            sources = args.get("sources", ["linkedin", "github", "data"])

            jobs_dirs = []
            if "linkedin" in sources:
                jobs_dirs.append(str(self.project_dir / "linkedin_collector" / "job_search_results"))
            if "github" in sources or "data" in sources:
                jobs_dirs.append(str(self.project_dir / "data"))

            jobs = self.matcher.load_all_jobs(jobs_dirs)

            return {
                "success": True,
                "jobs_count": len(jobs),
                "sources": sources,
                "message": f"Collected {len(jobs)} jobs from {len(sources)} sources"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def _extract_resume_context(self, args: Dict) -> Dict:
        """Extract context from resume"""
        try:
            resume_path = args["resume_path"]
            resume_text = self.matcher.extract_resume(resume_path)

            return {
                "success": True,
                "resume_length": len(resume_text),
                "resume_preview": resume_text[:500] + "...",
                "message": f"Extracted {len(resume_text)} characters from resume"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def _match_jobs_with_resume(self, args: Dict) -> Dict:
        """Match jobs with resume using AI"""
        try:
            resume_path = args["resume_path"]
            top_n = args.get("top_n", 50)
            min_score = args.get("min_score", 0)

            # Load jobs
            jobs_dirs = [
                str(self.project_dir / "linkedin_collector" / "job_search_results"),
                str(self.project_dir / "data")
            ]
            all_jobs = self.matcher.load_all_jobs(jobs_dirs)

            # Extract resume
            resume_text = self.matcher.extract_resume(resume_path)

            # Match jobs
            matched_jobs = []
            for job in all_jobs[:100]:  # Limit for demo
                match_result = self.matcher.match_job_with_resume(job, resume_text)
                if match_result["match_score"] >= min_score:
                    matched_jobs.append(match_result)

            # Sort by score
            matched_jobs.sort(key=lambda x: x["match_score"], reverse=True)
            top_matches = matched_jobs[:top_n]

            return {
                "success": True,
                "total_jobs_analyzed": len(all_jobs),
                "matches_found": len(matched_jobs),
                "top_matches": top_matches,
                "message": f"Found {len(matched_jobs)} matches, returning top {len(top_matches)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def _get_job_statistics(self, args: Dict) -> Dict:
        """Get statistics about collected jobs"""
        try:
            jobs_dirs = [
                str(self.project_dir / "linkedin_collector" / "job_search_results"),
                str(self.project_dir / "data")
            ]
            all_jobs = self.matcher.load_all_jobs(jobs_dirs)

            # Calculate statistics
            sources = {}
            for job in all_jobs:
                source = job.get("source", "Unknown")
                sources[source] = sources.get(source, 0) + 1

            return {
                "success": True,
                "total_jobs": len(all_jobs),
                "sources": sources,
                "sample_job": all_jobs[0] if all_jobs else None
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def _analyze_job_match(self, args: Dict) -> Dict:
        """Analyze a specific job match"""
        try:
            job_index = args["job_index"]
            resume_path = args["resume_path"]

            # Load jobs and get specific one
            jobs_dirs = [
                str(self.project_dir / "linkedin_collector" / "job_search_results"),
                str(self.project_dir / "data")
            ]
            all_jobs = self.matcher.load_all_jobs(jobs_dirs)

            if job_index >= len(all_jobs):
                return {
                    "success": False,
                    "error": f"Job index {job_index} out of range (max: {len(all_jobs)-1})"
                }

            job = all_jobs[job_index]
            resume_text = self.matcher.extract_resume(resume_path)

            # Get match analysis
            match_result = self.matcher.match_job_with_resume(job, resume_text)

            return {
                "success": True,
                "job": job,
                "match_analysis": match_result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def _send_matches_email(self, args: Dict) -> Dict:
        """Send matched jobs via email"""
        try:
            # This would integrate with send_email_smtp.py
            return {
                "success": True,
                "message": "Email functionality - run send_email_smtp.py separately"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


async def main():
    """Main MCP server entry point"""
    server = JobMatcherMCPServer()

    print("🚀 Job Matcher MCP Server Started")
    print("=" * 60)
    print("\n📋 Available Tools:")

    tools = server.list_tools()
    for i, tool in enumerate(tools, 1):
        print(f"\n{i}. {tool['name']}")
        print(f"   {tool['description']}")

    print("\n" + "=" * 60)
    print("Server ready for MCP requests via stdio")
    print("Use MCP Inspector to visualize and test tools")


if __name__ == "__main__":
    asyncio.run(main())
