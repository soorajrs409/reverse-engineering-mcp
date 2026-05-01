import json
import os
import sys

# Add current directory to path
sys.path.append(os.getcwd())

from modules.radare2_module import (
    get_r2_binary_info, get_r2_list_imports, get_r2_get_entropy, 
    get_r2_get_xrefs, get_r2_get_call_graph, get_r2_get_function_details,
    get_r2_rename_symbol, get_r2_set_comment, get_r2_cleanup_project,
    get_r2_cmd, get_r2_disassemble
)

TEST_BINARY = "samples/test_binary"

def test_tools():
    if not os.path.exists(TEST_BINARY):
        print(f"Error: {TEST_BINARY} not found. Run 'gcc test_binary.c -o test_binary' first.")
        return

    print("--- Testing get_r2_binary_info ---")
    info = get_r2_binary_info(TEST_BINARY)
    print(info[:200] + "...")

    print("\n--- Testing get_r2_list_imports ---")
    imports = get_r2_list_imports(TEST_BINARY)
    print(imports)

    print("\n--- Testing get_r2_get_entropy ---")
    entropy = get_r2_get_entropy(TEST_BINARY)
    print(entropy[:200] + "...")

    print("\n--- Testing get_r2_get_function_details (main) ---")
    details = get_r2_get_function_details(TEST_BINARY, "main")
    print(details[:200] + "...")

    print("\n--- Testing State Management (Rename & Comment) ---")
    get_r2_rename_symbol(TEST_BINARY, "main", "entry_point")
    get_r2_set_comment(TEST_BINARY, "entry_point", "This is the main entry")
    
    print("\n--- Verifying Persistence ---")
    disasm = get_r2_disassemble(TEST_BINARY, "entry_point", count=5)
    print(disasm)
    if "entry_point" in disasm and "main entry" in disasm:
        print("SUCCESS: Rename and Comment persisted!")
    else:
        print("FAILURE: Persistence check failed.")

    print("\n--- Testing get_r2_get_xrefs (entry_point) ---")
    xrefs = get_r2_get_xrefs(TEST_BINARY, "entry_point")
    print(xrefs)

    print("\n--- Testing get_r2_cleanup_project ---")
    cleanup = get_r2_cleanup_project(TEST_BINARY)
    print(cleanup)

if __name__ == "__main__":
    test_tools()
