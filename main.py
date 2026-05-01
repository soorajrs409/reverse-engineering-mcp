import logging
from fastmcp import FastMCP
from core.loader import load_modules
from core.utils import check_dependencies

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("radare2-mcp")

def main():
    # Check dependencies first
    if not check_dependencies():
        return

    # Initialize FastMCP server
    mcp = FastMCP("Radare2 Analysis Toolset")

    # Dynamically load modules from the modules/ directory
    logger.info("Loading analysis modules...")
    load_modules(mcp)

    # Run the server
    logger.info("Starting MCP server...")
    mcp.run()

if __name__ == "__main__":
    main()
