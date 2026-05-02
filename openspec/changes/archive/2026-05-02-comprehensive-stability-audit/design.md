## Context

The Radare2 MCP has evolved into a complex system with multiple specialized modules. While functional, the rapid pace of development has left potential gaps in error handling and cross-module stability. The system relies on `r2pipe` and a custom orchestration layer that must be resilient to binary-specific edge cases and transient tool failures.

## Goals / Non-Goals

**Goals:**
- **Standardize Error Handling**: Ensure every tool call returns a predictable, informative JSON error response.
- **Resilience**: Strengthen `r2_cmd_with_retry` to handle a broader range of transient Radare2 failures.
- **Session Integrity**: Verify that `Radare2SessionManager` and `DebugSessionManager` correctly manage lifecycle events and do not leak resources.
- **Automated Validation**: Create a `verify_stability.py` script that stresses all modules.

**Non-Goals:**
- Adding new feature capabilities (e.g., new decompiler support).
- Performance optimization (unless it directly impacts stability).
- Refactoring the entire codebase structure.

## Decisions

### 1. Unified Error Schema in `@mcp_tool_wrapper`
- **Rationale**: Currently, some errors might slip through if not explicitly caught. Standardizing the response format allows the LLM to handle failures gracefully.
- **Alternatives**: Individual `try-except` blocks in every tool (harder to maintain).

### 2. Enhanced Retry Logic in `core/r2_base.py`
- **Rationale**: Radare2 can occasionally time out or return malformed output for complex binaries. Implementing exponential backoff and specific pattern matching for "recoverable" errors will improve reliability.
- **Alternatives**: Failing immediately (current behavior in many cases).

### 3. Stress-Testing Framework
- **Rationale**: A dedicated stability test will use large binaries and concurrent requests to simulate heavy LLM usage.
- **Alternatives**: Relying on existing unit tests (too narrow).

## Risks / Trade-offs

- **[Risk]** Over-aggressive retries could mask deep architectural bugs → **Mitigation**: Limit retry counts and log detailed failure reasons.
- **[Risk]** Complex error objects might confuse the LLM → **Mitigation**: Keep the `message` field human-readable and use a standard `type` field.
- **[Risk]** Stress tests might be slow → **Mitigation**: Run stability audits as a separate, optional CI step.
