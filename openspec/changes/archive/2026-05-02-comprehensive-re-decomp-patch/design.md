## Context

The `Radare2SessionManager` currently handles project-based persistence but defaults to read-only access for safety. It lacks a mechanism to select decompiler backends or enable write-mode for patching.

## Goals / Non-Goals

**Goals:**
- Implement a tiered decompiler tool that prioritizes high-quality pseudo-code (Ghidra/r2dec) but falls back to native `pdc`.
- Implement a patching tool that allows for safe modification of binary content (assembly/hex).
- Update the session manager to support write-mode and decompiler configuration.

**Non-Goals:**
- Real-time interactive debugging (out of scope for this phase).
- Remote binary patching.

## Decisions

- **Decision: Tiered Decompilation Logic.**
  - **Rationale:** Different environments have different plugins installed. The MCP should be resilient.
  - **Logic:** Check for `pdg` (r2ghidra), then `pdd` (r2dec), then use `pdc`.
- **Decision: Write-Mode Session Management.**
  - **Rationale:** Patching requires the `-w` flag.
  - **Approach:** Add a `write_mode` parameter to `Radare2SessionManager`. Only tools requiring patching will request this.
- **Decision: Use of `r2pipe` for Patching.**
  - **Rationale:** `wa` (write assembly) and `wx` (write hex) are robust via `r2pipe`.

## Risks / Trade-offs

- **[Risk]** Accidental binary corruption during patching.
  - **Mitigation:** Ensure the session manager saves and cleans up correctly. Add a warning to the tool description.
- **[Risk]** Decompiler plugins failing or hanging.
  - **Mitigation:** Use timeouts for decompiler commands if possible, and rely on the fallback mechanism.
