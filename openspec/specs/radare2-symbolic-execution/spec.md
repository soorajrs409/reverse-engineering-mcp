## ADDED Requirements

### Requirement: Path Discovery
The system SHALL provide a tool to find execution paths to a specific target address using symbolic execution.

#### Scenario: Find path to address
- **WHEN** the user provides a target virtual address and optional start/avoid addresses
- **THEN** the system returns the required input (stdin or arguments) to reach that address, or an error if unreachable.

### Requirement: Constraint Solving for Registers
The system SHALL allow solving for input constraints that result in a specific register state at a given address.

#### Scenario: Solve for register value
- **WHEN** the user specifies an address and a desired register value (e.g., RAX=0)
- **THEN** the system identifies the input required to satisfy this condition.

### Requirement: Symbolic Function Summarization
The system SHALL provide a high-level symbolic summary of a function's side effects on registers and memory.

#### Scenario: Summarize function side effects
- **WHEN** the user requests a symbolic summary of a function
- **THEN** the system returns a description of how inputs (registers/memory) affect outputs.
