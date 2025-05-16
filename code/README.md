# Gen-AI Engineering Repository

This repository contains a collection of frameworks, applied examples, and utilities for building and deploying generative AI applications, with a focus on agent-based systems and large language model applications.

## Repository Structure

```
code/
├── frameworks/                  # Tool-specific demos and templates
│   ├── openai/                  # OpenAI SDK, Responses API, Assistants
│   ├── langgraph/               # LangGraph workflows
│   ├── crewai/                  # CrewAI agent orchestration
│   ├── langchain/               # LangChain examples
│   ├── chainlit/                # UI demos for agents
│   └── dapr/                    # Dapr workflows for agent orchestration
│
├── applied/                     # Real-world, end-to-end agentic apps
│   ├── customer_support_bot/    # LLM + vector DB + function calling
│   ├── legal_doc_analyzer/      # File tools + RAG + summarizer
│   ├── multi_agent_researcher/  # Planner-agent collaboration
│   ├── finance_report_agent/    # Data analysis with LLM and charts
│   └── ai_pair_programmer/      # Coding assistant agents
│
└── utils/                       # Shared helpers/utilities across projects
    ├── memory.py                # Memory implementations for agents
    ├── tools.py                 # Reusable tools for function calling
    └── prompts.py               # Common prompt templates
```

## Getting Started

Choose a framework or applied example to start exploring. Each directory contains examples and documentation to help you understand the implementation details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

