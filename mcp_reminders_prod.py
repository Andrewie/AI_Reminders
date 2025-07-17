#!/usr/bin/env python3
"""
AI Reminders MCP Service - Production Version
A minimalistic MCP server that provides AI access to reminder notes.
"""

import json
import sys
import os
from pathlib import Path
from typing import List, Dict, Any


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


class MCPReminderServer:
    """MCP server implementation for AI reminders."""
    
    def __init__(self, reminders_file: str = "reminders.txt"):
        self.reminders_service = RemindersService(reminders_file)
        self.server_info = {
            "name": "ai-reminders",
            "version": "1.0.0"
        }
    
    def log(self, message: str):
        """Log messages to stderr."""
        print(f"[MCP Reminders] {message}", file=sys.stderr)
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP requests."""
        method = request.get("method", "")
        request_id = request.get("id")
        
        try:
            if method == "initialize":
                return self._handle_initialize(request_id)
            elif method == "tools/list":
                return self._handle_tools_list(request_id)
            elif method == "tools/call":
                return self._handle_tools_call(request_id, request.get("params", {}))
            elif method == "ping":
                return self._handle_ping(request_id)
            else:
                return self._error_response(request_id, -32601, f"Method not found: {method}")
        
        except Exception as e:
            self.log(f"Error handling request: {e}")
            return self._error_response(request_id, -32603, f"Internal error: {str(e)}")
    
    def _handle_initialize(self, request_id) -> Dict[str, Any]:
        """Handle initialization request."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": self.server_info
            }
        }
    
    def _handle_tools_list(self, request_id) -> Dict[str, Any]:
        """Handle tools list request."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {
                        "name": "get_reminders",
                        "description": "Retrieve all current AI reminders from reminders.txt file",
                        "inputSchema": {
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    }
                ]
            }
        }
    
    def _handle_tools_call(self, request_id, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools call request."""
        tool_name = params.get("name")
        
        if tool_name == "get_reminders":
            reminders = self.reminders_service.get_reminders()
            
            if not reminders:
                content = "No reminders found. The reminders.txt file is either missing or empty."
            else:
                content = "Current AI Reminders:\n" + "\n".join(f"• {reminder}" for reminder in reminders)
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": content
                        }
                    ]
                }
            }
        else:
            return self._error_response(request_id, -32602, f"Unknown tool: {tool_name}")
    
    def _handle_ping(self, request_id) -> Dict[str, Any]:
        """Handle ping request."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {}
        }
    
    def _error_response(self, request_id, code: int, message: str) -> Dict[str, Any]:
        """Create an error response."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }
    
    def run(self):
        """Run the MCP server."""
        self.log("AI Reminders MCP Server starting...")
        self.log(f"Reminders file: {self.reminders_service.reminders_file}")
        
        try:
            for line in sys.stdin:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    request = json.loads(line)
                    response = self.handle_request(request)
                    print(json.dumps(response))
                    sys.stdout.flush()
                except json.JSONDecodeError as e:
                    self.log(f"Invalid JSON received: {e}")
                    continue
        except KeyboardInterrupt:
            self.log("Server interrupted by user")
        except Exception as e:
            self.log(f"Server error: {e}")
            raise


def test_reminders_locally():
    """Test the reminders functionality locally."""
    print("Testing AI Reminders Service locally...", file=sys.stderr)
    
    service = RemindersService()
    reminders = service.get_reminders()
    
    print(f"Found {len(reminders)} reminders:", file=sys.stderr)
    for i, reminder in enumerate(reminders, 1):
        print(f"  {i}. {reminder}", file=sys.stderr)
    
    if not reminders:
        print("  No reminders found (file missing or empty)", file=sys.stderr)
    
    print("Local test completed successfully!", file=sys.stderr)


def main():
    """Main entry point."""
    # Parse command line arguments
    reminders_file = "reminders.txt"
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            test_reminders_locally()
            return
        elif sys.argv[1] == "--help":
            print("AI Reminders MCP Server", file=sys.stderr)
            print("Usage:", file=sys.stderr)
            print("  python mcp_reminders_prod.py [reminders_file]", file=sys.stderr)
            print("  python mcp_reminders_prod.py --test", file=sys.stderr)
            print("  python mcp_reminders_prod.py --help", file=sys.stderr)
            return
        else:
            reminders_file = sys.argv[1]
    
    # Create and run the server
    server = MCPReminderServer(reminders_file)
    server.run()


if __name__ == "__main__":
    main()
