#!/usr/bin/env python3
"""
Pattern Analysis Agent for reverse engineering workflow.

Analyzes captured data to identify patterns in API endpoints, business logic,
UI components, and data flow.
"""

import re
from typing import Dict
from urllib.parse import urlparse
from src.workflows.state_management import ReverseEngineeringState


class PatternAnalysisAgent:
    """Agent responsible for analyzing patterns in captured data."""

    def analyze_api_patterns(
        self, state: ReverseEngineeringState
    ) -> ReverseEngineeringState:
        """
        Analyze network requests to identify API endpoint patterns.

        Args:
            state: Current workflow state with network requests

        Returns:
            Updated state with inferred API endpoints
        """
        network_requests = state.get("network_requests", [])
        endpoint_patterns = {}

        for request in network_requests:
            endpoint = self._extract_endpoint_pattern(request)
            if endpoint:
                key = self._create_endpoint_key(endpoint)

                if key in endpoint_patterns:
                    # Increment call count for existing pattern
                    endpoint_patterns[key]["call_count"] += 1
                else:
                    # Add new pattern with call count
                    endpoint["call_count"] = 1
                    endpoint_patterns[key] = endpoint

        # Convert to list of unique endpoints
        endpoints = list(endpoint_patterns.values())

        # Update state with inferred endpoints
        updated_state = state.copy()
        updated_state["inferred_api_endpoints"] = endpoints

        return updated_state

    def _extract_endpoint_pattern(self, request: Dict) -> Dict:
        """
        Extract API endpoint pattern from a single network request.

        Args:
            request: Network request data

        Returns:
            Endpoint pattern dictionary
        """
        url = request.get("url", "")
        method = request.get("method", "")

        if not url or not method:
            return None

        # Parse URL to extract components
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        path = parsed.path

        # Simple pattern detection - replace numeric IDs with {id}
        path_pattern = re.sub(r"/\d+", "/{id}", path)

        # Handle query parameters
        if parsed.query:
            query_pattern = self._extract_query_pattern(parsed.query)
            path_pattern = f"{path_pattern}?{query_pattern}"

        return {
            "method": method,
            "base_url": base_url,
            "path_pattern": path_pattern,
            "original_url": url,
        }

    def _extract_query_pattern(self, query_string: str) -> str:
        """
        Extract query parameter pattern from query string.

        Args:
            query_string: URL query string (e.g., "page=1&limit=10")

        Returns:
            Query parameter pattern (e.g., "page={page}&limit={limit}")
        """
        # Split query string to preserve original parameter order
        param_pairs = query_string.split("&")

        # Convert to pattern format while preserving order
        pattern_parts = []
        for pair in param_pairs:
            if "=" in pair:
                param_name = pair.split("=")[0]
                pattern_parts.append(f"{param_name}={{{param_name}}}")

        return "&".join(pattern_parts)

    def _create_endpoint_key(self, endpoint: Dict) -> str:
        """
        Create a unique key for endpoint consolidation.

        Args:
            endpoint: Endpoint pattern dictionary

        Returns:
            Unique key string for the endpoint pattern
        """
        return f"{endpoint['method']}:{endpoint['base_url']}{endpoint['path_pattern']}"
