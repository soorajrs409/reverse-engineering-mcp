## ADDED Requirements

### Requirement: ROP Gadget Discovery
The system SHALL provide a tool to discover Return-Oriented Programming (ROP) gadgets within a binary.

#### Scenario: Discover gadgets with filter
- **WHEN** the user requests ROP gadgets with a specific opcode filter (e.g., "pop rdi")
- **THEN** the system returns a JSON list of gadgets matching that pattern.

### Requirement: Mitigation Auditing
The system SHALL provide a tool to audit binary security mitigations.

#### Scenario: Audit sample binary
- **WHEN** the user audits a binary
- **THEN** the system returns a structured report including Canary, NX, PIE, and RELRO status.

### Requirement: Static Emulation
The system SHALL allow static emulation of code blocks using the ESIL engine.

#### Scenario: Emulate function
- **WHEN** the user requests emulation of a function at a specific address
- **THEN** the system returns the final register state after emulation.

### Requirement: Type Management
The system SHALL allow the definition and listing of C-style structs and types.

#### Scenario: Define struct
- **WHEN** the user provides a C-style struct definition
- **THEN** the system saves the definition to the radare2 project.

### Requirement: Signature Identification
The system SHALL support matching function signatures using Zignatures.

#### Scenario: Match library functions
- **WHEN** the user runs signature matching on a binary
- **THEN** the system identifies and renames known library functions.

### Requirement: Enhanced String Search
The system SHALL provide comprehensive string extraction from all binary sections.

#### Scenario: List all strings
- **WHEN** the user requests all strings in the binary
- **THEN** the system returns a JSON list of strings with their virtual addresses and sections.
