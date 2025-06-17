- **Agents**:  
  <!-- - Learn how to build agents with the OpenAI API.   -->
  - Agents represent **systems that intelligently accomplish tasks**, ranging from executing simple workflows to pursuing complex, open-ended objectives.  
  - OpenAI provides a **rich set of composable primitives that enable you to build agents**.

- **Overview**: Building agents involves assembling components across several domains:

  | Domain               | Description                                                                 | OpenAI Primitives                                           |
  |----------------------|-----------------------------------------------------------------------------|-------------------------------------------------------------|
  | **Models**           | Core intelligence capable of reasoning, making decisions, and processing different modalities. | o1, o3-mini, GPT-4.5, GPT-4o, GPT-4o-mini                   |
  | **Tools**            | Interface to the world, interact with environment, function calling, built-in tools, etc.    | Function calling, Web search, File search, Computer use     |
  | **Knowledge and memory** | Augment agents with external and persistent knowledge.                   | Vector stores, File search, Embeddings                      |
  | **Audio and speech** | Create agents that can understand audio and respond back in natural language. | Audio generation (realtime), Audio agents                   |
  | **Guardrails**       | Prevent irrelevant, harmful, or undesirable behavior.                        | Moderation, Instruction hierarchy                           |
  | **Orchestration**    | Develop, deploy, monitor, and improve agents.                                | Agents SDK, Tracing, Evaluations, Fine-tuning               |
  | **Voice agents**     | Create agents that can understand audio and respond back in natural language. | Realtime API, Voice support in the Agents SDK               |

- **Models**:

  | Model         | Agentic Strengths                                             |
  |---------------|---------------------------------------------------------------|
  | o1 and o3-mini| Best for long-term planning, hard tasks, and reasoning.       |
  | GPT-4.5       | Best for agentic execution.                                   |
  | GPT-4o        | Good balance of agentic capability and latency.               |
  | GPT-4o-mini   | Best for low-latency.                                         |

  **Capabilities**:  
  - **High intelligence:** Capable of reasoning and planning to tackle the most difficult tasks.  
  - **Tools:** Call your functions and leverage OpenAI's built-in tools.  
  - **Multimodality:** Natively understand text, images, audio, code, and documents.  
  - **Low-latency:** Support for real-time audio conversations and smaller, faster models.

- **Tools**:

  | Tool             | Description                                         |
  |------------------|-----------------------------------------------------|
  | Function calling | Interact with developer-defined code.               |
  | Web search       | Fetch up-to-date information from the web.          |
  | File search      | Perform semantic search across your documents.      |
  | Computer use     | Understand and control a computer or browser.       |

- **Knowledge and memory**:  
  - **Vector stores** enable agents to search your documents semantically and retrieve relevant information at runtime.  
  - **Embeddings** represent data efficiently for quick retrieval, powering dynamic knowledge solutions and long-term agent memory.

- **Guardrails**:  
  - Use OpenAI’s free **Moderation API** to automatically filter unsafe content.  
  - Leverage the **instruction hierarchy** to prioritize developer-defined prompts and mitigate unwanted agent behaviors.

- **Orchestration**:

  | Phase                | Description                                                                                     | OpenAI Primitives                |
  |----------------------|-------------------------------------------------------------------------------------------------|----------------------------------|
  | Build and deploy     | Rapidly build agents, enforce guardrails, and handle conversational flows using the Agents SDK. | Agents SDK                       |
  | Monitor              | Observe agent behavior in real-time, debug issues, and gain insights through tracing.           | Tracing                          |
  | Evaluate and improve | Measure agent performance, identify areas for improvement, and refine your agents.             | Evaluations, Fine-tuning         |

- **Get started**:

  ```bash
  pip install openai-agents
  ```