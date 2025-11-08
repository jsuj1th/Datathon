"""
Server package for LinkedIn Jobs MCP
"""

from .linkedin_mcp_client import mcp, search_jobs

__all__ = ["mcp", "search_jobs"]
