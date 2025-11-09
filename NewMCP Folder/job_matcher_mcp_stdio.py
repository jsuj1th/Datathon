#!/usr/bin/env python3
"""
MCP Server for Job Matching - STDIO Protocol
Implements the Model Context Protocol for use with MCP Inspector
"""

import asyncio
import json
import sys
import logging
from pathlib import Path
from typing import Any, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from job_matcher import JobMatcher


class JobMatcherMCPStdio:
    """MCP Server using stdio for communication"""

    def __init__(self):
        self.matcher = JobMatcher()
        self.project_dir = Path(__file__).parent
        self.request_id = 0

    async def handle_initialize(self, params: Dict) -> Dict:
        """Handle MCP initialize request"""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "job-matcher",
                "version": "1.0.0"
            }
        }

    async def handle_tools_list(self, params: Dict) -> Dict:
        """List available tools"""
        return {
            "tools": [
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
                    "name": "collect_jobs",
                    "description": "Collect jobs from all configured sources (LinkedIn, GitHub, job boards)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "sources": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of sources: linkedin, github, data"
                            }
                        }
                    }
                },
                {
                    "name": "extract_resume",
                    "description": "Extract text from resume PDF",
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
                    "name": "match_jobs",
                    "description": "Match jobs with resume using AI (returns top matches with scores)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "resume_path": {
                                "type": "string",
                                "description": "Path to resume PDF file (optional, will use uploads/ if not provided)"
                            },
                            "top_n": {
                                "type": "number",
                                "description": "Number of top matches to return (default: 10 for demo)",
                                "default": 10
                            }
                        }
                    }
                }
            ]
        }

    async def handle_tools_call(self, params: Dict) -> Dict:
        """Execute a tool"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        try:
            if tool_name == "get_job_statistics":
                result = await self._get_statistics()

            elif tool_name == "collect_jobs":
                result = await self._collect_jobs(arguments)

            elif tool_name == "extract_resume":
                result = await self._extract_resume(arguments)

            elif tool_name == "match_jobs":
                result = await self._match_jobs(arguments)

            else:
                result = f"Unknown tool: {tool_name}"

            return {
                "content": [
                    {
                        "type": "text",
                        "text": result if isinstance(result, str) else json.dumps(result, indent=2)
                    }
                ]
            }

        except Exception as e:
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Error executing {tool_name}: {str(e)}"
                    }
                ],
                "isError": True
            }

    async def _get_statistics(self) -> str:
        """Get job statistics"""
        jobs_dirs = [
            str(self.project_dir.parent / "linkedin_collector" / "job_search_results"),
            str(self.project_dir.parent / "data")
        ]
        jobs = self.matcher.load_all_jobs(jobs_dirs)

        sources = {}
        for job in jobs:
            source = job.get("source", "Unknown")
            sources[source] = sources.get(source, 0) + 1

        result = {
            "total_jobs": len(jobs),
            "sources": sources,
            "sample_jobs": jobs[:3] if jobs else []
        }

        return f"📊 Job Statistics:\n\n{json.dumps(result, indent=2)}"

    async def _collect_jobs(self, args: Dict) -> str:
        """Collect jobs"""
        sources = args.get("sources", ["linkedin", "github", "data"])

        jobs_dirs = []
        if "linkedin" in sources:
            jobs_dirs.append(str(self.project_dir.parent / "linkedin_collector" / "job_search_results"))
        if "github" in sources or "data" in sources:
            jobs_dirs.append(str(self.project_dir.parent / "data"))

        jobs = self.matcher.load_all_jobs(jobs_dirs)

        return f"✅ Collected {len(jobs)} jobs from {len(sources)} sources"

    async def _extract_resume(self, args: Dict) -> str:
        """Extract resume text"""
        resume_path = args.get("resume_path")
        if not resume_path:
            return "❌ resume_path is required"

        text = self.matcher.extract_resume(resume_path)
        preview = text[:500] + "..." if len(text) > 500 else text

        return f"📄 Resume Extracted:\n\nLength: {len(text)} characters\n\nPreview:\n{preview}"

    async def _match_jobs(self, args: Dict) -> str:
        """Match jobs with resume"""
        top_n = args.get("top_n", 10)  # Limit for demo

        # Load jobs
        jobs_dirs = [
            str(self.project_dir.parent / "linkedin_collector" / "job_search_results"),
            str(self.project_dir.parent / "data")
        ]
        all_jobs = self.matcher.load_all_jobs(jobs_dirs)

        # Check if resume_path was provided
        resume_path = args.get("resume_path")
        if not resume_path:
            # Try to find a default resume in uploads folder
            uploads_dir = self.project_dir.parent / "uploads"
            if uploads_dir.exists():
                pdf_files = list(uploads_dir.glob("*.pdf"))
                if pdf_files:
                    resume_path = str(pdf_files[0])
                    logger.info(f"Using default resume: {resume_path}")
        
        if not resume_path:
            return "❌ No resume found. Please provide resume_path or upload a PDF to the uploads/ folder"

        resume_text = self.matcher.extract_resume(resume_path)

        # Match jobs (limit to first 20 for demo speed)
        matched = []
        for job in all_jobs[:20]:
            match = self.matcher.match_job_with_resume(job, resume_text)
            matched.append(match)

        # Sort and get top N
        matched.sort(key=lambda x: x["match_score"], reverse=True)
        top_matches = matched[:top_n]

        # Format output
        output = f"🎯 Top {len(top_matches)} Job Matches:\n\n"
        for i, match in enumerate(top_matches, 1):
            output += f"{i}. {match['position']} at {match['company']}\n"
            output += f"   Score: {match['match_score']}/100\n"
            output += f"   Reason: {match['match_reason']}\n"
            output += f"   Link: {match.get('apply_link', 'N/A')}\n\n"

        return output

    async def process_request(self, request: Dict) -> Dict:
        """Process a single MCP request"""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        try:
            if method == "initialize":
                result = await self.handle_initialize(params)
            elif method == "tools/list":
                result = await self.handle_tools_list(params)
            elif method == "tools/call":
                result = await self.handle_tools_call(params)
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }

            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }

        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }

    async def run(self):
        """Main server loop - read from stdin, write to stdout"""
        import sys

        # Use line-buffered mode
        sys.stdout.reconfigure(line_buffering=True)
        sys.stderr.reconfigure(line_buffering=True)

        # Send startup message to stderr
        print("🚀 Job Matcher MCP Server started", file=sys.stderr)
        print("Waiting for requests on stdin...", file=sys.stderr)

        while True:
            try:
                # Read line from stdin
                line = sys.stdin.readline()
                if not line:
                    break

                line = line.strip()
                if not line:
                    continue

                # Parse JSON-RPC request
                request = json.loads(line)

                # Process request
                response = await self.process_request(request)

                # Send response to stdout
                print(json.dumps(response), flush=True)

            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}", file=sys.stderr)
                continue
            except Exception as e:
                print(f"Error processing request: {e}", file=sys.stderr)
                import traceback
                traceback.print_exc(file=sys.stderr)
                continue


async def main():
    """Entry point"""
    server = JobMatcherMCPStdio()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
