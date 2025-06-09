#!/usr/bin/env python3
"""
Tests for Pattern Analysis Agent

Following TDD principles - tests written first, then implementation.
"""

from src.agents.pattern_analyzer import PatternAnalysisAgent
from src.workflows.state_management import create_initial_state


class TestPatternAnalysisAgent:
    """Test suite for Pattern Analysis Agent functionality."""

    def test_detects_api_endpoints_from_network_requests(self):
        """Detects REST API endpoints from captured network requests."""
        # Arrange
        agent = PatternAnalysisAgent()

        # Sample network requests captured during workflow
        network_requests = [
            {
                "url": "https://api.example.com/users/123",
                "method": "GET",
                "status": 200,
                "response_time": 150,
                "headers": {"Content-Type": "application/json"},
                "response_body": '{"id": 123, "name": "John Doe", "email": "john@example.com"}',
            },
            {
                "url": "https://api.example.com/users",
                "method": "POST",
                "status": 201,
                "response_time": 200,
                "headers": {"Content-Type": "application/json"},
                "request_body": '{"name": "Jane Smith", "email": "jane@example.com"}',
                "response_body": '{"id": 124, "name": "Jane Smith", "email": "jane@example.com"}',
            },
        ]

        state = create_initial_state(
            workflow_description="User management workflow", domain="user_management"
        )
        state["network_requests"] = network_requests

        # Act
        result = agent.analyze_api_patterns(state)

        # Assert
        assert "inferred_api_endpoints" in result
        endpoints = result["inferred_api_endpoints"]

        # Should detect 2 distinct endpoints
        assert len(endpoints) == 2

        # Should identify GET /users/{id} endpoint
        get_endpoint = next((ep for ep in endpoints if ep["method"] == "GET"), None)
        assert get_endpoint is not None
        assert get_endpoint["path_pattern"] == "/users/{id}"
        assert get_endpoint["base_url"] == "https://api.example.com"

        # Should identify POST /users endpoint
        post_endpoint = next((ep for ep in endpoints if ep["method"] == "POST"), None)
        assert post_endpoint is not None
        assert post_endpoint["path_pattern"] == "/users"
        assert post_endpoint["base_url"] == "https://api.example.com"

    def test_consolidates_duplicate_endpoints(self):
        """Consolidates duplicate endpoint calls into single endpoint patterns."""
        # Arrange
        agent = PatternAnalysisAgent()

        # Multiple requests to same endpoints with different IDs/data
        network_requests = [
            {
                "url": "https://api.example.com/users/123",
                "method": "GET",
                "status": 200,
                "response_time": 150,
                "headers": {"Content-Type": "application/json"},
                "response_body": '{"id": 123, "name": "John Doe"}',
            },
            {
                "url": "https://api.example.com/users/456",
                "method": "GET",
                "status": 200,
                "response_time": 180,
                "headers": {"Content-Type": "application/json"},
                "response_body": '{"id": 456, "name": "Jane Smith"}',
            },
            {
                "url": "https://api.example.com/users/789",
                "method": "GET",
                "status": 200,
                "response_time": 120,
                "headers": {"Content-Type": "application/json"},
                "response_body": '{"id": 789, "name": "Bob Wilson"}',
            },
            {
                "url": "https://api.example.com/orders/101",
                "method": "GET",
                "status": 200,
                "response_time": 200,
                "headers": {"Content-Type": "application/json"},
                "response_body": '{"id": 101, "total": 99.99}',
            },
            {
                "url": "https://api.example.com/orders/202",
                "method": "GET",
                "status": 200,
                "response_time": 190,
                "headers": {"Content-Type": "application/json"},
                "response_body": '{"id": 202, "total": 149.99}',
            },
        ]

        state = create_initial_state(
            workflow_description="Multiple resource access workflow",
            domain="multi_resource",
        )
        state["network_requests"] = network_requests

        # Act
        result = agent.analyze_api_patterns(state)

        # Assert
        assert "inferred_api_endpoints" in result
        endpoints = result["inferred_api_endpoints"]

        # Should consolidate into 2 unique endpoint patterns, not 5 separate ones
        assert len(endpoints) == 2

        # Should have one GET /users/{id} endpoint (consolidating 3 calls)
        users_endpoint = next(
            (ep for ep in endpoints if ep["path_pattern"] == "/users/{id}"), None
        )
        assert users_endpoint is not None
        assert users_endpoint["method"] == "GET"
        assert users_endpoint["base_url"] == "https://api.example.com"
        assert users_endpoint["call_count"] == 3

        # Should have one GET /orders/{id} endpoint (consolidating 2 calls)
        orders_endpoint = next(
            (ep for ep in endpoints if ep["path_pattern"] == "/orders/{id}"), None
        )
        assert orders_endpoint is not None
        assert orders_endpoint["method"] == "GET"
        assert orders_endpoint["base_url"] == "https://api.example.com"
        assert orders_endpoint["call_count"] == 2

    def test_handles_basic_query_parameters(self):
        """Handles basic query parameters in URL patterns."""
        # Arrange
        agent = PatternAnalysisAgent()

        # Network requests with query parameters
        network_requests = [
            {
                "url": "https://api.example.com/users?page=1&limit=10",
                "method": "GET",
                "status": 200,
                "response_time": 150,
                "headers": {"Content-Type": "application/json"},
                "response_body": '{"users": [], "total": 100, "page": 1}',
            },
            {
                "url": "https://api.example.com/users?page=2&limit=10",
                "method": "GET",
                "status": 200,
                "response_time": 160,
                "headers": {"Content-Type": "application/json"},
                "response_body": '{"users": [], "total": 100, "page": 2}',
            },
        ]

        state = create_initial_state(
            workflow_description="Paginated user listing workflow", domain="pagination"
        )
        state["network_requests"] = network_requests

        # Act
        result = agent.analyze_api_patterns(state)

        # Assert
        assert "inferred_api_endpoints" in result
        endpoints = result["inferred_api_endpoints"]

        # Should consolidate into 1 endpoint pattern
        assert len(endpoints) == 1

        # Should identify GET /users with query parameter pattern
        endpoint = endpoints[0]
        assert endpoint["method"] == "GET"
        assert endpoint["base_url"] == "https://api.example.com"
        assert endpoint["path_pattern"] == "/users?page={page}&limit={limit}"
        assert endpoint["call_count"] == 2
