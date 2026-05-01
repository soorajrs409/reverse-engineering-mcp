<p align="center">
  <img src="banner.svg" width="800" alt="Radare2 MCP Banner">
</p>

# Radare2 MCP

A persistent binary analysis toolset for LLMs, powered by [Radare2](https://github.com/radareorg/radare2).

## Why?

Security researchers often need to perform deep, incremental analysis of binaries. Standard LLM context windows make it difficult to maintain state (like renamed symbols, comments, or identified vulnerabilities) across multiple turns. 

**Radare2 MCP** solves this by providing a persistent analysis environment. Every binary analyzed is tracked as a Radare2 project, ensuring that your insights persist and the LLM can "pick up where it left off."

## Feature Deep Dive

### 1. Static Analysis & Decompilation
Explore the binary without executing it. Use multiple decompiler backends to get clean pseudo-code.
*   **Example**: `Analyze the binary at samples/test_binary. What does the main function do?`
*   **Tools**: `get_r2_decompile`, `get_r2_disassemble`, `get_r2_binary_info`.

### 2. Interactive Debugging
Control process execution in real-time. Set breakpoints, step through instructions, and inspect live memory/registers.
*   **Example**: `Debug samples/test_binary. Break at main, run, and then step 5 times while showing me the RIP register.`
*   **Tools**: `r2_debug_start`, `r2_debug_action`, `r2_debug_read_state`.

### 3. Exploit Research (ROP & Mitigations)
Identify security weaknesses and find primitives for exploit development.
*   **Example**: `Search for ROP gadgets in samples/test_binary that end with 'jmp rax'. Also check if the binary has Stack Canaries enabled.`
*   **Tools**: `get_r2_rop_gadgets`, `get_r2_analyze_mitigations`.

### 4. Persistence & State Management
Rename obfuscated functions and add comments that stay there across sessions.
*   **Example**: `Rename the function at 0x1234 to 'validate_license' and add a comment 'This is where the check happens'.`
*   **Tools**: `get_r2_rename_symbol`, `get_r2_set_comment`.

### 5. Binary Patching
Modify the binary directly to bypass checks or fix bugs.
*   **Example**: `In samples/test_binary, the instruction at 0x11ae is a JNE. Patch it to a JMP to always bypass the check.`
*   **Tools**: `get_r2_patch_asm`, `get_r2_patch_hex`.

### 6. Type Management & Emulation
Define custom structs and emulate code paths to predict behavior without a full debugger.
*   **Example**: `Define a struct 'Config' with an int and a char array. Apply it at 0x4000 and emulate 'init_config' to see how it fills the struct.`
*   **Tools**: `get_r2_define_type`, `get_r2_apply_type`, `get_r2_emulate_function`.

## Prerequisites

- Python 3.12+ (if running locally)
- [Radare2](https://github.com/radareorg/radare2) (must be in your `$PATH`)
- [uv](https://github.com/astral-sh/uv) (recommended)
- [Docker](https://www.docker.com/) (optional, for containerized execution)

## Installation

### Local Setup (with uv)

```bash
uv run main.py
```

### Docker Setup

```bash
docker build -t radare2-mcp .
# Run the server
docker run -i --rm radare2-mcp
```

## Agent Configuration

### Claude Desktop

Edit your `config.json` (typically `~/Library/Application Support/Claude/config.json` on macOS):

**Docker Version (Recommended):**
```json
{
  "mcpServers": {
    "radare2": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-v", "radare2-cache:/app/.r2_projects",
        "-v", "/path/to/your/binaries:/data",
        "radare2-mcp"
      ]
    }
  }
}
```

### Cursor

1. Go to **Settings > Features > MCP**.
2. Click **+ Add New MCP Server**.
3. Name: `Radare2 MCP`
4. Type: `command`
5. Command: `uv run --project /path/to/radare2-mcp main.py`

### Windsurf

Add to your `mcp_config.json`:

```json
{
  "mcpServers": {
    "radare2": {
      "command": "uv",
      "args": [
        "run",
        "--project",
        "/path/to/radare2-mcp",
        "main.py"
      ]
    }
  }
}
```

## Persistence

All analysis data is stored in the `.r2_projects/` directory. If using Docker, ensure you mount a volume to this path to keep your analysis across sessions.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
