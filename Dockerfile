# Use Ubuntu for better package availability
FROM ubuntu:24.04

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install Radare2, Python, and other dependencies
RUN apt-get update && apt-get install -y \
    radare2 \
    python3 \
    python3-pip \
    python3-dev \
    libffi-dev \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up the working directory
WORKDIR /app

# Install 'uv' for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy project files
COPY pyproject.toml uv.lock ./
COPY main.py ./
COPY core/ ./core/
COPY modules/ ./modules/

# Install dependencies using uv
# Note: we use --system to install into the system python as it's a dedicated container
RUN uv sync --frozen

# Create a directory for persistent r2 projects
RUN mkdir -p /app/.r2_projects

# Run the MCP server
ENTRYPOINT ["uv", "run", "main.py"]
