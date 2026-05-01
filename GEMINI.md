# Radare2 MCP Engineering Standards

## Architecture Overview

This project follows a modular architecture designed for persistence and reliability in LLM-driven binary analysis.

### Core Components
- **`core/r2_base.py`**: The foundation of the toolchain. It provides:
    - `@mcp_tool_wrapper`: A decorator that handles orchestration metadata (like `wait_for_previous`) internally and returns structured JSON error responses instead of raising exceptions. This keeps tool signatures clean and compatible with `fastmcp`.
    - `r2_cmd_with_retry`: A utility for executing Radare2 commands with automatic retries on transient failures.
- **`modules/radare2_module.py`**: Handles static analysis and persistent session management. It uses `.r2_projects/` to track analysis state (renames, comments, type definitions) across tool calls.
    - **Advanced Capabilities**: Includes ROP discovery, mitigation auditing, ESIL emulation, and C-style type management.
- **`modules/debugging_module.py`**: Manages interactive debugging sessions using `r2pipe` in debug mode (`-d`).

## Development Conventions

### 1. Tool Implementation
Every tool function registered with the MCP server MUST:
- Use the `@mcp_tool_wrapper` decorator.
- Return a string (typically JSON-formatted for complex data).
- Handle its own `r2` session using the `Radare2SessionManager` (for static tools) or `manager.get_session()` (for debugging tools).
- **Signature Constraint**: Do NOT include `**kwargs` in the tool signature. The `@mcp_tool_wrapper` handles metadata transparently.

### 2. Session Management
- **Static Analysis**: Tools should leverage `Radare2SessionManager` to ensure that work is saved to a project file. This allows the LLM to resume analysis later.
- **Debugging**: Sessions are stateful and kept alive by the `DebugSessionManager`. They have a default timeout (e.g., 10 minutes) and are cleaned up by a background thread.

### 3. Error Handling
Never allow a raw Python exception to propagate out of a tool. Use the `@mcp_tool_wrapper` to catch errors and return a JSON object with:
```json
{
  "status": "error",
  "tool": "tool_name",
  "message": "Human-readable error",
  "type": "ExceptionType"
}
```

### 4. Persistence
The `.r2_projects/` directory is critical for maintaining state. It should be treated as a persistent volume in Docker environments.

## Testing Strategy
- **Manual Verification**: Use `tests/verify_all_features.py` (when available) to exercise the full stack.
- **Unit Testing**: Prefer tests that run with `PYTHONPATH=.` to ensure module imports resolve correctly.
