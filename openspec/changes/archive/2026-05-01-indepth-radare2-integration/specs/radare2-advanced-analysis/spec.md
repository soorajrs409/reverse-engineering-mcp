## ADDED Requirements

### Requirement: Cross-Reference (Xref) Tracking
The system SHALL provide a tool to find all locations that call a specific function or reference a specific address.

#### Scenario: Finding callers of system
- **WHEN** `r2_get_xrefs` is called for the address of `system`
- **THEN** the system returns a list of all functions and offsets that reference that address

### Requirement: Call Graph Generation
The system SHALL provide a tool to generate a call graph (to/from) for a specific function to visualize control flow.

#### Scenario: Visualizing a parser's call tree
- **WHEN** `r2_get_call_graph` is called for a function
- **THEN** the system returns a structured representation (e.g., DOT or JSON) of the function's call relationships

### Requirement: Stack Frame Analysis
The system SHALL provide a tool to analyze a function's stack frame, identifying local variables, their offsets, and types.

#### Scenario: Calculating buffer sizes
- **WHEN** `r2_get_function_details` is called
- **THEN** the system returns a list of local variables with their stack offsets and detected sizes
