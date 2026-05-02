import r2pipe
import logging
import json
import os
import uuid
import time
import threading
from typing import Dict, Optional
from fastmcp import FastMCP
from core.r2_base import mcp_tool_wrapper, r2_cmd_with_retry

logger = logging.getLogger("radare2-mcp.debugging")

# Configuration
SESSION_TIMEOUT = 600  # 10 minutes in seconds

class DebugSession:
    def __init__(self, file_path: str):
        self.session_id = str(uuid.uuid4())
        self.file_path = file_path
        self.r2 = r2pipe.open(file_path, flags=["-d"])
        self.last_access = time.time()
        self.lock = threading.Lock()
        
        try:
            # Initial analysis
            self.cmd("aa")
            logger.info(f"Started debug session {self.session_id} for {file_path}")
        except Exception as e:
            logger.error(f"Failed to initialize debug session: {e}")
            if self.r2:
                self.r2.quit()
            raise

    def touch(self):
        self.last_access = time.time()

    def cmd(self, command: str) -> str:
        """Executes a command using the session's r2 instance with retries."""
        if not self.r2:
            raise RuntimeError("Session closed.")
        return r2_cmd_with_retry(self.r2, command)

    def get_state(self) -> dict:
        """Captures the current state for concolic transition."""
        with self.lock:
            regs = json.loads(self.cmd("drj"))
            # Get memory maps
            maps = json.loads(self.cmd("dmj"))
            return {
                "registers": regs,
                "maps": maps
            }

    def close(self):
        if self.r2:
            try:
                self.r2.quit()
            except Exception as e:
                logger.warning(f"Error quitting r2 session {self.session_id}: {e}")
            self.r2 = None

class DebugSessionManager:
    def __init__(self):
        self.sessions: Dict[str, DebugSession] = {}
        self.lock = threading.Lock()
        self.cleanup_thread: Optional[threading.Thread] = None
        self.running = False

    def start_session(self, file_path: str) -> str:
        session = DebugSession(file_path)
        with self.lock:
            self.sessions[session.session_id] = session
        return session.session_id

    def get_session(self, session_id: str) -> Optional[DebugSession]:
        with self.lock:
            session = self.sessions.get(session_id)
            if session:
                session.touch()
            return session

    def terminate_session(self, session_id: str) -> bool:
        with self.lock:
            session = self.sessions.pop(session_id, None)
            if session:
                session.close()
                return True
        return False

    def cleanup_loop(self):
        logger.info("Debug session cleanup thread started.")
        while self.running:
            time.sleep(60)  # Check every minute
            now = time.time()
            expired_sessions = []
            
            with self.lock:
                expired_ids = [
                    sid for sid, session in self.sessions.items()
                    if now - session.last_access > SESSION_TIMEOUT
                ]
                for sid in expired_ids:
                    logger.info(f"Expiring debug session: {sid}")
                    expired_sessions.append(self.sessions.pop(sid))
            
            # Close expired sessions outside the lock
            for session in expired_sessions:
                try:
                    session.close()
                except Exception as e:
                    logger.error(f"Error closing expired session {session.session_id}: {e}")

    def start_cleanup(self):
        if not self.running:
            self.running = True
            self.cleanup_thread = threading.Thread(target=self.cleanup_loop, daemon=True)
            self.cleanup_thread.start()

    def stop_cleanup(self):
        self.running = False
        if self.cleanup_thread:
            self.cleanup_thread.join(timeout=2)

# Global manager instance
manager = DebugSessionManager()

@mcp_tool_wrapper
def r2_debug_start(file_path: str) -> str:
    """
    Starts a live debug session for a target binary.
    Returns a unique session_id.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return manager.start_session(file_path)

@mcp_tool_wrapper
def r2_debug_action(session_id: str, action: str) -> str:
    """
    Executes a debugging action (ds, dc, db, etc.) on an active session.
    Returns the output of the command.
    """
    session = manager.get_session(session_id)
    if not session:
        return f"Error: Session {session_id} not found or expired."
    
    with session.lock:
        output = session.cmd(action)
        return output

@mcp_tool_wrapper
def r2_debug_read_state(session_id: str) -> str:
    """
    Reads the current state of registers and disassembles the current instruction.
    """
    session = manager.get_session(session_id)
    if not session:
        return f"Error: Session {session_id} not found or expired."
    
    with session.lock:
        regs = session.cmd("drj")
        instruction = session.cmd("pd 1 @ rip")
        try:
            regs_obj = json.loads(regs)
        except json.JSONDecodeError:
            regs_obj = {"error": "Failed to parse registers"}
            
        return json.dumps({
            "registers": regs_obj,
            "instruction": instruction.strip()
        }, indent=2)

@mcp_tool_wrapper
def r2_debug_terminate(session_id: str) -> str:
    """
    Explicitly terminates a debug session.
    """
    if manager.terminate_session(session_id):
        return f"Session {session_id} terminated."
    else:
        return f"Session {session_id} not found."

def register(mcp: FastMCP):
    """
    Registers debugging tools with the MCP server and starts cleanup thread.
    """
    manager.start_cleanup()
    
    mcp.tool()(r2_debug_start)
    mcp.tool()(r2_debug_action)
    mcp.tool()(r2_debug_read_state)
    mcp.tool()(r2_debug_terminate)
    
    logger.info("Interactive debugging tools registered.")
