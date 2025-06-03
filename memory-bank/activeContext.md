# Active context

## Current work focus

### Primary objective

**Legacy system reverse engineering using AI agents - Ready for LangGraph development**

We have clarified the actual project scope: using LangGraph AI agents with Playwright MCP to reverse engineer legacy web applications through blackbox analysis. The project focuses on recreating system functionality in modern technology stacks without access to source code.

### Immediate priorities

#### 1. Project scope clarification ✅ COMPLETE

- ✅ Identified actual use case: legacy system reverse engineering
- ✅ Confirmed technology approach: LangGraph + Playwright MCP
- ✅ Defined target outputs: Python backend + React/TypeScript frontend
- ✅ Identified business domains: AP, consignment, returns, parts/repair

#### 2. LangGraph architecture design

- 🔄 **Current priority**: LangGraph multi-agent workflow design
- ⏳ **Next**: Playwright MCP integration with LangGraph state management
- ⏳ **Pending**: Agent coordination and state passing patterns

#### 3. Development environment setup

- ⏳ **Pending**: LangGraph development environment
- ⏳ **Pending**: Playwright MCP integration testing
- ⏳ **Pending**: Basic agent framework implementation

## Recent changes

### Major scope pivot

- **Project understanding corrected**: From retail AI applications to legacy system reverse engineering
- **Technology stack updated**: LangChain → LangGraph for multi-agent workflows
- **Target system identified**: Complex web application with 4 business domains
- **Output clarified**: Modern code recreation + comprehensive documentation

### Key decisions made

1. **LangGraph over LangChain**: Better suited for complex multi-agent coordination
2. **Playwright MCP integration**: Use existing global MCP, no extensions needed
3. **Blackbox methodology**: Pure behavioral analysis without source code access
4. **Modern tech targets**: Python backend, React/TypeScript frontend

## Target legacy system profile

### Business domains

- **Accounts Payable**: Queries and dispute management workflows
- **Consignment**: Shipping, planning, and discrepancy management
- **Return & Salvage**: Revenue management processes
- **Parts & Repair**: Ordering and repair scheduling workflows

### System characteristics

- **Type**: Complex web application
- **Complexity**: Intricate business workflows and logic
- **Access**: UI confirmed, database access probable but uncertain
- **Technology**: Unknown legacy stack

### Reverse engineering goals

- **API documentation**: Complete REST endpoint specifications
- **Database schema**: Full data model recreation
- **Business logic**: Documented rules and workflow patterns
- **Code generation**: Functional Python backend + React frontend
- **Documentation**: Comprehensive system architecture and user guides

## Next steps

### Immediate (Week 1)

1. **LangGraph workflow setup**

   - Design multi-agent workflow architecture
   - Implement basic LangGraph state management
   - Create agent coordination patterns

2. **Playwright MCP integration**

   - Connect LangGraph state with Playwright MCP
   - Test browser automation with state persistence
   - Implement audit log capture and processing

3. **Basic agent development**
   - Journey Executor Agent: Convert workflow descriptions to browser actions
   - Data Capture Agent: Process Playwright logs and network data
   - Pattern Analysis Agent: Basic API and data flow detection

### Short-term (Weeks 2-3)

1. **Core agent implementation**

   - Complete journey execution with complex workflows
   - Advanced pattern recognition from captured data
   - Basic code generation for simple endpoints

2. **Agent coordination**

   - Implement LangGraph conditional workflows
   - Add feedback loops between agents
   - State management for iterative analysis

3. **Testing framework**
   - Simple workflow testing with known applications
   - Validation of pattern recognition accuracy
   - Code generation quality assessment

### Medium-term (Weeks 4-8)

1. **Advanced code generation**

   - Python backend code generation (FastAPI/Django)
   - React/TypeScript frontend generation
   - Database schema recreation

2. **Business domain focus**
   - Domain-specific workflow analysis
   - Complex business logic inference
   - Integration between generated components

## Active decisions and considerations

### Technical architecture decisions

#### LangGraph workflow design

```python
# Proposed agent workflow
class ReverseEngineeringWorkflow:
    agents = [
        "journey_executor",    # Browser automation
        "data_capturer",      # Log analysis
        "pattern_analyzer",   # Business logic inference
        "backend_generator",  # Python code generation
        "frontend_generator", # React code generation
        "documentation_generator" # System documentation
    ]
```

#### State management approach

- **Persistent state**: Maintain context across agent interactions
- **Conditional workflows**: Different paths based on discovered patterns
- **Iterative refinement**: Loop back for additional data gathering

### Pending technical questions

- **Audit data specifics**: What additional data beyond standard browser interactions?
- **Database correlation**: Custom logging needs for database correlation?
- **Agent coordination**: Specific LangGraph coordination strategies
- **Validation approach**: Integration with QA team's test harness

### Business alignment questions

- **Initial workflow selection**: Which business domain workflow to start with?
- **System access**: Confirmation of database access availability
- **Success criteria**: How to measure reverse engineering accuracy?
- **QA integration**: Coordination with separate QA validation team

## Current blockers and risks

### Information gaps

- **Target system access**: Need access to legacy system for testing
- **Simple test workflow**: Need to identify first workflow to experiment with
- **Database access confirmation**: Uncertainty about data access level
- **QA team coordination**: Integration points with validation framework

### Technical uncertainties

- **LangGraph complexity**: Multi-agent coordination challenges
- **Pattern recognition accuracy**: Ensuring correct business logic inference
- **Code generation quality**: Producing maintainable, functional code
- **Playwright MCP integration**: State management with browser automation

### Development readiness

- **Team formation**: Development team composition and skills
- **Environment setup**: LangGraph and Playwright MCP development environment
- **Legacy system access**: Access to target system for analysis
- **Validation framework**: QA team test harness integration

## Success indicators for current phase

### Completion criteria

- ✅ Project scope and use case clarified
- ⏳ LangGraph multi-agent workflow designed
- ⏳ Playwright MCP integration functional
- ⏳ Basic agent framework implemented
- ⏳ Simple workflow test successful

### Quality measures

- **Agent coordination**: Smooth state passing between LangGraph agents
- **Data capture accuracy**: Comprehensive browser interaction logging
- **Pattern recognition**: Basic business logic inference from captured data
- **Code generation**: Simple but functional code output
- **Documentation quality**: Clear system behavior documentation

## Deferred considerations

### QA and validation

- **Test harness integration**: Handled by separate QA team
- **Validation framework**: QA team responsibility
- **Accuracy testing**: QA team oversight

### Advanced features

- **Multi-system capability**: Future expansion to multiple legacy systems
- **Advanced AI techniques**: Integration of latest AI developments
- **Production deployment**: Deployment of reverse-engineered systems
