# GenAI and Agentic System Design Interview Prep

This page combines the provided prep PDFs with the repo's agentic system design material. It separates reusable system-design guidance from interview questions, because the main system-design chapter should stay concept-first.

Source PDFs reviewed:

- `/Users/alirezadir/Library/CloudStorage/GoogleDrive-alireza.dirafzoon@gmail.com/My Drive/Session-1-Prep.pdf`
- `/Users/alirezadir/Library/CloudStorage/GoogleDrive-alireza.dirafzoon@gmail.com/My Drive/System-Design-Questions.pdf`

## Senior and Principal Bar

Strong answers are not longer answers. They show judgment.

| Dimension | Solid senior answer | Principal or senior-manager signal |
| --- | --- | --- |
| Problem framing | Restates the prompt and lists features | Converts ambiguity into measurable goals, SLOs, constraints, and explicit scope cuts |
| Structure | Moves between components | Drives a repeatable framework and parks non-critical details |
| Trade-offs | Names options | States the decision, discarded alternatives, and why |
| Depth | Deep in one familiar area | Can drill into architecture, inference, evals, safety, or cost on demand |
| Metrics | Generic accuracy or latency | Chooses offline, online, business, and serving metrics |
| Failure modes | Happy path | Names failures, detection, graceful degradation, and blast radius |
| Cost and scale | Says the system scales | Does rough QPS, token, GPU, latency, and cost math |
| Leadership | IC implementation framing | Discusses build-vs-buy, rollout, ownership, on-call, risk, and team enablement |

## Five-Step Answer Framework

Use this for every GenAI, ML, and agentic system-design prompt:

1. **Problem framing**
   Define users, use cases, constraints, scale, latency, privacy, safety, cost, and success metrics.
2. **High-level architecture**
   Walk the path from client to orchestration, context, tools, model, post-processing, telemetry, and storage.
3. **Deep dives**
   Go where the interviewer probes: RAG, inference, memory, evals, safety, tools, agent control flow, or cost.
4. **Trade-offs and failure modes**
   Cover what breaks, how to detect it, how to degrade gracefully, and what you would not build yet.
5. **Wrap and iteration**
   Summarize the design, top risks, rollout plan, and next iteration.

## Common Red Flags

- Treating the LLM as a source of truth.
- Skipping grounding, citations, or provenance.
- Skipping evals and monitoring.
- Ignoring safety, prompt injection, PII, or data leakage.
- Assuming model calls are free.
- Over-engineering before a simple working architecture exists.
- Jumping into low-level implementation before scope and requirements are clear.
- Using buzzwords without trade-offs.

## Core Topic Map for 2026 Interviews

### Tier 1: Almost Always

- LLM chatbot at scale.
- Enterprise search or RAG assistant.
- Cost and latency optimization for an LLM app.

### Tier 2: Frequent

- Agentic workflow with tools, memory, safety, and human approval.
- Guardrails and content or policy moderation.
- Document Q&A with citations and multi-hop retrieval.

### Tier 3: Role-Specific

- Large-scale LLM inference and serving platform.
- On-device or small-model assistant.
- Cross-conversation memory.
- Real-time LLM search.
- Multi-agent research system.
- AI coding assistant.
- Image-generation pipeline.

## System Design Templates

### 1. LLM Chatbot at Scale

Core architecture:

```text
client
  -> API gateway and auth
  -> conversation service
  -> prompt/context builder
  -> safety checks
  -> LLM inference
  -> output moderation
  -> streaming response
  -> logs, evals, and feedback
```

Must cover:

- Session and conversation state.
- Streaming and TTFT.
- Token budgeting and history compression.
- Safety and abuse controls.
- Caching.
- Evaluation and logging.
- Cost and latency awareness.

Bar-raiser moves:

- Model routing by query difficulty.
- KV-cache reuse and continuous batching.
- Multi-region and provider failover.
- Prompt-injection defense.
- Online and offline eval harness.
- Capacity math using tokens per request and requests per second.

### 2. Enterprise RAG Assistant

Core architecture:

```text
documents
  -> ingestion
  -> chunking
  -> embeddings
  -> vector and lexical indexes

query
  -> access control
  -> retrieval
  -> reranking
  -> grounded prompt
  -> LLM
  -> cited answer
  -> feedback and evals
```

Must cover:

- Ingestion and re-indexing.
- Chunking strategy.
- Embedding model and vector store.
- Hybrid search and reranking.
- Citations and provenance.
- ACL filtering and tenant isolation.
- Faithfulness and retrieval evals.

Bar-raiser moves:

- Query rewriting and multi-hop retrieval.
- RAG versus fine-tuning trade-off.
- Deletion and compliance.
- Confidence and abstention.
- Semantic response caching.
- Agentic RAG, where the model decides when and what to retrieve.

### 3. LLM Inference and Serving Platform

Core architecture:

```text
gateway
  -> scheduler and queue
  -> inference workers
  -> streaming output
  -> telemetry and billing
```

Must cover:

- GPU model hosting.
- Batching.
- KV-cache.
- Autoscaling.
- TTFT, TPOT, p50, p95, p99.
- Throughput in tokens per second.
- Cost per request.

Bar-raiser moves:

- Continuous batching.
- PagedAttention or RadixAttention.
- Speculative decoding.
- Prefill/decode disaggregation.
- Quantization with quality gates.
- Multi-tenancy, fairness, and rate limits.
- Canary rollout and model-version routing.
- GPU scarcity and fallback planning.

### 4. Agentic Support Workflow

Core architecture:

```text
ticket
  -> classifier
  -> orchestrator
  -> KB/RAG tools
  -> order/refund/escalation tools
  -> guardrails
  -> draft or action
  -> human approval
  -> trace and feedback
```

Must cover:

- Autonomy level.
- Tool interfaces and permissions.
- State per ticket.
- Human-in-the-loop.
- Guardrails for side effects.
- Task success evaluation.

Bar-raiser moves:

- Justify agent versus fixed workflow.
- Keep control flow in the orchestrator, not only in the prompt.
- Use idempotency keys for side-effecting actions.
- Add retries, reconciliation, and rollback.
- Add termination logic and step budgets.
- Roll out from shadow mode to draft-only to limited auto-action.

### 5. Multi-Agent Research System

Core architecture:

```text
query
  -> orchestrator
  -> search agents
  -> extraction agents
  -> synthesis agent
  -> citation verifier
  -> final report
```

Must cover:

- Task decomposition.
- Parallel versus sequential execution.
- Shared memory or scratchpad.
- Citation tracking.
- Aggregation and conflict resolution.
- Factuality and citation evals.

Bar-raiser moves:

- Justify multi-agent cost.
- Add budget caps and loop detection.
- Handle partial sub-agent failure.
- Use verifier gates before final output.
- Trace every claim to source evidence.
- Prefer a single-agent design when multi-agent overhead is not justified.

## Metrics Cheat Sheet

Offline and model metrics:

- Precision, recall, F1, ROC-AUC, PR-AUC.
- MRR, mAP, nDCG, precision@k, recall@k.
- BLEU, ROUGE, groundedness, faithfulness, helpfulness, toxicity.

Agent metrics:

- Task completion.
- Tool-call correctness.
- Tool-argument validity.
- Step efficiency.
- Termination quality.
- Human escalation rate.
- Action error rate.
- Trace-level quality.

Serving metrics:

- TTFT.
- TPOT.
- End-to-end p50, p95, p99.
- Requests per second.
- Tokens per second.
- GPU utilization.
- Cost per request.
- Fallback rate.

Business metrics:

- Deflection rate.
- Resolution rate.
- Time to first response.
- Conversion or task success.
- User satisfaction.
- Revenue lift.
- Negative feedback and reports.

## Interview Question Bank

Use these as practice prompts. Do not paste all answers from memory; practice the five-step framework.

### GenAI System Design

- Design an LLM chatbot at scale.
- Design an LLM-powered enterprise search or RAG assistant.
- Design a large-scale LLM inference and serving platform.
- Design an on-device or small-model LLM assistant.
- Design cross-conversation memory for a chat assistant.
- Design a real-time LLM search engine.
- Design a content or policy-violation moderation system.
- Design a recommendation or ranking system.

### Agentic AI System Design

- Design a multi-step agentic workflow for support-ticket triage and resolution.
- Design an agent that drafts customer replies and escalates complex cases.
- Design a multi-agent research system that produces a cited report.
- Design an AI coding assistant that reads code and suggests improvements.
- Design a unified agent over email, calendar, docs, and chat.
- Design guardrails for an agent with access to private tools.

### Inference and Cost Probes

- Scale an AI chat feature to 1M daily active users and cut cost.
- Your app receives 1M LLM queries per day. How do you optimize cost?
- What is KV-cache and how does it help inference?
- When would you use batching, continuous batching, quantization, or speculative decoding?
- How would you reduce p99 latency without reducing answer quality?
- How would you route between small and large models?

## Practice Routine

For each prompt:

1. Spend 5 minutes framing users, constraints, metrics, and scope.
2. Draw the high-level architecture.
3. Pick three deep dives.
4. List five failure modes and how to detect them.
5. Do one rough cost or capacity calculation.
6. End with rollout, ownership, and next iteration.

Self-grade against:

- Did you define success?
- Did you include evals and monitoring?
- Did you include safety and privacy?
- Did you discuss cost and latency?
- Did you defend trade-offs?
- Did you avoid unnecessary complexity?
