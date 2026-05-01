## MODIFIED Requirements

### Requirement: Persistent Project Lifecycle
The system SHALL manage the lifecycle of Radare2 projects, ensuring that analysis state (renames, comments, flags) is persisted to disk in a workspace-local `.r2_projects/` directory. All IO operations during the lifecycle MUST be resilient to transient failures through automatic retries.

#### Scenario: First time opening a binary
- **WHEN** a tool is called for a binary that has no existing project
- **THEN** the system SHALL create a new Radare2 project, perform initial analysis (`aaa`), and save it to `.r2_projects/` with automatic retries for each command

#### Scenario: Re-opening a known binary
- **WHEN** a tool is called for a binary that has an existing project in `.r2_projects/`
- **THEN** the system SHALL load the existing project instead of performing a fresh analysis, using retries for the loading commands
