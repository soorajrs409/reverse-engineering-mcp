## 1. Shared Infrastructure

- [x] 1.1 Create `core/r2_base.py` containing `@mcp_tool_wrapper` and `r2_cmd_with_retry`.
- [x] 1.2 Refactor `modules/radare2_module.py` to use the resilient base and permissive signatures.
- [x] 1.3 Refactor `modules/debugging_module.py` to use the resilient base and permissive signatures.

## 2. Verification

- [x] 2.1 Verify that tools now accept `**kwargs` and silently handle orchestration metadata.
- [x] 2.2 Verify that unhandled exceptions are caught and returned as structured JSON.
- [x] 2.3 Verify that Radare2 commands are automatically retried on transient failures.

## 3. Documentation

- [x] 3.1 Update `README.md` to highlight toolchain reliability.
- [x] 3.2 Create `GEMINI.md` to document engineering standards and the resilient toolchain pattern.
