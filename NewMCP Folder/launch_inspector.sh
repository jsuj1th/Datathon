#!/bin/bash
# Launch MCP Inspector with Job Matcher Server

echo "🚀 Launching MCP Inspector for Job Matcher Server"
echo "=================================================="

# Get the directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if npx is installed
if ! command -v npx &> /dev/null; then
    echo "❌ npx not found. Please install Node.js first."
    exit 1
fi

# Set the command to run the MCP server
export MCP_SERVER_COMMAND="python3 $DIR/job_matcher_mcp_stdio.py"

echo "📡 MCP Server: $MCP_SERVER_COMMAND"
echo "🌐 Starting Inspector..."
echo ""
echo "The browser will open automatically at http://localhost:5173"
echo "If it doesn't open, manually visit: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop the inspector"
echo ""

# Run the inspector
npx @modelcontextprotocol/inspector python3 "$DIR/job_matcher_mcp_stdio.py"
