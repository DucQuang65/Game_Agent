from importlib import import_module
from typing import Any, Dict, Optional, List, Annotated
from .state import AgentState

_PACKAGE_NAME = __name__.rpartition(".")[0] or None


def _load_nodes():
    """Load node functions without static imports to keep type checkers path-agnostic."""
    try:
        research_mod = import_module(".nodes.research_node", package=_PACKAGE_NAME)
        architect_mod = import_module(".nodes.architect_node", package=_PACKAGE_NAME)
        coder_mod = import_module(".nodes.coder_warrior", package=_PACKAGE_NAME)
        validation_mod = import_module(".nodes.validation_warrior", package=_PACKAGE_NAME)
    except (Exception, ImportError):
        research_mod = import_module("nodes.research_node")
        architect_mod = import_module("nodes.architect_node")
        coder_mod = import_module("nodes.coder_warrior")
        validation_mod = import_module("nodes.validation_warrior")

    return (
        research_mod.researcher_node,
        architect_mod.architect_node,
        coder_mod.coder_warrior_node,
        validation_mod.validation_warrior_node
    )


def build_app() -> Any:
    """Build and compile the LangGraph app when dependencies are available."""
    langgraph_graph = import_module("langgraph.graph")
    state_graph_cls = langgraph_graph.StateGraph
    end_sentinel = langgraph_graph.END
    
    res_node, arch_node, cod_node, val_node = _load_nodes()

    workflow = state_graph_cls(AgentState)

    workflow.add_node("researcher", res_node)
    workflow.add_node("architect", arch_node)
    workflow.add_node("coder", cod_node)
    workflow.add_node("validation", val_node)

    workflow.set_entry_point("researcher")

    workflow.add_edge("researcher", "architect")
    workflow.add_edge("architect", "coder")
    workflow.add_edge("coder", "validation")

    # Decide whether to loop back or end.
    def should_continue(state: AgentState):
        if state.get("task_complete"):
            return end_sentinel
        return "coder"

    workflow.add_conditional_edges("validation", should_continue)
    return workflow.compile()


try:
    app: Optional[Any] = build_app()
except Exception:
    app = None
