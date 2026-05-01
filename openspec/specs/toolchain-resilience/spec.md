## ADDED Requirements

### Requirement: Structured Tool Wrapping
The system SHALL provide a centralized mechanism to wrap all MCP tools, ensuring they handle common orchestration metadata and provide consistent error responses.

#### Scenario: Wrapping a tool
- **WHEN** a tool function is decorated with the `@mcp_tool_wrapper`
- **THEN** it accepts arbitrary keyword arguments and catches all exceptions

### Requirement: Permissive Tool Signatures
All MCP tools SHALL accept arbitrary keyword arguments (`**kwargs`) to prevent schema validation failures from client-provided orchestration metadata (e.g., `wait_for_previous`).

#### Scenario: Tool called with extra parameters
- **WHEN** a client calls a tool with an unexpected parameter like `wait_for_previous=True`
- **THEN** the tool executes successfully without a Pydantic validation error

### Requirement: Structured Error Responses
In the event of an unhandled exception within a tool, the system SHALL return a structured JSON response containing the error details.

#### Scenario: Tool encountering an exception
- **WHEN** a tool function raises an exception (e.g., `OSError`)
- **THEN** the wrapper catches it and returns a JSON string with `status: "error"`, the tool name, and the error message

### Requirement: Automated Command Retries
The system SHALL support automatic retries for brittle communication operations with the Radare2 engine.

#### Scenario: Transient command failure
- **WHEN** a Radare2 command fails due to a transient issue (e.g., a broken pipe)
- **THEN** the system automatically retries the command up to 3 times before returning an error
