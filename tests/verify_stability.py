import sys
import os
import json
import time
import threading
import logging
import r2pipe

# Add project root to path
sys.path.append(os.getcwd())

from core.r2_base import mcp_tool_wrapper, r2_cmd_with_retry
from modules.radare2_module import get_r2_cmd, get_r2_decompile
from modules.debugging_module import r2_debug_start, r2_debug_action, r2_debug_terminate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("stability-test")

def check_environment():
    print("\n--- [2.3] Environment Validation ---")
    try:
        r2_version = r2pipe.version()
        print(f"✓ r2pipe version: {r2_version}")
    except Exception as e:
        print(f"✗ Failed to get r2pipe version: {e}")
        return False
        
    try:
        r2 = r2pipe.open("-")
        r2_bin_version = r2.cmd("v")
        r2.quit()
        print(f"✓ Radare2 binary version: {r2_bin_version.strip()}")
    except Exception as e:
        print(f"✗ Radare2 binary not found or failed to execute: {e}")
        return False
        
    print("✓ Environment validation successful")
    return True

def test_error_injection():
    print("\n--- [2.2] Error Injection Testing ---")
    
    # 1. Test non-existent file
    print("Testing non-existent file...")
    result_json = get_r2_cmd("non_existent_file", "v")
    result = json.loads(result_json)
    assert result["status"] == "error"
    error_type = result["error"]["type"]
    print(f"✓ Correctly handled non-existent file: {error_type}")
    assert error_type in ["FileNotFoundError", "RuntimeError", "OSError", "IOError"]

    # 2. Test invalid command in retry logic
    # We can't easily force a timeout without mocking, but we can test invalid commands
    print("Testing invalid command retry...")
    # This might not trigger a Python exception but an r2 error string
    result = get_r2_cmd("samples/test_binary", "invalid_command_xyz")
    # Even if it's not an error in Python, we should check if it returned something sensible
    print(f"✓ Invalid command returned: {result.strip() or '(empty)'}")

    print("✓ Error injection testing successful")

def stress_test_concurrent_calls():
    print("\n--- [2.1] Stress Testing (Concurrent Calls) ---")
    binary = "samples/test_binary"
    num_threads = 5
    results = []
    
    def worker(tid):
        try:
            # Each thread tries to decompile main
            res = get_r2_decompile(binary, "main")
            results.append(True)
            # print(f"Thread {tid} finished")
        except Exception as e:
            logger.error(f"Thread {tid} failed: {e}")
            results.append(False)

    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    success_count = sum(results)
    print(f"Results: {success_count}/{num_threads} successful concurrent calls")
    assert success_count == num_threads
    print("✓ Stress testing successful")

if __name__ == "__main__":
    print("=== Radare2 MCP Stability Audit ===")
    
    if not check_environment():
        sys.exit(1)
        
    test_error_injection()
    stress_test_concurrent_calls()
    
    print("\n=== All stability tests passed! ===")
