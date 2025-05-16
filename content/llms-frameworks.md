
## LLMs
### 🔍 LLM Model Selection 

Source: [Panaverse – Which LLM](https://github.com/panaversity/learn-agentic-ai/tree/main/-01_lets_get_started/00_which_llm)

- LLMs Leaderboard
    - [chatbot-arena-leaderboard](https://huggingface.co/spaces/lmarena-ai/chatbot-arena-leaderboard)
    
## 📌 LLM Selection Criteria

When choosing a Large Language Model (LLM) for agentic AI applications, consider the following:

- **Performance** – Accuracy and reliability in output.
- **Cost** – Token pricing and operational expense.
- **Latency** – Response speed for interactive use.
- **Context Window** – How much input the model can handle.
- **Customization** – Support for fine-tuning and task adaptation.
- **Licensing** – Open-source availability and usage restrictions.

## 🏆 Recommended LLMs by Use Case

| **Use Case**                    | **Recommended LLM** | **Why**                                                                 |
|----------------------------------|----------------------|-------------------------------------------------------------------------|
| General-purpose applications     | **OpenAI GPT-4**     | High performance and broad task coverage                               |
| Cost-sensitive projects          | **Mistral**          | Affordable with strong capabilities                                     |
| Open-source required             | **Meta LLaMA**       | Open license and active community                                       |
| Multimodal input (text + image)  | **Google Gemini**    | Designed for handling diverse data types                                |
| Compliance and safety focus      | **Anthropic Claude** | Prioritizes alignment, ethical reasoning, and safer outputs             |

Choose your LLM based on **your project's needs**: balance **cost, speed, licensing, and capabilities**. For most general use, **GPT-4** remains top-tier. For open-source or budget-friendly setups, **LLaMA** or **Mistral** are strong contenders.

### LLMs
- **Best for general use:** OpenAI GPT-4, Claude 3
- **Best for code generation:** Code Llama
- **Best for chatbots:** ChatGPT 4.0
- **Best for open source:** LLaMA 3
- **Best for long context:** Gemini 1.5 Turbo

### Embeddings
- **Best for general use:** OpenAI Embeddings
- **Best for semantic search:** Cohere Embeddings
- **Best for open source:** Hugging Face Sentence Transformers

### APIs
- **Best for general use:** OpenAI API
- **Best for open source:** Hugging Face Inference API
- **Best for Google Cloud users and integrations:** Google Vertex AI

## Agent Frameworks
- **OpenAI Agents SDK: Best overall for most users:** 
    - Minimal abstraction, easy to learn, Python-native, direct control
- **CrewAI: Best for Multi-Agent Collaboration:** 
    - Role-based agents, team structure, built-in task and collaboration support
- **AutoGen: Best for conversation design and prototyping:** 
    - Strong support for conversational patterns, human-in-the-loop, flexible chats
- **LangGraph: Best for complex workflows and state management:** 
    - Graph-based workflows, explicit state management, powerful but complex
- **Google ADK: Best for Google Cloud users and integrations**

<!-- | Framework           | Summary                                                                                     |
|---------------------|---------------------------------------------------------------------------------------------|
| OpenAI Agents SDK   | Very simple and flexible. Easy to learn. Gives you direct control with minimal abstraction. Best for Python developers. |
| CrewAI              | Focuses on teamwork between agents. Slightly more complex but still accessible. Balances simplicity and control. |
| AutoGen             | Designed for conversation-based agents. Medium learning curve, good for interactive and human-involved tasks. |
| Google ADK          | Google Cloud-based with strong tooling. Supports complex agent setups. Moderate learning effort, slightly higher control. |
| LangGraph           | Uses graphs to define workflows. Very powerful but complex and harder to learn. Requires explicit state control. | -->
<!-- | Dapr Agents         | Event-driven and cloud-native. Good for resilient, distributed systems. Medium complexity, designed for scalable deployments. | -->
---
## Prompting
[GPT-4 Prompting Guide](https://cookbook.openai.com/examples/gpt4-1_prompting_guide)

---
## agents
- [Evolution of agentic AI](https://www.linkedin.com/posts/rakeshgohel01_how-did-the-agentic-ai-era-evolve-in-the-activity-7310276654218493953-8G4v/)
- [From LLMs to Stateful Long-Running Multi-Agent Systems](https://github.com/panaversity/learn-agentic-ai/blob/main/-01_lets_get_started/03_from_llms_to_stateful_long_runningl_multi_agents/01_what_are_multi_agent_systems.md)
- MCP (Model Context Protocol): MCP is a protocol that manages the context and state of the LLM during interactions (resources, tools, memory, role, goals, etc.).
- A2A: Agent-to-Agent communication protocol (from, to, type, content, etc.)


- AI agents will replace SaaS and traditional SW apps.
- vertical agents (e.g., for finance, healthcare, etc.) will be more common than general-purpose (horizontal) agents.