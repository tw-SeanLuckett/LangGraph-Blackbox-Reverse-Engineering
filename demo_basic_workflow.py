#!/usr/bin/env python3
"""
Demo script for basic LangGraph reverse engineering workflow

This demonstrates the foundation working end-to-end with a simple workflow.
"""

import asyncio

from src.workflows.reverse_engineering import ReverseEngineeringWorkflow
from src.workflows.state_management import create_initial_state


async def demo_basic_workflow():
    """Demonstrate the basic reverse engineering workflow."""

    print("🚀 AIFSD Legacy System Reverse Engineering - Basic Workflow Demo")
    print("=" * 70)

    # Create initial state
    print("\n📋 Creating initial workflow state...")
    initial_state = create_initial_state(
        workflow_description="Navigate to login page and click login button",
        domain="accounts_payable",
    )

    print(f"   Workflow: {initial_state['workflow_description']}")
    print(f"   Domain: {initial_state['current_domain']}")
    print(f"   Initial iteration count: {initial_state['iteration_count']}")

    # Create workflow
    print("\n🔧 Initializing LangGraph workflow...")
    workflow = ReverseEngineeringWorkflow()
    print("   ✅ Journey Executor Agent ready")
    print("   ✅ Data Capture Agent ready")
    print("   ✅ LangGraph workflow compiled")

    # Execute individual agents for demonstration
    print("\n🎯 Executing Journey Executor Agent...")
    after_journey = await workflow.execute_journey(initial_state)

    print(
        f"   ✅ Browser action executed: {after_journey['user_interactions'][0]['result']['action']}"
    )
    print(f"   ✅ Iteration count: {after_journey['iteration_count']}")
    print(
        f"   ✅ User interactions captured: {len(after_journey['user_interactions'])}"
    )
    print(f"   ✅ Playwright logs captured: {len(after_journey['playwright_logs'])}")
    print(f"   ✅ Network requests captured: {len(after_journey['network_requests'])}")

    print("\n📊 Executing Data Capture Agent...")
    after_capture = await workflow.capture_data(after_journey)

    print(
        f"   ✅ Interactions processed: {len(after_capture['processed_interactions'])}"
    )
    print(
        f"   ✅ Network requests correlated: {len(after_capture['processed_interactions'][0]['correlated_requests'])}"
    )

    # Execute complete workflow
    print("\n🔄 Executing complete LangGraph workflow...")
    final_state = await workflow.execute(initial_state)

    print("   ✅ Workflow completed successfully")
    print(f"   ✅ Final iteration count: {final_state['iteration_count']}")
    print(f"   ✅ Total interactions: {len(final_state['user_interactions'])}")
    print(
        f"   ✅ Total processed interactions: {len(final_state.get('processed_interactions', []))}"
    )

    # Show captured data summary
    print("\n📈 Captured Data Summary:")
    print(f"   • Playwright logs: {len(final_state['playwright_logs'])}")
    print(f"   • Network requests: {len(final_state['network_requests'])}")
    print(f"   • User interactions: {len(final_state['user_interactions'])}")
    print(
        f"   • Processed interactions: {len(final_state.get('processed_interactions', []))}"
    )

    # Show sample captured data
    if final_state["network_requests"]:
        print("\n🌐 Sample Network Request Captured:")
        sample_request = final_state["network_requests"][0]
        print(f"   URL: {sample_request['url']}")
        print(f"   Method: {sample_request['method']}")
        print(f"   Status: {sample_request['status']}")
        print(f"   Response Time: {sample_request['response_time']}ms")

    if final_state.get("processed_interactions"):
        print("\n🔗 Sample Data Correlation:")
        sample_processed = final_state["processed_interactions"][0]
        print(f"   Original action: {sample_processed['original_log']['action']}")
        print(f"   Correlated requests: {len(sample_processed['correlated_requests'])}")

    print("\n✨ Foundation Demo Complete!")
    print("   The basic LangGraph workflow is working correctly.")
    print("   Ready for next development phase: Pattern Analysis Agent")

    return final_state


if __name__ == "__main__":
    asyncio.run(demo_basic_workflow())
