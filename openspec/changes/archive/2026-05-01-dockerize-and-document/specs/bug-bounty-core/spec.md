# Capability: bug-bounty-core (Delta)

## Requirement Changes

1.  **Environment Validation**: The `check_dependencies` utility should be aware of the containerized environment or at least provide better error messages if `radare2` is missing in a way that suggests Docker as an alternative.
2.  **Pathing**: Ensure that the `PROJECTS_DIR` is configurable or uses a predictable absolute path within the container to avoid issues with working directory changes.

## Acceptance Criteria

- [ ] `core/utils.py` handles missing dependencies gracefully with helpful suggestions.
- [ ] `modules/radare2_module.py` uses a consistent path for projects.
