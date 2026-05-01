# Capability: Containerization

## Requirements

1.  **Environment**:
    *   Base OS: Linux (Debian-based slim).
    *   Python Version: 3.13.
    *   External Dependency: `radare2` must be installed and accessible via `r2` command.
2.  **Server Startup**:
    *   The container must start the MCP server using `uv run main.py`.
    *   Dependencies must be pre-installed in the image for fast startup.
3.  **Persistence**:
    *   The directory `/app/.r2_projects` must be designated as a volume or documented mount point for persistent analysis state.
4.  **File Access**:
    *   The container must be able to access binary files mounted from the host.
    *   The documentation must specify how to mount host directories (e.g., `-v /path/on/host:/data`).

## Acceptance Criteria

- [ ] `docker build` completes successfully.
- [ ] `docker run` starts the MCP server without errors.
- [ ] The MCP server inside the container can successfully run `radare2` commands.
- [ ] Analysis projects created inside the container persist if a volume is used.
