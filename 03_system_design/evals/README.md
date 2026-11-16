# Evals and AgentOps

Evaluation is the control system for GenAI and agentic products. It tells you whether a prompt, model, retrieval strategy, tool, memory policy, or orchestration change actually improved the system.

This section covers both pre-deployment evals and production AgentOps.

## Evaluation Stack

```text
unit checks
  -> component evals
  -> end-to-end task evals
  -> safety/adversarial evals
  -> online monitoring
  -> trace review and feedback
  -> regression datasets
```

AI evals are not a one-time benchmark. They are an engineering loop.

## What to Evaluate

| Layer | What to Measure | Example Metrics |
|-------|-----------------|-----------------|
| Model | Isolated model quality, latency, cost, schema adherence. | accuracy, rubric score, format validity, TTFT, TPOT, token cost |
| Retrieval | Whether the right evidence is found and ranked. | recall@k, precision@k, nDCG, citation coverage, ACL correctness |
| Context | Whether the model sees relevant, authorized, non-polluted context. | useful-token ratio, context length, injection blocks, source diversity |
| Tools | Whether tools are selected and called correctly. | tool selection accuracy, argument validity, tool error rate, retry rate |
| Agent loop | Whether the agent completes tasks efficiently and safely. | task success, step count, termination quality, recovery rate, approval rate |
| Memory | Whether memory is useful, correct, private, and forgettable. | memory precision, stale recall rate, write quality, deletion success |
| Safety | Whether the system blocks harmful behavior and data leakage. | policy violations, PII exposure, unsafe action attempts, injection success rate |
| Product | Whether users and the business get value. | CSAT, resolution rate, deflection, time saved, conversion, adoption |
| Operations | Whether the deployed system is reliable and economical. | p95 latency, cost per task, availability, fallback rate, incident count |

## Core Pages

- [GenAI Systems Evals](./gen-ai-evals.md): Evaluation methods for non-agentic GenAI systems.
- [Agentic AI Systems Evals](./agentic-ai-evals.md): Detailed metric catalog for agentic systems.
- [AI Product Evals](./ai-product-evals.md): Product-level quality and business metrics.
- [AgentOps](./agentops.md): Production observability, trace replay, online evals, alerts, and incident response.

## Evaluation Modes

### 1. Offline Evals

Run before deploy.

Use for:

- Prompt changes.
- Model changes.
- Retrieval/chunking changes.
- Tool schema changes.
- Memory policy changes.
- Guardrail changes.
- Regression tests after incidents.

Inputs:

- Golden datasets.
- Historical user tasks.
- Synthetic edge cases.
- Adversarial examples.
- Human-labeled examples.
- Production failure traces.

### 2. Component Evals

Evaluate the subsystem before blaming the whole product.

Examples:

- Retrieval recall before answer quality.
- Tool argument validity before task success.
- Memory read/write quality before personalization.
- Context packing before generation.
- Router accuracy before model comparison.

### 3. End-to-End Task Evals

Measure whether the user goal was completed.

Examples:

- Did the support ticket resolve correctly?
- Did the RAG assistant answer with valid citations?
- Did the coding agent produce a passing patch?
- Did the research agent produce a grounded report?
- Did the workflow stop or escalate at the right time?

### 4. Online Evals

Run on production traces.

Use for:

- Drift detection.
- Cost and latency monitoring.
- Safety event detection.
- User feedback queues.
- LLM-as-judge sampling.
- Human review sampling.
- Failure-to-regression conversion.

## LLM-as-Judge Guidance

Use model judges carefully. They are useful, not magic.

Good uses:

- Rubric-based quality scoring.
- Pairwise comparison.
- Style/tone checks.
- Groundedness checks with evidence supplied.
- Triage for human review.

Controls:

- Calibrate against human labels.
- Use explicit rubrics.
- Version prompts and judge models.
- Sample judge outputs for audit.
- Avoid using the same model as both generator and only judge for high-stakes decisions.

## Agent-Specific Evals

Agents need trajectory evals, not just final-answer evals.

Evaluate:

- Was the plan reasonable?
- Was the right tool selected?
- Were tool arguments valid?
- Were tool results interpreted correctly?
- Did the agent recover from errors?
- Did it stop at the right time?
- Did it request approval when required?
- Did it respect cost, time, and step budgets?
- Did it avoid unsafe or unauthorized actions?

Trace-level evaluation is often more useful than only scoring the final answer.

## Minimum Launch Gate

Before production launch, define:

- Golden task set.
- Safety/adversarial task set.
- Retrieval eval set if RAG is involved.
- Tool-call eval set if tools are involved.
- Human review rubric.
- Online monitoring dashboard.
- Incident-to-regression process.
- Rollback or draft-only fallback mode.

## AgentOps Loop

```text
production trace
  -> detect issue
  -> classify failure
  -> add to eval dataset
  -> fix prompt/retrieval/tool/orchestrator
  -> run regression evals
  -> staged rollout
  -> monitor again
```

The system improves only if failures become durable tests.

## Design Checklist

- What are the top user tasks?
- What does success mean for each task?
- Which components can fail independently?
- Which evals run before every release?
- Which evals run continuously in production?
- Who reviews ambiguous or high-risk cases?
- How are user corrections captured?
- How do incidents become regression tests?
- What dashboard proves quality, safety, latency, and cost?
- What is the rollback path when quality drops?
