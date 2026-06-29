# Agentic AI Foundations

This subchapter defines the core concepts behind agents and agentic AI systems. It is meant to be read before the system design chapter, where these ideas become architectures, trade-offs, and interview patterns.

## Mental Model

An agentic system gives a model controlled access to context, tools, state, and actions.

```text
goal -> observe state -> reason/plan -> choose action -> call tool -> observe result -> continue or stop
```

The model is not the whole system. The product is the loop around the model: tools, permissions, memory, orchestration, evaluation, user controls, and operational boundaries.

## 1. Workflow vs Agent vs Agentic System

These terms are often blurred. Keep them separate.

| Term | Meaning | Best For |
|------|---------|----------|
| LLM call | One model invocation with prompt/context and output. | Simple generation, extraction, classification, or summarization. |
| Workflow | Predetermined steps with limited branching. | Reliable business processes and repeatable pipelines. |
| Agent | Dynamic loop that chooses actions based on state and observations. | Open-ended tasks where the next step is not known upfront. |
| Agentic system | Product architecture around one or more agents plus deterministic services, data, policies, evals, and ops. | Real applications that need reliability, safety, observability, and scale. |

Use the simplest level that solves the problem. A deterministic workflow with one model call is often better than an autonomous agent.

Read more:

- [Agents and Agentic AI Systems](./agents/README.md)
- [Agents in AI Engineering](./ai-engineering-summary/Chapter_6_2_Agents.md)

## 2. Agent Anatomy

An agent usually has these building blocks:

- **Goal**: the task or objective the agent is trying to complete.
- **Model**: reasons, plans, decides, writes, extracts, or calls tools.
- **Instructions**: system, developer, task, and policy constraints.
- **Context**: current user request, retrieved evidence, tool outputs, and state.
- **Tools**: APIs, databases, search, browser, code execution, files, internal services, or other agents.
- **Memory**: persisted user, task, session, or experience information.
- **Controller**: the loop that executes steps, handles retries, enforces limits, and stops.
- **Guardrails**: validation, policy, permissions, approvals, and safety checks.
- **Trace**: record of model calls, decisions, tool calls, outputs, costs, and failures.

Minimal loop:

```text
while not done:
  decide next action
  validate action
  execute tool or respond
  observe result
  update state
```

## 3. Tools and Actions

Tools are how agents affect the world. They are also the largest source of production risk.

Tool categories:

- **Read tools**: search, retrieval, database queries, file reads, logs, analytics.
- **Write tools**: send email, update CRM, create ticket, modify file, deploy code, place order.
- **Execution tools**: code interpreter, shell, browser, notebook, workflow runner.
- **Communication tools**: Slack, email, calendar, ticketing, chat, phone, voice.
- **Specialist tools**: calculators, solvers, OCR, parsers, databases, vector search, payment APIs.
- **Other agents**: delegated specialists with their own tools and state.

Design questions:

- What is the tool allowed to do?
- Is the tool read-only or mutating?
- Does the tool need user approval?
- Are inputs schema-validated?
- Is the result trusted or should it be verified?
- What happens on timeout, partial success, or failure?
- Is the tool call logged with enough detail for audit and debugging?

Rule of thumb: the more irreversible the action, the more deterministic validation and human approval you need.

## 4. Planning and Control Flow

Planning converts a goal into steps. Control flow decides how those steps actually run.

Common patterns:

- **Single-step tool call**: model chooses one tool, returns result.
- **Plan then execute**: model writes a plan, system executes steps.
- **ReAct loop**: reason, act, observe, repeat.
- **Reflection loop**: generate, critique, revise.
- **Router**: classify request and send to a workflow, model, tool, or agent.
- **Supervisor-worker**: one controller delegates tasks to specialist agents.
- **Human checkpoint**: pause for approval, missing information, or risk review.
- **Background agent**: long-running task with durable state, retries, and resumability.

Control limits:

- Max steps.
- Max tokens.
- Max cost.
- Max runtime.
- Allowed tools.
- Required approval points.
- Cancellation and rollback behavior.

## 5. Memory and State

Memory is not the same as dumping all history into the prompt. Good agentic systems separate state, context, memory, and knowledge.

| Concept | Meaning |
|---------|---------|
| Context | Information included in the current model call. |
| State | Durable task/session data owned by the application. |
| Memory | Selected persisted information useful for future interactions. |
| Knowledge | External source of truth, often retrieved rather than stored in memory. |
| Trace | Execution record for debugging, evals, cost, and audit. |

Memory types:

- **Conversation memory**: recent turns, summaries, and unresolved facts.
- **Task memory**: plan, progress, intermediate artifacts, blockers, decisions.
- **User memory**: preferences, profile, permissions, recurring needs.
- **Semantic memory**: facts retrieved by similarity or entity lookup.
- **Episodic memory**: prior examples of similar tasks and outcomes.
- **Procedural memory**: reusable instructions, playbooks, or skills.

Risks:

- Storing sensitive user data without purpose or retention policy.
- Recalling stale or incorrect facts.
- Memory poisoning from untrusted inputs.
- Cross-tenant leakage.
- Inflating prompts with low-value history.

## 6. Human-in-the-Loop

Human-in-the-loop is not a fallback only. It is a design pattern for quality, trust, and risk control.

Use human checkpoints for:

- Ambiguous goals.
- Missing information.
- High-cost actions.
- Irreversible or external actions.
- Security-sensitive operations.
- Low-confidence predictions.
- Policy exceptions.
- User-facing communication in sensitive domains.

Checkpoint types:

- **Approval**: agent proposes an action; user confirms.
- **Correction**: user edits a draft, plan, or tool input.
- **Escalation**: system hands off to a person or support queue.
- **Review**: human audits final output or trace.
- **Teaching**: user feedback becomes examples, memory, or eval cases.

## 7. Multi-Agent Systems

Multi-agent systems split work across multiple agents. They are useful when specialization, parallelism, separation of permissions, or critique improves the result.

Good uses:

- Researcher, planner, writer, reviewer.
- Coder, tester, reviewer, release manager.
- Data analyst, SQL agent, charting agent, narrative agent.
- Customer support triage, policy checker, action executor.
- Supervisor with specialist agents for domains or tools.

Common failure modes:

- Too much coordination overhead.
- Agents repeating or contradicting each other.
- No clear owner for final quality.
- Tool permissions spread too broadly.
- Hard-to-debug traces.
- Higher cost and latency without better outcomes.

Design rule: start with one agent or workflow. Add agents only when a real boundary appears.

## 8. Agentic RAG

Agentic RAG extends retrieval from a fixed pipeline into a decision-making process.

Static RAG:

```text
query -> retrieve -> rerank -> answer
```

Agentic RAG:

```text
query -> decide what is needed -> retrieve/search/query tools -> inspect evidence -> retrieve more or answer
```

Use agentic RAG when:

- The information need is ambiguous.
- Multiple sources must be compared.
- The system needs SQL, search, documents, and APIs together.
- The agent must verify claims before answering.
- A single retrieval pass is not enough.

Keep retrieval bounded. Unbounded search loops are expensive, slow, and hard to evaluate.

## 9. Protocols and Interoperability

Agentic systems need consistent ways to connect models, tools, data, and agents.

Important concepts:

- **Tool schema**: machine-readable description of tool inputs, outputs, and constraints.
- **MCP**: standard interface for exposing tools and context to model applications.
- **A2A-style communication**: patterns for task handoff and agent-to-agent messages.
- **Tool registry**: approved inventory of tools, owners, scopes, versions, and risk tiers.
- **Gateway**: centralized control point for auth, policy, logging, rate limits, and tool access.

Interoperability is a production concern, not just a developer convenience. It affects security, governance, reuse, and observability.

## 10. Reliability and Safety Basics

Agents introduce failure modes beyond normal LLM calls.

Failure modes:

- Wrong tool selected.
- Correct tool called with wrong arguments.
- Tool result misread.
- Agent loops without progress.
- Agent succeeds at subtask but fails the real goal.
- Prompt injection changes tool behavior.
- Memory stores untrusted or sensitive data.
- Output is plausible but ungrounded.
- Cost grows due to retries, long context, or tool loops.

Basic controls:

- Tool allowlists and scoped permissions.
- Input/output schema validation.
- Human approval for risky actions.
- Step, time, token, and cost limits.
- Trace logging for every model and tool call.
- Regression evals for common and adversarial tasks.
- Retrieval/source attribution for knowledge-heavy answers.
- Clear stop conditions.

## 11. When Not to Use an Agent

Avoid agents when:

- The process is fixed and deterministic.
- A form, rules engine, SQL query, or script solves the task.
- The action is high-risk and cannot be validated.
- You cannot observe or evaluate the behavior.
- Latency or cost budgets are tight.
- The model lacks the needed context or tools.
- The user needs predictable repeatability more than flexibility.

Agentic AI is most useful when the task needs flexible decision-making under constraints. Otherwise, simpler systems are easier to ship and maintain.

## 12. What Moves to Later Chapters

Keep the boundaries clear:

- Agent architectures, background agents, memory systems, RAG architectures, and multi-agent system design move to [System Design](../03_system_design/README.md).
- Runtime, deployment, governance, observability, cost, latency, and AWS/Bedrock/AgentCore move to the new Prototype to Production chapter.
- Framework tutorials and runnable examples move to the hands-on appendix.
- Curated links move to [Resources](../RESOURCES.md).
