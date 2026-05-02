## Why

Reverse engineering Windows binaries (PE files) is significantly hampered without access to symbol information (PDB files). While Radare2 supports PDBs, the current MCP does not provide explicit tools to manage them or automate their download from Microsoft's Symbol Servers, making Windows analysis tedious and less insightful for the LLM.

## What Changes

- **New Windows Tools**:
    - `get_r2_load_pdb`: Manually load an external `.pdb` file for the current session.
    - `get_r2_download_pdb`: Automatically download and apply symbols from Microsoft's Symbol Server for the current binary.
- **Enhanced Configuration**:
    - Automatic configuration of Radare2's `pdb.server` and `pdb.symstore` to ensure symbols are persisted in the workspace's `.r2_projects/symbols` directory.
- **Improved PE Metadata**:
    - Ensure `get_r2_analyze_mitigations` and `get_r2_binary_info` correctly handle PE-specific features (GS, SafeSEH, CFG).

## Capabilities

### New Capabilities
- `radare2-windows-symbols`: Tools for managing PDB files and Microsoft Symbol Server integration.

### Modified Capabilities
- `radare2-analysis`: Ensure PE-specific analysis commands are prioritized when a PE binary is detected.

## Impact

- **Persistence**: Adds a new `symbols/` subdirectory within `.r2_projects/` to cache PDBs across sessions.
- **Tooling**: Introduces 2-3 new tools specifically for Windows workflows.
- **Context**: Improves the quality of disassembly and decompilation for Windows system DLLs and applications.
