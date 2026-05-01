## Why

Reverse engineering often requires observing a program's behavior in real-time to understand complex logic, dynamic memory allocation, and side effects. Current MCP capabilities are limited to static analysis and patching; adding interactive debugging allows for a "live" investigation of the target binary.

## What Changes

- Add a new `debugging_module.py` to handle background process management for live debug sessions.
- Implement tools for starting debug sessions, stepping through code, continuing execution, and reading/writing registers and memory.
- Introduce a `DebugSessionManager` to track active `r2 -d` sessions and handle cleanup of orphaned processes.

## Capabilities

### New Capabilities
- `radare2-debugging`: Provides interactive process control, register access, and memory inspection.

### Modified Capabilities
- `radare2-core`: Update initialization logic to support the discovery and registration of the new debugging module.

## Impact

- New file `modules/debugging_module.py`.
- Updates to `core/loader.py` (if necessary for module discovery).
- Persistent background processes during debug sessions.
- Enhanced real-time analysis capabilities for the LLM.
