import shutil
import logging

logger = logging.getLogger("radare2-mcp.utils")

def check_dependencies():
    """
    Checks if required external dependencies are installed.
    """
    dependencies = {
        "radare2": "r2"
    }
    
    missing = []
    for name, cmd in dependencies.items():
        if not shutil.which(cmd):
            missing.append(name)
    
    if missing:
        for m in missing:
            logger.error(f"Missing dependency: {m}. Please install it on your host or use the provided Docker environment.")
        return False
    
    logger.info("All external dependencies found.")
    return True
