## 1. Environment and Dependencies

- [x] 1.1 Add `angr` to `pyproject.toml`.
- [x] 1.2 Update `Dockerfile` to include necessary build dependencies for `angr` (e.g., `libffi-dev`, `python3-dev`).
- [x] 1.3 Verify `angr` installation in the environment.

## 2. Core Symbolic Module

- [x] 2.1 Create `modules/symbolic_module.py` with basic `angr` project initialization.
- [x] 2.2 Implement `get_r2_symbolic_reachability` tool.
- [x] 2.3 Implement `get_r2_symbolic_solve_registers` tool.
- [x] 2.4 Implement `get_r2_symbolic_function_summary` tool.

## 3. Concolic Integration

- [x] 3.1 Update `DebugSessionManager` in `modules/debugging_module.py` to support state capture.
- [x] 3.2 Implement `get_r2_symbolic_concolic_transition` tool to bridge `r2` debug session and `angr`.

## 4. Verification and Testing

- [x] 4.1 Create `tests/verify_symbolic.py` to test path finding on a simple branchy binary.
- [x] 4.2 Test concolic handoff with a live debug session.
- [x] 4.3 Update `README.md` with the new symbolic capabilities and tool documentation.
