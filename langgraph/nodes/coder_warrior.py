import os
from typing import Any, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from ..state import AgentState  # type: ignore
else:
    AgentState = Dict[str, Any]


def coder_warrior_node(state: AgentState) -> Dict:
    """
    Coder Warrior execution node:
    - Writes context files if project_root and target_file are provided.
    - Implements security sandbox validation to prevent path traversal.
    """
    print("--- NODE: CODER WARRIOR ---")

    project_root = state.get("project_root", "")
    target_file = state.get("target_file", "")
    code_patch = state.get("code_patch", "")

    # Security Sandbox: Prevent outside writes
    if project_root and target_file:
        full_path = os.path.abspath(os.path.join(project_root, target_file))
        if not full_path.startswith(os.path.abspath(project_root)):
            return {
                "agent_reasoning": "Blocked: Security Violation. Path escapes project root.",
                "terminal_history": [],
                "messages": state.get("messages", []) + ["Security Violation: Path escapes project root."]
            }

    # Execution Layer
    if project_root and target_file and code_patch:
        full_path = os.path.join(project_root, target_file)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(code_patch)

    # Simulated reasoning for agent history
    reasoning = (
        "1. Analyzing codebase: GameController.cs depends on PlayerNode.\n"
        "2. Applying Signal patch in GDScript.\n"
        "3. Running shell command: 'git add .' and 'aider --message \"Fix Player Signal Connection\"'"
    )

    # Simulated shell command output
    shell_output = {"cmd": "aider --message ...", "out": "Successfully committed changes."}

    return {
        "agent_reasoning": reasoning,
        "terminal_history": [shell_output],
        "messages": state.get("messages", []) + ["Coder Warrior has implemented and committed the fix."]
    }
