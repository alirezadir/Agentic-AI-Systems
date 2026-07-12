# 12-Step GenAI and Agentic System Design Framework

Use this framework for product design reviews and system-design interviews. It works for LLM apps, RAG systems, agentic workflows, multimodal assistants, coding agents, and long-running background agents.

The goal is not to force every system into maximum complexity. The goal is to make the important decisions explicit.

## One-Page Flow

```text
1. Frame problem and scope
2. Define success metrics and SLOs
3. Pick system mode and autonomy level
4. Design high-level architecture
5. Design data, context, and retrieval
6. Select models and adaptation strategy
7. Design tools, actions, and permissions
8. Design memory and durable state
9. Design orchestration and runtime control
10. Design safety, guardrails, and governance
11. Design evals, observability, and feedback
12. Design deployment, scaling, cost, and rollout
```

## Step 1: Frame Problem and Scope

Clarify the product contract before designing components.

Ask:

- Who are the users?
- What job must the system complete?
- What is in scope for v1?
- What is explicitly out of scope?
- What modalities are involved: text, code, documents, images, audio, video, UI?
- Is the system interactive, batch, event-driven, or long-running?
- Is this a user-facing product, internal tool, API, or platform capability?
- What privacy, safety, compliance, or business constraints apply?

Output:

- User and use case.
- Functional requirements.
- Non-functional requirements.
- Assumptions and scope cuts.
- Launch stage: prototype, MVP, beta, production.

## Step 2: Define Success Metrics and SLOs

AI systems need product, quality, serving, and safety metrics.

Metrics:

- **Task success**: resolution, answer correctness, extraction accuracy, action completion.
- **Quality**: groundedness, helpfulness, completeness, tone, format validity.
- **Retrieval**: recall@k, precision@k, nDCG, citation accuracy, freshness.
- **Agent behavior**: tool-call correctness, step efficiency, termination quality, recovery.
- **Serving**: TTFT, TPOT, p50/p95/p99 latency, availability, throughput.
- **Cost**: cost per request, session, workflow, and successful task.
- **Safety**: policy violations, prompt-injection events, PII exposure, unsafe actions.
- **Human experience**: CSAT, edits, escalation rate, approval rate, user feedback.

Output:

- Offline eval metrics.
- Online metrics and dashboards.
- SLOs and error budgets where relevant.
- A minimum quality bar for launch.

## Step 3: Pick System Mode and Autonomy Level

Choose the simplest architecture that satisfies the product contract.

System modes:

| Mode | Use When |
|------|----------|
| Single model call | Task is simple and low-risk. |
| Compound GenAI workflow | Steps are known and repeatable. |
| RAG system | Answers depend on external knowledge. |
| Agentic workflow | The system must choose tools/actions dynamically. |
| Multi-agent system | Roles, tools, permissions, or parallel work justify separation. |
| Background agent | Work is scheduled, event-driven, durable, or long-running. |

Autonomy levels:

- **Suggest only**: user takes action.
- **Draft and approve**: system drafts; human approves.
- **Execute with checkpoints**: system acts after explicit gates.
- **Limited auto-action**: system acts within narrow policies.
- **Autonomous with rollback**: only for well-tested, low-blast-radius tasks.

Output:

- Chosen system mode.
- Autonomy level.
- Human checkpoint policy.
- Justification for not using a simpler design.

## Step 4: Design High-Level Architecture

Draw the path from request to response/action.

Reference skeleton:

```text
client / trigger
  -> API gateway and auth
  -> router or orchestrator
  -> context builder
  -> retrieval, memory, tools, and policy services
  -> model gateway or agent runtime
  -> validators, guardrails, and human checkpoints
  -> response/action
  -> traces, evals, metrics, and feedback
```

Specify:

- Main services.
- Synchronous vs asynchronous boundaries.
- Data stores.
- Trust boundaries.
- Failure and fallback paths.
- Which components are deterministic vs model-driven.

Output:

- Component diagram.
- Request/action sequence.
- Ownership boundaries.
- First MVP architecture.

## Step 5: Design Data, Context, and Retrieval

Context is the model's runtime environment. Treat it as a first-class subsystem.

Design:

- Source-of-truth data.
- Ingestion and freshness.
- Chunking and metadata.
- Embeddings and lexical indexes.
- Hybrid retrieval and reranking.
- ACL and tenant filtering.
- Context packing and compression.
- Citations and provenance.
- Deletion and retention.

For RAG:

```text
documents -> ingestion -> chunking -> embeddings/indexes
query -> rewrite -> retrieve -> rerank -> pack context -> model -> cited answer
```

Output:

- Data model.
- Retrieval strategy.
- Context budget.
- Provenance and citation strategy.
- Retrieval eval plan.

## Step 6: Select Models and Adaptation Strategy

Model choice is a trade-off across quality, latency, cost, modality, privacy, and tool support.

Decide:

- Model provider or self-hosting.
- Model routing strategy.
- Context window needs.
- Structured output and tool-call support.
- Multimodal needs.
- Streaming needs.
- Fallbacks.
- Fine-tuning, adapters, distillation, or prompting only.

RAG vs fine-tuning:

- Use **RAG** for changing facts, source-grounded answers, and private knowledge.
- Use **fine-tuning** for repeated behavior, format, style, domain language, tool-call consistency, or cost reduction.

Output:

- Model matrix.
- Routing/fallback plan.
- Adaptation plan.
- Cost and latency assumptions.

## Step 7: Design Tools, Actions, and Permissions

Tool access changes the risk profile of the system.

Classify tools:

- Read-only tools.
- Write/action tools.
- Code/browser/desktop tools.
- Internal APIs.
- External APIs.
- Other agents.

Design:

- Tool schemas.
- Tool registry or gateway.
- Auth and scoped credentials.
- Input validation.
- Idempotency keys for side effects.
- Approval gates.
- Timeouts and retries.
- Tool result trust model.
- Audit logs.

Output:

- Tool inventory.
- Permission model.
- Approval policy.
- Side-effect handling plan.

## Step 8: Design Memory and Durable State

Separate context, state, memory, and knowledge.

| Concept | Role |
|---------|------|
| Context | Information included in the current model call. |
| State | Durable task/session data owned by the application. |
| Memory | Persisted information selected for future use. |
| Knowledge | External source of truth, usually retrieved. |
| Trace | Execution record for debugging and evals. |

Design:

- Session state.
- Task state.
- User memory.
- Long-term memory.
- Memory write filters.
- Memory retrieval.
- Summarization and consolidation.
- Forgetting and deletion.
- Cross-tenant isolation.

Output:

- State schema.
- Memory policy.
- Retention/deletion policy.
- Privacy controls.

## Step 9: Design Orchestration and Runtime Control

Control flow can be deterministic, model-driven, graph-based, or hybrid.

Patterns:

- Router.
- Fixed workflow.
- ReAct loop.
- Plan-execute.
- Reflection/revision.
- Supervisor-worker.
- Background worker.
- Human checkpoint.

Runtime controls:

- Step limit.
- Time limit.
- Token budget.
- Cost budget.
- Retry policy.
- Cancellation.
- Checkpointing.
- Resume and recovery.
- Loop detection.

Output:

- Orchestration pattern.
- Runtime limits.
- Recovery behavior.
- Human handoff behavior.

## Step 10: Design Safety, Guardrails, and Governance

Agents can read private data and perform actions, so safety is architectural.

Threats:

- Prompt injection.
- Tool poisoning.
- Data exfiltration.
- Memory poisoning.
- Over-permissioned tools.
- Unsafe side effects.
- PII leakage.
- Cross-tenant leakage.
- Supply-chain risk from plugins or tool servers.

Controls:

- Input/output validation.
- Policy checks before tool calls.
- Least-privilege credentials.
- Read/write tool separation.
- Sandboxed execution.
- DLP and PII detection.
- Human approval for risky actions.
- Audit logs.
- Rate limits and abuse controls.

Output:

- Threat model.
- Guardrail plan.
- Audit/compliance plan.
- Incident response hooks.

## Step 11: Design Evals, Observability, and Feedback

Evals are the test suite for AI behavior. Observability makes failures debuggable.

Offline evals:

- Golden task sets.
- RAG retrieval evals.
- Tool-call evals.
- Safety/adversarial evals.
- Regression tests.
- Human-reviewed samples.

Online monitoring:

- Task success.
- Trace-level quality.
- Tool errors.
- Latency and cost.
- User feedback.
- Escalations.
- Policy events.
- Drift and incident alerts.

Trace fields:

- Prompt/context version.
- Model and parameters.
- Retrieved sources.
- Tool calls and outputs.
- Memory reads/writes.
- Validation results.
- Human approvals.
- Cost and latency.

Output:

- Eval suite.
- Trace schema.
- Dashboards and alerts.
- Feedback-to-eval loop.

## Step 12: Design Deployment, Scaling, Cost, and Rollout

Production design needs rollout and operating plans, not just architecture diagrams.

Deployment:

- API service.
- Worker service.
- Queue/scheduler.
- Model gateway.
- Vector store.
- State/memory stores.
- Observability stack.
- CI/CD and config/versioning.

Scaling:

- Request QPS.
- Tokens per second.
- Tool-call throughput.
- Indexing throughput.
- Queue depth.
- Storage growth.
- Multi-region or tenant needs.

Cost levers:

- Model routing.
- Context pruning.
- Prompt/prefix caching.
- Semantic caching.
- Smaller models.
- Batch/offline processing.
- Tool-call reduction.
- Early termination.
- Quantization or distillation.

Rollout:

- Offline eval pass.
- Shadow mode.
- Internal beta.
- Draft-only mode.
- Human approval mode.
- Limited auto-action.
- Gradual ramp.
- Incident rollback.

Output:

- Deployment plan.
- Scale estimates.
- Cost estimate.
- Rollout plan.
- Operational ownership.

## Example: Customer Support Agent

Use the framework to design a support agent.

### Scope

Build an agent that answers policy/order questions, drafts customer replies, looks up order status, and can request refunds with human approval.

### Architecture

```text
chat/email ticket
  -> API gateway and auth
  -> intent classifier
  -> support orchestrator
  -> policy RAG + order tools + CRM tools
  -> response/action draft
  -> safety checks and approval gates
  -> customer response or human escalation
  -> traces, evals, and feedback
```

### Key Decisions

- Start with draft-only for refunds and account changes.
- Use RAG for policies and order FAQs.
- Use tools for order status, refund eligibility, and escalation.
- Keep customer profile as state, not uncontrolled prompt history.
- Add idempotency keys for refund actions.
- Log every tool call, retrieved source, approval, and final response.
- Evaluate task resolution, citation accuracy, tone, escalation quality, tool-call correctness, latency, and cost per resolved ticket.

### Failure Modes

- Wrong policy retrieved.
- Refund eligibility tool called with wrong user/order.
- Agent answers with stale policy.
- Prompt injection through customer email.
- Agent loops between retrieval and tool calls.
- Customer PII leaks into logs or external tools.

### MVP Rollout

1. Offline evals with historical tickets.
2. Shadow mode against live tickets.
3. Draft replies for human agents.
4. Limited auto-replies for low-risk FAQ intents.
5. Approval-gated actions for refunds and account changes.
6. Gradual ramp with monitoring and rollback.
