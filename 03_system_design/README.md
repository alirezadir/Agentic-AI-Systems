# Chapter 2: GenAI and Agentic System Design

This chapter is the system-design backbone of the repo. It turns the foundations into architecture decisions: how to design compound AI systems, RAG systems, agentic workflows, multimodal products, coding agents, long-running agents, eval loops, safety controls, and cost-aware production paths.

The goal is a self-contained design chapter: a reader should be able to start here, learn the reusable patterns, and practice interview-quality designs without jumping across unrelated folders.

## Design Lens

Modern GenAI products are compound systems:

```text
user/task
  -> product/API layer
  -> router or orchestrator
  -> context builder
  -> retrieval, memory, tools, and policies
  -> model or agent loop
  -> validation, evals, and guardrails
  -> response/action
  -> traces, metrics, feedback, and iteration
```

The model matters, but the design quality usually comes from the surrounding system: context, control flow, tools, memory, evals, observability, security, and cost controls.

## Learning Path

| Order | Topic | What to Learn | Current Notes |
|-------|-------|---------------|---------------|
| 1 | 2026 system-design shift | Harnesses, background agents, AgentOps, protocols, security, and cost-aware design. | [2026 Agentic AI System Design Update](./2026-agentic-ai-system-design.md) |
| 2 | Architecture framework | How to structure a full GenAI or agentic system-design answer. | [Architectures](./architectures/README.md), [12-Step Agentic System Design](./architectures/ASD-12-step-v1.5.md) |
| 3 | Compound AI systems | How models, tools, retrieval, orchestration, evals, and UI compose into products. | [Cookbooks](./cookbooks/README.md), [Compound AI Systems](./cookbooks/compund-ai-systems.md) |
| 4 | RAG and knowledge systems | Ingestion, chunking, hybrid retrieval, reranking, citations, agentic RAG, and ACLs. | [RAG Architectures](./RAGs/README.md) |
| 5 | Agent architecture | Planning, tool use, human approval, durable state, background execution, and multi-agent patterns. | [Design Patterns](./design-patterns/agentic-ai-design-patterns.md), [Durable Agents](./architectures/durable-background-agents.md) |
| 6 | Memory and state | Context, state, memory stores, consolidation, forgetting, and privacy. | [Memory](./memory/README.md) |
| 7 | Evals and AgentOps | Offline evals, online evals, trace replay, observability, incident response, and product metrics. | [Evals](./evals/README.md), [AgentOps](./evals/agentops.md) |
| 8 | Protocols and interoperability | MCP, A2A-style handoff, tool gateways, registries, auth, and trust boundaries. | [Protocols](./protocols/README.md) |
| 9 | Interview practice | Repeatable answer framework, system templates, metrics, and question bank. | [Interview Prep](./interview-prep/README.md) |

## Core Design Questions

Use these questions for every GenAI or agentic system:

1. **What is the product contract?**
   Users, jobs-to-be-done, success metrics, latency budget, cost budget, safety constraints, and launch scope.
2. **What owns control flow?**
   Deterministic workflow, model planner, graph orchestrator, background worker, or hybrid.
3. **What context does the model see?**
   User state, retrieved evidence, memory, policies, tool outputs, conversation history, and compression strategy.
4. **What can the system do?**
   Read-only tools, write tools, code/browser tools, other agents, approvals, idempotency, and rollback.
5. **How is truth grounded?**
   Source-of-truth data, retrieval, citations, provenance, confidence, abstention, and verifier gates.
6. **How is behavior evaluated?**
   Offline evals, online monitoring, task success, safety events, human feedback, and regression suites.
7. **How does it fail safely?**
   Prompt injection, bad retrieval, invalid tool calls, stale memory, retries, timeouts, escalation, and incident response.
8. **How does it scale economically?**
   Model routing, caching, context pruning, batching, smaller models, token budgets, and cost per successful task.

## System Types Covered

### Compound GenAI Systems

Systems that combine models with retrieval, tools, deterministic code, UI, evals, and feedback loops. Examples: chatbots, enterprise copilots, search assistants, document processors, coding assistants, and workflow automation.

### RAG and Knowledge Systems

Systems where correctness depends on external knowledge. Design concerns: ingestion, ACLs, chunking, embeddings, hybrid search, reranking, citations, freshness, deletion, and groundedness evals.

### Agentic Systems

Systems where a model can choose actions through tools. Design concerns: autonomy level, tool permissions, control flow, memory, human approval, durable state, traceability, and rollback.

### Multimodal Systems

Systems that reason over documents, images, screenshots, audio, video, charts, or UI state. Design concerns: perception reliability, artifact metadata, multimodal retrieval, safety, and source grounding.

### Coding and Computer-Use Agents

Systems that read codebases, edit files, operate browsers/desktops, run tests, or use developer tools. Design concerns: sandboxing, permissions, diff review, test verification, repo context, and user approval.

## Chapter Boundary

This chapter focuses on system design. It should include compact patterns, diagrams, trade-offs, and interview-ready structure.

- Foundations belong in [Chapter 1](../01_foundations/README.md).
- Production platform details belong in the upcoming Prototype to Production chapter.
- Runnable framework tutorials and code-heavy walkthroughs belong in the hands-on appendix.
- Curated links belong in [Resources](../RESOURCES.md).

## Phase 2 Migration Notes

In this phase:

- Interview prep moved into this chapter under [`interview-prep/`](./interview-prep/README.md).
- The chapter landing page now frames GenAI and agentic system design together.
- Existing architecture, RAG, eval, memory, protocol, and pattern notes remain in place while they are refactored one subchapter at a time.
