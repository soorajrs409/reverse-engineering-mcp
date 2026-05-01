## ADDED Requirements

### Requirement: Debug Session Initiation
The system SHALL provide a tool to start a live debug session for a target binary.

#### Scenario: Starting a new session
- **WHEN** the `r2_debug_start` tool is called with a valid file path
- **THEN** the system spawns a background Radare2 process in debug mode (`-d`), returns a unique `session_id`, and performs initial analysis (`aa`)

### Requirement: Interactive Debug Control
The system SHALL provide a tool to execute debugging actions (step, continue, breakpoint) on an active session.

#### Scenario: Stepping through code
- **WHEN** the `r2_debug_action` tool is called with a valid `session_id` and action `ds` (step)
- **THEN** the system proxies the command to the background process and returns the updated register state and current instruction

### Requirement: Register and Memory Inspection
The system SHALL provide a tool to read the current state of registers and memory for an active debug session.

#### Scenario: Reading registers
- **WHEN** the `r2_debug_read_state` tool is called with a valid `session_id`
- **THEN** the system returns a structured JSON containing the current register values and the disassembled instruction at the program counter

### Requirement: Automatic Session Cleanup
The system SHALL automatically terminate and clean up debug sessions that have been idle for more than 10 minutes.

#### Scenario: Cleanup of idle session
- **WHEN** a session has not received a tool call for 10 minutes
- **THEN** the system kills the background Radare2 process and removes the session from the manager
