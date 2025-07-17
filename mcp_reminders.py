#!/usr/bin/env python3
"""
AI Reminders MCP Service
A minimalistic MCP server that provides AI access to reminder notes.
"""

import asyncio
import sys
from pathlib import Path
from typing import List

# MCP imports
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
from mcp.types import Tool, TextContent
from mcp import types


class RemindersService:
    """Simple service to read reminders from a text file."""
    
    def __init__(self, reminders_file: str = "reminders.txt"):
        self.reminders_file = Path(reminders_file)
    
    def get_reminders(self) -> List[str]:
        """
        Read all reminders from the file.
        Returns empty list if file doesn't exist or is empty.
        """
        try:
            if not self.reminders_file.exists():
                return []
            
            with open(self.reminders_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Filter out empty lines and strip whitespace
            reminders = [line.strip() for line in lines if line.strip()]
            return reminders
        
        except PermissionError:
            return ["Error: Cannot read reminders file - permission denied"]
        except Exception as e:
            return [f"Error reading reminders: {str(e)}"]


# Initialize the service
reminders_service = RemindersService()

# Create MCP server
server = Server("ai-reminders")


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="get_reminders",
            description="Retrieve all current AI reminders from reminders.txt file",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> List[TextContent]:
    """Handle tool calls."""
    if name == "get_reminders":
        reminders = reminders_service.get_reminders()
        
        if not reminders:
            return [TextContent(
                type="text",
                text="No reminders found. The reminders.txt file is either missing or empty."
            )]
        
        # Format reminders as a clean list
        reminder_text = "Current AI Reminders:\n" + "\n".join(f"• {reminder}" for reminder in reminders)
        
        return [TextContent(
            type="text",
            text=reminder_text
        )]
    
    raise ValueError(f"Unknown tool: {name}")


async def main():
    """Main server entry point."""
    # Allow custom reminders file via command line
    if len(sys.argv) > 1:
        reminders_file = sys.argv[1]
        global reminders_service
        reminders_service = RemindersService(reminders_file)
        print(f"Using reminders file: {reminders_file}", file=sys.stderr)
    
    # Run the server using stdio
    async with stdio_server() as (read_stream, write_stream):
        init_options = InitializationOptions(
            server_name="ai-reminders",
            server_version="1.0.0",
            capabilities=server.get_capabilities(
                notification_options=types.NotificationOptions(),
                experimental_capabilities={},
            ),
        )
        await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    asyncio.run(main())
