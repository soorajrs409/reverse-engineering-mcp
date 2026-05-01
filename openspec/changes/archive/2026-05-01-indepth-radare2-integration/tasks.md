## 1. Setup & Session Management

- [x] 1.1 Create the `.r2_projects/` directory and ensure it is ignored by git if necessary.
- [x] 1.2 Implement the `Radare2SessionManager` class in `modules/radare2_module.py` to handle project persistence and auto-analysis.
- [x] 1.3 Refactor existing tools (`r2_cmd`, `r2_disassemble`, `r2_search_strings`) to use the new `Radare2SessionManager`.

## 2. Reconnaissance Tools

- [x] 2.1 Implement `r2_get_binary_info` to extract security metadata (NX, Canary, PIE, etc.) in JSON format.
- [x] 2.2 Implement `r2_list_imports` with a filter for dangerous sinks (e.g., `strcpy`, `system`).
- [x] 2.3 Implement `r2_get_entropy` to map section entropy and detect packing/encryption.

## 3. Advanced Analysis Tools

- [x] 3.1 Implement `r2_get_xrefs` to find cross-references (to/from) for a given address or symbol.
- [x] 3.2 Implement `r2_get_call_graph` to return a structured representation of function call relationships.
- [x] 3.3 Implement `r2_get_function_details` to extract stack variable offsets, sizes, and basic block info.

## 4. State Management Tools

- [x] 4.1 Implement `r2_rename_symbol` to allow agents to rename functions and addresses persistently.
- [x] 4.2 Implement `r2_set_comment` to allow agents to add persistent notes to specific addresses.
- [x] 4.3 Implement `r2_cleanup_project` to provide a mechanism for deleting persistent analysis state.

## 5. Validation & Testing

- [x] 5.1 Verify all new tools against `test_binary` and ensure JSON outputs are correctly formatted.
- [x] 5.2 Validate persistence by renaming a symbol in one session and verifying it remains renamed in a subsequent session.
- [x] 5.3 Confirm that `.r2_projects/` correctly stores project files and that they are loaded upon re-analysis.
