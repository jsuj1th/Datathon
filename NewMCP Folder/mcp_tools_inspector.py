#!/usr/bin/env python3
"""
MCP Tools Inspector
Interactive tool to visualize and test MCP server capabilities
"""

import asyncio
import json
from pathlib import Path
from job_matcher_mcp_server import JobMatcherMCPServer


def print_tool_details(tool: dict, index: int):
    """Print detailed information about a tool"""
    print(f"\n{'='*70}")
    print(f"🔧 Tool #{index}: {tool['name']}")
    print(f"{'='*70}")
    print(f"\n📝 Description:")
    print(f"   {tool['description']}\n")

    print("📥 Input Schema:")
    schema = tool['inputSchema']

    if 'properties' in schema and schema['properties']:
        print("\n   Parameters:")
        for param_name, param_info in schema['properties'].items():
            param_type = param_info.get('type', 'any')
            param_desc = param_info.get('description', 'No description')
            required = '(required)' if param_name in schema.get('required', []) else '(optional)'

            print(f"      • {param_name} [{param_type}] {required}")
            print(f"        {param_desc}")

            if 'default' in param_info:
                print(f"        Default: {param_info['default']}")

            if 'items' in param_info:
                print(f"        Items: {param_info['items']}")
    else:
        print("   No parameters required")

    print()


def print_usage_example(tool: dict):
    """Print usage example for a tool"""
    print("💡 Example Usage:")

    example_args = {}

    if tool['name'] == 'collect_jobs':
        example_args = {
            "sources": ["linkedin", "github"],
            "keywords": ["AI", "ML", "new grad"]
        }

    elif tool['name'] == 'extract_resume_context':
        example_args = {
            "resume_path": "path/to/resume.pdf"
        }

    elif tool['name'] == 'match_jobs_with_resume':
        example_args = {
            "resume_path": "path/to/resume.pdf",
            "top_n": 50,
            "min_score": 70
        }

    elif tool['name'] == 'get_job_statistics':
        example_args = {}

    elif tool['name'] == 'analyze_job_match':
        example_args = {
            "job_index": 0,
            "resume_path": "path/to/resume.pdf"
        }

    elif tool['name'] == 'send_matches_email':
        example_args = {
            "recipient": "user@example.com",
            "top_n": 50
        }

    print(f"   await server.call_tool('{tool['name']}', {json.dumps(example_args, indent=6)})")
    print()


async def test_tool_interactive(server: JobMatcherMCPServer):
    """Interactive tool testing"""
    print("\n🧪 Interactive Tool Testing")
    print("="*70)

    tools = server.list_tools()

    print("\nSelect a tool to test:")
    for i, tool in enumerate(tools, 1):
        print(f"  {i}. {tool['name']}")
    print(f"  0. Exit")

    try:
        choice = int(input("\nEnter tool number: "))
        if choice == 0:
            return False

        if 1 <= choice <= len(tools):
            tool = tools[choice - 1]
            print(f"\n🔧 Testing: {tool['name']}")

            # Get arguments based on tool
            args = {}

            if tool['name'] == 'get_job_statistics':
                # No args needed
                pass

            elif tool['name'] == 'collect_jobs':
                args = {
                    "sources": ["linkedin", "github", "data"]
                }

            elif tool['name'] in ['extract_resume_context', 'match_jobs_with_resume', 'analyze_job_match']:
                resume_path = input("Enter resume PDF path (or press Enter for default): ").strip()
                if not resume_path:
                    resume_path = str(Path(__file__).parent / "MCP_Servers" / "pdfDocs" / "Resume_NEW_ML_Pathakota_Pranavi_2.pdf")
                args["resume_path"] = resume_path

                if tool['name'] == 'match_jobs_with_resume':
                    top_n = input("Top N matches (default 50): ").strip()
                    args["top_n"] = int(top_n) if top_n else 50

                if tool['name'] == 'analyze_job_match':
                    job_idx = input("Job index to analyze (default 0): ").strip()
                    args["job_index"] = int(job_idx) if job_idx else 0

            # Call the tool
            print(f"\n⏳ Executing {tool['name']}...\n")
            result = await server.call_tool(tool['name'], args)

            # Display result
            print("📊 Result:")
            print(json.dumps(result, indent=2, default=str))

            return True
        else:
            print("Invalid choice")
            return True

    except KeyboardInterrupt:
        print("\n\nExiting...")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return True


async def main():
    """Main inspector interface"""
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║           MCP TOOLS INSPECTOR - Job Matcher Server            ║")
    print("╚════════════════════════════════════════════════════════════════╝")

    server = JobMatcherMCPServer()

    while True:
        print("\n📋 Main Menu:")
        print("  1. List All Tools")
        print("  2. View Tool Details")
        print("  3. Test Tool (Interactive)")
        print("  4. Export Tools Schema (JSON)")
        print("  0. Exit")

        try:
            choice = input("\nSelect option: ").strip()

            if choice == "0":
                print("\n👋 Goodbye!")
                break

            elif choice == "1":
                # List all tools
                print("\n🔧 Available MCP Tools")
                print("="*70)
                tools = server.list_tools()
                for i, tool in enumerate(tools, 1):
                    print(f"\n{i}. {tool['name']}")
                    print(f"   {tool['description']}")

            elif choice == "2":
                # View tool details
                tools = server.list_tools()
                print("\n🔧 Select a tool to view details:")
                for i, tool in enumerate(tools, 1):
                    print(f"  {i}. {tool['name']}")

                tool_choice = int(input("\nEnter tool number: "))
                if 1 <= tool_choice <= len(tools):
                    tool = tools[tool_choice - 1]
                    print_tool_details(tool, tool_choice)
                    print_usage_example(tool)

            elif choice == "3":
                # Test tool interactively
                continue_testing = await test_tool_interactive(server)
                if not continue_testing:
                    break

            elif choice == "4":
                # Export schema
                tools = server.list_tools()
                schema = {
                    "server_name": "job-matcher",
                    "server_description": "AI-Powered Job Matching MCP Server",
                    "tools": tools,
                    "version": "1.0.0"
                }

                output_file = "mcp_tools_schema.json"
                with open(output_file, 'w') as f:
                    json.dump(schema, f, indent=2)

                print(f"\n✅ Schema exported to: {output_file}")
                print(f"📄 Total tools: {len(tools)}")

            else:
                print("Invalid option")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
