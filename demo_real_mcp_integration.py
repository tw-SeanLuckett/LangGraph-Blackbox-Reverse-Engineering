#!/usr/bin/env python3
"""
Demo script for real Playwright MCP integration.

Demonstrates the new browser automation capabilities using actual Playwright MCP methods
instead of mock implementations.
"""

import asyncio
import logging
from src.integrations.playwright_mcp import PlaywrightMCPClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Demonstrate real Playwright MCP integration capabilities."""

    print("🚀 AIFSD Real Playwright MCP Integration Demo")
    print("=" * 60)

    # Initialize the MCP client
    print("\n📋 Initializing Playwright MCP Client...")
    mcp_client = PlaywrightMCPClient()
    print("   ✅ MCP Client ready")

    # Demo 1: Basic Navigation
    print("\n🌐 Demo 1: Basic Navigation")
    print("-" * 30)

    result = await mcp_client.navigate_to_url("https://example.com")
    print(f"   Navigation result: {result['success']}")
    print(f"   URL: {result['url']}")
    print(f"   Timestamp: {result['timestamp']}")

    # Check captured network requests
    network_requests = mcp_client.get_network_requests()
    print(f"   Network requests captured: {len(network_requests)}")
    if network_requests:
        print(
            f"   First request: {network_requests[0]['method']} {network_requests[0]['url']}"
        )

    # Demo 2: Element Interaction
    print("\n🖱️  Demo 2: Element Interaction")
    print("-" * 30)

    result = await mcp_client.click_element("login button", "button#login")
    print(f"   Click result: {result['success']}")
    print(f"   Element: {result['element']}")
    print(f"   Selector: {result['selector']}")

    # Demo 3: Complete User Journey
    print("\n🎯 Demo 3: Complete User Journey")
    print("-" * 30)

    # Clear previous data for clean demo
    mcp_client.clear_session_data()

    journey_steps = [
        {"action": "navigate", "url": "https://example.com/login"},
        {"action": "click", "element": "username field", "selector": "input#username"},
        {"action": "click", "element": "password field", "selector": "input#password"},
        {"action": "click", "element": "login button", "selector": "button#login"},
        {"action": "navigate", "url": "https://example.com/dashboard"},
    ]

    result = await mcp_client.execute_user_journey(journey_steps)
    print(f"   Journey result: {result['success']}")
    print(f"   Total steps: {result['total_steps']}")
    print(f"   Completed steps: {result['completed_steps']}")

    # Show step details
    for i, step in enumerate(result["steps"], 1):
        action_type = step.get("action", "unknown")
        success = step.get("success", False)
        status = "✅" if success else "❌"
        print(f"   Step {i}: {action_type} {status}")

    # Demo 4: Audit Logs and Data Capture
    print("\n📊 Demo 4: Captured Data Summary")
    print("-" * 30)

    audit_logs = mcp_client.get_audit_logs()
    network_requests = mcp_client.get_network_requests()

    print(f"   Total audit logs: {len(audit_logs)}")
    print(f"   Total network requests: {len(network_requests)}")

    # Show recent audit logs
    print("\n   Recent audit logs:")
    for log in audit_logs[-3:]:  # Show last 3 logs
        action = log.get("action", "unknown")
        success = log.get("success", False)
        status = "✅" if success else "❌"
        timestamp = log.get("timestamp", "")[:19]  # Truncate timestamp
        print(f"     {timestamp} - {action} {status}")

    # Show network requests
    print("\n   Network requests:")
    for req in network_requests[-3:]:  # Show last 3 requests
        method = req.get("method", "GET")
        url = req.get("url", "")
        status = req.get("status", 200)
        print(f"     {method} {url} ({status})")

    print("\n✨ Real Playwright MCP Integration Demo Complete!")
    print("   The system now has structured browser automation capabilities")
    print("   ready for integration with the Pattern Analysis Agent.")


if __name__ == "__main__":
    asyncio.run(main())
