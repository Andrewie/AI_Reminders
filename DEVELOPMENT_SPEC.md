# AI Reminders MCP Service - Development Specification

## Overview
A minimalistic Model Context Protocol (MCP) service that provides AI with constant access to reminder notes. The AI can check reminders with each prompt to maintain context across conversations.

## Core Requirements

### Functional Requirements
1. **Scan for reminders.txt** - Check project directory for reminders file
2. **Return reminders** - Provide all reminder content when file exists
3. **Handle missing file gracefully** - No errors when file doesn't exist or is empty
4. **Simple text format** - Plain text file, one reminder per line

### Non-Functional Requirements
- **Minimalistic**: Single-file implementation
- **Local execution**: No external dependencies or servers
- **Fast response**: Sub-100ms file read operations
- **Cross-platform**: Works on Windows, Mac, Linux

## Technical Architecture

### Technology Stack
- **Language**: Python 3.8+ (minimal dependencies)
- **Protocol**: Model Context Protocol (MCP)
- **Storage**: Plain text file (`reminders.txt`)
- **Packaging**: Single executable script

### File Structure
```
ai-reminders-mcp/
├── mcp_reminders.py          # Main MCP server
├── reminders.txt             # Reminder storage (created by user)
├── requirements.txt          # Python dependencies
├── README.md                 # Usage instructions
└── run.bat                   # Windows startup script
```

## Implementation Details

### MCP Server Capabilities
The service exposes one tool:
- **Tool Name**: `get_reminders`
- **Description**: "Retrieve all current AI reminders"
- **Input**: None
- **Output**: List of reminder strings or empty list

### File Format (reminders.txt)
```
Remember to validate user input before processing
Always check for edge cases in date calculations
Project deadline: July 30, 2025
Use consistent error handling patterns
```

### Error Handling
- File not found: Return empty list (no error)
- Empty file: Return empty list (no error)
- File read permission denied: Return error message
- Malformed file: Return available readable lines

### Performance Targets
- File read time: < 50ms for files up to 10KB
- Memory usage: < 5MB total
- Startup time: < 500ms

## Development Phases

### Phase 1: Core Implementation (1-2 hours)
1. Set up basic MCP server structure
2. Implement file reading functionality
3. Add reminder parsing logic
4. Basic error handling

### Phase 2: Polish & Testing (1 hour)
1. Add comprehensive error handling
2. Test with various file states
3. Create startup scripts
4. Write documentation

### Phase 3: Deployment (30 minutes)
1. Package for easy distribution
2. Test on target operating system
3. Create usage examples

## Usage Examples

### AI Integration
The AI can call the `get_reminders` tool with each prompt to access current reminders:

```
User: "Help me write a function to process dates"
AI: [Calls get_reminders tool]
AI: "I notice you have a reminder about checking edge cases in date calculations. Here's a robust date processing function..."
```

### User Workflow
1. Create/edit `reminders.txt` with any text editor
2. Add reminders (one per line)
3. AI automatically accesses reminders in conversations
4. Update reminders as needed

### Sample Reminders
```
Always validate input parameters
Remember to handle timezone conversions
Project uses UTC for all timestamps
Prefer explicit error messages over generic ones
Code review checklist: security, performance, readability
```

## Configuration

### Environment Variables
- `REMINDERS_FILE`: Path to reminders file (default: "./reminders.txt")
- `MCP_PORT`: Server port (default: auto-assign)
- `LOG_LEVEL`: Logging verbosity (default: "WARNING")

### Command Line Options
```bash
python mcp_reminders.py --file custom_reminders.txt --port 8080
```

## Security Considerations
- File access limited to specified reminders file
- No network access required
- No user input processing (read-only operation)
- File path validation to prevent directory traversal

## Testing Strategy
1. **Unit Tests**: File reading, parsing, error handling
2. **Integration Tests**: MCP protocol compliance
3. **Edge Case Tests**: Missing files, empty files, large files
4. **Performance Tests**: File read speed with various file sizes

## Deployment Instructions
1. Install Python 3.8+
2. Install MCP library: `pip install model-context-protocol`
3. Run server: `python mcp_reminders.py`
4. Configure AI client to connect to MCP server

## Success Criteria
- ✅ AI can retrieve reminders in < 100ms
- ✅ Service handles missing files gracefully
- ✅ Works on Windows without configuration
- ✅ Single command startup
- ✅ No external dependencies beyond Python stdlib + MCP

## Future Enhancements (Optional)
- Web interface for reminder management
- Reminder categories/tags
- Timestamp tracking for reminders
- Integration with task management systems
- Reminder scheduling/expiration

---

**Estimated Development Time**: 2-3 hours total
**Estimated Lines of Code**: ~150 lines Python
**Target File Size**: < 10KB executable
