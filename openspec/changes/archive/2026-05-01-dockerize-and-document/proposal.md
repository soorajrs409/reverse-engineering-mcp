## Why

The `bug-bounty-mcp` is a powerful tool for binary analysis, but it requires manual installation of `radare2` and Python 3.13, which can be a barrier for new users and security researchers who prefer isolated environments. Additionally, the project lacks documentation for common MCP integrations (Claude, Cursor, Windsurf), making it difficult to adopt.

## What Changes

- Add a `Dockerfile` and `docker-compose.yml` for containerized execution.
- Add a comprehensive `README.md` with configuration guides for popular AI agents.
- Add an `MIT LICENSE` file for open-source compliance.
- Update `.gitignore` to exclude local `.r2_projects` cache and container-specific files.

## Capabilities

### New Capabilities
- `containerization`: Provides a consistent, reproducible environment for the MCP server using Docker.
- `documentation`: Provides onboarding and configuration guides for various MCP clients and agents.

### Modified Capabilities
- `bug-bounty-core`: Update setup instructions and environment requirements.

## Impact

- **Setup**: Users can now start the MCP server with a single `docker run` or `docker-compose up` command.
- **Dependencies**: Moves `radare2` and Python environment management into the container.
- **Deployment**: Facilitates easier deployment on any platform that supports Docker.
- **Maintenance**: Persistent binary analysis projects will now be stored in a volume or mounted directory for consistency across container restarts.
