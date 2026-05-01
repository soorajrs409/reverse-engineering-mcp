import r2pipe
import logging
import json
import os
import hashlib
from fastmcp import FastMCP
from core.r2_base import mcp_tool_wrapper, r2_cmd_with_retry

logger = logging.getLogger("radare2-mcp.radare2")

PROJECTS_DIR = ".r2_projects"

class Radare2SessionManager:
    """
    Manages persistent Radare2 sessions using project files.
    """
    def __init__(self, file_path: str, write_mode: bool = False):
        self.file_path = file_path
        self.write_mode = write_mode
        self.project_name = self._generate_project_name(file_path)
        self.project_path = os.path.join(PROJECTS_DIR, self.project_name)
        self.r2 = None

    def _generate_project_name(self, file_path: str) -> str:
        """Generates a unique project name based on the file path hash."""
        file_hash = hashlib.md5(file_path.encode()).hexdigest()
        base_name = os.path.basename(file_path)
        return f"{base_name}_{file_hash}"

    def cmd(self, command: str) -> str:
        """Executes a command using the session's r2 instance with retries."""
        if not self.r2:
            raise RuntimeError("Session not started. Use 'with' statement.")
        return r2_cmd_with_retry(self.r2, command)

    def __enter__(self):
        try:
            # Open in write mode if requested
            flags = ["-w"] if self.write_mode else []
            self.r2 = r2pipe.open(self.file_path, flags=flags)
            
            # Ensure project directory exists
            if not os.path.exists(PROJECTS_DIR):
                os.makedirs(PROJECTS_DIR)
            
            # Use absolute path for dir.projects
            abs_proj_dir = os.path.abspath(PROJECTS_DIR)
            self.cmd(f"e dir.projects = {abs_proj_dir}")
            
            projects_json = self.cmd("Plj")
            try:
                projects = json.loads(projects_json)
            except json.JSONDecodeError:
                logger.warning("Failed to parse project list JSON, falling back to empty list")
                projects = []

            if self.project_name in projects:
                logger.info(f"Loading existing project: {self.project_name}")
                self.cmd(f"P {self.project_name}")
            else:
                logger.info(f"Creating new project for: {self.file_path}")
                self.cmd("aaa")
                self.cmd(f"Ps {self.project_name}")
            
            if self.write_mode:
                logger.info("Enabling write mode (oo+ and io.cache)")
                self.cmd("oo+")
                self.cmd("e io.cache=true")
            
            return self
        except Exception as e:
            logger.error(f"Failed to open radare2 session: {e}")
            if self.r2:
                self.r2.quit()
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.r2:
            try:
                self.cmd(f"P+ {self.project_name}")
            except Exception as e:
                logger.warning(f"Failed to save project on exit: {e}")
            finally:
                self.r2.quit()

# Global state for decompiler availability
DECOMPILERS = {
    "pdg": False, # r2ghidra
    "pdd": False, # r2dec
    "pdc": True   # native (always available)
}

def detect_decompilers():
    """Checks for available decompiler plugins."""
    try:
        r2 = r2pipe.open("-")
        # Check pdg (r2ghidra)
        help_pdg = r2.cmd("pdg?")
        if "Usage: pdg" in help_pdg:
            DECOMPILERS["pdg"] = True
            logger.info("Decompiler found: r2ghidra (pdg)")
        
        # Check pdd (r2dec)
        help_pdd = r2.cmd("pdd?")
        if "Usage: pdd" in help_pdd:
            DECOMPILERS["pdd"] = True
            logger.info("Decompiler found: r2dec (pdd)")
        
        r2.quit()
    except Exception as e:
        logger.warning(f"Failed to detect decompiler plugins: {e}")

# Call detection on module load
detect_decompilers()

# Standalone tool functions for better testability

@mcp_tool_wrapper
def get_r2_decompile(file_path: str, address_or_symbol: str = "main") -> str:
    """
    Decompiles a function or address into pseudo-code.
    Tries r2ghidra (pdg), then r2dec (pdd), and falls back to native pdc.
    """
    with Radare2SessionManager(file_path) as session:
        if DECOMPILERS["pdg"]:
            return session.cmd(f"pdg @ {address_or_symbol}")
        elif DECOMPILERS["pdd"]:
            return session.cmd(f"pdd @ {address_or_symbol}")
        else:
            return session.cmd(f"pdc @ {address_or_symbol}")

@mcp_tool_wrapper
def get_r2_cmd(file_path: str, command: str) -> str:
    with Radare2SessionManager(file_path) as session:
        return session.cmd(command)

@mcp_tool_wrapper
def get_r2_disassemble(file_path: str, address_or_symbol: str = "main", count: int = 20) -> str:
    with Radare2SessionManager(file_path) as session:
        return session.cmd(f"pd {count} @ {address_or_symbol}")

@mcp_tool_wrapper
def get_r2_search_strings(file_path: str, pattern: str) -> str:
    with Radare2SessionManager(file_path) as session:
        return session.cmd(f"/ {pattern}")

@mcp_tool_wrapper
def get_r2_binary_info(file_path: str) -> str:
    with Radare2SessionManager(file_path) as session:
        return session.cmd("iIj")

@mcp_tool_wrapper
def get_r2_list_imports(file_path: str, filter_dangerous: bool = True) -> str:
    with Radare2SessionManager(file_path) as session:
        imports_json = session.cmd("iij")
        if not filter_dangerous:
            return imports_json
        dangerous = ["system", "strcpy", "gets", "popen", "scanf", "sprintf", "strcat", "memcpy", "memmove"]
        all_imports = json.loads(imports_json)
        filtered = [imp for imp in all_imports if any(d in imp.get("name", "").lower() for d in dangerous)]
        return json.dumps(filtered, indent=2)

@mcp_tool_wrapper
def get_r2_get_entropy(file_path: str) -> str:
    with Radare2SessionManager(file_path) as session:
        return session.cmd("p=ej")

@mcp_tool_wrapper
def get_r2_get_xrefs(file_path: str, address_or_symbol: str) -> str:
    with Radare2SessionManager(file_path) as session:
        refs_to = session.cmd(f"axtj {address_or_symbol}")
        refs_from = session.cmd(f"axfj {address_or_symbol}")
        return json.dumps({
            "references_to": json.loads(refs_to or "[]"),
            "references_from": json.loads(refs_from or "[]")
        }, indent=2)

@mcp_tool_wrapper
def get_r2_get_call_graph(file_path: str) -> str:
    with Radare2SessionManager(file_path) as session:
        return session.cmd("agCj")

@mcp_tool_wrapper
def get_r2_get_function_details(file_path: str, function_name: str) -> str:
    with Radare2SessionManager(file_path) as session:
        vars_json = session.cmd(f"afvj @ {function_name}")
        blocks_json = session.cmd(f"afbj @ {function_name}")
        info_json = session.cmd(f"afij @ {function_name}")
        return json.dumps({
            "info": json.loads(info_json or "[]"),
            "variables": json.loads(vars_json or "{}"),
            "basic_blocks": json.loads(blocks_json or "[]")
        }, indent=2)

@mcp_tool_wrapper
def get_r2_rename_symbol(file_path: str, old_name: str, new_name: str) -> str:
    with Radare2SessionManager(file_path) as session:
        session.cmd(f"afn {new_name} {old_name}")
        return f"Successfully renamed {old_name} to {new_name}"

@mcp_tool_wrapper
def get_r2_set_comment(file_path: str, address_or_symbol: str, comment: str) -> str:
    with Radare2SessionManager(file_path) as session:
        session.cmd(f"CC {comment} @ {address_or_symbol}")
        return f"Successfully added comment to {address_or_symbol}"

@mcp_tool_wrapper
def get_r2_patch_asm(file_path: str, address_or_symbol: str, instruction: str) -> str:
    """
    Writes assembly instructions to a specific address in the binary.
    WARNING: This modifies the binary file.
    """
    with Radare2SessionManager(file_path, write_mode=True) as session:
        session.cmd(f"wa {instruction} @ {address_or_symbol}")
        return f"Successfully patched {address_or_symbol} with: {instruction}"

@mcp_tool_wrapper
def get_r2_patch_hex(file_path: str, address_or_symbol: str, hex_bytes: str) -> str:
    """
    Writes raw hex bytes to a specific address in the binary.
    WARNING: This modifies the binary file.
    """
    with Radare2SessionManager(file_path, write_mode=True) as session:
        session.cmd(f"wx {hex_bytes} @ {address_or_symbol}")
        return f"Successfully patched {address_or_symbol} with hex: {hex_bytes}"

@mcp_tool_wrapper
def get_r2_rop_gadgets(file_path: str, search_pattern: str = "") -> str:
    """
    Searches for ROP gadgets in the binary.
    """
    with Radare2SessionManager(file_path) as session:
        session.cmd("aa") # Basic analysis helps gadget discovery
        cmd = f"/Rj {search_pattern}" if search_pattern else "/Rj"
        return session.cmd(cmd)

@mcp_tool_wrapper
def get_r2_analyze_mitigations(file_path: str) -> str:
    """
    Analyzes binary security mitigations (NX, Canary, PIE, RELRO).
    """
    with Radare2SessionManager(file_path) as session:
        return session.cmd("iIj")

@mcp_tool_wrapper
def get_r2_search_hex(file_path: str, hex_pattern: str) -> str:
    """
    Searches for a hex pattern in the binary.
    """
    with Radare2SessionManager(file_path) as session:
        return session.cmd(f"/xj {hex_pattern}")

@mcp_tool_wrapper
def get_r2_list_strings(file_path: str, data_only: bool = False) -> str:
    """
    Lists strings in the binary.
    """
    with Radare2SessionManager(file_path) as session:
        cmd = "izj" if data_only else "izzj"
        return session.cmd(cmd)

@mcp_tool_wrapper
def get_r2_apply_signatures(file_path: str) -> str:
    """
    Applies signatures to identify library functions.
    """
    with Radare2SessionManager(file_path) as session:
        session.cmd("zg")
        return "Signatures applied successfully."

@mcp_tool_wrapper
def get_r2_emulate_function(file_path: str, address_or_symbol: str) -> str:
    """
    Emulates a function using the ESIL engine and returns the final register state.
    """
    with Radare2SessionManager(file_path) as session:
        session.cmd("aei")  # Init ESIL
        session.cmd("aeim") # Init ESIL memory
        session.cmd(f"aeu @ {address_or_symbol}") # Emulate until function return
        return session.cmd("arj") # Return registers as JSON

@mcp_tool_wrapper
def get_r2_define_type(file_path: str, type_definition: str) -> str:
    """
    Defines a C-style type or struct in the project.
    Example: "struct foo { int a; int b; };"
    """
    with Radare2SessionManager(file_path) as session:
        session.cmd(f"\"td {type_definition}\"")
        return f"Type defined successfully: {type_definition}"

@mcp_tool_wrapper
def get_r2_list_types(file_path: str) -> str:
    """
    Lists all defined types in the project.
    """
    with Radare2SessionManager(file_path) as session:
        return session.cmd("tsj")

@mcp_tool_wrapper
def get_r2_apply_type(file_path: str, address_or_symbol: str, type_name: str) -> str:
    """
    Applies a defined type to a specific address.
    """
    with Radare2SessionManager(file_path) as session:
        session.cmd(f"av {type_name} @ {address_or_symbol}")
        return f"Applied type {type_name} to {address_or_symbol}"

@mcp_tool_wrapper
def get_r2_cleanup_project(file_path: str) -> str:
    session_mgr = Radare2SessionManager(file_path)
    project_name = session_mgr.project_name
    with Radare2SessionManager(file_path) as session:
        session.cmd(f"Pd {project_name}")
    return f"Successfully deleted project: {project_name}"

def register(mcp: FastMCP):
    """
    Registers radare2 analysis tools with the MCP server.
    """
    mcp.tool()(get_r2_decompile)
    mcp.tool()(get_r2_patch_asm)
    mcp.tool()(get_r2_patch_hex)
    mcp.tool()(get_r2_cmd)
    mcp.tool()(get_r2_disassemble)
    mcp.tool()(get_r2_search_strings)
    mcp.tool()(get_r2_binary_info)
    mcp.tool()(get_r2_list_imports)
    mcp.tool()(get_r2_get_entropy)
    mcp.tool()(get_r2_get_xrefs)
    mcp.tool()(get_r2_get_call_graph)
    mcp.tool()(get_r2_get_function_details)
    mcp.tool()(get_r2_rename_symbol)
    mcp.tool()(get_r2_set_comment)
    mcp.tool()(get_r2_rop_gadgets)
    mcp.tool()(get_r2_analyze_mitigations)
    mcp.tool()(get_r2_search_hex)
    mcp.tool()(get_r2_list_strings)
    mcp.tool()(get_r2_apply_signatures)
    mcp.tool()(get_r2_emulate_function)
    mcp.tool()(get_r2_define_type)
    mcp.tool()(get_r2_list_types)
    mcp.tool()(get_r2_apply_type)
    mcp.tool()(get_r2_cleanup_project)

    logger.info("Radare2 module tools registered with persistent session support.")
