## ADDED Requirements

### Requirement: Modular Module Loading
The system SHALL dynamically load Python modules from a designated `modules/` directory at startup.

#### Scenario: Successful module discovery
- **WHEN** the server starts and valid Python files are present in the `modules/` directory
- **THEN** each module's registration function is executed to add its tools to the MCP server

### Requirement: Centralized MCP Server Management
The system SHALL provide a central entry point that initializes the FastMCP server and coordinates the registration of tools from all loaded modules.

#### Scenario: Server initialization
- **WHEN** `main.py` is executed
- **THEN** a FastMCP server instance is created and all tools from discovered modules are registered
