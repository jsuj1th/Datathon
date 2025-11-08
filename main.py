#!/usr/bin/env python3
"""
Main entry point for the LinkedIn MCP Server
"""

import os
import sys
import asyncio
import uvicorn
from dotenv import load_dotenv

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from server.linkedin_mcp_client import mcp

def main():
    """Main function to start the MCP server"""
    # Load environment variables
    load_dotenv()
    
    # Check for required environment variables
    required_vars = ['LINKEDIN_EMAIL', 'LINKEDIN_PASSWORD']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these variables in your .env file or environment.")
        sys.exit(1)
    
    # Get server configuration
    host = os.getenv('MCP_SERVER_HOST', 'localhost')
    port = int(os.getenv('MCP_SERVER_PORT', 8000))
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    
    print(f"Starting LinkedIn MCP Server on {host}:{port}")
    print(f"Debug mode: {debug}")
    
    # Start the server
    try:
        # Import here to avoid circular imports
        from src.server.linkedin_mcp_client import mcp
        
        uvicorn.run(
            mcp.run,
            host=host,
            port=port,
            reload=debug,
            log_level="info" if not debug else "debug"
        )
    except KeyboardInterrupt:
        print("\nShutting down LinkedIn MCP Server...")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
