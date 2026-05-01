## Context

The current `bug-bounty-mcp` is a Python-based MCP server that interacts with `radare2` via `r2pipe`. It relies on the host system for Python 3.13 and a `radare2` installation. Analysis metadata is stored in a local `.r2_projects` directory.

## Goals / Non-Goals

**Goals:**
- Provide a single command to run the MCP server using Docker.
- Ensure persistent storage for Radare2 projects across container restarts.
- Document configuration for Cursor, Claude Desktop, and Windsurf.
- Minimize the image size using a slim base image and `uv` for dependency management.

**Non-Goals:**
- Porting the server to another language.
- Implementing a web UI for the analysis.
- Supporting non-Docker container runtimes (e.g., Podman) explicitly, though it may work.

## Decisions

### 1. Base Image: `python:3.13-slim`
- **Rationale**: Provides a small footprint while including the necessary Python environment. `slim` is preferred over `alpine` to avoid potential library compatibility issues with `radare2` and Python C extensions.
- **Alternatives**: `alpine` (too many issues with `r2` dependencies), `ubuntu` (unnecessarily large).

### 2. Dependency Manager: `uv`
- **Rationale**: `uv` is extremely fast and produces predictable environments via `uv.lock`. It simplifies the Docker build process.
- **Alternatives**: `pip` (slower, less reliable locking), `poetry` (heavier, slower install).

### 3. Persistent Storage via Volumes
- **Rationale**: The `.r2_projects` directory must survive container restarts. We will design the Docker image to expect a volume mount at `/app/.r2_projects`.
- **Alternatives**: Storing projects inside the container (lost on restart), using a database (overkill for `radare2` projects).

### 4. Mounting Host Binaries
- **Rationale**: To analyze files on the host, the container needs access to them. We will recommend mounting a specific host directory (e.g., `/data`) into the container.

## Risks / Trade-offs

- **[Risk] Path Mismatches** → Mitigation: Use relative paths in the MCP tools or provide a clear "root" path (e.g., `/data`) that the agent should use when referring to files.
- **[Risk] Performance Overhead** → Mitigation: Docker overhead for static analysis is negligible.
- **[Risk] Security of Analyzed Binaries** → Mitigation: Running inside a container provides an extra layer of isolation, though researchers should still be cautious.
