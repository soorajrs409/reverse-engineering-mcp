## Context

The Radare2 MCP toolset previously suffered from two main issues:
1. **Schema Inflexibility**: Standard orchestration parameters like `wait_for_previous` caused Pydantic validation errors because the tool signatures were too strict.
2. **Brittle Error Handling**: Exceptions (like `BrokenPipeError` or `OSError`) would propagate as raw Python tracebacks, which are difficult for agents to handle gracefully.

## Goals / Non-Goals

**Goals:**
- **Robustness**: Tools should handle unexpected metadata without failing.
- **Consistency**: All failures should return a structured, machine-readable JSON response.
- **Reliability**: Brittle IO operations with the Radare2 engine should include automatic retries.
- **Maintainability**: Centralize infrastructure to avoid code duplication across modules.

**Non-Goals:**
- Refactoring the internal logic of analysis tools (e.g., disassembly parsing).
- Replacing `r2pipe` with a different communication backend.
- Modifying the Radare2 engine itself.

## Decisions

### Decorator-based Tool Wrapping
- **Decision**: Implement a `@mcp_tool_wrapper` decorator in `core/r2_base.py`.
- **Rationale**: This allows us to inject shared behavior (error handling, signature adaptation) into dozens of tools without modifying their individual logic. It maintains a clean separation of concerns.
- **Alternatives**: Manually wrapping every tool in `try/except` (too verbose/error-prone) or modifying the `FastMCP` core (too invasive).

### Permissive Tool Signatures
- **Decision**: Add `**kwargs` to all registered MCP tool functions.
- **Rationale**: This is the most efficient way to silently absorb orchestration metadata like `wait_for_previous` without breaking Pydantic validation. It future-proofs the tools against new metadata fields.

### Standardized JSON Error Schema
- **Decision**: Catch all exceptions in the wrapper and return a JSON string containing `status`, `tool`, `message`, and `type`.
- **Rationale**: Standardizing on `{"status": "error", ...}` allows the calling agent to recognize and handle failures programmatically.

### Retry Mechanism for R2 Commands
- **Decision**: Implement `r2_cmd_with_retry` with a default of 3 attempts.
- **Rationale**: Radare2 sessions can occasionally hang or suffer from pipe issues. Retries provide a first line of defense against transient failures.

## Risks / Trade-offs

- **[Risk]**: The decorator might hide bugs by converting them to JSON errors. 
  - **Mitigation**: The wrapper logs the full traceback to the server's `logger.error` for developer debugging, while returning a clean message to the LLM.
- **[Risk]**: Over-reliance on retries might mask performance issues.
  - **Mitigation**: Keep the default `max_retries` low (3) and log every retry attempt as a warning.
- **[Risk]**: `**kwargs` makes function signatures less explicit for developers.
  - **Mitigation**: Use type hinting and clear docstrings for the primary parameters.
