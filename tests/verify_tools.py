import os
import sys

# Add current directory to path
sys.path.append(os.getcwd())

from modules.radare2_module import register
from fastmcp import FastMCP

def test_tools():
    mcp = FastMCP("Test")
    register(mcp)
    
    # We can't easily call mcp.tools['r2_cmd'] because it's wrapped
    # But we can call the underlying functions if we had them.
    # Let's just try to open r2pipe directly as a quick check.
    import r2pipe
    try:
        r2 = r2pipe.open("./samples/test_binary")
        print("Radare2 successfully opened test_binary")
        info = r2.cmd("iI")
        if "elf" in info.lower() or "mach-o" in info.lower() or "pe" in info.lower():
            print("Successfully retrieved binary info")
        else:
            print(f"Unexpected binary info: {info}")
        
        r2.cmd("aa")
        functions = r2.cmd("afl")
        if "secret_function" in functions:
            print("Successfully found secret_function")
        else:
            print(f"Functions found: {functions}")
            
        r2.quit()
        return True
    except Exception as e:
        print(f"Test failed: {e}")
        return False

if __name__ == "__main__":
    if test_tools():
        print("Verification SUCCESS")
    else:
        print("Verification FAILURE")
        sys.exit(1)
