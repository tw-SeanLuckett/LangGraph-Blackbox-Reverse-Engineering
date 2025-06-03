# Prompts

## Initial prompt

Let's start with 1--Primary use case.

What we're looking to do is using an AI agent we want to take a blackbox approach to reverse engineering a legacy software system where we have access to a database and a UI, but no the application code.

Langchain's roll, and we're just experimenting with this, is to have agents that exercise the browser (given instructions on for individual user journey/workflow) via Playwright global MCP, capture data structure through the playwright MCP audit logs, and reverse engineer code in real time.

---

## Followup prompt

This is a good understanding. I'll answer your questions to clarify approach, though, to help even further:

1. Target Legacy System Details

- What type of legacy system are we reverse engineering? Web app
- Do we have read access to the database or just the UI? Probabably but not certain
- Are there specific user journeys/workflows we should focus on first? Not yet
- What's the complexity level - complex business workflows. Here's a list of application capabilities:
  -- Accounts Payable-related queries and dispute management
  -- Consignment shipping, planning, and discrepancy management
  -- Return & Salvage revenue management
  -- Parts ordering and repair scheduling

2. Reverse Engineering Scope
   What level of code generation are we aiming for?

- API endpoint documentation
- Database schema recreation
- Business logic pseudocode
- Full application recreation
  All of these things would be great

Should we focus on specific technologies (REST APIs, specific frameworks)?
Not sure about this, yet, but will likely be two separate implementations: backend and frontend. Back end in Python (though might change); frontend in React and Typescript

3. Playwright MCP Integration

- Are we using the existing Playwright MCP or do we need to extend it?
  We're using the global Playwright MCP and don't need to extend it.
- What specific audit data do we need to capture beyond standard browser interactions?
  I'm not sure about this. Hold on to this question and I'll have to ask others for an answer
- Do we need custom logging for database correlation?
  I'm not sure about this. Hold on to this question and I'll have to ask others for an answer

4. AI Agent Coordination
   Unfortunately, I'm too new to Langchain to know the answers to any of these questions. We'll have to come back to them.

5. Output Format and Validation

- What format should the reverse-engineered code be in?
  I'm not sure what you're asking re: "format"
- How do we validate that our reverse engineering is accurate?
  Great question. Thanks for reminding me. There will be a test harness for validation but the QA on our team will preside over that entire part. We can hold off on that part for now.
- Should we generate tests that can verify our understanding?
  We will but the QA on our team will preside over that entire part. We can hold off on that part for now.

Oh, and finally, I realize I'd like to use LangGraph, not LangChain
