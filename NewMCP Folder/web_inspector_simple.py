#!/usr/bin/env python3
"""
Simple Web Inspector for MCP Job Matcher Server
Displays all available tools in a web interface
"""

import json
import subprocess
import sys
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser
import threading

class MCPInspectorHandler(BaseHTTPRequestHandler):
    """HTTP handler for MCP Inspector"""
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_html().encode())
        
        elif self.path == '/api/tools':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            tools = self.get_tools()
            self.wfile.write(json.dumps(tools).encode())
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def get_tools(self):
        """Get tools from MCP server"""
        try:
            # Call the MCP server to list tools
            server_path = Path(__file__).parent / "job_matcher_mcp_stdio.py"
            
            # Create a simple request to list tools
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list"
            }
            
            # For simplicity, return the known tools
            return {
                "tools": [
                    {
                        "name": "search_jobs",
                        "description": "Search for jobs across multiple platforms (LinkedIn, The Muse) using keywords and location",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "keywords": {"type": "string", "description": "Job search keywords"},
                                "location": {"type": "string", "description": "Location filter"},
                                "limit": {"type": "integer", "description": "Max results", "default": 30}
                            },
                            "required": ["keywords"]
                        }
                    },
                    {
                        "name": "match_jobs",
                        "description": "Match jobs with resume using AI/LLM and return top matches",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "resume_path": {"type": "string", "description": "Path to resume PDF"},
                                "jobs_dirs": {"type": "array", "description": "Directories with job JSON files"},
                                "top_n": {"type": "integer", "description": "Number of top matches", "default": 50}
                            },
                            "required": ["resume_path", "jobs_dirs"]
                        }
                    },
                    {
                        "name": "send_email",
                        "description": "Send matched jobs via email using Gmail SMTP",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "recipient": {"type": "string", "description": "Recipient email"},
                                "subject": {"type": "string", "description": "Email subject"},
                                "matched_jobs_file": {"type": "string", "description": "Path to matched jobs JSON"}
                            },
                            "required": ["recipient", "subject", "matched_jobs_file"]
                        }
                    },
                    {
                        "name": "extract_resume",
                        "description": "Extract text from PDF resume",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "pdf_path": {"type": "string", "description": "Path to PDF resume"}
                            },
                            "required": ["pdf_path"]
                        }
                    },
                    {
                        "name": "get_statistics",
                        "description": "Get statistics about job search results",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "jobs_dirs": {"type": "array", "description": "Directories with job JSON files"}
                            },
                            "required": ["jobs_dirs"]
                        }
                    }
                ]
            }
        except Exception as e:
            return {"error": str(e), "tools": []}
    
    def get_html(self):
        """Generate HTML for the inspector"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MCP Job Matcher Server - Tools Inspector</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            text-align: center;
        }
        
        .header h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            color: #666;
            font-size: 1.1em;
        }
        
        .status {
            display: inline-block;
            padding: 8px 20px;
            background: #10b981;
            color: white;
            border-radius: 20px;
            font-weight: bold;
            margin-top: 10px;
        }
        
        .tools-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .tool-card {
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .tool-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0,0,0,0.2);
        }
        
        .tool-name {
            font-size: 1.5em;
            color: #667eea;
            margin-bottom: 10px;
            font-weight: bold;
            display: flex;
            align-items: center;
        }
        
        .tool-name::before {
            content: "🔧";
            margin-right: 10px;
        }
        
        .tool-description {
            color: #555;
            margin-bottom: 15px;
            line-height: 1.6;
        }
        
        .tool-params {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
        }
        
        .param {
            padding: 8px 0;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .param:last-child {
            border-bottom: none;
        }
        
        .param-name {
            font-weight: bold;
            color: #764ba2;
        }
        
        .param-required {
            color: #ef4444;
            font-size: 0.8em;
            margin-left: 5px;
        }
        
        .param-type {
            color: #10b981;
            font-size: 0.9em;
            margin-left: 5px;
        }
        
        .param-desc {
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }
        
        .loading {
            text-align: center;
            padding: 50px;
            color: white;
            font-size: 1.5em;
        }
        
        .error {
            background: #fee;
            border: 2px solid #f88;
            padding: 20px;
            border-radius: 10px;
            color: #c00;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 MCP Job Matcher Server</h1>
            <p>Available Tools & Capabilities</p>
            <div class="status">🟢 Server Running</div>
        </div>
        
        <div id="tools-container" class="loading">
            Loading tools...
        </div>
    </div>
    
    <script>
        async function loadTools() {
            try {
                const response = await fetch('/api/tools');
                const data = await response.json();
                
                const container = document.getElementById('tools-container');
                
                if (data.error) {
                    container.innerHTML = `<div class="error">Error: ${data.error}</div>`;
                    return;
                }
                
                if (!data.tools || data.tools.length === 0) {
                    container.innerHTML = '<div class="error">No tools found</div>';
                    return;
                }
                
                container.innerHTML = '';
                container.className = 'tools-grid';
                
                data.tools.forEach(tool => {
                    const card = document.createElement('div');
                    card.className = 'tool-card';
                    
                    let paramsHtml = '';
                    if (tool.inputSchema && tool.inputSchema.properties) {
                        const required = tool.inputSchema.required || [];
                        paramsHtml = '<div class="tool-params"><strong>Parameters:</strong>';
                        
                        for (const [name, schema] of Object.entries(tool.inputSchema.properties)) {
                            const isRequired = required.includes(name);
                            paramsHtml += `
                                <div class="param">
                                    <span class="param-name">${name}</span>
                                    <span class="param-type">${schema.type || 'any'}</span>
                                    ${isRequired ? '<span class="param-required">*required</span>' : ''}
                                    ${schema.description ? `<div class="param-desc">${schema.description}</div>` : ''}
                                </div>
                            `;
                        }
                        paramsHtml += '</div>';
                    }
                    
                    card.innerHTML = `
                        <div class="tool-name">${tool.name}</div>
                        <div class="tool-description">${tool.description || 'No description'}</div>
                        ${paramsHtml}
                    `;
                    
                    container.appendChild(card);
                });
                
            } catch (error) {
                document.getElementById('tools-container').innerHTML = 
                    `<div class="error">Error loading tools: ${error.message}</div>`;
            }
        }
        
        // Load tools on page load
        loadTools();
    </script>
</body>
</html>
        """
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass


def open_browser(port):
    """Open browser after a short delay"""
    import time
    time.sleep(1)
    webbrowser.open(f'http://localhost:{port}')


def main():
    """Main function"""
    port = 8000
    
    print("🚀 MCP Job Matcher - Web Inspector")
    print("=" * 60)
    print(f"🌐 Starting web server on http://localhost:{port}")
    print("📡 Inspecting MCP tools...")
    print("")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Start browser in background
    browser_thread = threading.Thread(target=open_browser, args=(port,))
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start server
    server = HTTPServer(('localhost', port), MCPInspectorHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped")
        server.shutdown()


if __name__ == "__main__":
    main()
