# Project brief

## Project overview

**AIFSD-Macys-blackbox-langchain** is an AI Full Stack Development project focused on using AI agents to reverse engineer legacy software systems through blackbox analysis. The project uses LangGraph and Playwright MCP to analyze system behavior without access to source code.

## Core objectives

### Primary goals

- Develop AI agents that can reverse engineer legacy web applications
- Use LangGraph for complex multi-agent workflows
- Implement blackbox analysis using Playwright MCP for browser automation
- Generate comprehensive system documentation and code recreation

### Key deliverables

- LangGraph-based multi-agent system for reverse engineering
- Playwright MCP integration for browser automation and data capture
- Generated backend code (Python) and frontend code (React/TypeScript)
- API endpoint documentation and database schema recreation
- Business logic inference and documentation

## Project scope

### In scope

- Legacy web application reverse engineering
- Multi-agent AI system using LangGraph
- Browser automation and interaction capture via Playwright MCP
- Code generation for backend (Python) and frontend (React/TypeScript)
- Business workflow analysis across 4 domains:
  - Accounts Payable queries and dispute management
  - Consignment shipping, planning, and discrepancy management
  - Return & Salvage revenue management
  - Parts ordering and repair scheduling

### Out of scope (initially)

- Direct database access integration (pending confirmation)
- Production deployment of reverse-engineered systems
- QA validation framework (handled by separate QA team)
- Real-time system integration

## Success criteria

1. **Functional AI agent system** that can execute complex user workflows via browser automation
2. **Accurate pattern recognition** from captured browser interactions and network traffic
3. **Generated code quality** that recreates system functionality in modern tech stack
4. **Comprehensive documentation** of reverse-engineered system architecture
5. **Proof of concept** demonstrating blackbox reverse engineering capabilities

## Stakeholders

- **Development team**: AI/ML engineers, full stack developers
- **QA team**: Responsible for validation framework and testing
- **Business stakeholders**: System owners and domain experts
- **Technical leadership**: Architecture and methodology oversight

## Timeline and phases

### Phase 1: LangGraph Foundation (Week 1)

- LangGraph workflow framework setup
- Playwright MCP integration
- Basic agent structure development

### Phase 2: Core Agent Development (Weeks 2-3)

- Journey execution agent implementation
- Data capture and pattern analysis agents
- Basic code generation capabilities

### Phase 3: Code Generation (Weeks 4-5)

- Backend code generation (Python)
- Frontend code generation (React/TypeScript)
- Integration and validation

### Phase 4: Business Domain Focus (Weeks 6-8)

- Domain-specific workflow analysis
- Complex business logic inference
- Comprehensive system recreation

## Risk considerations

- **Technical complexity**: LangGraph multi-agent coordination challenges
- **Pattern recognition accuracy**: Ensuring correct inference from blackbox analysis
- **Code generation quality**: Generated code must be functional and maintainable
- **Legacy system complexity**: Complex business workflows may be difficult to reverse engineer
- **Data access limitations**: Uncertainty about database access availability

## Next steps

1. Set up LangGraph development environment
2. Integrate Playwright MCP with agent workflow
3. Define simple test workflow for initial experimentation
4. Begin agent development and testing
