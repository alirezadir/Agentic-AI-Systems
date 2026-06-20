# AgentOps

AgentOps is the operational discipline for deployed agentic systems. It combines observability, evaluation, safety monitoring, cost control, trace replay, incident response, and continuous improvement.

Traditional app monitoring answers:

- Is the service up?
- Is latency acceptable?
- Are errors increasing?

AgentOps also answers:

- Did the agent choose the right tools?
- Did it use the right arguments?
- Did memory or retrieved context influence the answer correctly?
- Did it stop at the right time?
- Did it ask for approval when required?
- Did it spend too much money?
- Can we replay the trajectory and explain the final action?

## Core Telemetry

Capture every meaningful execution unit:

| Unit | What to log |
| --- | --- |
| Task | task id, user, tenant, goal, status, trigger, budget, policy |
| Model call | model, prompt version, input tokens, output tokens, latency, cost |
| Tool call | tool name, arguments, result schema, latency, error, idempotency key |
| Retrieval | query, sources, scores, ACL filters, selected chunks, citations |
| Memory | read ids, write ids, confidence, retention policy, deletion state |
| Decision | route, plan step, approval request, refusal, escalation |
| Safety event | injection signal, PII flag, policy violation, blocked tool |
| Output | final answer, structured payload, citations, approval outcome |

## Trace Schema

A trace should be queryable by task, user, tenant, tool, model, cost, policy, and failure mode.

```json
{
  "trace_id": "tr_123",
  "task_id": "task_456",
  "tenant_id": "acme",
  "started_at": "2026-06-19T18:00:00Z",
  "status": "completed",
  "budget": {
    "max_steps": 12,
    "max_cost_usd": 1.5,
    "max_runtime_seconds": 300
  },
  "events": [
    {
      "type": "model_call",
      "model": "small-router",
      "latency_ms": 420,
      "input_tokens": 1200,
      "output_tokens": 80
    },
    {
      "type": "tool_call",
      "tool": "ticket_lookup",
      "idempotency_key": "task_456:ticket_lookup:1",
      "latency_ms": 210,
      "status": "ok"
    }
  ]
}
```

## Metrics

### Quality

- Task success rate.
- First-pass success rate.
- Groundedness score.
- Citation accuracy.
- Tool selection accuracy.
- Tool argument validity.
- Human correction rate.
- Escalation quality.

### Reliability

- Task completion rate.
- Timeout rate.
- Retry rate.
- Tool error rate.
- Fallback rate.
- Recovery rate.
- Duplicate side-effect rate.
- Availability by dependency.

### Efficiency

- Cost per task.
- Cost per successful task.
- Tokens per task.
- Tool calls per task.
- Steps per task.
- Runtime per task.
- Cache hit rate.
- Model routing distribution.

### Safety

- Unsafe action attempt rate.
- Prompt-injection detection rate.
- PII exposure rate.
- Policy block rate.
- Approval bypass rate.
- Memory poisoning detection rate.
- Cross-tenant access attempt rate.

## Offline and Online Evals

Offline evals are pre-deployment checks:

- Golden task suites.
- Historical trace replay.
- Regression tests for prompts, tools, and policies.
- Adversarial injection tests.
- Tool outage simulations.
- Side-effect dry runs.

Online evals run on production traces:

- Reference-free quality checks.
- Safety and policy checks.
- Anomaly detection.
- Cost and latency alerts.
- Human annotation queues.
- Failure-to-dataset conversion.

The key loop:

```text
production trace
  -> detect issue
  -> annotate or classify
  -> add to offline dataset
  -> fix prompt/tool/orchestrator
  -> regression eval
  -> staged rollout
  -> monitor again
```

## Dashboards

Minimum dashboards:

- Agent quality dashboard: success, groundedness, tool correctness, escalation.
- Cost dashboard: cost per task, tokens per task, model routing, cache hit rate.
- Reliability dashboard: timeouts, retries, dependency errors, fallbacks.
- Safety dashboard: blocked actions, prompt injection, PII, policy violations.
- Long-running task dashboard: scheduled, running, waiting for approval, expired, failed.

## Alerts

Useful alert patterns:

- Cost per successful task exceeds threshold.
- Tool error rate spikes.
- Step count or retry count rises.
- Prompt-injection detections spike from one source.
- Approval queue grows beyond SLA.
- Citation accuracy falls below threshold.
- Fallback model usage rises.
- Task expiry or cancellation rate rises.

## Incident Response

Agent incidents often involve side effects or data access. The runbook should include:

1. Freeze risky tools or switch agent to draft-only mode.
2. Identify affected users, tenants, tasks, and tool calls.
3. Replay traces for root cause.
4. Check whether any side effects need reversal or reconciliation.
5. Patch the control layer, not only the prompt.
6. Add the incident trace to regression evals.
7. Roll out gradually with extra monitoring.

## Rollout Strategy

Use staged autonomy:

1. **Shadow mode**: agent proposes actions but nothing is shown or executed.
2. **Draft mode**: agent drafts and a human sends.
3. **Approval mode**: agent can execute only after approval.
4. **Limited auto-action**: low-risk actions execute automatically.
5. **Broad auto-action**: only after strong evals, monitoring, and rollback paths exist.

## Practical Rule

If you cannot trace it, replay it, evaluate it, and stop it, it is not production-ready.
