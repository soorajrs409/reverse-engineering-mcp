import angr
import logging
import json
import os
from core.r2_base import mcp_tool_wrapper
from modules.debugging_module import manager as debug_manager

logger = logging.getLogger("radare2-mcp.symbolic")

class AngrSessionManager:
    """
    Manages Angr projects and states.
    """
    def __init__(self, file_path: str, base_addr: int = None):
        self.file_path = file_path
        self.base_addr = base_addr
        self.project = None

    def __enter__(self):
        try:
            # Enable libs for simprocedures (like strcmp)
            kwargs = {'auto_load_libs': True}
            if self.base_addr is not None:
                kwargs['main_opts'] = {'base_addr': self.base_addr}
            self.project = angr.Project(self.file_path, **kwargs)
            return self
        except Exception as e:
            logger.error(f"Failed to load binary in Angr: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

@mcp_tool_wrapper
def get_r2_symbolic_reachability(file_path: str, target_address: str, avoid_addresses: str = "") -> str:
    """
    Finds a path to a target address using symbolic execution.
    target_address: hex address or symbol name
    avoid_addresses: comma-separated hex addresses to avoid
    """
    with AngrSessionManager(file_path) as session:
        proj = session.project
        
        # Resolve address if it's a symbol
        try:
            if target_address.startswith("0x"):
                find_addr = int(target_address, 16)
            else:
                find_addr = proj.loader.main_object.get_symbol(target_address).rebased_addr
        except Exception:
            # Fallback for r2-style symbols if loader doesn't have them
            return json.dumps({"status": "error", "message": f"Could not resolve target address: {target_address}"})

        avoid_addrs = []
        if avoid_addresses:
            for addr in avoid_addresses.split(","):
                addr = addr.strip()
                if addr.startswith("0x"):
                    avoid_addrs.append(int(addr, 16))

        # Start from the entry point by default
        state = proj.factory.entry_state()
        simgr = proj.factory.simulation_manager(state)
        
        # Limit exploration to prevent memory exhaustion/hangs
        simgr.explore(find=find_addr, avoid=avoid_addrs, n=100)

        if simgr.found:
            found_state = simgr.found[0]
            # Get stdin using dumps
            stdin_content = found_state.posix.dumps(0)
            
            return json.dumps({
                "status": "success",
                "message": f"Path to {hex(find_addr)} found",
                "stdin": stdin_content.decode(errors='replace'),
                "found_at": hex(find_addr)
            })
        else:
            return json.dumps({"status": "error", "message": "No path found to target address"})

@mcp_tool_wrapper
def get_r2_symbolic_solve_registers(file_path: str, address: str, register_constraints: str) -> str:
    """
    Solves for input constraints that result in specific register states.
    register_constraints: JSON string mapping registers to values, e.g., '{"rax": 0, "rbx": 1}'
    """
    with AngrSessionManager(file_path) as session:
        proj = session.project
        
        try:
            target_addr = int(address, 16) if address.startswith("0x") else proj.loader.main_object.get_symbol(address).rebased_addr
        except Exception:
            return json.dumps({"status": "error", "message": f"Could not resolve address: {address}"})

        try:
            constraints = json.loads(register_constraints)
        except json.JSONDecodeError:
            return json.dumps({"status": "error", "message": "Invalid register_constraints JSON"})

        state = proj.factory.entry_state()
        simgr = proj.factory.simulation_manager(state)
        
        # We want to find a state at the target address that satisfies the constraints
        def check_constraints(s):
            if s.addr != target_addr:
                return False
            try:
                for reg, val in constraints.items():
                    if s.solver.eval(getattr(s.regs, reg)) != val:
                        return False
                return True
            except Exception:
                return False

        simgr.explore(find=check_constraints, n=100)

        if simgr.found:
            found_state = simgr.found[0]
            stdin_content = found_state.posix.dumps(0)
            
            return json.dumps({
                "status": "success",
                "message": f"Found state at {hex(target_addr)} matching constraints",
                "stdin": stdin_content.decode(errors='replace')
            })
        else:
            return json.dumps({"status": "error", "message": "No path found satisfying register constraints"})

@mcp_tool_wrapper
def get_r2_symbolic_function_summary(file_path: str, address_or_symbol: str) -> str:
    """
    Provides a high-level symbolic summary of a function's side effects.
    """
    with AngrSessionManager(file_path) as session:
        proj = session.project
        
        try:
            func_addr = int(address_or_symbol, 16) if address_or_symbol.startswith("0x") else proj.loader.main_object.get_symbol(address_or_symbol).rebased_addr
        except Exception:
            return json.dumps({"status": "error", "message": f"Could not resolve function: {address_or_symbol}"})

        # Use a symbolic state starting at the function entry
        state = proj.factory.call_state(func_addr)
        simgr = proj.factory.simulation_manager(state)
        
        # Step until function return
        simgr.run()

        if simgr.deadended:
            end_state = simgr.deadended[0]
            # Look at registers that are typically used for return values
            rax_val = end_state.regs.rax
            
            return json.dumps({
                "status": "success",
                "function": address_or_symbol,
                "address": hex(func_addr),
                "return_register_symbolic": str(rax_val),
                "is_rax_symbolic": rax_val.symbolic
            })
        else:
            return json.dumps({"status": "error", "message": "Failed to symbolically execute function to completion"})

@mcp_tool_wrapper
def get_r2_symbolic_concolic_transition(session_id: str, target_address: str) -> str:
    """
    Transitions an active debug session into a symbolic state and finds a path.
    """
    session = debug_manager.get_session(session_id)
    if not session:
        return json.dumps({"status": "error", "message": f"Debug session {session_id} not found"})

    state_data = session.get_state()
    file_path = session.file_path
    
    # Find base address from maps to align angr with r2
    base_addr = None
    abs_file_path = os.path.abspath(file_path)
    if "maps" in state_data:
        for m in state_data["maps"]:
            # Find the executable segment corresponding to our binary
            m_file = m.get("file", "")
            m_name = m.get("name", "")
            if m_file == abs_file_path or m_name == abs_file_path or m_file.endswith(file_path) or m_name.endswith(file_path):
                # The first matching map is usually the base
                m_addr = m.get("addr")
                if m_addr is not None:
                    if base_addr is None or m_addr < base_addr:
                        base_addr = m_addr

    print(f"DEBUG: Calculated base_addr: {hex(base_addr) if base_addr is not None else 'None'}")
    with AngrSessionManager(file_path, base_addr=base_addr) as angr_session:
        proj = angr_session.project
        
        # Initialize state from registers
        initial_regs = state_data["registers"]
        
        # Create a blank state at the current RIP
        current_rip = initial_regs.get("rip") or initial_regs.get("pc")
        if current_rip is None:
             return json.dumps({"status": "error", "message": "Could not determine current RIP from debug session"})
        
        state = proj.factory.blank_state(addr=current_rip)
        
        # Sync registers
        for reg, val in initial_regs.items():
            try:
                setattr(state.regs, reg, val)
            except AttributeError:
                continue # Skip registers angr doesn't recognize

        # Resolve target
        try:
            find_addr = int(target_address, 16) if target_address.startswith("0x") else proj.loader.main_object.get_symbol(target_address).rebased_addr
        except Exception:
             return json.dumps({"status": "error", "message": f"Could not resolve target address: {target_address}"})

        simgr = proj.factory.simulation_manager(state)
        simgr.explore(find=find_addr, n=100)

        if simgr.found:
            found_state = simgr.found[0]
            stdin_content = found_state.posix.dumps(0)
            
            return json.dumps({
                "status": "success",
                "message": f"Path from live session at {hex(current_rip)} to {hex(find_addr)} found",
                "stdin": stdin_content.decode(errors='replace')
            })
        else:
            return json.dumps({"status": "error", "message": "No path found from current live state to target"})

def register(mcp):
    """Registers symbolic execution tools with the MCP server."""
    mcp.tool()(get_r2_symbolic_reachability)
    mcp.tool()(get_r2_symbolic_solve_registers)
    mcp.tool()(get_r2_symbolic_function_summary)
    mcp.tool()(get_r2_symbolic_concolic_transition)
