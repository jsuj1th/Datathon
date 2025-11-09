#!/bin/bash
# Launch MCP Inspector Web Interface for Job Matcher

echo "🚀 Launching MCP Inspector Web Interface"
echo "========================================"
echo ""
echo "This will open a web browser at: http://localhost:5173"
echo ""
echo "You'll be able to:"
echo "  ✅ Browse all 4 MCP tools"
echo "  ✅ View tool schemas and descriptions"
echo "  ✅ Test tools interactively"
echo "  ✅ See request/response logs"
echo ""
echo "Press Ctrl+C to stop the inspector"
echo ""
echo "========================================"
echo ""

# Launch the inspector
npx @modelcontextprotocol/inspector mcp-server-config.json
