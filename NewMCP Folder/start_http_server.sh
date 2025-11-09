#!/bin/bash
# Start the MCP HTTP Server for GitHub Copilot

echo "🚀 Starting MCP HTTP Server for GitHub Copilot..."
echo ""

cd "$(dirname "$0")"

# Check if the job data exists
if [ ! -f "../data/texas_ml_jobs_latest.json" ]; then
    echo "📊 Job data not found. Generating..."
    python3 ../get_texas_ml_jobs.py
    echo ""
fi

# Start the server
echo "🌐 Starting HTTP server on http://localhost:8080"
echo ""
python3 simple_mcp_http_server.py
