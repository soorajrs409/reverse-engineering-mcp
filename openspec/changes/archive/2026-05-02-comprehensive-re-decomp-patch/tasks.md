## 1. Refactor Session Management

- [x] 1.1 Update `Radare2SessionManager` to support `write_mode` parameter
- [x] 1.2 Implement decompiler plugin detection logic in the Radare2 module

## 2. Implement Decompilation

- [x] 2.1 Create `get_r2_decompile` tool with tiered fallback logic (pdg > pdd > pdc)
- [x] 2.2 Register the `r2_decompile` tool with FastMCP

## 3. Implement Patching

- [x] 3.1 Create `get_r2_patch_asm` tool using write-mode sessions
- [x] 3.2 Create `get_r2_patch_hex` tool using write-mode sessions
- [x] 3.3 Register patching tools with FastMCP

## 4. Verification

- [x] 4.1 Create test script to verify decompilation fallback
- [x] 4.2 Create test script to verify assembly and hex patching on a sample binary
- [x] 4.3 Update documentation to reflect new capabilities
