"""
State management for LangGraph reverse engineering workflow

Defines the state structure and initialization functions for the
multi-agent reverse engineering workflow.
"""

from typing import Dict, List, Any, TypedDict


class ReverseEngineeringState(TypedDict):
    """
    State structure for the reverse engineering workflow.

    This state is passed between all LangGraph agents and maintains
    the complete context of the reverse engineering process.
    """

    # Input and workflow control
    workflow_description: str
    current_domain: str  # AP, consignment, returns, parts
    iteration_count: int

    # Captured data from browser automation
    playwright_logs: List[Dict[str, Any]]
    network_requests: List[Dict[str, Any]]
    dom_changes: List[Dict[str, Any]]
    user_interactions: List[Dict[str, Any]]

    # Analysis results from pattern recognition
    inferred_api_endpoints: List[Dict[str, Any]]
    database_schema: Dict[str, Any]
    business_logic_patterns: List[Dict[str, Any]]
    ui_component_patterns: List[Dict[str, Any]]

    # Generated outputs
    backend_code: Dict[str, str]  # filename -> code content
    frontend_code: Dict[str, str]  # filename -> code content
    documentation: Dict[str, str]  # doc_type -> content

    # Workflow state control
    analysis_complete: bool
    generation_targets: List[str]
    next_actions: List[str]


def create_initial_state(
    workflow_description: str, domain: str
) -> ReverseEngineeringState:
    """
    Create initial state for reverse engineering workflow.

    Args:
        workflow_description: Natural language description of the workflow to analyze
        domain: Business domain (accounts_payable, consignment, returns, parts)

    Returns:
        Initialized ReverseEngineeringState with empty collections
    """
    return ReverseEngineeringState(
        # Input and workflow control
        workflow_description=workflow_description,
        current_domain=domain,
        iteration_count=0,
        # Captured data - initialized as empty lists
        playwright_logs=[],
        network_requests=[],
        dom_changes=[],
        user_interactions=[],
        # Analysis results - initialized as empty
        inferred_api_endpoints=[],
        database_schema={},
        business_logic_patterns=[],
        ui_component_patterns=[],
        # Generated outputs - initialized as empty dicts
        backend_code={},
        frontend_code={},
        documentation={},
        # Workflow state control
        analysis_complete=False,
        generation_targets=[],
        next_actions=[],
    )
