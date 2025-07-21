#!/usr/bin/env python3
"""
WHOOP MCP Server

A Model Context Protocol server that provides access to WHOOP fitness data
through Claude Desktop using FastMCP.
"""
import asyncio
import json
import sys
from datetime import datetime
from typing import Dict, Any

from mcp.server.fastmcp import FastMCP

# Import our WHOOP client
from whoop_client import WhoopClient

# Create FastMCP server
mcp = FastMCP("whoop-mcp-server")

# Global WHOOP client
whoop_client = None

def init_whoop_client():
    """Initialize WHOOP client"""
    global whoop_client
    if whoop_client is None:
        print("Initializing WHOOP client...", file=sys.stderr)
        whoop_client = WhoopClient()
        auth_status = whoop_client.get_auth_status()
        print(f"WHOOP auth status: {auth_status['status']}", file=sys.stderr)
    return whoop_client

@mcp.tool()
def get_whoop_auth_status() -> Dict[str, Any]:
    """Get WHOOP authentication status"""
    print("Tool called: get_whoop_auth_status", file=sys.stderr)
    
    try:
        init_whoop_client()
        status = whoop_client.get_auth_status()
        result = {
            "tool": "get_whoop_auth_status",
            "data": status,
            "timestamp": datetime.now().isoformat()
        }
        print(f"Auth status result: {status['status']}", file=sys.stderr)
        return result
    except Exception as e:
        print(f"Error in get_whoop_auth_status: {e}", file=sys.stderr)
        return {
            "tool": "get_whoop_auth_status",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@mcp.tool()
async def get_whoop_profile() -> Dict[str, Any]:
    """Get WHOOP user profile information"""
    print("Tool called: get_whoop_profile", file=sys.stderr)
    
    try:
        init_whoop_client()
        data = await whoop_client.get_user_profile()
        result = {
            "tool": "get_whoop_profile",
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        print(f"Profile result: {data.get('first_name', 'N/A')}", file=sys.stderr)
        return result
    except Exception as e:
        print(f"Error in get_whoop_profile: {e}", file=sys.stderr)
        return {
            "tool": "get_whoop_profile",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@mcp.tool()
async def get_whoop_workouts(limit: int = 5) -> Dict[str, Any]:
    """Get WHOOP workout data"""
    print(f"Tool called: get_whoop_workouts (limit={limit})", file=sys.stderr)
    
    try:
        init_whoop_client()
        data = await whoop_client.get_workouts(limit=limit)
        result = {
            "tool": "get_whoop_workouts",
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        print(f"Workouts result: {len(data)} workouts", file=sys.stderr)
        return result
    except Exception as e:
        print(f"Error in get_whoop_workouts: {e}", file=sys.stderr)
        return {
            "tool": "get_whoop_workouts",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@mcp.tool()
async def get_whoop_recovery(limit: int = 5) -> Dict[str, Any]:
    """Get WHOOP recovery data"""
    print(f"Tool called: get_whoop_recovery (limit={limit})", file=sys.stderr)
    
    try:
        init_whoop_client()
        data = await whoop_client.get_recovery(limit=limit)
        result = {
            "tool": "get_whoop_recovery",
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        print(f"Recovery result: {len(data)} records", file=sys.stderr)
        return result
    except Exception as e:
        print(f"Error in get_whoop_recovery: {e}", file=sys.stderr)
        return {
            "tool": "get_whoop_recovery",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    print("Starting Final WHOOP MCP Server with FastMCP...", file=sys.stderr)
    
    # Initialize WHOOP client early
    init_whoop_client()
    
    print("FastMCP server ready", file=sys.stderr)
    # Run the FastMCP server
    mcp.run()