## Context

The current `radare2_module.py` implements a stateless interface where each tool call opens a new `r2pipe` connection, performs minimal analysis, executes a command, and closes. This results in significant overhead for large binaries and prevents AI agents from maintaining state (such as function renames or comments) across multiple turns. For bug bounty tasks, this lack of continuity is a major bottleneck.

## Goals / Non-Goals

**Goals:**
- Implement a stateful `SessionManager` that handles Radare2 project persistence.
- Store analysis data in a workspace-local `.r2_projects/` directory.
- Provide a suite of "High-Signal" tools for reconnaissance (security flags, dangerous sinks).
- Enable agents to label and comment on code, with those changes persisting across sessions.
- Reduce latency by avoiding redundant analysis on every tool call.

**Non-Goals:**
- Support for dynamic analysis or debugging (static analysis only).
- Integration with other tools like Ghidra or GDB (focused strictly on Radare2).
- Real-time collaborative analysis (single-user focus).

## Decisions

### 1. Workspace-Local Project Storage
**Decision**: Store Radare2 projects in `.r2_projects/` within the project root.
**Rationale**: Keeps analysis data isolated to the workspace and prevents cluttering the user's global `~/.config/radare2` directory. It also ensures that the analysis state is easily manageable and deletable by the user.

### 2. Dedicated Session Manager Class
**Decision**: Create a `Radare2SessionManager` class to encapsulate `r2pipe` lifecycle and project path logic.
**Rationale**: Centralizes the logic for checking if a project exists, performing initial analysis (`aaa`), and saving state. This reduces code duplication across tool definitions.

### 3. JSON-First Communication
**Decision**: Use Radare2's JSON output commands (e.g., `iIj`, `iij`, `aflj`) whenever possible.
**Rationale**: JSON is easier for the MCP (and the LLM) to parse reliably compared to raw text tables, which are prone to formatting issues.

### 4. Tiered Analysis
**Decision**: Perform `aaa` (deep analysis) on the first time a binary is opened, and use the saved project for all subsequent calls.
**Rationale**: Deep analysis is expensive but necessary for tools like Xrefs and Call Graphs. Doing it once and persisting the results is the most efficient approach for a stateful agent.

## Risks / Trade-offs

- **[Risk] Initial Analysis Latency** → For very large binaries, the first `aaa` call might take a long time. 
  - **Mitigation**: We could consider a "Quick Analysis" (`aa`) option if the agent only needs basic info, but for "In-Depth" capability, deep analysis is preferred.
- **[Risk] Project File Bloat** → Persistent projects can grow large.
  - **Mitigation**: Added a `r2_cleanup_project` tool to allow manual or automated cleanup of the `.r2_projects/` folder.
- **[Risk] State Desync** → If multiple agents or tools modify the same binary project simultaneously.
  - **Mitigation**: The current MCP architecture is largely sequential for a single user/session, which naturally mitigates most race conditions.
