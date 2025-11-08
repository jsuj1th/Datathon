#!/usr/bin/env python3
"""
GitHub Copilot MCP HTTP Server Runner
Runs the LinkedIn Jobs MCP server as an HTTP server for GitHub Copilot integration.
"""

import sys
import os
import asyncio
from dotenv import load_dotenv

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Load environment variables
load_dotenv()

# Import the MCP server
from src.server.linkedin_mcp_client import mcp

async def main():
    """Main function to run MCP server as HTTP server for GitHub Copilot."""
    
    # Check for required environment variables
    email = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")
    
    if not email or not password:
        print("❌ Error: LinkedIn credentials not found!")
        print("Please set LINKEDIN_EMAIL and LINKEDIN_PASSWORD environment variables.")
        print("You can set them in your .env file or as environment variables.")
        sys.exit(1)
    
    print("🚀 Starting LinkedIn Jobs MCP HTTP Server for GitHub Copilot...")
    print(f"📧 Authenticated as: {email[:5]}...@{email.split('@')[1] if '@' in email else 'unknown'}")
    print("🔧 Available tool: search_jobs")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📡 Listening for HTTP MCP requests...\n")
    
    try:
        # Run the FastMCP server as HTTP server using the built-in HTTP support
        await mcp.run_http_async(
            host="0.0.0.0",
            port=8000,
            transport="http"
        )
    except KeyboardInterrupt:
        print("\n👋 MCP HTTP server stopped by user.")
    except Exception as e:
        print(f"❌ Error running MCP HTTP server: {e}")
        sys.exit(1)

def run_sync():
    """Synchronous wrapper for running the server."""
    asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main())
