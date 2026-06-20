# 2026 Agentic AI System Design Update

This page summarizes the 2026 shift in agentic AI system design. The repo already covers foundations, frameworks, RAG, memory, protocols, evals, and multi-agent patterns. The biggest missing layer is the production harness around agents: scheduling, state, tools, permissions, evals, observability, cost control, and recovery.

## What Changed From 2025 to 2026

| 2025 focus | 2026 focus | What this means for system design |
| --- | --- | --- |
| Prompt engineering | Context engineering | Design the full information environment, not just the instruction text. |
| Chatbots and copilots | Long-running agents | Agents need state, goals, schedules, permissions, and recovery. |
| Single LLM calls | Agent harnesses | The LLM is one component inside orchestration, tools, memory, evals, and monitoring. |
| Basic RAG | Agentic RAG and tool-mediated retrieval | Agents decide when to retrieve, what source to use, and when to abstain. |
| Model benchmarks | Agent evaluation | Measure trajectories, tool choices, task completion, and production behavior. |
| Ad hoc tool integrations | MCP and A2A ecosystems | Standard protocols are becoming core infrastructure for tool and agent interoperability. |

## 2026 Core Design Themes

### 1. Harness Engineering

A production agent is not `llm(prompt)`. It is a runtime harness:

```text
request or schedule
  -> intent and policy checks
  -> planner or router
  -> context builder
  -> agent loop
  -> tools and MCP servers
  -> memory and state store
  -> evaluator and guardrails
  -> retry, rollback, or human approval
  -> trace, metrics, and feedback
```

Key design questions:

- What owns control flow: a deterministic orchestrator, a model planner, or a hybrid?
- What is the autonomy level: suggest-only, draft-and-approve, or execute-with-rollback?
- What actions require human approval?
- How are retries, idempotency, and side effects handled?
- What budget caps stop runaway loops?

### 2. Context Engineering

Context engineering is the discipline of selecting, ranking, compressing, isolating, and proving the information an agent sees. A strong design treats context as a first-class subsystem.

Core components:

- Context sources: user profile, session history, documents, tool outputs, memory, policies, and environment state.
- Context selection: query rewriting, retrieval, reranking, recency, authority, and permission filters.
- Context compression: summaries, structured state, chunk pruning, and prompt budgeting.
- Context provenance: every claim should be traceable to source, tool output, memory item, or user instruction.
- Context isolation: prevent private, tenant-specific, or adversarial context from leaking across users or tools.

Design trade-offs:

- Larger context improves recall but increases cost, latency, and context pollution.
- Memory improves personalization but creates privacy, poisoning, and deletion problems.
- Summaries reduce token load but may erase details needed for correctness.

### 3. Long-Running and Scheduled Agents

2026 agent products increasingly need background execution:

- Monitor GitHub issues or incidents.
- Follow up on email or customer requests.
- Run daily research.
- Watch competitors, prices, jobs, or compliance signals.
- Continue multi-step workflows after the user leaves.

Required architecture:

- Scheduler or event trigger.
- Durable task state.
- Goal and policy store.
- Tool permission model.
- Checkpointing and resumability.
- Notification and approval channel.
- Expiration, cancellation, and audit trail.

Failure modes:

- Agent keeps working after the goal is stale.
- Agent acts with outdated permissions.
- Agent repeats a side-effecting action.
- Agent spends too much money on tool calls or model calls.
- Agent wakes at the wrong cadence and creates notification fatigue.

### 4. AgentOps and Observability

AgentOps is the operational layer for deployed agents. Logs are not enough; agent systems need traces that capture model calls, tool calls, state transitions, memory reads/writes, retrieved evidence, costs, and human approvals.

Minimum production telemetry:

- Task success rate.
- Tool call success and error rate.
- Step count per task.
- Cost per task and cost per successful task.
- Latency: p50, p95, p99, TTFT, TPOT.
- Escalation and human-approval rate.
- Retry rate, rollback rate, and timeout rate.
- Safety events: prompt injection, policy refusal, PII exposure, unsafe tool request.
- Trace replay for debugging.

The LangSmith evaluation docs frame evals as a lifecycle from pre-deployment testing to production monitoring, and recommend breaking the system into critical components such as LLM calls, retrieval steps, tool invocations, and output formatting before defining quality criteria.

### 5. Evaluation-Driven Development

For AI systems, evals are the practical equivalent of test suites. A 2026-ready repo should teach both offline and online evals.

Offline evals:

- Golden task suites.
- Regression tests for prompts, tools, retrieval, and policies.
- Simulated user tasks.
- Adversarial tests for injection, tool misuse, and data leakage.
- LLM-as-judge with calibration and human audit.

Online evals:

- Quality monitoring on live traces.
- User feedback and annotation queues.
- Drift detection.
- Cost, latency, and safety dashboards.
- Automatic conversion of failures into offline test cases.

Agent-specific eval dimensions:

- Correct tool selection.
- Correct tool arguments.
- Grounded final answer.
- Safe action choice.
- Termination quality.
- Step efficiency.
- Recovery from tool failure.
- Human handoff quality.

### 6. Protocols: MCP and A2A

MCP standardizes connections between LLM applications and external tools or data sources. The official MCP specification describes hosts, clients, and servers communicating over JSON-RPC, with servers exposing resources, prompts, and tools. Anthropic introduced MCP to replace fragmented custom integrations with a single protocol for connecting AI systems to data sources and tools.

A2A focuses on agent-to-agent interoperability. Google's A2A announcement emphasizes cross-system collaboration, message exchange, artifacts, and open contribution paths for agent interoperability. In system design, MCP is mostly agent-to-tool and agent-to-context; A2A is agent-to-agent.

Design implications:

- Treat protocol boundaries as trust boundaries.
- Use explicit identity and permission propagation.
- Scope credentials per tool, task, user, and tenant.
- Log every tool call and agent-to-agent delegation.
- Add rate limits, timeouts, schema validation, and budget caps at the protocol gateway.

### 7. Security for Connected Agents

Agent security is now central because agents can read private data and perform actions.

Threat model:

- Prompt injection through documents, webpages, tickets, emails, or tool outputs.
- Tool poisoning through malicious or lookalike tools.
- Data exfiltration by combining benign tools.
- Memory poisoning.
- Over-permissioned tools.
- Side effects without user approval.
- Supply-chain risk from MCP servers, plugins, and agent skills.

Controls:

- Least privilege and scoped credentials.
- Tool allowlists and schema validation.
- Separate read tools from write tools.
- Human approval for irreversible or sensitive actions.
- Sandboxed execution for code and browser use.
- Data loss prevention checks before external calls.
- Memory write filters and user-visible memory controls.
- Audit logs with source, actor, tool, and reason.

### 8. Inference and Cost as First-Class Design

System design interviews and production reviews increasingly ask for cost and latency reasoning.

Core serving metrics:

- TTFT: time to first token.
- TPOT: time per output token.
- End-to-end p50, p95, p99 latency.
- Tokens per second.
- GPU utilization.
- Cost per request and cost per successful task.
- Cache hit rate.
- Fallback rate.

Optimization levers:

- Model routing by task difficulty.
- Prompt and context compression.
- Semantic response caching.
- Prompt or prefix caching.
- KV-cache reuse.
- Continuous batching.
- Speculative decoding.
- Quantization and distillation.
- Tool-call reduction.
- Early termination and budget caps.

Never optimize blindly. Profile the bottleneck first, then pick the lever that improves the target metric without breaking quality or safety guardrails.

## Recommended Repo Updates

- Add a durable-agent architecture page covering scheduling, state, checkpointing, resumability, and human approvals.
- Expand memory docs from screenshots into concrete memory write/read/consolidation/forgetting patterns.
- Add a context-engineering guide covering retrieval, memory, policy context, tool outputs, provenance, and context isolation.
- Add an AgentOps page under evals or a new operations folder.
- Expand protocols with current MCP concepts, remote MCP, authorization, security risks, and A2A.
- Add an interview-prep chapter separate from the main learning chapters.
- Add examples for agent budget caps, tool gateways, trace schemas, and idempotent side-effecting actions.

## Sources

- [OpenAI, New tools for building agents](https://openai.com/index/new-tools-for-building-agents/)
- [Anthropic, Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)
- [Model Context Protocol specification, 2025-06-18](https://modelcontextprotocol.io/specification/2025-06-18)
- [Google Developers Blog, Announcing Agent2Agent Protocol](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
- [Anthropic, Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [LangSmith, Evaluation concepts](https://docs.langchain.com/langsmith/evaluation-concepts)
- Local notes: [2026-1.md](../05_resources/source-material/2026-agentic-ai/2026-1.md)
- Local notes: [2026-2.md](../05_resources/source-material/2026-agentic-ai/2026-2.md)
- Local image: [Claude-cheatsheet.jpg](../05_resources/source-material/2026-agentic-ai/Claude-cheatsheet.jpg)
