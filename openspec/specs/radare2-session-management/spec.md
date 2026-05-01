## ADDED Requirements

### Requirement: Persistent Project Lifecycle
The system SHALL manage the lifecycle of Radare2 projects, ensuring that analysis state (renames, comments, flags) is persisted to disk in a workspace-local `.r2_projects/` directory. All IO operations during the lifecycle MUST be resilient to transient failures through automatic retries.

#### Scenario: First time opening a binary
- **WHEN** a tool is called for a binary that has no existing project
- **THEN** the system SHALL create a new Radare2 project, perform initial analysis (`aaa`), and save it to `.r2_projects/` with automatic retries for each command

#### Scenario: Re-opening a known binary
- **WHEN** a tool is called for a binary that has an existing project in `.r2_projects/`
- **THEN** the system SHALL load the existing project instead of performing a fresh analysis, using retries for the loading commands

### Requirement: Auto-Save State
The system SHALL automatically save the state of the Radare2 project after any operation that modifies the database (e.g., renaming a symbol, adding a comment).

#### Scenario: Renaming a function
- **WHEN** the `r2_rename_symbol` tool is called
- **THEN** the system updates the symbol in the session AND ensures the project is saved to disk

### Requirement: Session Cleanup
The system SHALL provide a mechanism to delete a specific project's persistent state.

#### Scenario: Wiping analysis data
- **WHEN** the `r2_cleanup_project` tool is called for a file
- **THEN** the system deletes the corresponding project files from `.r2_projects/`
