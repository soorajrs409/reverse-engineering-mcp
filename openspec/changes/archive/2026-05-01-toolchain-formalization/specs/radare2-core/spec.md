## MODIFIED Requirements

### Requirement: Centralized MCP Server Management
The system SHALL provide a central entry point that initializes the FastMCP server and coordinates the registration of tools from all loaded modules. Registered tools MUST use the shared resilience infrastructure (decorators) to ensure consistent behavior.

#### Scenario: Server initialization
- **WHEN** `main.py` is executed
- **THEN** a FastMCP server instance is created and all tools from discovered modules are registered using the `@mcp_tool_wrapper`
