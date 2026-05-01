## 1. Environment & Project Setup

- [x] 1.1 Initialize project directory and create a virtual environment using `uv`.
- [x] 1.2 Install core dependencies: `fastmcp` and `r2pipe`.
- [x] 1.3 Create the basic directory structure: `core/`, `modules/`, and `main.py`.

## 2. Core Server Implementation

- [x] 2.1 Implement the entry point `main.py` that initializes the FastMCP server instance.
- [x] 2.2 Implement the modular loader in `core/loader.py` to discover and register modules from the `modules/` folder.
- [x] 2.3 Implement a basic health check or dependency verification for `radare2`.

## 3. Radare2 Module Implementation

- [x] 3.1 Create `modules/radare2_module.py` and register it with the core server.
- [x] 3.2 Implement the `r2_cmd` tool for executing arbitrary radare2 commands via `r2pipe`.
- [x] 3.3 Implement the `r2_disassemble` tool to return disassembly of functions or addresses.
- [x] 3.4 Implement the `r2_search_strings` tool for pattern and string searching.

## 4. Verification

- [x] 4.1 Create a simple "Hello World" binary for testing purposes.
- [x] 4.2 Verify the MCP tools by running the server and performing basic analysis on the test binary.
