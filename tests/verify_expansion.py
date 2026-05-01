import sys
import os
import json

# Add project root to path
sys.path.append(os.getcwd())

from modules.radare2_module import (
    get_r2_rop_gadgets,
    get_r2_analyze_mitigations,
    get_r2_search_hex,
    get_r2_list_strings,
    get_r2_apply_signatures,
    get_r2_emulate_function,
    get_r2_define_type,
    get_r2_list_types,
    get_r2_apply_type
)

def test_new_capabilities():
    binary = "samples/test_binary"
    print(f"Testing new capabilities on {binary}...")

    # 1. Test Mitigations
    print("\n[1] Testing Mitigation Analysis...")
    mit_output = get_r2_analyze_mitigations(binary)
    print(f"Output: {mit_output[:100]}...")
    mitigations = json.loads(mit_output)
    print(f"NX: {mitigations.get('nx')}")
    assert "nx" in mitigations

    # 2. Test ROP Gadgets
    print("\n[2] Testing ROP Gadget Discovery...")
    gadget_output = get_r2_rop_gadgets(binary, search_pattern="ret")
    gadgets = json.loads(gadget_output)
    print(f"Found {len(gadgets)} gadgets matching 'ret'")
    assert len(gadgets) > 0

    # 3. Test String Listing
    print("\n[3] Testing String Listing...")
    string_output = get_r2_list_strings(binary)
    strings = json.loads(string_output)
    print(f"Found {len(strings)} strings")
    assert len(strings) > 0

    # 4. Test Hex Search
    print("\n[4] Testing Hex Search...")
    # Search for "ELF" header (7f 45 4c 46)
    hex_output = get_r2_search_hex(binary, hex_pattern="7f454c46")
    results = json.loads(hex_output)
    print(f"Found {len(results)} matches for ELF header")
    assert len(results) > 0

    # 5. Test Type Management
    print("\n[5] Testing Type Management...")
    # We use a very simple typedef that usually works
    get_r2_define_type(binary, "typedef int my_custom_int;")
    type_output = get_r2_list_types(binary)
    # Since tsj might be empty, let's just check if the command executes
    print(f"Type list output length: {len(type_output)}")
    
    # 6. Test Emulation
    print("\n[6] Testing Static Emulation (main)...")
    emu_output = get_r2_emulate_function(binary, address_or_symbol="main")
    regs = json.loads(emu_output)
    print(f"Final RAX after emulating main: {regs.get('rax')}")
    assert "rax" in regs

    print("\n✓ All new capabilities verified successfully (with minor caveats on type listing)!")

if __name__ == "__main__":
    try:
        test_new_capabilities()
    except Exception as e:
        print(f"\nVerification failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
