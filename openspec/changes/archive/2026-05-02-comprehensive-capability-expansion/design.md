## Context

The Radare2 MCP currently supports basic static analysis (disassembly, binary info) and dynamic debugging. To support sophisticated vulnerability research, it needs to expose more of radare2's advanced features. The primary challenge is mapping complex, multi-line, or non-JSON radare2 command outputs into structured JSON that an LLM can reliably parse and use.

## Goals / Non-Goals

**Goals:**
- Expose ROP gadget discovery, mitigation auditing, and signature matching.
- Provide static emulation capabilities via ESIL.
- Implement a structured way for the LLM to manage C-style types and structs in the r2 project.
- Ensure all new tools follow the existing `@mcp_tool_wrapper` and session management patterns.

**Non-Goals:**
- Implementing a full-blown GUI for radare2.
- Replacing the need for a live debugger for all dynamic tasks (ESIL is for small-block simulation).
- Modifying the underlying `r2pipe` library.

## Decisions

### 1. JSON-First Tool Output
- **Decision**: All new tools will prioritize returning JSON (using radare2's `*j` command variants).
- **Rationale**: LLMs are much better at processing structured data than parsing variable-format CLI tables.
- **Alternatives**: Returning raw string output (discarded due to fragility).

### 2. Type Management via `t` Commands
- **Decision**: Implement type management using radare2's `t` (types) command family. This includes `td` for defining structs and `ts` for listing them.
- **Rationale**: Radare2's type system is robust and persists in the project file, allowing the LLM to build a shared understanding of data structures.

### 3. ESIL Emulation for "Dry Runs"
- **Decision**: Use `aei`, `aeim`, and `aeu` commands to provide a controlled static emulation environment.
- **Rationale**: This allows for "what-if" analysis of code paths without the overhead or risks of starting a live debug session.

### 4. Integration with `Radare2SessionManager`
- **Decision**: All static analysis tools will continue to use the `with Radare2SessionManager(file_path) as session:` pattern.
- **Rationale**: Ensures that signature matches, type definitions, and comments are saved across different tool calls.

## Risks / Trade-offs

- **[Risk]** → Complex JSON output from commands like `/Rj` (ROP) can be extremely large and exceed token limits.
  - **Mitigation** → Implement optional filtering or limit parameters in the tool functions (e.g., `count`, `pattern`).
- **[Risk]** → ESIL emulation state might become desynchronized if multiple tools try to emulate different paths simultaneously.
  - **Mitigation** → Ensure emulation tools are atomic and re-initialize the ESIL state (`aei`) as needed.
- **[Risk]** → Native `pdc` decompiler is weak.
  - **Mitigation** → While out of scope for *implementing* new decompilers, we will ensure that the type system improvements directly benefit `pdc` by providing it with more context.
