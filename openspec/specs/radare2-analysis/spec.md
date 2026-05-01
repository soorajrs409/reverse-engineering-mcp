## MODIFIED Requirements

### Requirement: Execute Radare2 Commands
The system SHALL provide a tool to execute arbitrary radare2 commands on a target file via `r2pipe` using a persistent project session and return the output.

#### Scenario: Running a simple command
- **WHEN** the `r2_cmd` tool is called with a command like `iI` (binary info) and a valid file path
- **THEN** the system loads the persistent project (creating it if necessary) and returns the output of the radare2 command as a string

### Requirement: Disassemble Functions
The system SHALL provide a tool to disassemble specific functions or addresses in a binary using the existing analysis state from the persistent project.

#### Scenario: Disassembling main
- **WHEN** the `r2_disassemble` tool is called with the symbol `main`
- **THEN** the system returns the disassembly listing for that function, including any custom labels or comments stored in the project

### Requirement: Search for Strings
The system SHALL provide a tool to search for strings within a binary using the persistent session.

#### Scenario: Searching for "http"
- **WHEN** the `r2_search_strings` tool is called with the pattern "http"
- **THEN** the system returns a list of addresses where the string was found, persisting the search results if necessary
