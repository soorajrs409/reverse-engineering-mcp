## MODIFIED Requirements

### Requirement: Environment Validation
The system SHALL validate its external dependencies (e.g., `radare2`) at startup and provide helpful guidance if they are missing. It SHALL also detect available decompiler plugins (r2ghidra, r2dec).

#### Scenario: Plugin detection
- **WHEN** the server starts
- **THEN** it checks for `pdg` and `pdd` availability and logs their status
