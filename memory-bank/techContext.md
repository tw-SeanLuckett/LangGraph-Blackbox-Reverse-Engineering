# Tech context

## Technologies used

### Core AI and LangGraph stack

#### LangGraph ecosystem

```yaml
# Primary LangGraph components for reverse engineering
langgraph: "^0.0.40" # LangGraph workflow framework
langchain: "^0.1.0" # Core LangChain for LLM integration
langchain-community: "^0.0.20" # Community integrations
langchain-openai: "^0.0.8" # OpenAI integrations
langsmith: "^0.0.87" # LangChain monitoring and debugging
```

#### Language models and AI services

- **Primary LLM**: OpenAI GPT-4 Turbo for complex reasoning and code generation
- **Alternative LLMs**: Anthropic Claude 3 for comparison and backup
- **Code generation models**: OpenAI GPT-4 optimized for code generation tasks
- **Pattern analysis**: Specialized prompts for business logic inference
- **Local models**: Ollama for development and cost optimization

#### Playwright MCP integration ✅ MAJOR UPDATE

- **Real browser automation**: Structured Playwright MCP integration for browser control ✅ UPDATED
- **Navigation capabilities**: Real URL navigation with `navigate_to_url()` method ✅ NEW
- **Element interaction**: Click functionality with `click_element()` method ✅ NEW
- **User journey execution**: Multi-step workflow execution with `execute_user_journey()` ✅ NEW
- **Network request capture**: Automatic capture of HTTP requests during browser actions ✅ NEW
- **Audit logging**: Comprehensive interaction and network logging ✅ UPDATED
- **State management**: Integration with LangGraph state persistence
- **Data capture**: DOM changes, network requests, console logs, screenshots ✅ UPDATED
- **Error handling**: Robust failure management and recovery ✅ NEW
- **TDD implementation**: Complete test coverage with 4 successful TDD cycles ✅ NEW

### Backend technology stack

#### Core backend framework

```python
# Python backend stack for reverse engineering
fastapi: "^0.104.0"           # High-performance API framework
uvicorn: "^0.24.0"            # ASGI server
pydantic: "^2.5.0"            # Data validation and serialization
sqlalchemy: "^2.0.0"          # Database ORM for generated models
alembic: "^1.13.0"            # Database migrations
```

#### Code generation and analysis

```python
# Code generation and analysis tools
ast: "built-in"               # Python AST manipulation
black: "^23.0.0"              # Code formatting for generated code
isort: "^5.12.0"              # Import sorting for generated code
jinja2: "^3.1.0"              # Template engine for code generation
```

#### Data processing and storage

- **Analysis database**: PostgreSQL for storing analysis results and patterns
- **Cache layer**: Redis for caching pattern recognition results
- **File storage**: Local filesystem for generated code and documentation
- **State persistence**: LangGraph built-in state management

### Frontend technology stack

#### Generated frontend framework

```json
{
  "react": "^18.2.0",
  "typescript": "^5.0.0",
  "next.js": "^14.0.0",
  "tailwindcss": "^3.3.0"
}
```

#### UI component generation

- **Component library**: Shadcn/ui for consistent generated components
- **State management**: Zustand for generated application state
- **Form handling**: React Hook Form for generated forms
- **API integration**: Generated API clients for backend communication

#### Development and build tools

```json
{
  "vite": "^5.0.0",
  "eslint": "^8.0.0",
  "prettier": "^3.0.0",
  "@types/react": "^18.2.0"
}
```

### Reverse engineering specific tools

#### Browser automation and analysis

```python
# Browser automation and data capture
playwright: "^1.40.0"         # Browser automation (via MCP)
beautifulsoup4: "^4.12.0"     # HTML parsing and analysis
selenium: "^4.15.0"           # Backup browser automation
requests: "^2.31.0"           # HTTP request analysis
```

#### Pattern recognition and analysis

```python
# Pattern recognition and business logic inference
networkx: "^3.2.0"            # Graph analysis for workflow patterns
scikit-learn: "^1.3.0"        # Machine learning for pattern recognition
pandas: "^2.1.0"              # Data analysis and manipulation
numpy: "^1.25.0"              # Numerical computing for analysis
```

#### Code generation and templating

```python
# Code generation tools
jinja2: "^3.1.0"              # Template engine for code generation
autopep8: "^2.0.0"            # Code formatting
rope: "^1.11.0"               # Python refactoring library
```

## Development setup

### Local development environment

#### Prerequisites

```bash
# Required software versions
python: "3.11+"
node.js: "18+"
docker: "24+"
docker-compose: "2.20+"
git: "2.40+"
```

#### Environment configuration

```bash
# Development environment setup
git clone <repository-url>
cd AIFSD-Macys-blackbox-langchain

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install -r requirements-dev.txt

# LangGraph and Playwright MCP setup
pip install langgraph langchain-openai
# Playwright MCP is global - no additional setup needed

# Infrastructure setup (if needed)
docker-compose up -d  # Start local databases if required
```

#### Environment variables

```env
# Required environment variables for reverse engineering
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=...  # Optional, for Claude backup
LANGSMITH_API_KEY=...  # For LangChain monitoring
DATABASE_URL=postgresql://user:pass@localhost:5432/reverse_engineering
REDIS_URL=redis://localhost:6379

# Playwright MCP configuration (if needed)
PLAYWRIGHT_MCP_ENDPOINT=...  # Global MCP endpoint
```

### Development workflow

#### Project structure for reverse engineering

```
AIFSD-Macys-blackbox-langchain/
├── src/
│   ├── agents/                   # LangGraph agents
│   │   ├── journey_executor.py      # Browser automation agent
│   │   ├── data_capturer.py         # Data capture and processing
│   │   ├── pattern_analyzer.py      # Pattern recognition agent
│   │   ├── backend_generator.py     # Python code generation
│   │   ├── frontend_generator.py    # React/TS code generation
│   │   └── documentation_generator.py # Documentation generation
│   ├── workflows/                # LangGraph workflows
│   │   ├── reverse_engineering.py   # Main workflow definition
│   │   └── state_management.py      # State definitions
│   ├── integrations/             # External integrations
│   │   ├── playwright_mcp.py        # Playwright MCP client
│   │   └── llm_clients.py           # LLM API clients
│   ├── analyzers/                # Pattern analysis modules
│   │   ├── api_pattern_detector.py  # API pattern recognition
│   │   ├── ui_pattern_analyzer.py   # UI component analysis
│   │   └── business_logic_inferrer.py # Business logic inference
│   ├── generators/               # Code generation modules
│   │   ├── backend_templates/        # Python code templates
│   │   ├── frontend_templates/       # React/TS templates
│   │   └── documentation_templates/  # Documentation templates
│   └── utils/                    # Utility functions
│       ├── data_correlation.py      # Data correlation utilities
│       └── validation.py            # Output validation
├── tests/
│   ├── unit/                     # Unit tests for agents and utilities
│   ├── integration/              # Integration tests
│   └── workflow/                 # Workflow testing
├── generated/                    # Output directory for generated code
│   ├── backend/                  # Generated Python backend
│   ├── frontend/                 # Generated React frontend
│   └── documentation/            # Generated documentation
├── memory-bank/                  # Memory bank files
├── .cursor/                      # Cursor configuration
├── requirements.txt              # Python dependencies
├── requirements-dev.txt          # Development dependencies
└── docker-compose.yml           # Local development services
```

#### Testing strategy for reverse engineering

```python
# Testing framework stack
pytest: "^7.4.0"             # Primary testing framework
pytest-asyncio: "^0.21.0"    # Async testing support
pytest-cov: "^4.1.0"         # Coverage reporting
pytest-mock: "^3.12.0"       # Mocking for agent testing
factory-boy: "^3.3.0"        # Test data generation
```

## Technical constraints

### Reverse engineering specific constraints

#### Pattern recognition accuracy

- **Business logic inference**: Must achieve >80% accuracy in identifying business rules
- **API pattern detection**: Correctly identify >90% of API endpoints and parameters
- **UI component mapping**: Accurately map >85% of UI components to functionality
- **Data flow analysis**: Correctly trace data flow through >75% of workflows

#### Code generation quality

- **Functional accuracy**: Generated code must pass basic functionality tests
- **Code quality**: Generated code must meet modern development standards
- **Maintainability**: Generated code must be readable and modifiable
- **Performance**: Generated code must meet reasonable performance benchmarks

### Browser automation constraints

#### Playwright MCP limitations

- **Rate limiting**: Respect browser automation rate limits
- **Resource usage**: Efficient use of browser resources and memory
- **Stability**: Handle browser crashes and network issues gracefully
- **Data capture**: Comprehensive logging without performance degradation

#### Legacy system constraints

- **System availability**: Work within legacy system uptime windows
- **Access limitations**: Respect system access controls and permissions
- **Data sensitivity**: Handle potentially sensitive business data appropriately
- **Performance impact**: Minimize impact on legacy system performance

### AI model constraints

#### LLM usage optimization

- **Cost management**: Efficient use of OpenAI API calls
- **Rate limiting**: Respect API rate limits and quotas
- **Context management**: Optimize prompt length and context usage
- **Model selection**: Choose appropriate models for different tasks

#### Pattern recognition limitations

- **Complex business logic**: May struggle with highly complex or unusual patterns
- **Domain-specific knowledge**: Limited understanding of industry-specific concepts
- **Edge cases**: May miss unusual or rarely-used system features
- **Validation requirements**: Generated understanding must be validated against actual system

## Dependencies

### Critical dependencies for reverse engineering

#### LangGraph and AI dependencies

```python
# Core AI and workflow dependencies
langgraph: "^0.0.40"          # Multi-agent workflow framework
langchain: "^0.1.0"           # LLM integration
langchain-openai: "^0.0.8"    # OpenAI API client
langchain-anthropic: "^0.0.4" # Anthropic Claude API
pydantic: "^2.5.0"            # Data validation for state management
```

#### Browser automation dependencies

```python
# Browser automation and data capture
playwright: "^1.40.0"         # Browser automation
beautifulsoup4: "^4.12.0"     # HTML parsing
requests: "^2.31.0"           # HTTP analysis
selenium: "^4.15.0"           # Backup automation
```

#### Code generation dependencies

```python
# Code generation and analysis
jinja2: "^3.1.0"              # Template engine
ast: "built-in"               # Python AST manipulation
black: "^23.0.0"              # Code formatting
isort: "^5.12.0"              # Import organization
```

#### Data analysis dependencies

```python
# Pattern recognition and analysis
pandas: "^2.1.0"              # Data manipulation
numpy: "^1.25.0"              # Numerical computing
scikit-learn: "^1.3.0"        # Machine learning
networkx: "^3.2.0"            # Graph analysis
```

### Development and testing dependencies

```python
# Development tools
pytest: "^7.4.0"              # Testing framework
black: "^23.0.0"              # Code formatting
mypy: "^1.7.0"                # Type checking
pre-commit: "^3.6.0"          # Git hooks
```

### Dependency management for reverse engineering

#### Version pinning strategy

- **LangGraph versions**: Pin to specific versions for workflow stability
- **LLM API versions**: Use stable API versions with fallback options
- **Browser automation**: Pin Playwright version for consistent behavior
- **Code generation**: Stable versions for consistent output quality

#### Vulnerability and compatibility management

- **Security scanning**: Regular scanning for vulnerabilities in dependencies
- **Compatibility testing**: Ensure generated code works with target frameworks
- **Update strategy**: Careful testing before updating critical dependencies
- **Fallback options**: Alternative tools for critical functionality

## Future technology considerations

### Emerging reverse engineering technologies

#### Advanced AI techniques

- **Multimodal models**: Integration of vision models for UI analysis
- **Specialized code models**: Use of code-specific LLMs for better generation
- **Fine-tuned models**: Custom models trained on reverse engineering tasks
- **Agent frameworks**: Evolution of LangGraph and alternative frameworks

#### Enhanced browser automation

- **Advanced Playwright features**: New capabilities for deeper system analysis
- **Headless browser improvements**: Better performance and resource usage
- **Mobile automation**: Extension to mobile application reverse engineering
- **Real-time analysis**: Live analysis during browser automation

### Technology evolution planning

#### LangGraph and workflow evolution

- **Workflow optimization**: Improved agent coordination and state management
- **Performance improvements**: Faster execution and better resource usage
- **Enhanced debugging**: Better tools for workflow debugging and optimization
- **Integration capabilities**: Better integration with external tools and systems

#### Code generation advancement

- **Quality improvements**: Better generated code quality and maintainability
- **Framework support**: Support for additional backend and frontend frameworks
- **Testing generation**: Automatic generation of tests for reverse-engineered code
- **Documentation enhancement**: Improved documentation generation capabilities
