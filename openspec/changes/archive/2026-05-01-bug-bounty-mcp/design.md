## Context

The project aims to build a specialized MCP server for bug bounty hunters. Currently, there is no unified interface to expose low-level security tools like radare2 to LLMs in a modular way.

## Goals / Non-Goals

**Goals:**
- Provide a modular Python framework for bug bounty tools.
- Implement a comprehensive radare2 module.
- Use `uv` for environment setup.
- Enable dynamic loading of new modules without core server changes.

**Non-Goals:**
- Building a full GUI for radare2.
- Support for non-Python based modules (at this stage).
- Providing built-in exploit payloads (focus is on analysis tools).

## Decisions

### 1. Framework: FastMCP
**Choice**: Use `jlowin/fastmcp` instead of the low-level `modelcontextprotocol/python-sdk`.
**Rationale**: FastMCP provides a much more ergonomic, decorator-driven API (similar to FastAPI/Flask) which significantly reduces boilerplate and accelerates tool development.

### 2. Architecture: Dynamic Module Loading
**Choice**: A "Core + Modules" pattern where `main.py` discovers and registers tools from a `modules/` directory.
**Rationale**: This promotes separation of concerns and allows the user to easily share or add new bug bounty modules without touching the core server logic.

### 3. Radare2 Interface: r2pipe
**Choice**: Use the official `r2pipe` library.
**Rationale**: It is the standard, stable way to communicate with radare2 over various protocols (pipe, tcp, etc.) and handles JSON serialization of radare2 output cleanly.

## Risks / Trade-offs

- **[Risk] Radare2 Requirement**: The host system MUST have `radare2` installed and in the PATH.
  - **Mitigation**: Add a check at startup to verify `r2` availability and provide a clear error message.
- **[Risk] Command Injection (r2 level)**: Exposing an arbitrary command tool (`r2_cmd`) could be misused if the agent attempts malicious patterns.
  - **Mitigation**: While we want "full access," we should document that this tool operates with the permissions of the user running the MCP server.
- **[Risk] Large Output**: Some radare2 commands (like full disassembly) can return massive amounts of text that exceed LLM context windows.
  - **Mitigation**: Implement truncation or suggest specific range-based tools to the agent.
