#!/bin/bash

# Job Search Pipeline Launcher
# Simple menu to launch different components

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         🎯 JOB SEARCH & MATCHING SYSTEM                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Choose an option:"
echo ""
echo "  1) 🚀 Run Complete Pipeline (Interactive Job Search)"
echo "  2) 🌐 Launch MCP Tools Inspector (Web UI)"
echo "  3) 🔍 Search GitHub Jobs Only"
echo "  4) 🔍 Search LinkedIn Jobs Only"
echo "  5) 🤖 Run Job Matcher Only"
echo "  6) 📧 Send Email Test"
echo "  7) ❌ Exit"
echo ""
read -p "Enter your choice (1-7): " choice

case $choice in
    1)
        echo ""
        echo "🚀 Launching Complete Pipeline..."
        echo "============================================================"
        python3 main_complete_pipeline.py
        ;;
    2)
        echo ""
        echo "🌐 Launching MCP Tools Inspector..."
        echo "============================================================"
        echo "   Opening browser at http://localhost:8000"
        echo "   Press Ctrl+C to stop"
        echo ""
        cd "NewMCP Folder"
        python3 web_inspector_simple.py
        ;;
    3)
        echo ""
        echo "🔍 Searching GitHub Jobs..."
        echo "============================================================"
        cd github_collector
        python3 main.py
        ;;
    4)
        echo ""
        echo "🔍 Searching LinkedIn Jobs..."
        echo "============================================================"
        cd linkedin_collector
        python3 job_searcher.py
        ;;
    5)
        echo ""
        echo "🤖 Running Job Matcher..."
        echo "============================================================"
        cd "NewMCP Folder"
        python3 job_matcher.py
        ;;
    6)
        echo ""
        echo "📧 Testing Email Configuration..."
        echo "============================================================"
        python3 send_email_smtp.py
        ;;
    7)
        echo ""
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo ""
        echo "❌ Invalid choice. Please run again and choose 1-7."
        exit 1
        ;;
esac
