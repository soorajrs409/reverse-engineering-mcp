## ADDED Requirements

### Requirement: PDB File Loading
The system SHALL provide a tool to manually load an external `.pdb` symbol file for the current analysis session.

#### Scenario: Load PDB for a binary
- **WHEN** the user provides a valid path to a `.pdb` file
- **THEN** the system imports the symbols and applies them to the current binary as flags.

### Requirement: Automated PDB Downloading
The system SHALL provide a tool to automatically download and apply symbols from Microsoft's Symbol Server for the current binary.

#### Scenario: Download PDB for a system DLL
- **WHEN** the user requests a symbol download for a binary that has a PDB GUID
- **THEN** the system downloads the `.pdb` file to the local symbol store and applies the symbols.

### Requirement: Symbol Store Persistence
The system SHALL maintain a persistent local symbol store within the workspace.

#### Scenario: Cache PDB files
- **WHEN** a PDB is downloaded or loaded
- **THEN** it MUST be stored in the `.r2_projects/symbols` directory to ensure it is available across tool calls and sessions.

### Requirement: Windows Mitigation Analysis
The system SHALL correctly identify Windows-specific security mitigations during audit.

#### Scenario: Audit PE binary
- **WHEN** a PE binary is analyzed using `get_r2_analyze_mitigations`
- **THEN** the report MUST include Windows-specific protections such as GS (stack cookies), SafeSEH, and CFG.
