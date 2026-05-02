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
    2. Ensures the response is always a string (JSON formatted if error).
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> str:
        try:
            result = func(*args, **kwargs)
            if not isinstance(result, str):
                return str(result)
            return result
        except Exception as e:
            logger.error(f"Error in tool {func.__name__}: {e}", exc_info=True)
            error_response = {
                "status": "error",
                "tool": func.__name__,
                "error": {
                    "type": type(e).__name__,
                    "message": str(e),
                    "context": "An unexpected error occurred during tool execution."
                }
            }
            return json.dumps(error_response, indent=2)
    return wrapper

def r2_cmd_with_retry(r2_instance, command: str, max_retries: int = 3, initial_delay: float = 0.5) -> str:
    """
    Executes a radare2 command with exponential backoff retry.
    Handles transient failures and tool-specific edge cases.
    """
    last_exception = None
    delay = initial_delay
    
    for attempt in range(max_retries):
        try:
            # Check if r2_instance is still valid/alive if possible
            # For r2pipe, we just try the command
            result = r2_instance.cmd(command)
            
            # Basic sanity check on result - some r2 errors are returned as strings
            if result and ("ERROR" in result or "Invalid" in result) and attempt < max_retries - 1:
                logger.warning(f"R2 returned error string (attempt {attempt+1}/{max_retries}): {result.strip()}")
                time.sleep(delay)
                delay *= 2
                continue
                
            return result
        except Exception as e:
            last_exception = e
            logger.warning(f"R2 command failed (attempt {attempt+1}/{max_retries}): {command}. Error: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2
            else:
                break
    
    error_msg = f"Failed to execute r2 command after {max_retries} attempts: {command}"
    if last_exception:
        error_msg += f". Last error: {last_exception}"
    
    raise RuntimeError(error_msg)
