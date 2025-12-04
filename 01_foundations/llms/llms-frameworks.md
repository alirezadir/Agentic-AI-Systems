
## LLMs
###  LLM Model Selection 

Source: [Panaverse  Which LLM](https://github.com/panaversity/learn-agentic-ai/tree/main/-01_lets_get_started/00_which_llm)

- LLMs Leaderboard
    - [chatbot-arena-leaderboard](https://huggingface.co/spaces/lmarena-ai/chatbot-arena-leaderboard)
    
##  LLM Selection Criteria

When choosing a Large Language Model (LLM) for agentic AI applications, consider the following:

- **Performance**  Accuracy and reliability in output.
- **Cost**  Token pricing and operational expense.
- **Latency**  Response speed for interactive use.
- **Context Window**  How much input the model can handle.
- **Customization**  Support for fine-tuning and task adaptation.
- **Licensing**  Open-source availability and usage restrictions.

##  Recommended LLMs by Use Case (2025)

| **Use Case**                    | **Recommended LLM** | **Why**                                                                 |
|----------------------------------|----------------------|-------------------------------------------------------------------------|
| General-purpose applications     | **OpenAI GPT-4o**    | High performance, multimodal capabilities, and broad task coverage      |
| Cost-sensitive projects          | **Mistral**          | Affordable with strong capabilities                                     |
| Open-source required             | **Meta LLaMA 3**     | Open license, active community, strong performance                      |
| Multimodal input (text + image)  | **Google Gemini 1.5**| Designed for handling diverse data types, long context windows         |
| Compliance and safety focus      | **Anthropic Claude 3.5** | Prioritizes alignment, ethical reasoning, and safer outputs            |
| Computer-using agents            | **GPT-4o, Claude 3.5** | Vision-language models with advanced reasoning capabilities            |
| Long context tasks               | **Gemini 1.5 Pro**   | Up to 2M token context window                                            |

Choose your LLM based on **your project's needs**: balance **cost, speed, licensing, and capabilities**. For most general use, **GPT-4o** and **Claude 3.5** are top-tier in 2025. For open-source or budget-friendly setups, **LLaMA 3** or **Mistral** are strong contenders.

### LLMs (2025 Updates)
- **Best for general use:** OpenAI GPT-4o, Claude 3.5 Sonnet
- **Best for code generation:** GPT-4o, Claude 3.5 Sonnet, Code Llama 3
- **Best for chatbots:** GPT-4o, Claude 3.5 Sonnet
- **Best for open source:** LLaMA 3.1, Mistral Large 2
- **Best for long context:** Gemini 1.5 Pro (2M tokens), Claude 3.5 Sonnet (200K tokens)
- **Best for vision/multimodal:** GPT-4o, Gemini 1.5 Pro, Claude 3.5 Sonnet
- **Best for computer-using agents:** GPT-4o (Operator), Claude 3.5 Sonnet

### Embeddings (2025)
- **Best for general use:** OpenAI text-embedding-3-large, text-embedding-3-small
- **Best for semantic search:** Cohere Embeddings, OpenAI Embeddings
- **Best for open source:** Hugging Face Sentence Transformers (e.g., all-MiniLM-L6-v2, all-mpnet-base-v2)
- **Best for multimodal:** OpenAI CLIP embeddings, Open CLIP

### APIs
- **Best for general use:** OpenAI API
- **Best for open source:** Hugging Face Inference API
- **Best for Google Cloud users and integrations:** Google Vertex AI

## Agent Frameworks (2025)

- **OpenAI Agents SDK (March 11, 2025): Best overall for most users:** 
    - Lightweight, Python-first, open-source framework with minimal abstractions
    - Features Responses API, built-in tools (web search, file search, computer use), handoffs, guardrails, sessions
    - Production-ready with integrated tracing and observability
    - Direct upgrade from Swarm framework
- **LangGraph v1.0 (October 22, 2025): Best for complex workflows and state management:** 
    - Graph-based workflows, explicit state management, durable state persistence
    - First stable major release in durable agent framework space
    - LangGraph Platform enables teams to run agent workflows at scale with production tools
- **LangChain v1.0 (October 22, 2025): Best for provider-agnostic workflows:**
    - Standard tool calling architecture, works with any model/provider
    - `create_agent` abstraction, standard content blocks, middleware for customization
    - Extensive integrations and streamlined package surface area
    - Python 3.10+ required (3.9 support dropped)
- **CrewAI: Best for Multi-Agent Collaboration:** 
    - Role-based agents, team structure, built-in task and collaboration support
- **AutoGen: Best for conversation design and prototyping:** 
    - Strong support for conversational patterns, human-in-the-loop, flexible chats
- **LlamaIndex: Best for RAG-focused agent systems:**
    - Strong integration with vector databases and retrieval systems
- **Google ADK: Best for Google Cloud users and integrations**

<!-- | Framework           | Summary                                                                                     |
|---------------------|---------------------------------------------------------------------------------------------|
| OpenAI Agents SDK   | Very simple and flexible. Easy to learn. Gives you direct control with minimal abstraction. Best for Python developers. |
| CrewAI              | Focuses on teamwork between agents. Slightly more complex but still accessible. Balances simplicity and control. |
| AutoGen             | Designed for conversation-based agents. Medium learning curve, good for interactive and human-involved tasks. |
| Google ADK          | Google Cloud-based with strong tooling. Supports complex agent setups. Moderate learning effort, slightly higher control. |
| LangGraph           | Uses graphs to define workflows. Very powerful but complex and harder to learn. Requires explicit state control. | -->
<!-- | Dapr Agents         | Event-driven and cloud-native. Good for resilient, distributed systems. Medium complexity, designed for scalable deployments. | -->
## Prompting
[GPT-4 Prompting Guide](https://cookbook.openai.com/examples/gpt4-1_prompting_guide)

## Agents (2025 Updates)

- [Evolution of agentic AI](https://www.linkedin.com/posts/rakeshgohel01_how-did-the-agentic-ai-era-evolve-in-the-activity-7310276654218493953-8G4v/)
- [From LLMs to Stateful Long-Running Multi-Agent Systems](https://github.com/panaversity/learn-agentic-ai/blob/main/-01_lets_get_started/03_from_llms_to_stateful_long_runningl_multi_agents/01_what_are_multi_agent_systems.md)

### Protocols
- **MCP (Model Context Protocol)**: Standard protocol that manages the context and state of the LLM during interactions (resources, tools, memory, role, goals, etc.). Widely adopted in 2025 by OpenAI, Anthropic, and other providers.
- **A2A (Agent-to-Agent)**: Agent-to-Agent communication protocol (from, to, type, content, etc.) for multi-agent systems.

### Trends (2025)
- **AI agents are replacing SaaS and traditional software apps** in many domains
- **Vertical agents** (e.g., for finance, healthcare, legal) are becoming more common than general-purpose (horizontal) agents
- **Computer-Using Agents (CUA)** are emerging as a major category, enabling agents to interact with computer interfaces
- **Agentic RAG** represents the evolution from static retrieval to dynamic, intelligent knowledge systems
- **Standardized evaluation frameworks** have emerged for production agent systems