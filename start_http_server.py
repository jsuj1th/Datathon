#!/usr/bin/env python3
"""
Simple HTTP Server Starter for LinkedIn MCP Server
Quick way to start the HTTP server for GitHub Copilot integration.
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Start the HTTP server."""
    print("🚀 Starting LinkedIn Jobs MCP HTTP Server...")
    print("🔧 This will start the server at http://localhost:8000")
    print("📋 Make sure your .env file has LinkedIn credentials set up")
    print("⏹️  Press Ctrl+C to stop the server\n")
    
    # Check if .env exists
    env_path = Path(".env")
    if not env_path.exists():
        print("⚠️  Warning: .env file not found. Make sure to set LINKEDIN_EMAIL and LINKEDIN_PASSWORD")
    
    try:
        # Run the copilot runner
        subprocess.run([sys.executable, "copilot_runner.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running server: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ Error: copilot_runner.py not found. Make sure you're in the right directory.")
        sys.exit(1)

if __name__ == "__main__":
    main()
