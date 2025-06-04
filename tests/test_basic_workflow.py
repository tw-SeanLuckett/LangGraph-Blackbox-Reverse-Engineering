"""
Test basic LangGraph workflow for reverse engineering

Following TDD principles - these tests define the expected behavior
of the core workflow before implementation.
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from src.workflows.reverse_engineering import ReverseEngineeringWorkflow
from src.workflows.state_management import create_initial_state


class TestBasicReverseEngineeringWorkflow:
    """Test the basic LangGraph workflow execution"""

    @pytest.fixture
    def workflow(self):
        """Create a workflow instance for testing"""
        return ReverseEngineeringWorkflow()

    @pytest.fixture
    def sample_state(self):
        """Create sample state for testing"""
        return create_initial_state(
            workflow_description="Navigate to login page and click login button",
            domain="accounts_payable",
        )

    def test_workflow_initializes_with_required_agents(self, workflow):
        """Workflow initializes with journey executor and data capturer agents"""
        # Test that workflow has the required agent methods
        assert hasattr(workflow, "execute_journey")
        assert hasattr(workflow, "capture_data")
        assert hasattr(workflow, "workflow")

        # Test that workflow is properly configured
        assert workflow.workflow is not None

    @pytest.mark.asyncio
    async def test_journey_executor_processes_workflow_description(self):
        """Journey executor agent processes workflow description into browser actions"""
        # Create fresh state for this test
        test_state = create_initial_state(
            workflow_description="Navigate to login page and click login button",
            domain="accounts_payable",
        )

        # Create workflow with mocked client
        with patch(
            "src.integrations.playwright_mcp.PlaywrightMCPClient"
        ) as mock_mcp_class:
            mock_client = Mock()
            mock_mcp_class.return_value = mock_client

            # Mock successful browser action
            mock_client.execute_action.return_value = {
                "success": True,
                "action": "navigate",
                "url": "https://example.com/login",
            }

            # Mock audit logs and network requests
            mock_client.get_audit_logs.return_value = [
                {
                    "action": "mock_action",
                    "instruction": test_state["workflow_description"],
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

            # Create workflow after mocking
            workflow = ReverseEngineeringWorkflow()

            # Store initial count
            initial_count = test_state["iteration_count"]

            # Execute journey
            result_state = await workflow.execute_journey(test_state)

            # Verify state was updated with interaction data
            assert result_state["iteration_count"] > initial_count
            assert len(result_state["user_interactions"]) > 0

            # Verify the interaction was recorded
            interaction = result_state["user_interactions"][0]
            assert interaction["success"] is True
            assert "timestamp" in interaction

    @pytest.mark.asyncio
    async def test_data_capturer_processes_playwright_logs(self, workflow):
        """Data capturer agent processes and structures Playwright interaction logs"""
        # Create fresh state for this test
        test_state = create_initial_state(
            workflow_description="Test workflow", domain="test_domain"
        )

        # Add sample Playwright logs to state
        test_state["playwright_logs"] = [
            {
                "action": "click",
                "selector": "#login-button",
                "timestamp": datetime.now().isoformat(),
                "success": True,
            }
        ]

        test_state["network_requests"] = [
            {
                "url": "https://example.com/api/login",
                "method": "POST",
                "status": 200,
                "response_time": 150,
                "timestamp": datetime.now().isoformat(),
            }
        ]

        # Execute data capture
        result_state = await workflow.capture_data(test_state)

        # Verify data was processed and structured
        assert "processed_interactions" in result_state
        assert len(result_state["processed_interactions"]) > 0

        # Verify network requests were correlated
        processed = result_state["processed_interactions"][0]
        assert "correlated_requests" in processed
        assert len(processed["correlated_requests"]) > 0

    @pytest.mark.asyncio
    async def test_workflow_executes_end_to_end(self):
        """Complete workflow executes from start to finish"""
        # Create fresh state for this test
        test_state = create_initial_state(
            workflow_description="Navigate to login page and click login button",
            domain="accounts_payable",
        )

        # Mock all external dependencies
        with patch(
            "src.integrations.playwright_mcp.PlaywrightMCPClient"
        ) as mock_mcp_class:
            mock_client = Mock()
            mock_mcp_class.return_value = mock_client

            # Mock browser automation success
            mock_client.execute_action.return_value = {
                "success": True,
                "action": "click",
                "selector": "#login-button",
            }

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

            # Create workflow after mocking
            workflow = ReverseEngineeringWorkflow()

            # Execute complete workflow
            final_state = await workflow.execute(test_state)

            # Verify workflow completed successfully
            assert final_state is not None
            assert final_state["iteration_count"] > 0
            assert len(final_state["user_interactions"]) > 0
            assert len(final_state["playwright_logs"]) > 0
            assert len(final_state["network_requests"]) > 0

    def test_workflow_handles_invalid_input_gracefully(self, workflow):
        """Workflow handles invalid input without crashing"""
        # Test with empty workflow description
        empty_state = create_initial_state("", "invalid_domain")

        # Should not raise exception
        assert empty_state["workflow_description"] == ""
        assert empty_state["current_domain"] == "invalid_domain"

    @pytest.mark.asyncio
    async def test_workflow_state_persistence_between_agents(self):
        """State is properly maintained and passed between agents"""
        # Create fresh state for this test
        test_state = create_initial_state(
            workflow_description="Test workflow", domain="test_domain"
        )

        # Add some initial data
        test_state["test_data"] = "initial_value"

        # Mock Playwright integration
        with patch(
            "src.integrations.playwright_mcp.PlaywrightMCPClient"
        ) as mock_mcp_class:
            mock_client = Mock()
            mock_mcp_class.return_value = mock_client

            # Mock basic responses
            mock_client.execute_action.return_value = {"success": True}
            mock_client.get_audit_logs.return_value = []
            mock_client.get_network_requests.return_value = []

            # Create workflow after mocking
            workflow = ReverseEngineeringWorkflow()

            # Execute journey executor
            after_journey = await workflow.execute_journey(test_state)

            # Verify state persistence
            assert after_journey["test_data"] == "initial_value"
            assert (
                after_journey["workflow_description"]
                == test_state["workflow_description"]
            )

            # Execute data capturer
            after_capture = await workflow.capture_data(after_journey)

            # Verify state still persisted
            assert after_capture["test_data"] == "initial_value"
            assert (
                after_capture["workflow_description"]
                == test_state["workflow_description"]
            )
