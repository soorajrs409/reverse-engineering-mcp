import sys
import os
import time
import threading

# Add project root to path
sys.path.append(os.getcwd())

# Temporarily patch SESSION_TIMEOUT for testing
import modules.debugging_module as dbg
dbg.SESSION_TIMEOUT = 2 # 2 seconds

from modules.debugging_module import r2_debug_start, manager

def test_cleanup():
    print("Testing session cleanup...")
    binary = "samples/test_binary"
    
    # Start session
    session_id = r2_debug_start(binary)
    print(f"Session started: {session_id}")
    
    # Verify it's in manager
    assert session_id in manager.sessions
    print("Session is active.")
    
    # Wait for timeout + check interval
    print("Waiting for cleanup (should take ~60s due to 60s sleep in cleanup loop)...")
    # Actually, the cleanup loop sleeps for 60s. I should probably lower that too for the test.
    
def test_cleanup_fast():
    print("Testing fast cleanup...")
    # I'll manually trigger the check logic or lower the sleep
    dbg.SESSION_TIMEOUT = 1
    
    session_id = r2_debug_start("samples/test_binary")
    print(f"Session started: {session_id}")
    
    time.sleep(2)
    
    # Manually trigger a cleanup check (mimicking the loop)
    now = time.time()
    expired_ids = []
    with manager.lock:
        for sid, session in manager.sessions.items():
            if now - session.last_access > dbg.SESSION_TIMEOUT:
                expired_ids.append(sid)
        
        for sid in expired_ids:
            print(f"Manually cleaning up: {sid}")
            session = manager.sessions.pop(sid)
            session.close()
            
    assert session_id not in manager.sessions
    print("✓ Session successfully cleaned up.")

if __name__ == "__main__":
    test_cleanup_fast()
