## 1. Project Infrastructure

- [x] 1.1 Add `LICENSE` (MIT) to the root directory.
- [x] 1.2 Update `.gitignore` to include `.r2_projects/` and Docker cache.

## 2. Dockerization

- [x] 2.1 Create `Dockerfile` based on `python:3.13-slim`.
- [x] 2.2 Install `radare2` and `uv` in the `Dockerfile`.
- [x] 2.3 Configure `Dockerfile` to sync dependencies and set the entrypoint.
- [x] 2.4 Create `docker-compose.yml` with a volume for `.r2_projects`.
- [x] 2.5 Test the Docker build and run locally.

## 3. Documentation

- [x] 3.1 Draft `README.md` with "Why", "Features", and "Prerequisites".
- [x] 3.2 Add "Installation" section (Local vs Docker).
- [x] 3.3 Add "Agent Configuration" for Claude Desktop, Cursor, and Windsurf.
- [x] 3.4 Add "Usage Example" with `test_binary`.
- [x] 3.5 Add "Persistence" and "License" sections.

## 4. Code Refinement

- [x] 4.1 Update `core/utils.py` to provide better hints for missing `radare2`.
- [x] 4.2 Ensure `modules/radare2_module.py` uses absolute paths for project persistence within the container.
- [x] 4.3 Verify the entire flow (Local and Docker) works as expected.
