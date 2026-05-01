## ADDED Requirements

### Requirement: Binary Patching via Assembly
The system SHALL provide a tool to write assembly instructions to a specific address in the binary.

#### Scenario: NOP-ing a check
- **WHEN** `r2_patch_asm` is called with address `0x1234` and instruction `nop`
- **THEN** the system opens the binary in write-mode, applies the patch, and saves the changes

### Requirement: Binary Patching via Hex
The system SHALL provide a tool to write raw hex bytes to a specific address in the binary.

#### Scenario: Modifying a byte
- **WHEN** `r2_patch_hex` is called with address `0x1234` and hex `9090`
- **THEN** the system opens the binary in write-mode, writes the hex bytes, and saves the changes
