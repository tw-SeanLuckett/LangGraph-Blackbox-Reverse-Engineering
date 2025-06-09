#!/usr/bin/env python3
"""
Tests for real Playwright MCP integration.

Tests the actual browser automation capabilities using the global Playwright MCP.
"""

import pytest
from src.integrations.playwright_mcp import PlaywrightMCPClient


class TestPlaywrightMCPIntegration:
    """Test real Playwright MCP integration capabilities."""

    @pytest.fixture
    def mcp_client(self):
        """Create a real MCP client for testing."""
        return PlaywrightMCPClient()

    @pytest.mark.asyncio
    async def test_can_navigate_to_url(self, mcp_client):
        """Test that we can navigate to a real URL using Playwright MCP."""
        # This test will fail initially because we're still using mock implementation

        # Execute navigation action
        result = await mcp_client.navigate_to_url("https://example.com")

        # Verify navigation was successful
        assert result["success"] is True
        assert result["action"] == "navigate"
        assert result["url"] == "https://example.com"
        assert "timestamp" in result

        # Verify audit logs captured the navigation
        audit_logs = mcp_client.get_audit_logs()
        assert len(audit_logs) > 0
        assert audit_logs[-1]["action"] == "navigate"
        assert audit_logs[-1]["url"] == "https://example.com"

    @pytest.mark.asyncio
    async def test_captures_network_requests_during_navigation(self, mcp_client):
        """Test that network requests are captured when navigating to URLs."""
        # Clear any existing data
        mcp_client.clear_session_data()

        # Navigate to a URL
        result = await mcp_client.navigate_to_url("https://httpbin.org/get")

        # Verify navigation was successful
        assert result["success"] is True

        # Verify network requests were captured
        network_requests = mcp_client.get_network_requests()
        assert len(network_requests) > 0

        # Verify the main request was captured
        main_request = network_requests[0]
        assert main_request["url"] == "https://httpbin.org/get"
        assert main_request["method"] == "GET"
        assert "status" in main_request
        assert "timestamp" in main_request

    @pytest.mark.asyncio
    async def test_can_click_element(self, mcp_client):
        """Test that we can click on elements using Playwright MCP."""
        # Clear any existing data
        mcp_client.clear_session_data()

        # Click on an element
        result = await mcp_client.click_element("login button", "button#login")

        # Verify click was successful
        assert result["success"] is True
        assert result["action"] == "click"
        assert result["element"] == "login button"
        assert result["selector"] == "button#login"
        assert "timestamp" in result

        # Verify audit logs captured the click
        audit_logs = mcp_client.get_audit_logs()
        assert len(audit_logs) > 0
        assert audit_logs[-1]["action"] == "click"
        assert audit_logs[-1]["element"] == "login button"
        assert audit_logs[-1]["selector"] == "button#login"

    @pytest.mark.asyncio
    async def test_can_execute_complete_user_journey(self, mcp_client):
        """Test that we can execute a complete user journey using real MCP methods."""
        # Clear any existing data
        mcp_client.clear_session_data()

        # Execute a complete user journey
        result = await mcp_client.execute_user_journey(
            [
                {"action": "navigate", "url": "https://example.com/login"},
                {
                    "action": "click",
                    "element": "login button",
                    "selector": "button#login",
                },
                {"action": "navigate", "url": "https://example.com/dashboard"},
            ]
        )

        # Verify journey was successful
        assert result["success"] is True
        assert result["action"] == "user_journey"
        assert len(result["steps"]) == 3
        assert "timestamp" in result

        # Verify all steps were executed
        for i, step in enumerate(result["steps"]):
            assert step["success"] is True
            assert step["step_number"] == i + 1

        # Verify audit logs captured all actions
        audit_logs = mcp_client.get_audit_logs()
        assert len(audit_logs) >= 3  # At least 3 actions

        # Verify network requests were captured
        network_requests = mcp_client.get_network_requests()
        assert len(network_requests) >= 2  # At least 2 navigation requests
