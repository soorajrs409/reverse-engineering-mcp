import sys
import os
import json

# Add project root to path
sys.path.append(os.getcwd())

from modules.radare2_module import get_r2_decompile, get_r2_patch_asm, get_r2_patch_hex, get_r2_disassemble

def test_decompilation():
    print("Testing decompilation...")
    binary = "samples/test_binary"
    output = get_r2_decompile(binary, "main")
    print(f"Decompilation output:\n{output[:200]}...")
    assert "main" in output.lower() or "Hello" in output
    print("✓ Decompilation successful")

def test_patching():
    print("Testing patching...")
    # Create a copy of the binary for patching
    source = "samples/test_binary"
    target = "samples/test_binary_patched"
    import shutil
    shutil.copy2(source, target)
    
    try:
        # 1. Check original disassembly
        orig = get_r2_disassemble(target, "main", count=5)
        print(f"Original disassembly:\n{orig}")
        
        # 2. Patch with NOPs
        print("Applying NOP patch...")
        get_r2_patch_asm(target, "main", "nop")
        
        # 3. Verify patch
        patched = get_r2_disassemble(target, "main", count=5)
        print(f"Patched disassembly:\n{patched}")
        assert "nop" in patched.lower()
        
        # 4. Patch with Hex (0x90 is NOP)
        print("Applying Hex patch (0x9090)...")
        get_r2_patch_hex(target, "main+1", "9090")
        
        # 5. Verify final patch
        final = get_r2_disassemble(target, "main", count=5)
        print(f"Final disassembly:\n{final}")
        # Count nops - should have at least 3 now (one from asm patch, two from hex)
        assert final.lower().count("nop") >= 3
        
        print("✓ Patching successful")
    finally:
        if os.path.exists(target):
            os.remove(target)

if __name__ == "__main__":
    try:
        test_decompilation()
        test_patching()
        print("\nAll RE core tools verified successfully!")
    except Exception as e:
        print(f"\nVerification failed: {e}")
        sys.exit(1)
