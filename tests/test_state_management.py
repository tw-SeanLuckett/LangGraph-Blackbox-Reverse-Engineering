"""
Test state management for reverse engineering workflow

Following TDD principles - these tests define the expected behavior
before implementation.
"""

from datetime import datetime

from src.workflows.state_management import create_initial_state


class TestReverseEngineeringState:
    """Test the core state management for reverse engineering workflow"""

    def test_creates_initial_state_with_required_fields(self):
        """Creates initial state with all required fields populated"""
        workflow_description = "Navigate to login page and enter credentials"
        domain = "accounts_payable"

        state = create_initial_state(workflow_description, domain)

        # Test required fields are present
        assert state["workflow_description"] == workflow_description
        assert state["current_domain"] == domain
        assert state["iteration_count"] == 0

        # Test data collection fields are initialized as empty lists
        assert state["playwright_logs"] == []
        assert state["network_requests"] == []
        assert state["dom_changes"] == []
        assert state["user_interactions"] == []

        # Test analysis fields are initialized
        assert state["inferred_api_endpoints"] == []
        assert state["database_schema"] == {}
        assert state["business_logic_patterns"] == []
        assert state["ui_component_patterns"] == []

        # Test generation fields are initialized
        assert state["backend_code"] == {}
        assert state["frontend_code"] == {}
        assert state["documentation"] == {}

        # Test workflow control fields
        assert state["analysis_complete"] is False
        assert state["generation_targets"] == []
        assert state["next_actions"] == []

    def test_state_can_be_updated_with_playwright_data(self):
        """State can be updated with captured Playwright interaction data"""
        state = create_initial_state("test workflow", "test_domain")

        # Sample Playwright data
        playwright_log = {
            "action": "click",
            "selector": "#login-button",
            "timestamp": datetime.now().isoformat(),
            "success": True,
        }

        network_request = {
            "url": "https://example.com/api/login",
            "method": "POST",
            "status": 200,
            "response_time": 150,
        }

        # Update state
        state["playwright_logs"].append(playwright_log)
        state["network_requests"].append(network_request)
        state["iteration_count"] += 1

        # Verify updates
        assert len(state["playwright_logs"]) == 1
        assert len(state["network_requests"]) == 1
        assert state["iteration_count"] == 1
        assert state["playwright_logs"][0]["action"] == "click"
        assert state["network_requests"][0]["method"] == "POST"

    def test_state_supports_analysis_results(self):
        """State can store pattern analysis results"""
        state = create_initial_state("test workflow", "test_domain")

        # Sample analysis results
        api_endpoint = {
            "url": "/api/users/login",
            "method": "POST",
            "parameters": ["username", "password"],
            "response_schema": {"token": "string", "user_id": "integer"},
        }

        business_logic = {
            "pattern": "authentication_flow",
            "description": "User login with credential validation",
            "steps": ["validate_input", "check_credentials", "generate_token"],
        }

        # Update state with analysis
        state["inferred_api_endpoints"].append(api_endpoint)
        state["business_logic_patterns"].append(business_logic)

        # Verify analysis storage
        assert len(state["inferred_api_endpoints"]) == 1
        assert len(state["business_logic_patterns"]) == 1
        assert state["inferred_api_endpoints"][0]["method"] == "POST"
        assert state["business_logic_patterns"][0]["pattern"] == "authentication_flow"

    def test_state_supports_code_generation_results(self):
        """State can store generated code and documentation"""
        state = create_initial_state("test workflow", "test_domain")

        # Sample generated code
        backend_code = {
            "models.py": "class User(BaseModel):\n    username: str\n    password: str",
            "auth.py": "def authenticate_user(username, password):\n    # Authentication logic",
        }

        frontend_code = {
            "LoginForm.tsx": "export const LoginForm = () => {\n  // Login form component\n}",
            "types.ts": "export interface User {\n  username: string;\n  password: string;\n}",
        }

        documentation = {
            "api_docs": "# Authentication API\n\n## POST /api/users/login",
            "user_guide": "# User Guide\n\n## How to login",
        }

        # Update state with generated content
        state["backend_code"].update(backend_code)
        state["frontend_code"].update(frontend_code)
        state["documentation"].update(documentation)

        # Verify code generation storage
        assert "models.py" in state["backend_code"]
        assert "LoginForm.tsx" in state["frontend_code"]
        assert "api_docs" in state["documentation"]
        assert "class User" in state["backend_code"]["models.py"]
