#!/usr/bin/env python3
"""
HTTP Wrapper for MCP Server
Makes the STDIO-based MCP server accessible via HTTP for GitHub Copilot
"""

import asyncio
import json
import logging
from pathlib import Path
from aiohttp import web
import sys

# Add parent directory to path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import your MCP server components
from complete_job_search_mcp_server import (
    search_jobs_complete_impl,
    search_github_jobs_impl,
    search_linkedin_jobs_impl,
    match_resume_with_jobs_impl,
    send_job_matches_email_impl,
    generate_search_keywords_impl
)


class MCPHTTPServer:
    """HTTP server that wraps MCP STDIO functionality"""
    
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.app = web.Application()
        self.setup_routes()
    
    def setup_routes(self):
        """Setup HTTP routes"""
        self.app.router.add_post('/mcp', self.handle_mcp_request)
        self.app.router.add_get('/health', self.health_check)
        self.app.router.add_get('/', self.index)
    
    async def index(self, request):
        """Index page"""
        return web.Response(text="""
MCP HTTP Server for Job Search
==============================

Available endpoints:
- POST /mcp - MCP protocol endpoint
- GET /health - Health check

Available MCP tools:
- search_jobs_complete
- search_github_jobs
- search_linkedin_jobs
- match_resume_with_jobs
- send_job_matches_email
- generate_search_keywords

Server is running and ready to accept requests from GitHub Copilot.
        """, content_type='text/plain')
    
    async def health_check(self, request):
        """Health check endpoint"""
        return web.json_response({
            'status': 'healthy',
            'server': 'MCP HTTP Server',
            'version': '1.0.0'
        })
    
    async def handle_mcp_request(self, request):
        """Handle MCP protocol requests"""
        try:
            data = await request.json()
            logger.info(f"Received MCP request: {data.get('method', 'unknown')}")
            
            method = data.get('method')
            params = data.get('params', {})
            request_id = data.get('id')
            
            # Handle different MCP methods
            if method == 'initialize':
                response = {
                    'jsonrpc': '2.0',
                    'id': request_id,
                    'result': {
                        'protocolVersion': '2024-11-05',
                        'capabilities': {
                            'tools': {}
                        },
                        'serverInfo': {
                            'name': 'complete-job-search-server',
                            'version': '1.0.0'
                        }
                    }
                }
            
            elif method == 'tools/list':
                response = {
                    'jsonrpc': '2.0',
                    'id': request_id,
                    'result': {
                        'tools': [
                            {
                                'name': 'search_jobs_complete',
                                'description': 'Search for jobs and match with resume',
                                'inputSchema': {
                                    'type': 'object',
                                    'properties': {
                                        'keywords': {'type': 'string'},
                                        'location': {'type': 'string', 'default': 'Remote'},
                                        'experience_level': {'type': 'string', 'default': 'mid'},
                                        'resume_path': {'type': 'string'},
                                        'top_n': {'type': 'number', 'default': 20}
                                    },
                                    'required': ['keywords', 'resume_path']
                                }
                            },
                            {
                                'name': 'search_linkedin_jobs',
                                'description': 'Search for jobs on LinkedIn',
                                'inputSchema': {
                                    'type': 'object',
                                    'properties': {
                                        'keywords': {'type': 'string'},
                                        'location': {'type': 'string', 'default': ''},
                                        'limit': {'type': 'number', 'default': 25}
                                    },
                                    'required': ['keywords']
                                }
                            },
                            {
                                'name': 'search_github_jobs',
                                'description': 'Search for jobs on GitHub',
                                'inputSchema': {
                                    'type': 'object',
                                    'properties': {
                                        'keywords': {'type': 'string'},
                                        'location': {'type': 'string', 'default': ''},
                                        'limit': {'type': 'number', 'default': 20}
                                    },
                                    'required': ['keywords']
                                }
                            }
                        ]
                    }
                }
            
            elif method == 'tools/call':
                tool_name = params.get('name')
                arguments = params.get('arguments', {})
                
                logger.info(f"Calling tool: {tool_name} with args: {arguments}")
                
                # Call the appropriate tool
                result = await self.execute_tool(tool_name, arguments)
                
                response = {
                    'jsonrpc': '2.0',
                    'id': request_id,
                    'result': {
                        'content': [
                            {
                                'type': 'text',
                                'text': result
                            }
                        ]
                    }
                }
            
            else:
                response = {
                    'jsonrpc': '2.0',
                    'id': request_id,
                    'error': {
                        'code': -32601,
                        'message': f'Method not found: {method}'
                    }
                }
            
            return web.json_response(response)
        
        except Exception as e:
            logger.error(f"Error handling MCP request: {e}", exc_info=True)
            return web.json_response({
                'jsonrpc': '2.0',
                'id': data.get('id') if 'data' in locals() else None,
                'error': {
                    'code': -32603,
                    'message': f'Internal error: {str(e)}'
                }
            }, status=500)
    
    async def execute_tool(self, tool_name: str, arguments: dict) -> str:
        """Execute a tool and return the result"""
        try:
            if tool_name == 'search_jobs_complete':
                result = await search_jobs_complete_impl(**arguments)
            
            elif tool_name == 'search_linkedin_jobs':
                result = await search_linkedin_jobs_impl(**arguments)
            
            elif tool_name == 'search_github_jobs':
                result = await search_github_jobs_impl(**arguments)
            
            elif tool_name == 'match_resume_with_jobs':
                result = await match_resume_with_jobs_impl(**arguments)
            
            elif tool_name == 'send_job_matches_email':
                result = await send_job_matches_email_impl(**arguments)
            
            elif tool_name == 'generate_search_keywords':
                result = await generate_search_keywords_impl(**arguments)
            
            else:
                result = json.dumps({
                    'error': f'Unknown tool: {tool_name}'
                })
            
            # Ensure result is a string
            if isinstance(result, dict) or isinstance(result, list):
                result = json.dumps(result, indent=2)
            
            return result
        
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}", exc_info=True)
            return json.dumps({
                'error': str(e),
                'tool': tool_name
            })
    
    async def start(self):
        """Start the HTTP server"""
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        logger.info(f"🚀 MCP HTTP Server started on http://{self.host}:{self.port}")
        logger.info(f"   Ready to accept requests from GitHub Copilot")
        logger.info(f"   Health check: http://{self.host}:{self.port}/health")


async def main():
    """Main entry point"""
    server = MCPHTTPServer(host='localhost', port=8080)
    await server.start()
    
    # Keep the server running
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")


if __name__ == '__main__':
    asyncio.run(main())
