## Why

Resolving schema validation errors (e.g., `wait_for_previous`), structuring error responses, consolidating session management, and implementing automatic retries for transient failures to improve the reliability and developer experience of the Radare2 MCP. This formalizes the infrastructure as a stable pillar for future development.

## What Changes

- **Centralized Infrastructure**: Added `core/r2_base.py` to house shared tool logic and decorators.
- **Robust Tool Signatures**: Updated all MCP tools to accept `**kwargs`, allowing them to silently absorb orchestration metadata (like `wait_for_previous`) without Pydantic validation errors.
- **Structured Error Responses**: Implemented `@mcp_tool_wrapper` to catch exceptions and return standardized JSON error objects instead of raw Python tracebacks.
- **Automated Retries**: Introduced `r2_cmd_with_retry` to handle transient communication failures or timeouts with the Radare2 engine.
- **Refactored Modules**: Updated `radare2_module.py` and `debugging_module.py` to leverage the new resilient foundation.

## Capabilities

### New Capabilities
- `toolchain-resilience`: Provides the core reliability features (wrappers, retries, structured errors) for the entire MCP toolset.

### Modified Capabilities
- `radare2-core`: Updated the modular loading and tool registration process to incorporate the new infrastructure.
- `radare2-session-management`: Hardened the persistent session lifecycle with retries and consistent error handling.

## Impact

- **Core**: New file `core/r2_base.py`.
- **Modules**: Significant refactor of `modules/radare2_module.py` and `modules/debugging_module.py`.
- **Clients**: Improved compatibility with LLM clients that send additional orchestration metadata.
