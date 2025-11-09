#!/bin/bash
# Quick launcher for Job Matcher Application

echo "🚀 Job Matcher Application Launcher"
echo "===================================="
echo ""
echo "Choose an option:"
echo ""
echo "1. 🎯 Run Interactive Job Search (Recommended)"
echo "2. 🌐 Open Web Inspector (View MCP Tools)"
echo "3. 🔧 Test MCP Server"
echo "4. 📊 View Existing Matched Jobs"
echo ""
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🎯 Starting Interactive Job Search..."
        echo ""
        cd "/Users/sujithjulakanti/Desktop/Datathon"
        python3 main_job_application.py
        ;;
    2)
        echo ""
        echo "🌐 Opening Web Inspector..."
        echo "   Access at: http://localhost:8000"
        echo ""
        cd "/Users/sujithjulakanti/Desktop/Datathon/NewMCP Folder"
        python3 web_inspector_simple.py
        ;;
    3)
        echo ""
        echo "🔧 Testing MCP Server..."
        echo ""
        cd "/Users/sujithjulakanti/Desktop/Datathon/NewMCP Folder"
        python3 job_matcher_mcp_stdio.py --version
        ;;
    4)
        echo ""
        echo "📊 Viewing Matched Jobs..."
        echo ""
        cd "/Users/sujithjulakanti/Desktop/Datathon"
        if [ -f "matched_jobs/top_matches.json" ]; then
            python3 -c "
import json
with open('matched_jobs/top_matches.json') as f:
    data = json.load(f)
    print(f\"Total Matches: {data.get('total_matches', 0)}\")
    print(f\"Generated: {data.get('generated_at', 'Unknown')}\")
    print(\"\nTop 10 Jobs:\")
    for i, job in enumerate(data.get('matched_jobs', [])[:10], 1):
        print(f\"{i}. {job.get('position')} at {job.get('company')}\")
        print(f\"   Score: {job.get('match_score')}/100\")
        print(f\"   {job.get('match_reason', '')}\")
        print()
"
        else
            echo "❌ No matched jobs found. Run option 1 first!"
        fi
        ;;
    *)
        echo ""
        echo "❌ Invalid choice. Please run again and select 1-4."
        ;;
esac
