import importlib
import os
import logging
from fastmcp import FastMCP

logger = logging.getLogger("radare2-mcp.loader")

def load_modules(mcp: FastMCP):
    """
    Dynamically loads all modules from the modules/ directory.
    Each module should have a register(mcp) function.
    """
    modules_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "modules")
    
    if not os.path.exists(modules_dir):
        logger.warning(f"Modules directory not found: {modules_dir}")
        return

    for filename in os.listdir(modules_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            try:
                # Import the module dynamically
                module = importlib.import_module(f"modules.{module_name}")
                
                # Look for the register function
                if hasattr(module, "register"):
                    logger.info(f"Registering module: {module_name}")
                    module.register(mcp)
                else:
                    logger.warning(f"Module {module_name} has no register() function.")
            except Exception as e:
                logger.error(f"Failed to load module {module_name}: {e}")
