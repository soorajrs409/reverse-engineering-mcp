import sys
import os
import json

# Add project root to path
sys.path.append(os.getcwd())

from modules.symbolic_module import (
    get_r2_symbolic_reachability,
    get_r2_symbolic_solve_registers,
    get_r2_symbolic_function_summary,
    get_r2_symbolic_concolic_transition
)
from modules.debugging_module import (
    r2_debug_start,
    r2_debug_action,
    r2_debug_terminate
)

def test_symbolic_capabilities():
    binary = "samples/branch_binary"
    print(f"Testing symbolic capabilities on {binary}...")

    # 1. Test Function Summary for 'check'
    print("\n[1] Testing Function Summary for 'check'...")
    sum_output = get_r2_symbolic_function_summary(binary, address_or_symbol="check")
    print(f"Output: {sum_output}")
    summary = json.loads(sum_output)
    assert summary["status"] == "success"
    print(f"✓ Summary generated for {summary['function']}")

    # 2. Test Reachability to 'main'
    print("\n[2] Testing Reachability to 'main'...")
    reach_output = get_r2_symbolic_reachability(binary, target_address="main")
    print(f"Output: {reach_output}")
    reach = json.loads(reach_output)
    assert reach["status"] == "success"
    print(f"✓ Reached main")

    # 3. Test Concolic Handoff
    print("\n[3] Testing Concolic Handoff (transition from live debug to 'check')...")
    session_id = r2_debug_start(binary)
    try:
        # Continue to main
        r2_debug_action(session_id, "db main")
        r2_debug_action(session_id, "dc")
        
        handoff_output = get_r2_symbolic_concolic_transition(session_id, target_address="check")
        print(f"Handoff Output: {handoff_output}")
        handoff = json.loads(handoff_output)
        # Note: Depending on where we are, it might not find a path if it already passed 'check' 
        # but since 'check' is called from main it should be fine.
        assert handoff["status"] == "success"
        print(f"✓ Concolic handoff and reachability successful")
    finally:
        r2_debug_terminate(session_id)

    print("\n✓ Symbolic capabilities verified successfully!")

if __name__ == "__main__":
    try:
        test_symbolic_capabilities()
    except Exception as e:
        print(f"\nVerification failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
