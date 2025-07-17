#!/bin/bash
echo "Starting AI Reminders MCP Service..."
echo "Press Ctrl+C to stop the service"
/e/DEV/anaconda3/python.exe mcp_reminders_prod.py
read -p "Press any key to continue..."
