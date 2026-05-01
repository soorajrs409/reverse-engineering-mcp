## Why

The current Radare2 MCP provides foundational analysis and debugging tools but lacks specialized capabilities required for advanced security research, such as ROP gadget discovery, automated mitigation analysis, static emulation, and formal type management. Expanding these capabilities will empower the LLM to perform more autonomous and in-depth vulnerability research.

## What Changes

- **New Security Tools**: Added tools for ROP gadget discovery and binary mitigation analysis.
- **Enhanced Data Discovery**: Added comprehensive string extraction and hex byte searching.
- **Static Emulation**: Introduced ESIL-based function emulation for dry-running code without a live debugger.
- **Type & Struct Management**: Added capabilities to define, manage, and apply C-style structs and types to the analysis project.
- **Signature Identification**: Added support for Zignatures to identify library functions in stripped binaries.

## Capabilities

### New Capabilities
- `radare2-rop-analysis`: Tools for finding and analyzing ROP gadgets.
- `radare2-mitigation-audit`: Automated check of binary security mitigations (NX, Canary, PIE, RELRO).
- `radare2-emulation`: Static code emulation using radare2's ESIL engine.
- `radare2-type-system`: Capabilities to define and apply structs and types to memory addresses.
- `radare2-enhanced-search`: Advanced string extraction and hex pattern searching.
- `radare2-signatures`: Signature matching (Zignatures) for identifying library code.

### Modified Capabilities
- `radare2-analysis`: Updated to include more granular search and identification tools.

## Impact

- **`modules/radare2_module.py`**: Major expansion of registered tools.
- **`core/r2_base.py`**: Potential updates to support complex JSON parsing from new commands.
- **Project Persistence**: `.r2_projects/` will now store type definitions and signature matches.
