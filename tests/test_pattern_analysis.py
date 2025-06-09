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

    def test_handles_mixed_path_and_query_parameters(self):
        """Handles URLs with both path parameters and query parameters."""
        # Arrange
        agent = PatternAnalysisAgent()

        # Network requests with mixed path and query parameters
        network_requests = [
            {
                "url": "https://api.example.com/users/123?include=profile",
                "method": "GET",
                "status": 200,
                "response_time": 150,
                "headers": {"Content-Type": "application/json"},
                "response_body": '{"id": 123, "name": "John", "profile": {...}}',
            },
            {
                "url": "https://api.example.com/users/456?include=profile",
                "method": "GET",
                "status": 200,
                "response_time": 160,
                "headers": {"Content-Type": "application/json"},
                "response_body": '{"id": 456, "name": "Jane", "profile": {...}}',
            },
            {
                "url": "https://api.example.com/orders/789?expand=items&format=json",
                "method": "GET",
                "status": 200,
                "response_time": 180,
                "headers": {"Content-Type": "application/json"},
                "response_body": '{"id": 789, "items": [...], "total": 99.99}',
            },
            {
                "url": "https://api.example.com/orders/101?expand=items&format=json",
                "method": "GET",
                "status": 200,
                "response_time": 170,
                "headers": {"Content-Type": "application/json"},
                "response_body": '{"id": 101, "items": [...], "total": 149.99}',
            },
        ]

        state = create_initial_state(
            workflow_description="Mixed path and query parameter workflow",
            domain="mixed_params",
        )
        state["network_requests"] = network_requests

        # Act
        result = agent.analyze_api_patterns(state)

        # Assert
        assert "inferred_api_endpoints" in result
        endpoints = result["inferred_api_endpoints"]

        # Should consolidate into 2 endpoint patterns
        assert len(endpoints) == 2

        # Should identify GET /users/{id}?include={include} endpoint
        users_endpoint = next(
            (ep for ep in endpoints if "/users/{id}" in ep["path_pattern"]), None
        )
        assert users_endpoint is not None
        assert users_endpoint["method"] == "GET"
        assert users_endpoint["base_url"] == "https://api.example.com"
        assert users_endpoint["path_pattern"] == "/users/{id}?include={include}"
        assert users_endpoint["call_count"] == 2

        # Should identify GET /orders/{id}?expand={expand}&format={format} endpoint
        orders_endpoint = next(
            (ep for ep in endpoints if "/orders/{id}" in ep["path_pattern"]), None
        )
        assert orders_endpoint is not None
        assert orders_endpoint["method"] == "GET"
        assert orders_endpoint["base_url"] == "https://api.example.com"
        assert (
            orders_endpoint["path_pattern"]
            == "/orders/{id}?expand={expand}&format={format}"
        )
        assert orders_endpoint["call_count"] == 2

    def test_handles_different_http_methods_on_same_path(self):
        """Handles different HTTP methods on the same path as separate endpoints."""
        # Arrange
        agent = PatternAnalysisAgent()

        # Network requests with same path but different HTTP methods
        network_requests = [
            {
                "url": "https://api.example.com/users",
                "method": "GET",
                "status": 200,
                "response_time": 150,
                "headers": {"Content-Type": "application/json"},
                "response_body": '{"users": [{"id": 1, "name": "John"}]}',
            },
            {
                "url": "https://api.example.com/users",
                "method": "POST",
                "status": 201,
                "response_time": 200,
                "headers": {"Content-Type": "application/json"},
                "request_body": '{"name": "Jane", "email": "jane@example.com"}',
                "response_body": '{"id": 2, "name": "Jane", "email": "jane@example.com"}',
            },
            {
                "url": "https://api.example.com/users",
                "method": "GET",
                "status": 200,
                "response_time": 140,
                "headers": {"Content-Type": "application/json"},
                "response_body": '{"users": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]}',
            },
            {
                "url": "https://api.example.com/orders/123",
                "method": "PUT",
                "status": 200,
                "response_time": 180,
                "headers": {"Content-Type": "application/json"},
                "request_body": '{"status": "shipped"}',
                "response_body": '{"id": 123, "status": "shipped"}',
            },
            {
                "url": "https://api.example.com/orders/456",
                "method": "DELETE",
                "status": 204,
                "response_time": 120,
                "headers": {},
                "response_body": "",
            },
        ]

        state = create_initial_state(
            workflow_description="HTTP method variations workflow",
            domain="http_methods",
        )
        state["network_requests"] = network_requests

        # Act
        result = agent.analyze_api_patterns(state)

        # Assert
        assert "inferred_api_endpoints" in result
        endpoints = result["inferred_api_endpoints"]

        # Should identify 4 distinct endpoints (GET /users, POST /users, PUT /orders/{id}, DELETE /orders/{id})
        assert len(endpoints) == 4

        # Should identify GET /users endpoint (called twice)
        get_users_endpoint = next(
            (
                ep
                for ep in endpoints
                if ep["method"] == "GET" and ep["path_pattern"] == "/users"
            ),
            None,
        )
        assert get_users_endpoint is not None
        assert get_users_endpoint["base_url"] == "https://api.example.com"
        assert get_users_endpoint["call_count"] == 2

        # Should identify POST /users endpoint (called once)
        post_users_endpoint = next(
            (
                ep
                for ep in endpoints
                if ep["method"] == "POST" and ep["path_pattern"] == "/users"
            ),
            None,
        )
        assert post_users_endpoint is not None
        assert post_users_endpoint["base_url"] == "https://api.example.com"
        assert post_users_endpoint["call_count"] == 1

        # Should identify PUT /orders/{id} endpoint
        put_orders_endpoint = next(
            (
                ep
                for ep in endpoints
                if ep["method"] == "PUT" and ep["path_pattern"] == "/orders/{id}"
            ),
            None,
        )
        assert put_orders_endpoint is not None
        assert put_orders_endpoint["base_url"] == "https://api.example.com"
        assert put_orders_endpoint["call_count"] == 1

        # Should identify DELETE /orders/{id} endpoint
        delete_orders_endpoint = next(
            (
                ep
                for ep in endpoints
                if ep["method"] == "DELETE" and ep["path_pattern"] == "/orders/{id}"
            ),
            None,
        )
        assert delete_orders_endpoint is not None
        assert delete_orders_endpoint["base_url"] == "https://api.example.com"
        assert delete_orders_endpoint["call_count"] == 1

    def test_handles_invalid_and_malformed_urls_gracefully(self):
        """Handles invalid and malformed URLs without crashing."""
        # Arrange
        agent = PatternAnalysisAgent()

        # Network requests with various invalid/malformed URLs
        network_requests = [
            # Valid request for comparison
            {
                "url": "https://api.example.com/users/123",
                "method": "GET",
                "status": 200,
                "response_time": 150,
                "headers": {"Content-Type": "application/json"},
                "response_body": '{"id": 123, "name": "John"}',
            },
            # Missing URL
            {
                "url": "",
                "method": "GET",
                "status": 400,
                "response_time": 50,
                "headers": {},
                "response_body": "",
            },
            # Missing method
            {
                "url": "https://api.example.com/orders/456",
                "method": "",
                "status": 200,
                "response_time": 160,
                "headers": {"Content-Type": "application/json"},
                "response_body": '{"id": 456, "total": 99.99}',
            },
            # Invalid URL format (no scheme)
            {
                "url": "api.example.com/products/789",
                "method": "GET",
                "status": 200,
                "response_time": 140,
                "headers": {"Content-Type": "application/json"},
                "response_body": '{"id": 789, "name": "Product"}',
            },
            # URL with special characters that might break parsing
            {
                "url": "https://api.example.com/search?q=hello%20world&filter=<script>alert('xss')</script>",
                "method": "GET",
                "status": 200,
                "response_time": 180,
                "headers": {"Content-Type": "application/json"},
                "response_body": '{"results": []}',
            },
            # None values
            {
                "url": None,
                "method": None,
                "status": 500,
                "response_time": 0,
                "headers": {},
                "response_body": "",
            },
        ]

        state = create_initial_state(
            workflow_description="Invalid URL handling workflow",
            domain="error_handling",
        )
        state["network_requests"] = network_requests

        # Act - should not crash
        result = agent.analyze_api_patterns(state)

        # Assert
        assert "inferred_api_endpoints" in result
        endpoints = result["inferred_api_endpoints"]

        # Should only extract valid endpoints and skip invalid ones
        # Valid endpoints: /users/{id} and /search?q={q}&filter={filter}
        assert len(endpoints) >= 1  # At least the valid /users/{id} endpoint

        # Should identify the valid GET /users/{id} endpoint
        users_endpoint = next(
            (ep for ep in endpoints if ep.get("path_pattern") == "/users/{id}"), None
        )
        assert users_endpoint is not None
        assert users_endpoint["method"] == "GET"
        assert users_endpoint["base_url"] == "https://api.example.com"
        assert users_endpoint["call_count"] == 1

        # Should handle the search endpoint with special characters
        search_endpoint = next(
            (ep for ep in endpoints if "search" in ep.get("path_pattern", "")), None
        )
        if search_endpoint:  # May or may not be present depending on URL parsing
            assert search_endpoint["method"] == "GET"
            assert "search" in search_endpoint["path_pattern"]

    def test_analyzes_request_response_body_patterns(self):
        """Analyzes patterns in request and response bodies."""
        # Arrange
        agent = PatternAnalysisAgent()

        # Network requests with request/response bodies to analyze
        network_requests = [
            {
                "url": "https://api.example.com/users",
                "method": "POST",
                "status": 201,
                "response_time": 200,
                "headers": {"Content-Type": "application/json"},
                "request_body": '{"name": "John Doe", "email": "john@example.com", "age": 30}',
                "response_body": '{"id": 123, "name": "John Doe", "email": "john@example.com", "age": 30, "created_at": "2024-01-15T10:30:00Z"}',
            },
            {
                "url": "https://api.example.com/users",
                "method": "POST",
                "status": 201,
                "response_time": 180,
                "headers": {"Content-Type": "application/json"},
                "request_body": '{"name": "Jane Smith", "email": "jane@example.com", "age": 25}',
                "response_body": '{"id": 124, "name": "Jane Smith", "email": "jane@example.com", "age": 25, "created_at": "2024-01-15T10:35:00Z"}',
            },
            {
                "url": "https://api.example.com/orders/123",
                "method": "PUT",
                "status": 200,
                "response_time": 150,
                "headers": {"Content-Type": "application/json"},
                "request_body": '{"status": "shipped", "tracking_number": "ABC123"}',
                "response_body": '{"id": 123, "status": "shipped", "tracking_number": "ABC123", "updated_at": "2024-01-15T11:00:00Z"}',
            },
        ]

        state = create_initial_state(
            workflow_description="Request/response body analysis workflow",
            domain="body_analysis",
        )
        state["network_requests"] = network_requests

        # Act
        result = agent.analyze_api_patterns(state)

        # Assert
        assert "inferred_api_endpoints" in result
        endpoints = result["inferred_api_endpoints"]

        # Should identify 2 endpoints
        assert len(endpoints) == 2

        # Should identify POST /users endpoint with body patterns
        post_users_endpoint = next(
            (
                ep
                for ep in endpoints
                if ep["method"] == "POST" and ep["path_pattern"] == "/users"
            ),
            None,
        )
        assert post_users_endpoint is not None
        assert post_users_endpoint["call_count"] == 2

        # Should have request body pattern analysis
        if "request_body_pattern" in post_users_endpoint:
            request_pattern = post_users_endpoint["request_body_pattern"]
            assert "name" in request_pattern
            assert "email" in request_pattern
            assert "age" in request_pattern

        # Should have response body pattern analysis
        if "response_body_pattern" in post_users_endpoint:
            response_pattern = post_users_endpoint["response_body_pattern"]
            assert "id" in response_pattern
            assert "name" in response_pattern
            assert "email" in response_pattern
            assert "created_at" in response_pattern

        # Should identify PUT /orders/{id} endpoint
        put_orders_endpoint = next(
            (
                ep
                for ep in endpoints
                if ep["method"] == "PUT" and ep["path_pattern"] == "/orders/{id}"
            ),
            None,
        )
        assert put_orders_endpoint is not None
        assert put_orders_endpoint["call_count"] == 1
