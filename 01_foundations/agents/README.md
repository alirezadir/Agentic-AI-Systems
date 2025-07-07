# Agents & Agentic AI Systems
This page provides an overview of agents and agentic AI systems. 
There is no single definition of an AI agent, but there are some common characteristics.

There is a lot of confusion about the difference between agents and LLM workflows. This page aims to clarify the differences and provide a comprehensive overview of agents.



## 1. Agent Definitions
Here are some definitions of an agent from different sources:

#### Anthropic: 
<img src="../../assets/agents/agent-anthropic.png" alt="Agents" width="110%" />

An **agent** is an LLM system with dynamic control over tools, memory, and the flow of tasks. Key characteristics include:

- **Autonomous Planning and Operation:** Agents independently plan and execute actions, but can return to a human for additional information or judgment when needed.
- **Tool Use in a Feedback Loop:** Agents typically use tools (APIs, code execution, etc.) in a loop, making decisions based on feedback from the environment.
- **Grounded Decision-Making:** At each step, agents obtain "ground truth" from the environment (e.g., results from tool calls or code execution) to assess progress and inform next actions.
- **Human-in-the-Loop Capability:** Agents can pause at checkpoints or when encountering blockers to request human feedback or intervention.
- **Flexible Task Termination:** Tasks are completed when a goal is reached or a stopping condition is met (such as a maximum number of iterations or a time limit).

#### OpenAI: 
- Agents represent **systems that intelligently accomplish tasks**, ranging from executing simple workflows to pursuing complex, open-ended objectives. 

- Agents Components
    - **Models**: Handle reasoning, decision-making, and process various modalities.
    - **Tools**: Extend agent capabilities using hosted tools, function tools, or other agents.
    - **Knowledge and Memory**: Provide external or persistent knowledge to agents.
    <!-- - **Audio and Speech**: Enable audio or speech-based interactions. -->
    - **Guardrails**: Ensure safety and relevance through input/output validations.
    - **Orchestration**: Manage workflows and task delegation across multiple agents.

<!-- **LangGraph**:  -->

#### Langgraph (Augmented LLM vs an Agent)
- Augmented LLM
<img src="../../assets/agents/augmented_llm.png" alt="Agents" width="60%" />

- Agent (action with a feedback loop)
<img src="../../assets/agents/agent-def.png" alt="Agents" width="70%" />

#### AI engineering Book (Chip Huyen): 
* **Agents**: autonomous systems that:  a) **perceive an environment** and 2) **take actions** upon the environment, to achieve goals.
  - *Environment*: e.g. a game, computer, files, internet, road, etc
  - *Set of Actions*: via **Tools** that agents have access to
    - Set of Actions depend on the environment: e.g. actions a chess player agent can take (limited to chess game) 
* **AI Agents**: accomplish tasks provided by a user input: 
  - AI: perceive information (task, feedback from environment), plan a sequence actions
  * **AI Agent = Model + Memory + Tools access + Control Flow**

  * Key capabilities:

    * Interact with digital / physical environments.
    * Invoke & combine tools to augment abilities.
    * Plan, reflect, and iterate based on feedback.
    * Support both read (perceive) and write (act) actions (e.g., send emails, execute code).


** See [🤖  Agents in AI Engineering](./huyen-agents.md) for more details. **

---
## 2. LLM Workflows vs Agents 

<img src="../../assets/agents/agent-not-agent.jpeg" alt="Agents" width="90%" />

*Figure: Agent vs Not Agent. Adapted from []).*

<img src="../../assets/agents/llm-workflow-vs-agent.png" alt="Agents" width="80%" />

---
## 3. Agents vs Agentic AI Systems
- Agents are a subset of agentic AI systems. There are many different definitions of agentic AI, but they all share some common characteristics. 
- Mainly agentic AI systems are composed of multi-agent systems with multi-agent orchestration,  and higher levels of autonomy, and more complex control goals. 






<img src="../../assets/agents/agents-vs-agentic-ai.png  " alt="Agents" width="100%" />

*Figure: Agents vs Agentic AI. Adapted from []).*





---
## 4. Evolution of AI Agents


#### Hugging Face: 
<img src="../../assets/agents/agents-5-levels.png" alt="Agents" width="110%" />

*Figure: Hugging Face Agentic AI. Adapted from []).*

<img src="../../assets/agents/agent-evolution.jpeg" alt="Agents" width="90%" />

*Figure: Agentic AI Evolution. Adapted from [Rakesh Gohel]).*





