## Context

The Radare2 MCP currently provides static analysis (via `radare2_module.py`) and dynamic analysis (via `debugging_module.py`). While it can emulate code using Radare2's ESIL engine, it lacks the ability to solve for specific inputs or explore complex execution paths. Angr is a powerful symbolic execution framework that can fill this gap by providing constraint solving (via Z3) and sophisticated path exploration.

## Goals / Non-Goals

**Goals:**
- Integrate Angr as a library within the MCP.
- Provide tools to find paths to specific code locations.
- Support solving for input constraints (stdin, arguments).
- Enable "concolic" transition from a live r2 debug session to an Angr symbolic state.
- Keep the integration modular and lightweight where possible.

**Non-Goals:**
- Replacing Radare2 as the primary analysis engine.
- Supporting every architecture that Angr supports (initial focus on x86_64/ARM).
- Real-time symbolic execution (Angr is relatively slow).

## Decisions

### 1. Direct Angr Library Usage
We will use `angr` as a Python library rather than calling an external CLI or plugin.
- **Rationale:** Better control over the exploration process and easier integration with the existing Python-based MCP.
- **Alternative:** `r2angr` plugin. Discarded because it's harder to manage dependencies and versioning across different environments.

### 2. Module Separation
Create `modules/symbolic_module.py` instead of adding to `radare2_module.py`.
- **Rationale:** `angr` is a heavy dependency and the symbolic execution logic is distinct from general radare2 management. This keeps the core lightweight.

### 3. State Handoff via Register/Memory Sync
To support concolic execution, we will capture the CPU state (registers) and memory maps from a live `r2` debug session and initialize an Angr `SimState` with them.
- **Rationale:** Allows the user to bypass complex initialization (like loaders, encryption setup) concretely in the debugger before switching to symbolic exploration.

## Risks / Trade-offs

- **[Risk]** → `angr` is resource-intensive and may crash in low-memory environments.
  - **Mitigation** → Use `fastmcp` timeouts and provide clear error messages if memory limits are hit.
- **[Risk]** → State explosion in symbolic execution.
  - **Mitigation** → Implement conservative exploration limits (e.g., max steps, max paths) and allow the LLM to specify target/avoid addresses.
- **[Risk]** → Environment mismatch between `r2` and `angr` (e.g., libc versions).
  - **Mitigation** → Use `angr`'s `CLE` loader to load the same binary being analyzed by `r2`.
