# Radare2 MCP Stability Guidelines

## Overview

The Radare2 MCP is designed to be a robust orchestration layer for binary analysis. This document outlines the stability benchmarks, known edge cases, and mitigation strategies implemented in the core and modules.

## Stability Benchmarks

- **Concurrent Access**: The system supports up to 5 concurrent tool calls per binary by using project-specific locks to prevent git index conflicts.
- **Error Resilience**: Every tool call is wrapped in `@mcp_tool_wrapper` which ensures a standardized JSON error response, preventing server crashes.
- **Retry Logic**: Radare2 commands use exponential backoff (initial delay 0.5s, max 3 retries) to handle transient failures.
- **Session Lifecycle**: 
    - **Static Sessions**: Auto-saved to `.r2_projects/` on exit.
    - **Debug Sessions**: Auto-cleaned after 10 minutes of inactivity.
- **Symbolic Execution**: Limited to 100 steps per exploration to prevent memory exhaustion.

## Known Edge Cases

### 1. Large Binaries
- **Issue**: Analysis (`aaa`) can take a long time and potentially timeout the MCP connection.
- **Mitigation**: Use persistent projects. The first load will be slow, but subsequent loads will use the saved state.

### 2. Project Corruption
- **Issue**: If a Radare2 process crashes during a project save, a stale `index.lock` might be left behind.
- **Mitigation**: `Radare2SessionManager` automatically detects and removes stale `index.lock` files before opening a session.

### 3. Debug Session Timeouts
- **Issue**: If the LLM doesn't interact with a debug session for 10 minutes, the session is closed.
- **Mitigation**: The system logs expiration events. The LLM should be prepared to restart sessions if needed.

### 4. Symbolic State Explosion
- **Issue**: Complex functions can lead to a state explosion in Angr.
- **Mitigation**: Explorations are capped at 100 steps. If no path is found within this limit, an error is returned.

## Stability Audit Tool

To run the latest stability tests:
```bash
./.venv/bin/python3 tests/verify_stability.py
```
This tool performs:
1. Environment validation.
2. Error injection (invalid files/commands).
3. Stress testing (concurrent analysis).
