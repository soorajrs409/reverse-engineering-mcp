## Why

Reverse engineering complex binaries often requires answering reachability questions (e.g., "How can I trigger this crash?") or solving constraints on inputs. Currently, the Radare2 MCP relies on basic ESIL emulation, which is insufficient for deep path exploration or automatic input generation. Integrating a symbolic execution engine like Angr will allow the LLM to perform more rigorous analysis and automate path discovery.

## What Changes

- **New Dependency**: Add `angr` to the project dependencies.
- **New Module**: Create `modules/symbolic_module.py` to house symbolic execution tools.
- **New Tools**:
    - `get_r2_symbolic_reachability`: Find a path to a target address and provide the required input.
    - `get_r2_symbolic_solve_registers`: Solve for input constraints that result in specific register states.
    - `get_r2_symbolic_concolic_transition`: Seamlessly transition from a live debugging session (stopped at a breakpoint) into a symbolic state for exploration.
- **Analysis Integration**: Synchronize Radare2 symbols and function names with the symbolic engine for better context.

## Capabilities

### New Capabilities
- `radare2-symbolic-execution`: Tools for path exploration, constraint solving, and concolic execution using Angr.

### Modified Capabilities
- `radare2-debugging`: Add ability to hand off a live session to the symbolic engine.

## Impact

- **Dependencies**: Adds `angr`, which is a significant dependency.
- **Core**: Enhances the `DebugSessionManager` to support state serialization for symbolic handoff.
- **User Experience**: Drastically reduces the manual effort required for the LLM to find paths or solve input requirements.
