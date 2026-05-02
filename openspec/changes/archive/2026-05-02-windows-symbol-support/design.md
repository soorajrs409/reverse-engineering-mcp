## Context

The Radare2 MCP currently excels at Linux binary analysis but lacks specialized support for Windows PE files, particularly regarding symbol management. Radare2 has powerful built-in commands (`idp`, `idpd`) for handling PDBs, but these require specific environment configurations to be effective in a persistent MCP setup.

## Goals / Non-Goals

**Goals:**
- Provide tools to load local and remote PDBs.
- Persist downloaded symbols in a workspace-local cache.
- Ensure the LLM can trigger symbol resolution for system libraries (DLLs).
- Maintain compatibility with the existing `Radare2SessionManager`.

**Non-Goals:**
- Supporting live debugging of Windows binaries on Linux (out of scope for this change).
- Rewriting PDB parsing logic (we rely entirely on Radare2's plugins).

## Decisions

### 1. Unified Symbol Store
We will redirect Radare2's `pdb.symstore` to `.r2_projects/symbols/` within the workspace.
- **Rationale**: Ensures that symbols downloaded in one turn are available in future turns and can be persisted if the workspace is mounted as a volume.
- **Alternative**: Using the default `~/.local/share/radare2/pdb`. Discarded because it's harder to manage persistence across different container instances.

### 2. Default Symbol Servers
We will configure `pdb.server` to include Microsoft's official symbol server by default.
- **Rationale**: Most Windows analysis involves standard system DLLs (ntdll, kernel32) which are readily available there.

### 3. "idp" vs "idpi*"
When loading a PDB, we will prefer `idpi*` (importing as flags) to ensure the LLM sees the symbols as part of the disassembly immediately.
- **Rationale**: Provides better immediate context in `pd` (disassemble) and `pdf` (function disassembly) outputs.

## Risks / Trade-offs

- **[Risk]** → PDB downloads can be slow and may time out.
  - **Mitigation** → Use `r2_cmd_with_retry` and ensure the tool wrapper handles network-related errors gracefully.
- **[Risk]** → Large PDBs might consume significant disk space.
  - **Mitigation** → Document the persistence directory so users can clear it if needed.
- **[Risk]** → The `idp` plugin might not be installed in all Radare2 distributions.
  - **Mitigation** → Add a check for `idp?` availability during tool execution and return a clear error if missing.
