## Why

The current MCP provides static analysis but lacks the ability to view high-level pseudo-code (decompilation) and modify binary behavior (patching). Adding these capabilities transforms the MCP from a passive reader into an active tool for comprehensive reverse engineering and vulnerability research.

## What Changes

- Add a decompilation tool that leverages available Radare2 backends (`pdc`, `pdd`, `pdg`) to provide pseudo-code.
- Add a binary patching tool that enables writing assembly or hex directly to the binary in write-mode.
- Update the Radare2 module to support write-mode and decompiler selection logic.

## Capabilities

### New Capabilities
- `radare2-decompilation`: Provides pseudo-code for functions using multiple decompiler backends.
- `radare2-patching`: Enables binary modification via assembly or hex writes.

### Modified Capabilities
- `radare2-core`: Update to handle write-mode sessions and environmental checks for decompiler plugins.

## Impact

- `modules/radare2_module.py`: New tools and updated session management.
- `tests/`: New verification scripts for decompilation and patching.
- Potential impact on binary files during patching (requires careful session handling).
