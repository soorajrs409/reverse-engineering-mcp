## Why

Current Radare2 tools are stateless and limited to raw command execution, which forces AI agents to re-analyze binaries on every call and prevents them from maintaining an evolving mental model of the target. To be effective in bug bounties, agents need a persistent analysis environment where they can label findings, trace data flows, and perform deep reconnaissance without session overhead.

## What Changes

- **Persistent Sessions**: Transition from a stateless "open-close" model to a stateful project-based model using Radare2 projects stored in a workspace-local `.r2_projects/` directory.
- **Deep Recon Tools**: New tools for extracting security protections (NX, Canary, ASLR), identifying dangerous imports (sinks), and mapping entry points.
- **Data & Control Flow**: Implementation of cross-reference (Xref) and call graph tools to allow agents to trace user input to vulnerable code paths.
- **State Management**: Tools for agents to rename symbols, label functions, and add comments that persist throughout the analysis.
- **Advanced Analysis**: Support for stack variable analysis and entropy mapping to find packed sections.

## Capabilities

### New Capabilities
- `radare2-session-management`: Handling the lifecycle of persistent Radare2 projects, including creation, loading, and auto-saving.
- `radare2-vulnerability-recon`: Extracting high-signal binary metadata and highlighting dangerous API usage to map the attack surface.
- `radare2-advanced-analysis`: Providing deep insights into function structures, variable offsets, and code relationships (Xrefs/Call Graphs).

### Modified Capabilities
- `radare2-analysis`: Upgrading the existing basic analysis tools to utilize the new persistent session architecture.

## Impact

- **`modules/radare2_module.py`**: Major refactor to implement session management and the new tool suite.
- **`main.py`**: Minor updates to ensure proper initialization of the new capabilities.
- **File System**: Introduction of a `.r2_projects/` directory to store persistent analysis data.
- **Dependencies**: Ensures `r2pipe` is optimized for session-based interaction.
