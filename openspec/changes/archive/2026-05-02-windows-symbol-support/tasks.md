## 1. Symbol Store Setup

- [x] 1.1 Update `Radare2SessionManager` in `modules/radare2_module.py` to configure `pdb.symstore` and `pdb.server`.
- [x] 1.2 Ensure the `.r2_projects/symbols` directory is created automatically.

## 2. PDB Management Tools

- [x] 2.1 Implement `get_r2_load_pdb` in `modules/radare2_module.py`.
- [x] 2.2 Implement `get_r2_download_pdb` in `modules/radare2_module.py`.
- [x] 2.3 Register the new tools with the FastMCP server.

## 3. PE Analysis Enhancements

- [x] 3.1 Verify `get_r2_analyze_mitigations` output for PE files and ensure it captures Windows-specific metadata.
- [x] 3.2 Update `README.md` to include documentation for Windows-specific analysis tools.

## 4. Verification

- [x] 4.1 Create a verification script `tests/verify_windows_symbols.py` (using a mock or a small public PE with available symbols).
- [x] 4.2 Perform a full end-to-end test of the Windows workflow.
