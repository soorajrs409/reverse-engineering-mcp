## ADDED Requirements

### Requirement: Multi-backend Decompilation
The system SHALL provide a tool to decompile a function or address into pseudo-code, automatically selecting the best available decompiler backend (r2ghidra > r2dec > native pdc).

#### Scenario: Decompiling with fallback
- **WHEN** the `r2_decompile` tool is called
- **THEN** the system attempts to use `pdg`, then `pdd`, and finally `pdc` to return pseudo-code
