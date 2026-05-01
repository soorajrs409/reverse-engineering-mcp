## 1. Setup and Session Management

- [x] 1.1 Create `modules/debugging_module.py` with the base structure
- [x] 1.2 Implement `DebugSessionManager` class to track active r2 sessions
- [x] 1.3 Implement background cleanup thread for idle sessions (10min timeout)

## 2. Implement Debugging Tools

- [x] 2.1 Implement `r2_debug_start` tool to spawn `r2 -d` and return a session ID
- [x] 2.2 Implement `r2_debug_action` tool for ds, dc, db commands
- [x] 2.3 Implement `r2_debug_read_state` tool for register and context inspection
- [x] 2.4 Implement `r2_debug_terminate` tool for explicit session closure

## 3. Integration and Refinement

- [x] 3.1 Update `register` function to ensure background threads start/stop correctly
- [x] 3.2 Add error handling for process crashes or invalid session IDs
- [x] 3.3 Ensure thread safety for concurrent access to the session manager

## 4. Verification

- [x] 4.1 Create `tests/verify_debugging.py` to test start, step, and register read
- [x] 4.2 Verify cleanup logic by spawning a session and waiting for timeout (shorter for testing)
- [x] 4.3 Update README.md with debugging usage instructions
