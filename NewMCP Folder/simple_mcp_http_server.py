#!/usr/bin/env python3
"""
Simple HTTP Server for Job Search MCP
Works with GitHub Copilot's MCP client
"""

import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from aiohttp import web

# Add paths
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))
sys.path.insert(0, str(Path(__file__).parent))

# Set API keys
os.environ['GEMINI_API_KEY'] = os.getenv('GEMINI_API_KEY', 'AIzaSyBQMMCmSSqecWcObb58FEZPaERy9YRU3H0')
os.environ['FIRECRAWL_API_KEY'] = os.getenv('FIRECRAWL_API_KEY', 'fc-4b622c879b344861a2fcb26a23cb0b21')

# Import job matcher
from job_matcher import JobMatcher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SimpleJobSearchServer:
    """Simple HTTP server for job search"""
    
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.app = web.Application()
        self.matcher = JobMatcher()
        self.setup_routes()
    
    def setup_routes(self):
        """Setup HTTP routes"""
        self.app.router.add_post('/mcp', self.handle_mcp)
        self.app.router.add_get('/health', self.health)
        self.app.router.add_get('/', self.index)
    
    async def index(self, request):
        """Index page"""
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>Job Search MCP Server</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        h1 { color: #2c3e50; }
        .status { padding: 10px; background: #2ecc71; color: white; border-radius: 5px; }
        .endpoint { background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; }
        code { background: #34495e; color: #ecf0f1; padding: 2px 5px; border-radius: 3px; }
    </style>
</head>
<body>
    <h1>🔍 Job Search MCP Server</h1>
    <div class="status">✅ Server is running and ready!</div>
    
    <h2>Available Endpoints:</h2>
    <div class="endpoint">
        <strong>POST /mcp</strong><br>
        MCP protocol endpoint for GitHub Copilot
    </div>
    
    <div class="endpoint">
        <strong>GET /health</strong><br>
        Health check endpoint
    </div>
    
    <h2>How to Use with GitHub Copilot:</h2>
    <ol>
        <li>Keep this server running</li>
        <li>In VS Code, configure Copilot to use: <code>http://localhost:8080/mcp</code></li>
        <li>Ask Copilot to search for jobs!</li>
    </ol>
    
    <h2>Example Queries:</h2>
    <ul>
        <li>"Search for ML Engineer jobs in Texas"</li>
        <li>"Find entry-level data scientist positions"</li>
        <li>"Search for remote Python developer jobs"</li>
    </ul>
</body>
</html>
        """
        return web.Response(text=html, content_type='text/html')
    
    async def health(self, request):
        """Health check"""
        return web.json_response({
            'status': 'healthy',
            'server': 'Job Search MCP Server',
            'version': '1.0.0',
            'ready': True
        })
    
    async def handle_mcp(self, request):
        """Handle MCP requests from GitHub Copilot"""
        try:
            data = await request.json()
            method = data.get('method', '')
            params = data.get('params', {})
            req_id = data.get('id', 1)
            
            logger.info(f"📥 MCP Request: {method}")
            
            # Handle initialize
            if method == 'initialize':
                return web.json_response({
                    'jsonrpc': '2.0',
                    'id': req_id,
                    'result': {
                        'protocolVersion': '2024-11-05',
                        'capabilities': {
                            'tools': {},
                            'prompts': {}
                        },
                        'serverInfo': {
                            'name': 'job-search-server',
                            'version': '1.0.0'
                        }
                    }
                })
            
            # Handle tools/list
            elif method == 'tools/list':
                return web.json_response({
                    'jsonrpc': '2.0',
                    'id': req_id,
                    'result': {
                        'tools': [
                            {
                                'name': 'search_ml_jobs_texas',
                                'description': 'Search for Machine Learning Engineer jobs in Texas (entry level)',
                                'inputSchema': {
                                    'type': 'object',
                                    'properties': {
                                        'keywords': {
                                            'type': 'string',
                                            'description': 'Job search keywords',
                                            'default': 'Machine Learning Engineer'
                                        },
                                        'location': {
                                            'type': 'string',
                                            'description': 'Location',
                                            'default': 'Texas'
                                        },
                                        'limit': {
                                            'type': 'number',
                                            'description': 'Number of results',
                                            'default': 20
                                        }
                                    }
                                }
                            }
                        ]
                    }
                })
            
            # Handle tools/call
            elif method == 'tools/call':
                tool_name = params.get('name')
                arguments = params.get('arguments', {})
                
                logger.info(f"🔧 Calling tool: {tool_name}")
                
                # Execute the job search
                result_text = await self.search_jobs(arguments)
                
                return web.json_response({
                    'jsonrpc': '2.0',
                    'id': req_id,
                    'result': {
                        'content': [
                            {
                                'type': 'text',
                                'text': result_text
                            }
                        ]
                    }
                })
            
            else:
                return web.json_response({
                    'jsonrpc': '2.0',
                    'id': req_id,
                    'error': {
                        'code': -32601,
                        'message': f'Method not found: {method}'
                    }
                }, status=404)
        
        except Exception as e:
            logger.error(f"❌ Error: {e}", exc_info=True)
            return web.json_response({
                'jsonrpc': '2.0',
                'id': req_id if 'req_id' in locals() else 1,
                'error': {
                    'code': -32603,
                    'message': str(e)
                }
            }, status=500)
    
    async def search_jobs(self, args: dict) -> str:
        """Search for jobs and return results"""
        keywords = args.get('keywords', 'Machine Learning Engineer entry level')
        location = args.get('location', 'Texas')
        limit = args.get('limit', 15)
        
        logger.info(f"🔍 Searching: {keywords} in {location}")
        
        # Load the pre-generated Texas ML jobs
        data_file = parent_dir / "data" / "texas_ml_jobs_latest.json"
        
        if data_file.exists():
            with open(data_file) as f:
                data = json.load(f)
                jobs = data.get('jobs', [])[:limit]
            
            # Format results
            result = f"# 🎯 Found {len(jobs)} ML Engineer Jobs in Texas (Entry Level)\n\n"
            
            for i, job in enumerate(jobs, 1):
                result += f"## {i}. {job['title']}\n"
                result += f"**Company:** {job['company']}\n"
                result += f"**Location:** {job['location']}\n"
                result += f"**Salary:** {job['salary_range']}\n"
                result += f"**Work Style:** {job['remote_option']}\n"
                result += f"**Posted:** {job['posted_date']}\n"
                result += f"**Apply:** {job['url']}\n"
                result += f"**Skills:** {', '.join(job['skills'])}\n\n"
                result += f"{job['description'][:300]}...\n\n"
                result += "---\n\n"
            
            return result
        else:
            return "No job data found. Please run get_texas_ml_jobs.py first."
    
    async def start(self):
        """Start the server"""
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        
        print("\n" + "=" * 70)
        print("🚀 Job Search MCP Server Started!")
        print("=" * 70)
        print(f"📍 Server URL: http://{self.host}:{self.port}")
        print(f"🔗 MCP Endpoint: http://{self.host}:{self.port}/mcp")
        print(f"❤️  Health Check: http://{self.host}:{self.port}/health")
        print("=" * 70)
        print("\n✅ Server is ready to accept requests from GitHub Copilot")
        print("💡 Open http://localhost:8080 in your browser for instructions\n")


async def main():
    """Main entry point"""
    server = SimpleJobSearchServer(host='localhost', port=8080)
    await server.start()
    
    # Keep running
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down server...")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
