# Frameworks & Tools

This directory contains comprehensive documentation, guides, tutorials, and code examples for building AI agents using specific frameworks and tools. Each subfolder provides examples, starter templates, and best practices for building agentic AI systems with that framework.

### Contents:

- [OpenAI Agents](./1_openai/README.md): Comprehensive documentation, guides, tutorials ([docs](./1_openai/docs/)), and code examples ([codes](./1_openai/code/README.md)) for building AI agents using the OpenAI API and **Agents SDK** (released March 11, 2025). The Agents SDK is a lightweight, Python-first, open-source framework for orchestrating single-agent and multi-agent workflows. Features include Responses API, built-in tools (web search, file search, computer use), handoffs, guardrails, sessions, and integrated tracing/observability.
- [LangChain](./2_langchain/README.md): Examples using the LangChain framework. **LangChain reached v1.0 on October 22, 2025**, providing a standard tool calling architecture, provider-agnostic design, and middleware for production deployments. Key features include `create_agent` abstraction, standard content blocks, and streamlined package surface area. Python 3.10+ required.
- [LangGraph](./3_langgraph/README.md): Workflows and graph-based agent flows with LangGraph. **LangGraph reached v1.0 on October 22, 2025**, marking the first stable major release in the durable agent framework space. It offers node-based architecture for building multi-agent systems with structured state management, durable state persistence, built-in persistence for saving/resuming workflows, and human-in-the-loop patterns. LangGraph Platform enables teams to run agent workflows at scale with tools to track, debug, and manage them in production.
- [LlamaIndex](./4_llamaindex/README.md): Integrations and workflows using LlamaIndex for building agentic systems and RAG applications.
- [Crew AI](./5_crewai/README.md): Orchestration and collaboration with CrewAI for multi-agent team workflows.
- [Anthropic](./7_anthropic/README.md): Building agents with Anthropic's Claude API, including Claude Skills and the Model Context Protocol (MCP).
- [UI Tools](./6_ui_tools/README.md): UI demos and chat interfaces for agentic systems.

### Framework Comparison (2025)

When choosing a framework for your agentic AI system, consider:

- **OpenAI Agents SDK (March 11, 2025)**: Best for teams using OpenAI models who want a lightweight, Python-first framework with minimal abstractions. Features Responses API, built-in tools, handoffs, guardrails, and integrated tracing. Production-ready upgrade of Swarm framework.
- **LangChain v1.0 (October 22, 2025)**: Ideal for teams needing maximum control over workflows across any model/provider with extensive integrations. Fastest way to build an AI agent with standard tool calling architecture and middleware for customization.
- **LangGraph v1.0 (October 22, 2025)**: Excellent for complex, stateful multi-agent workflows requiring structured state management, durable state persistence, and visual debugging. First stable major release in durable agent framework space.
- **LlamaIndex**: Strong choice for RAG-focused applications and data-centric agent systems, with Agentic Document Workflows (ADW) for end-to-end document processing automation.
- **CrewAI**: Best for collaborative multi-agent scenarios where agents work as a team with defined roles, hierarchical structures, and robust memory systems.

Each subfolder contains its own docs and example codes. 