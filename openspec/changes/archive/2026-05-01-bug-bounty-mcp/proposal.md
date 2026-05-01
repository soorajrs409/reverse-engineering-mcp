## Why

Bug bounty activities often involve repetitive manual tasks across various security tools. By building a modular Model Context Protocol (MCP) server, we can expose these tools (starting with radare2) to LLMs, enabling automated analysis, faster vulnerability research, and a unified interface for specialized security tooling.

## What Changes

- **FastMCP Server**: Establish a Python-based MCP server using the FastMCP framework for high-level tool definition.
- **Modular Core**: Implement a plugin-style architecture that dynamically loads modules from a dedicated directory.
- **Radare2 Module**: Integrate `r2pipe` to provide the LLM with comprehensive access to radare2's binary analysis capabilities.
- **Environment Management**: Use `uv` for fast and reliable Python environment and dependency management.

## Capabilities

### New Capabilities
- `bug-bounty-core`: A modular foundation for registering and managing multiple security-focused MCP tools.
- `radare2-analysis`: A comprehensive set of tools exposing radare2's disassembly, analysis, and search functions to the MCP.

### Modified Capabilities
- None

## Impact

- **New Repository/Structure**: Creates the initial project layout for the Bug Bounty MCP suite.
- **Dependencies**: Introduces `fastmcp` and `r2pipe`.
- **Tooling**: Requires `radare2` to be installed on the host system.
- **Agent Interaction**: Provides the agent with direct binary analysis capabilities.
