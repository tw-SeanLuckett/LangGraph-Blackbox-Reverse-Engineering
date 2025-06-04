"""
Basic integration test for reverse engineering workflow

Tests the actual workflow execution to verify the foundation works.
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from src.workflows.reverse_engineering import ReverseEngineeringWorkflow
from src.workflows.state_management import create_initial_state


@pytest.mark.asyncio
async def test_basic_workflow_integration():
    """Test basic workflow integration with mocked Playwright"""

    # Create initial state
    initial_state = create_initial_state(
        workflow_description="Navigate to login page and click login button",
        domain="accounts_payable",
    )

    # Mock Playwright MCP client
    with patch("src.integrations.playwright_mcp.PlaywrightMCPClient") as mock_mcp_class:
        mock_client = Mock()
        mock_mcp_class.return_value = mock_client

        # Mock browser automation
        mock_client.execute_action.return_value = {
            "success": True,
            "action": "click",
            "selector": "#login-button",
        }

        # Mock data capture
        mock_client.get_audit_logs.return_value = [
            {
                "action": "click",
                "selector": "#login-button",
                "timestamp": datetime.now().isoformat(),
                "success": True,
            }
        ]

        mock_client.get_network_requests.return_value = [
            {
                "url": "https://example.com/api/login",
                "method": "POST",
                "status": 200,
                "response_time": 150,
            }
        ]

        # Create and execute workflow
        workflow = ReverseEngineeringWorkflow()

        # Test individual agents first
        print("Testing journey executor...")
        after_journey = await workflow.execute_journey(initial_state)

        print(f"After journey - iteration_count: {after_journey['iteration_count']}")
        print(
            f"After journey - user_interactions: {len(after_journey['user_interactions'])}"
        )
        print(
            f"After journey - playwright_logs: {len(after_journey['playwright_logs'])}"
        )
        print(
            f"After journey - network_requests: {len(after_journey['network_requests'])}"
        )

        print("Testing data capturer...")
        after_capture = await workflow.capture_data(after_journey)

        print(
            f"After capture - processed_interactions: {len(after_capture.get('processed_interactions', []))}"
        )

        # Verify basic functionality
        assert after_journey["iteration_count"] > 0
        assert len(after_journey["user_interactions"]) > 0
        assert len(after_journey["playwright_logs"]) > 0
        assert len(after_journey["network_requests"]) > 0

        assert "processed_interactions" in after_capture
        assert len(after_capture["processed_interactions"]) > 0


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_basic_workflow_integration())
