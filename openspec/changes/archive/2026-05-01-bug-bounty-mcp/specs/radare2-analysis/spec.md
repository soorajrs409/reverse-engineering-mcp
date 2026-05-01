## ADDED Requirements

### Requirement: Execute Radare2 Commands
The system SHALL provide a tool to execute arbitrary radare2 commands on a target file via `r2pipe` and return the output.

#### Scenario: Running a simple command
- **WHEN** the `r2_cmd` tool is called with a command like `iI` (binary info) and a valid file path
- **THEN** the system returns the output of the radare2 command as a string

### Requirement: Disassemble Functions
The system SHALL provide a tool to disassemble specific functions or addresses in a binary.

#### Scenario: Disassembling main
- **WHEN** the `r2_disassemble` tool is called with the symbol `main`
- **THEN** the system returns the disassembly listing for that function

### Requirement: Search for Strings
The system SHALL provide a tool to search for strings within a binary.

#### Scenario: Searching for "http"
- **WHEN** the `r2_search_strings` tool is called with the pattern "http"
- **THEN** the system returns a list of addresses where the string was found
