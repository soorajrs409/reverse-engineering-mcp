import sys
import os
import json
import time

# Add project root to path
sys.path.append(os.getcwd())

from modules.debugging_module import r2_debug_start, r2_debug_action, r2_debug_read_state, r2_debug_terminate

def test_debugging_flow():
    print("Testing interactive debugging flow...")
    binary = "samples/test_binary"
    
    # 1. Start session
    session_id = r2_debug_start(binary)
    print(f"Session started: {session_id}")
    
    try:
        # 2. Read initial state
        state = json.loads(r2_debug_read_state(session_id))
        print(f"Initial instruction: {state['instruction']}")
        
        # 3. Step once
        print("Stepping...")
        r2_debug_action(session_id, "ds")
        
        # 4. Read state after step
        state_after = json.loads(r2_debug_read_state(session_id))
        print(f"Instruction after step: {state_after['instruction']}")
        
        # Verify PC changed
        orig_rip = state['registers']['rip']
        new_rip = state_after['registers']['rip']
        print(f"RIP: {orig_rip} -> {new_rip}")
        assert orig_rip != new_rip
        
        # 5. Set breakpoint at main
        print("Setting breakpoint at main...")
        r2_debug_action(session_id, "db main")
        
        # 6. Continue to breakpoint
        print("Continuing to main...")
        r2_debug_action(session_id, "dc")
        
        # 7. Final state check
        final_state = json.loads(r2_debug_read_state(session_id))
        print(f"Instruction at breakpoint: {final_state['instruction']}")
        
        print("✓ Debugging flow successful")
        
    finally:
        r2_debug_terminate(session_id)
        print("Session terminated.")

if __name__ == "__main__":
    try:
        test_debugging_flow()
        print("\nInteractive debugging verified successfully!")
    except Exception as e:
        print(f"\nVerification failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
