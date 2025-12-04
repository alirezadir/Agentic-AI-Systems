# **OpenAI's A Practical Guide to Building Agents**

**Updated 2025**: This guide provides foundational principles for building agents with OpenAI's framework. With the release of the Agents SDK in March 2025, many of these patterns are now implemented as first-class features.

<!-- * 25, 2024* -->
A summary from the OpenAI Guide: [A Practical Guide to Building Agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)

## 1. Agents Intro

- Conventional software: automate workflows
- Agent: accomplish tasks (perform workflows) on behalf of users, with high independence
- Workflow: sequence of steps to be executed
    - e.g. resolve a customer service issue, book a reservation
- LLM vs Agent apps: agent apps use LLMs to control workflow execution
- Agents core characteristics:
    1. LLM to manage workflow execution & make decisions; recognize workflow completion, proactive action correction, execution halt
    2. Tool access & external system interaction (gather context + take actions); dynamically select tools (f(state)); operate within guardrails

**Traditional Software vs LLM Agents**
- Traditional Software: deterministic & rule-based; like a checklist
- LLM Agent: nuanced reasoning; evaluates context, reasoning (outside clear rules)

**When to Use Agents**
1. Complex decision making: context-sensitive decisions, nuanced judgment, exceptions
    - e.g. refund approval in customer service
2. Difficult to maintain rules: extensive rules, updates costly or error-prone
3. Reliance on unstructured data (natural language): e.g. extract meaning from documents, conversation with users
    - e.g. insurance claim

## 2. Agent Design

### Agent Components:
1. **Model**: LLM; reasoning + decision-making
2. **Tools**: functions or APIs (to take action)
3. **Instructions**: explicit guidelines + guardrails

Example (OpenAI Agent SDK):
```python
agent = Agent(name="Weather agent", instructions="You are a ...", tools=[get_weather])
```

### Model Selection
- Model trade-offs: task complexity, latency, cost
- Use a variety of models in the workflow
    - Simple tasks (intent classifier, retrieval): smaller, faster model
    - Harder tasks (approve refund): more complex models

**Model Selection Principles**
1. Build a performance baseline: setup evaluations; prototype with the most capable model
2. Swap smaller models (success/fail); optimize for cost and latency

### Tools
- Use APIs (from apps or systems); web/app UI (if no API)
- Standardized definitions: enable flexible, many-to-many relationships
- Well-documented, thoroughly tested, reusable

**3 Types of Tools**:
1. **Data**: retrieve context
    - e.g. query DB, read document, search web
2. **Action**: interact with systems; add new info, update DB, send messages
    - e.g. send emails/texts, update a CRM record
3. **Orchestration**: Agents as tools for other agents (manager pattern)
    - e.g. refund agent, research agent, write agent

As the number of tools increases  split tasks across multiple agents

```python
from agents import Agent, WebSearchTool, function_tool 
@function_tool
def save_results(output): 
    ...
search_agent = Agent(name="search agent", instructions=..., tools=[WebSearchTool(), save_results])
```

### Instructions
- High quality is essential
- Clear: reduce ambiguity, improve decision-making, fewer errors

**Instruction Practices**
- Use existing documents: operation procedures, policy/support docs
    - e.g. customer service: map routines to individual articles (KB)
- Prompt agents for task breakdown: smaller, clearer steps
- Define clear actions: every step in routine mapped to a specific action/output; even user-facing messages
    - e.g. step: ask user for order No., call an API
- Capture edge cases: e.g. when user info is incomplete, user asks unexpected questions

Automatic instruction generation from existing docs: use advanced models (e.g. o1 or o3-mini)

```text
You are an expert in ... convert the following doc into a clear set of instructions, in a numbered list ...
```

## 3. Orchestration
- For workflow execution
- Incremental approach for success

**Orchestration Patterns**:
- **Single Agent Systems**: single model + tools & instructions  execute workflow in a loop
- **Multi-Agent Systems**: distributed workflow execution across multiple agents
    - Sequence of tool calls & handoffs between agents, run multiple steps until exit condition is met

- Modeled as Graphs:
    - Nodes: agents
    - Edges: tool calls (manager), execution hand-offs (decentralized)
- Principles: flexible, composable components + clear, well-structured prompts

### Single Agent Systems
- Incremental expansion (tool addition): lower complexity, simpler evaluation and maintenance
- 'Run' implemented as a loop until exit condition met
- Exit conditions: (final/output) tool call, certain output, errors, max turns
```python
Agents.run(agent, [UserMessage("...")])
```
- Prompt templates: manage complexity without MAS
    - Single flexible base prompt with policy variables (instead of multiple prompts)
```python
""" You are a call center agent. You are interacting with {{user_first_name}} ... about {{user_complaint_categories}} ... """
```

### Multi-Agent Systems
Two main categories:
1. **Manager (Agents as Tools)**: central manager agent (LLM) orchestrates multiple specialized agents (as tools) via tool calls
    - Delegates tasks to the right agent at the right time (async)
    - e.g. translation manager agent, spanish_agent, french_agent, etc.

2. **Decentralized (Handing Off to Agents)**: multiple agents as peers, handing off tasks to one another
    - Hand-offs: one-way transfer of execution to another agent
    - Hand-off tool or function: start execution on new agent + transfer latest state
    - e.g. User  Triage  Issues  Orders  Output

**Single Agent vs Multi-Agent Architecture**:
- More agents: separation of concepts, scalability, but more complexity & overhead
- Maximize single agent's capabilities with tools first
- Introduce more agents when agents fail to follow instructions, or select tools:
    - Complex logic: prompts with many conditional statements (if-then-else)
    - Tool overload: number of tools, similarity/overlap of tools

- Declarative vs Non-Declarative
    - Declarative: define every branch, loop, condition upfront
    - Non-declarative: no need to predefine graph upfront, code-first approach, more dynamic & adaptable

## 4. Guardrails
- Layered defense mechanism to address risks, e.g.
    - Data privacy risks (system prompt leaks)
    - Reputation risks
- Coupled with authentication, authorization, access control, software security
- Layered approach (multiple specialized guardrails): already identified risks + new ones uncovered

**Types of Guardrails**:
- LLM-based, rule-based, moderation APIs
- Relevance classifier: flag off-topic
- Safety classifier: unsafe input (jailbreak, prompt injection) to extract system prompts
- PII (Personally Identifiable Information): vet model output
- Moderation: flag harmful/inappropriate input (hate, harassment, violence)
- Tool guards: risk of tools rated (low, medium, high), trigger automated actions (pause, GR check, escalate to human)
- Rule-based: deterministic (blocklists, length limits, regex filters), for known threats (prohibited terms, injections)
- Output validation: aligns with brand values (prompt engineering, content checks)
- Tips: focus on privacy & content safety, add over new edge cases, optimize for both security & user experience

