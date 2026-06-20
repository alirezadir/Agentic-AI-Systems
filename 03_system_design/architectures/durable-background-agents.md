# Durable and Background Agents

Durable agents are agents that can keep working after the initial user request ends. They may wake up later, resume a task, monitor external systems, ask for approval, or recover from partial failure. This is one of the biggest practical differences between a chat assistant and a production agent.

## When You Need a Durable Agent

Use a durable agent when the task has at least one of these properties:

- It runs longer than a normal request/response interaction.
- It depends on future events or schedules.
- It performs multiple tool calls with side effects.
- It needs human approval before continuing.
- It must recover after model, tool, network, or process failure.
- It needs auditability for compliance or debugging.

Examples:

- Monitor GitHub issues and open a draft PR when a regression appears.
- Check a vendor portal every morning and summarize changes.
- Follow up on unanswered customer emails after 48 hours.
- Run weekly research and send a cited report.
- Triage support tickets and request approval before refunds.

## Reference Architecture

```text
trigger
  -> scheduler or event bus
  -> task registry
  -> policy and permission check
  -> durable orchestrator
  -> agent loop
  -> tool gateway
  -> checkpoint store
  -> approval queue
  -> trace and eval pipeline
  -> notification or final action
```

Core services:

- **Scheduler or event bus**: wakes the agent by time, webhook, queue event, or user action.
- **Task registry**: stores goal, owner, status, deadlines, budgets, permissions, and cancellation state.
- **Durable orchestrator**: owns control flow and persists each step.
- **Checkpoint store**: records state after each meaningful transition.
- **Tool gateway**: validates schemas, permissions, rate limits, idempotency keys, and audit logs.
- **Approval queue**: pauses execution until a human approves sensitive actions.
- **Trace pipeline**: captures model calls, tool calls, memory reads/writes, costs, and decisions.

## Task State Machine

```text
created
  -> scheduled
  -> running
  -> waiting_for_tool
  -> waiting_for_approval
  -> retrying
  -> completed

terminal states:
  cancelled
  expired
  failed
  blocked
```

State should be explicit. Do not infer task state from logs alone.

## Control Flow Rules

Durable agents need deterministic guardrails around nondeterministic reasoning:

- The orchestrator owns state transitions.
- The model may propose a plan, but the orchestrator validates it.
- Every side-effecting tool call must have an idempotency key.
- Every task needs a max step count, max cost, max runtime, and expiry.
- Every sensitive action needs a policy check and often human approval.
- Every retry needs a reason, attempt count, and backoff policy.
- Every resumed task should reload state from durable storage, not chat history.

## Memory and Context

Separate memory from task state:

- **Task state**: current plan, completed steps, pending approvals, tool results, failures.
- **Working memory**: short context needed for the next step.
- **Episodic memory**: previous task traces and outcomes.
- **Semantic memory**: stable facts, preferences, policies, and domain knowledge.

For long-running tasks, summarize context into structured state instead of relying on a growing transcript.

## Human Approval

Approval is not just a UI prompt. It is a control point in the architecture.

Approval records should include:

- Proposed action.
- Tool and arguments.
- User or tenant affected.
- Risk level.
- Evidence and citations.
- Cost or financial impact.
- Expiration time.
- Approver identity.
- Final decision and reason.

Common approval gates:

- Sending external messages.
- Spending money.
- Deleting or modifying data.
- Changing production configuration.
- Sharing private information.
- Executing code or shell commands.

## Failure Modes

| Failure | Detection | Mitigation |
| --- | --- | --- |
| Runaway loop | Step count, repeated tool sequence, cost spike | Step budget, loop detector, human escalation |
| Duplicate side effect | Repeated idempotency key or same target/action | Idempotency store, reconciliation job |
| Stale goal | Task age, changed source state, user cancellation | Expiry, pre-action state refresh |
| Tool outage | Timeout, error rate, circuit breaker | Backoff, alternate tool, human handoff |
| Permission drift | Credential or role changed since scheduling | Re-check permission before each action |
| Context pollution | Conflicting tool output, suspicious retrieved text | source ranking, prompt-injection checks |
| Silent quality drift | Falling eval score, rising escalation rate | Online evals, shadow runs, rollback |

## Design Checklist

- What wakes the agent?
- Where is durable task state stored?
- What are the terminal states?
- What are the cost, time, and step budgets?
- What side effects can happen?
- Which actions require approval?
- How are tool calls made idempotent?
- How does the system resume after a crash?
- How does a user cancel or inspect the task?
- Which traces and evals prove the agent behaved correctly?

## Interview Framing

For system design interviews, durable agents are a strong bar-raiser topic. Mention them when the prompt includes monitoring, follow-up, long-running work, or real-world actions.

Good senior/principal signals:

- Explicit state machine.
- Deterministic orchestrator around model reasoning.
- Idempotency and reconciliation for side effects.
- Budget caps and termination logic.
- Human approval path.
- Trace replay and online evals.
- Clear rollout path: shadow mode, draft-only, limited auto-action, broader automation.
