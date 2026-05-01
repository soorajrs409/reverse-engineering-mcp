## ADDED Requirements

### Requirement: Modular Module Loading
The system SHALL dynamically load Python modules from a designated `modules/` directory at startup. It SHALL ensure that stateful modules (like the debugging module) are initialized with necessary cleanup listeners.

#### Scenario: Stateful module initialization
- **WHEN** the server starts and the debugging module is loaded
- **THEN** the module's registration function is called, and any background cleanup threads are started

### Requirement: Centralized MCP Server Management
The system SHALL provide a central entry point that initializes the FastMCP server and coordinates the registration of tools from all loaded modules. Registered tools MUST use the shared resilience infrastructure (decorators) to ensure consistent behavior.

#### Scenario: Server initialization
- **WHEN** `main.py` is executed
- **THEN** a FastMCP server instance is created and all tools from discovered modules are registered using the `@mcp_tool_wrapper`

### Requirement: Environment Validation
The system SHALL validate its external dependencies (e.g., `radare2`) at startup and provide helpful guidance if they are missing. It SHALL also detect available decompiler plugins (r2ghidra, r2dec).

#### Scenario: Plugin detection
- **WHEN** the server starts
- **THEN** it checks for `pdg` and `pdd` availability and logs their status
