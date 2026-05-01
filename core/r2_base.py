import functools
import json
import logging
import time
from typing import Any, Callable

logger = logging.getLogger("radare2-mcp.base")

def mcp_tool_wrapper(func: Callable) -> Callable:
    """
    Decorator for MCP tools to handle robustness:
    1. Catches all exceptions and returns a structured JSON error response.
    Note: fastmcp doesn't support **kwargs in tool signatures.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> str:
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.error(f"Error in tool {func.__name__}: {e}", exc_info=True)
            return json.dumps({
                "status": "error",
                "tool": func.__name__,
                "message": str(e),
                "type": type(e).__name__
            }, indent=2)
    return wrapper

def r2_cmd_with_retry(r2_instance, command: str, max_retries: int = 3, delay: float = 0.5) -> str:
    """
    Executes a radare2 command with a simple retry mechanism.
    """
    last_exception = None
    for attempt in range(max_retries):
        try:
            return r2_instance.cmd(command)
        except Exception as e:
            last_exception = e
            logger.warning(f"R2 command failed (attempt {attempt+1}/{max_retries}): {command}. Error: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
    
    raise last_exception or RuntimeError(f"Failed to execute command after {max_retries} attempts: {command}")
