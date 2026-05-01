## Context

The current MCP server architecture is designed for stateless tool execution. However, interactive debugging requires a persistent connection to a running process (`r2 -d`). To bridge this gap, we must implement a mechanism to manage background Radare2 processes that remain alive between discrete tool calls.

## Goals / Non-Goals

**Goals:**
- Provide a stateful debugging experience through stateless tool calls.
- Support essential debugging operations: step, continue, breakpoint, register read/write.
- Ensure efficient resource management and automatic cleanup of abandoned sessions.

**Non-Goals:**
- Multi-user session sharing.
- Remote debugging over a network (sessions are local to the server/container).
- High-frequency tracing (performance is limited by the overhead of discrete tool calls).

## Decisions

- **Decision: Persistent Background Processes.**
  - **Rationale:** Standard `r2pipe` sessions terminate when the script ends. We need a background "daemon" or long-lived process to maintain the debug state.
  - **Implementation:** Use a global `DebugSessionManager` that holds references to `r2pipe` objects and their associated subprocesses.
- **Decision: Session Tracking via UUIDs.**
  - **Rationale:** Multiple debug sessions might be active. UUIDs provide a safe way for the LLM to target a specific session.
- **Decision: Automatic Time-based Cleanup.**
  - **Rationale:** Orphaned debug sessions consume system resources (PIDs, memory).
  - **Approach:** Implement a background thread or a per-call check that terminates sessions that haven't been accessed for a configurable period (e.g., 10 minutes).
- **Decision: Simplified Action Tool.**
  - **Rationale:** Instead of dozens of small tools, a unified `r2_debug_action` tool reduces complexity and makes the API more flexible for various Radare2 debug commands.

## Risks / Trade-offs

- **[Risk] Resource Exhaustion.**
  - **Mitigation:** Strict session limits and aggressive cleanup of idle processes.
- **[Risk] Process Hangs.**
  - **Mitigation:** Use timeouts for all `r2.cmd` calls within the debug session.
- **[Risk] Security Vulnerabilities (Code Execution).**
  - **Mitigation:** The system runs inside a Docker container, providing isolation. The LLM's access is restricted to the tools provided.
