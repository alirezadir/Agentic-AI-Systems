# System Design for Agentic AI Systems

This directory provides concise resources for designing, building, and evaluating agentic AI systems. Each subdirectory contains focused guides, patterns, and real-world examples.

**Latest Updates (2026):**
- Agentic systems are shifting from prompt/context engineering toward production harnesses: orchestration, scheduling, state, memory, tool execution, evals, observability, and cost controls.
- Long-running and background agents need durable task state, approval flows, checkpointing, and cancellation.
- AgentOps and eval-driven development are now core system design topics, not optional add-ons.
- Protocols like MCP and A2A are becoming standard infrastructure for tool and agent interoperability.
- Security now includes prompt injection, tool poisoning, memory poisoning, scoped permissions, and auditability.

## Directory Overview

- **[Architectures](./architectures/README.md):** System blueprints and the 12-Step Agentic System Design. Includes AI-native architectures and enterprise patterns.
- **[2026 Agentic AI System Design Update](./2026-agentic-ai-system-design.md):** Current production patterns for harness engineering, background agents, context engineering, AgentOps, protocols, security, and inference cost.
- **[Durable and Background Agents](./architectures/durable-background-agents.md):** Architecture for scheduled, resumable, approval-aware, long-running agents.
- **[Design Patterns](./design-patterns/agentic-ai-design-patterns.md):** Comprehensive patterns and code examples for agentic systems. Updated with 2025 enterprise patterns including multi-agent architectures, agentic RAG patterns, and computer-using agent designs.
- **[Cookbooks](./cookbooks/README.md):** Practical guides and tutorials from leading organizations (Anthropic, OpenAI, Google).
- **[Agents](../01_foundations/agents/README.md):** Agentic system agent definitions and resources.
<!-- - **[Layers](./layers/README.md):** Cognitive and reasoning layer designs. -->
- **[RAGs](./RAGs/README.md):** Retrieval-Augmented Generation architectures, including **Agentic RAG** (the future of RAG in 2025), multi-modal RAGs, and advanced RAG patterns.
- **[Evals](./evals/README.md):** Comprehensive agent evaluation frameworks, benchmarks, and tools (2025 updates).
- **[AgentOps](./evals/agentops.md):** Observability, trace replay, online evals, cost monitoring, alerts, and incident response for deployed agents.
- **[Protocols](./protocols/README.md):** Communication standards for agentic systems, including Model Context Protocol (MCP).
- **[Memory](./memory/README.md):** Memory system documentation and implementation patterns.
<!-- - **[_agent_ops](./_agent_ops/README.md):** Agent operations and monitoring tools. -->


*Use this directory as a starting point for robust, scalable agentic AI system design. See each folder for details and implementation examples.*
