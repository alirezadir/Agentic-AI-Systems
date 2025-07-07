## Agentic AI Design Patterns 
- This page provides a comprehensive overview of design patterns in Gen-AI and agentic AI systems.
- It includes reusable design patterns and template codes for building agentic systems. Use these patterns as starting points or inspiration for structuring your own agentic AI applications.


##### Table of Contents

1. [Workflow Patterns](#1-workflow-patterns)
2. [Reasoning Patterns](#2-reasoning-patterns)
   2.1. [Self-Improving / Reflective Patterns](#21-reflective-reasoning-patterns)
3. [Retrieval-Augmented Generation (RAG) Patterns](#3-rag-patterns)
4. [Multi-Agent System Patterns](#4-multi-agent-patterns)
5. [Tool-Use Patterns](#5-tool-use-patterns)

<!-- ### Agentic Design Patterns
Reusable solutions to common problems in Agentic AI development.

- Reflection-based patterns
- Tool-use patterns
- Planning pattern
- Multi-agent patterns
- RAG patterns
- Symbolic reasoning patterns
- More: 
  - Hierarchical patternds 
  - Learning-Based patterns
  - Collaborative patterns ...  -->

## 1. Workflow Patterns

#### Prompt Chaining
- **Pattern**: Sequential prompt execution with conditional flow.
- **Flow**:  
  Input → LLM Call 1 → Output → Gate (Fail → Exit, Pass → LLM Call 2) → Final Output
- **Use Case**: Proofreading, Copywriting, Sequential execution logic
- [Code](./Code/basic_workflows.ipynb), [Langgraph](https://langchain-ai.github.io/langgraph/tutorials/workflows/#prompt-chaining)

#### Routing
- **Pattern**: Decision-based branching to different LLMs.
- **Flow**:  
  LLM Call 1 → Output evaluated → Routed to LLM Call 2/3/4 → Output
- **Use Case**: CRM agents, Agentic task delegation
- [Code](./Code/basic_workflows.ipynb), [Langgraph](https://langchain-ai.github.io/langgraph/tutorials/workflows/#routing)

#### Parallel Execution
- **Pattern**: Multiple LLMs called in parallel, then aggregated.
- **Flow**:  
  LLM Call 1 → Multiple LLM Call 2s (parallel) → Aggregator → Output
- **Use Case**: Vulnerability analysis, ensemble reasoning
- [Code](./Code/basic_workflows.ipynb), [Langgraph](https://langchain-ai.github.io/langgraph/tutorials/workflows/#parallelization)

#### Orchestrator-Workers
- **Pattern**: Orchestrator parses input, dynamically decomposes tasks, delegates subtasks to worker LLMs, then synthesizes their results.
- **Flow**:  
  Input → Orchestrator (parse & decompose) → Multiple Worker LLMs (execute subtasks, in parallel or sequence) → Synthesizer (aggregate/summarize results) → Output
- **Use Case**: Vulnerability analysis, ensemble reasoning
- [Code](./Code/orchestrator_workers.ipynb), [Langgraph](https://langchain-ai.github.io/langgraph/tutorials/workflows/#orchestrator-worker)

## 2. Reasoning Patterns

#### CoT Pattern
- **Pattern**: Chain-of-Thought reasoning
- **Category**: Step-by-step reasoning
- **Flow**:  
  Query → LLM (generates step-by-step reasoning) → Intermediate Steps → LLM (final answer synthesis) → Output
- **Use Case**: Used by most AI agents
- **Types**:
  - **Zero-shot CoT**: Add a trigger phrase like “Let’s think step by step” without examples
  - **Few-shot CoT**: Provide examples with step-by-step reasoning before the actual query
  - **Self-consistent CoT**: Sample multiple CoT outputs and pick the most common final answer
- **Variants**:
  - **Tree-of-Thought (ToT)**: *Tree-based reasoning*, where each node represents a possible "thought" or reasoning step, and branches represent alternative next steps.
    - **Code**: [Langgraph](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/tot/tot.ipynb)
  - **Graph-of-Thought (GoT)**: *Graph-based reasoning*, where nodes are thoughts and edges indicate inference or flow between them.


<!-- #### Tree-of-Thought (ToT) Pattern

- **Pattern**: Break down a problem into a tree structure, where each node represents a possible "thought" or reasoning step, and branches represent alternative next steps.
- **Flow**:  
  `Query → LLM generates multiple next-step thoughts → Tree expands (breadth/depth) → Each branch evaluated (by LLM or heuristic) → Best path selected → Final answer`
- **Use Cases**:  
  Creative writing, planning, program synthesis, logical puzzles, theorem proving, agent decision-making



#### Graph-of-Thought (GoT) Pattern

- **Pattern**: Represent reasoning as a directed graph, where nodes are thoughts and edges indicate inference or flow between them.
- **Flow**:  
  `Query → Construct thought nodes and reasoning edges → LLM explores, updates, or revisits nodes → Graph traversal and evaluation → Final synthesis`
- **Use Case**: Complex reasoning, iterative refinement, multi-agent systems, scientific exploration, compound workflows -->

#### ReAct Pattern
- **Pattern**: Interleaves Reasoning, Acting, and Observing. 
  - The LLM reasons, acts (e.g., uses tools), and integrates observations back into reasoning (in a loop). 
- **Category**: Iterative reasoning
- **Flow**:  
  - Query
    - **Reasoning** (analyze, plan, select tool) -> **Action** (invoke tool or API) -> **Observation** (receive result, update context)
  - Repeat steps above as needed
  - **Final Answer**
- **Use Case**:  
  - Foundation of modern agent frameworks; supports iterative, tool-augmented decision-making. 
  - Popular use case as **reasoning agent** and **supervisor agent**.
  - Implemented in systems like LangChain, OpenAI Agents SDK, the ReAct paper, AutoGPT, and more.
- Code: [Langchain](https://langchain-ai.github.io/langgraph/how-tos/react-agent-from-scratch/), [LlamaIndex](https://docs.llamaindex.ai/en/stable/examples/agent/react_agent/)

#### ReWoo (Reasoning With-Out Observations)

- **Pattern**: Symbolic Reasoning over Workflows: Plan first, execute all tool calls in parallel
  - LLM reasons *about* a workflow 
  - Decouples reasoning from execution 
  - Plans all tool calls upfront without observing intermediate outputs.
- **Category**: Symbolic pre-planning, parallel execution
- **How it Works**:
  - Input → LLM chooses symbolic actions/modules
  - Each module performs a sub-task (e.g., search, calculation, summarization) -> LLM coordinates these in structured reasoning steps
- **Flow**:
  1. Input → Planner (LLM)
  2. Planner → Symbolic Workflow (API/Tool/Model)
  3. Submodules execute (Parallel Tool Executions)
  4. Results fed back to LLM (Synthesizer)→ Final reasoning/output
- **Code**: [Langgraph](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/rewoo/rewoo.ipynb)
 
<!-- Query → LLM (Reason & Plan all tool calls) → Parallel Tool Executions → LLM (Synthesize using tool outputs) → Output -->

- **Benefits**:
  - **Interpretability** via symbolic ( structured, interpretable) steps
  - **Modularity** and low hallucination
- **Use cases**: 
  - Efficient for parallelizable, latency-sensitive, or deterministic agent tasks — e.g. search + retrieval, fact aggregation, batch queries.
  - Microsoft’s ReWoo, AutoGPT-style agents with module planners

#### CodeAct Pattern
- **Pattern**: Combines planning, acting, and tool-use in a loop using a sandbox.
- **Category**: Executable reasoning
- **Flow**:  

  - Query → Plan (CoT, Reflection) → generates code (LLM) → Sandboxed Execution → observes output & feedback(LLM) → Response
- **Use Case**: Real-time dynamic tool control and Python execution (used by Manus AI)


### 2.1 Reflective Reasoning Patterns

#### Evaluator-Optimizer Pattern
- **Pattern**: Output validated via a second LLM, feedback given if rejected.
- **Flow**:  
   **Generator** (LLM) → **Evaluator** (LLM) → (Accepted → Output, Rejected → Feedback Loop to Generator)
- **Use Case**: Personalized agents, search optimization
- **Code**: [Code](./Code/evaluator_optimizer.ipynb), [Langgraph](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/multi_agent/agent_supervisor.ipynb)

#### Reflection / Self-Reflection 
- **Pattern:**  The agent critiques and refines its own output in a single or iterative loop, often during the same session.

- **Flow:**  
  User Query → Responder LLM → Evaluator (self or separate LLM), if unsatisfactory → Self-Reflection (LLM: critique or rationale) → Revision → (repeat Evaluation, Self-Reflection, Revision as needed) → Final Output

- **Features:**  
  - Uses short-term context (reflection and correction within a single session)  
  - Optional tool calls (e.g., search, validation) can be incorporated to assist reflection or revision  
- **Code**: [Langgraph](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/reflection/reflection.ipynb)

#### Reflexion
- **Pattern**: 
  - Agent uses memory + reflection to revise strategy over multiple task attempts
  - Full loop with planner, responder (executor), evaluator,and memory integration
- **Flow**:
  Query → Responder LLM  (Output) → Evaluator (LLM) → If unsatisfactory: → Reflection (LLM) → Memory Update (trajectory, failure reason, reflection) Revise → Iterate until success
- **Uses**:
  - **Short-Term Memory** (Insights)
  - **Long-Term Memory** (Experience)
  - **Tool Execution** (Google, APIs)
- **Use Case**: Long-term self-learning and output improvement
- **Used by**: OpenAI’s Reflexion architecture, OpenServe AI
- **Code**: [Langgraph](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/reflexion/reflexion.ipynb)

### 3. RAG Patterns

#### Agentic RAG Pattern
- **Pattern**: An LLM-based agent autonomously plans and controls the retrieval and synthesis process — possibly using multiple retrieval agents, tool calls, and memory — rather than relying on a static embedding + retrieval pipeline.
- **Flow**:
  Query → Planner Agent → Retrieve (via one or more Retrieval Agents/Tools) → Intermediate Reasoning → Synthesis Agent → Reflection → Output
- **Use Case**:
  Complex question answering,  factual generation (used by Perplexity AI), contextual reasoning over large corpora, dynamic document understanding (e.g., enterprise RAG, long-form QA, Gemini Deep Retrieval)
-  **Code**: [langgraph](https://github.com/langchain-ai/langgraph/blob/main/examples/rag/langgraph_agentic_rag.ipynb), [LlamaIndex](https://www.llamaindex.ai/blog/agentic-rag-with-llamaindex-2721b8a49ff6), [Autogen](https://microsoft.github.io/autogen/0.2/docs/topics/retrieval_augmentation/)


For more RAG petterns see the specific section [RAGs](../RAGs/README.md). 


## 4. Multi-Agent Patterns

#### Multi-Agent Workflow
- **Pattern**: A structured sequence or network of agents, each with a specialized role, collaborating to complete a task through staged or parallel processing. Coordination may be explicit (via a controller) or implicit (via shared context).
- **Flow**:
  Input → Agent A (stage 1) → Agent B (stage 2) → … or → Agents A–C (parallel) → Aggregator or Finalizer → Output
- **Use Case**:
End-to-end pipelines with modular reasoning, content creation (e.g., Researcher → Writer → Reviewer), or mixed-mode systems (e.g., search, summarization, generation)

- **Notes**:
  - Can be sequential, parallel, or a hybrid
  - May be supervised (Meta-Agent/Supervisor) or decentralized
  - Emphasizes modularity, composition, and scalability

#### Planner–Executor / Plan-and-Execute (PaE)
- **Pattern**: A planner agent that generates a plan, and an executor agent that executes the plan.
- **Flow**:  
  Query → Planner → Executor (tool calls, code execution, API access)
→ Observes results → Output
- **Use Case**: Collaborative reasoning, consensus building
- **Code**: [Langgraph](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/plan-and-execute/plan-and-execute.ipynb)

#### Multi-agent supervisor (centralized)
- **Pattern**: A supervisor agent that coordinates multiple specialized agents.
- **Similar to**: classic Orchestrator, but added monitoring and feedback control (oversees execution of sub-agents rather than task decomposition and delegation). 
- **Category**: Centralized, hierarchical coordination
- **Flow**:  
  Query → Supervisor → Sub-Agents → Output
- **Use Case**: Collaborative reasoning, consensus building

- **Code**: [Langgraph](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/multi_agent/agent_supervisor.ipynb)


#### Meta-Agent Pattern (centralized)
- **Pattern**: an autonomous Meta-Agent that plans, routes, and orchestrates other sub-agents or tools based on task needs.
- **Similar to**: a supervisor agent, but more autonomous (cognitive orchestrator)reasoning agent (routing, and planning).
- **Flow**:  
  Input → Meta-Agent → n Sub-Agents → Aggregation → Summarization → Output
- **Use Case**: Modular, compositional agents, scalable reasoning

#### Multi-Agent Collaboration (decentralized)
- **Pattern**: Decentralized group of agents collaborate on a shared task by exchanging insights, critiques, or intermediate outputs — with no central supervisor.
- **Flow**:
  Input → Agents A, B, C (interact & refine each other’s outputs) → Merge or consensus → Output
- **Use Case**: Co-creative generation, multi-perspective reasoning, research teams, reflection chains
- **Code**: [Langgraph](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/multi_agent/multi-agent-collaboration.ipynb)

#### Hierarchical Agent Teams 
- **Pattern**: A hierarchical structure of agents, with a top-level supervisor agent and teams of agents coordinating lower-level agents.
- **Flow**:
  Input → Supervisor-Agent → n teams of agents → m Sub-Agents → Aggregation → Summarization → Output
- **Use Case**: Modular, compositional agents, scalable reasoning
- **Code**: [Langgraph](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/multi_agent/hierarchical_agent_teams.ipynb)




#### Reflection Chain
- **Pattern**: A chain of agents that iteratively refine their outputs based on feedback.
- **Flow**:
  Input → Agent A → Output → Agent B (Critique) → Agent C (Revise) → … → Aggregator or Judge → Final Output
- **Use Case**: Self-improving agents, error correction, truthfulness, and multi-perspective reasoning (e.g., peer review simulation)

#### Mixture of Agents
- **Pattern**: A mixture of agents that are specialized in different tasks.
- **Similar to**:  Routing Pattern, optimized for agent expertise selection
- **Flow**:  
  Input → Router Agent → Select Expert Agent (1 of n) → Task Execution → Output
- **Use Case**: Collaborative reasoning, consensus building
- **Code**: [Autogen](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/design-patterns/mixture-of-agents.html)

#### Network Pattern
- **Pattern**: A meta-agent routes tasks to a network (mesh) of specialized agents that may operate in parallel, interact, or pass results across edges.
- **Flow**:
  Meta-Agent → Task-Specific Agents (e.g., CodeGen, Debugger, Validator) → Cross-agent Communication → Aggregated Output
- **Use Case**:
  Complex task graphs, distributed reasoning, modular AI systems with inter-agent dependencies (e.g., coding + testing + deployment)

#### Debate Pattern
- **Pattern**: Two or more agents take conflicting or diverse positions on a task and engage in structured debate. A judge (agent or LLM) selects or synthesizes the final answer.
- **Flow**:
  Query → Agent A (Argument) + Agent B (Counterargument) → Iterative Exchange → Judge Agent or LLM → Final Output
- **Use Case**:
  Truthfulness evaluation, multi-perspective reasoning, critical thinking tasks, adversarial robustness
- **Code**: [Autogen](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/design-patterns/multi-agent-debate.html)



<!-- #### Autonomous Agent Loop
- **Pattern**: Two or more agents interact recursively until goal is achieved.
- **Flow**:  
  Agent 1 ↔ Agent 2 (loop) → Output
- **Use Case**: Closed-loop autonomous goal-seeking systems -->




### 5. Tool-Use Patterns

#### Tool Use Pattern (Tool-Calling / Tool-Planning)
- **Pattern**: An agent integrates external tools (APIs, databases, code exec, etc.) to enhance reasoning — either by *calling* them reactively or by *pre-planning* their usage in advance.
- **Flow**:
  Query → Agent → Decide Tool Use Strategy (reactive vs pre-planned) → Execute Tool(s) → Integrate Results → Output

#### Tool Use with MCP
- **Pattern**: Agent uses external APIs (e.g., AWS, Kagi) via Model Context Protocol (MCP)
  - MCP is a standardized interface for data sharing in LLMs, allowing agents to interact with external tools and systems.
  - like a USB-C port for AI applications
- **Flow**:  
  Query → Agent → MCP Server → Tool APIs → Output
- **Use Case**: Minimal-code integration with SaaS or cloud services


#### Agents as Tools
- **Pattern**: An agent is used as a tool in another agent's workflow.
- **Flow**:
  Query → Agent A → Agent B (uses Agent A as a tool) → Output
- **Use Case**:
  Collaborative reasoning, consensus building
- [Code](./Code/agents_as_tools.py)


#### Code-as-Tool (CodeAct Sandbox)

- **Pattern**: LLM generates code to perform logic, then executes it in a sandbox.
- **Flow**:
  Query → LLM writes code → Execute in sandbox → LLM observes result → Final Answer
- **Use Case**:
  Math, data analysis, API workflows, scripting-heavy reasoning


## System Design using Patterns



##### Notes: 
- These patterns are not exhaustive, but they are a good starting point for building agentic systems.
- The patterns are not mutually exclusive, and can be combined to create more complex systems. As an example (in [Langgraph](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/usaco/usaco.ipynbb)), a **zero-shot CoT with Reflection** can be combined with a **Few-shot semantic retrival** and **Human in the loop** (HITL) to solve competitive programming problems.
- The patterns are not prescriptive, and the best pattern for a given task will depend on the specific requirements of the task.


## Appendix 
#### Patterns with Codes

1. **Anthropic Workflow Design Pattern**  
    - [LangGraph](https://github.com/langchain-ai/langgraph/blob/main/examples/anthropic/anthropic_agentic_pattern.ipynb)

2. **ReAct Agent**  
   - [LangGraph](https://langchain-ai.github.io/langgraph/how-tos/react-agent-from-scratch/), [LlamaIndex](https://docs.llamaindex.ai/en/stable/examples/agent/react_agent/)

3. **Agentic RAG**  
   - [LangGraph](https://github.com/langchain-ai/langgraph/blob/main/examples/rag/langgraph_agentic_rag.ipynb), [LlamaIndex](https://www.llamaindex.ai/blog/agentic-rag-with-llamaindex-2721b8a49ff6), [Microsoft Autogen](https://microsoft.github.io/autogen/0.2/docs/topics/retrieval_augmentation/)

4. **Reflexion**  
   - [LangGraph](https://github.com/langchain-ai/langgraph/blob/main/examples/reflexion/reflexion.ipynb), [Paper](https://arxiv.org/abs/2303.11366)

5. **Evaluator-Optimizer (Self-Improving Loop)**  
   - [Code Example](./Code/evaluator_optimizer.ipynb)

6. **ReWoo (Reasoning Without Observation)**  
   - [LangGraph](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/rewoo/rewoo.ipynb)

7. **Meta-Agent (Hierarchical Multi-Agents)**  
   - [LangGraph](https://github.com/langchain-ai/langgraph/blob/main/examples/meta_agents/meta_agents.ipynb)

8. **Agents as Tools**  
   - [Code Example](./Code/agents_as_tools.py)

9. **CodeAct (Code-as-Tool / Sandbox Execution)**  
   - [LangGraph](https://github.com/langchain-ai/langgraph/blob/main/examples/codeact/codeact.ipynb)

10. **MAD (Multi-Agent Debate)**  
    - [Microsoft Autogen](https://microsoft.github.io/autogen/docs/topics/debate/)

11. **MOA (Mixture of Agents)**  
    - [Microsoft Autogen](https://microsoft.github.io/autogen/docs/topics/mixture_of_agents/) 



<!-- 
### Summary Table

| **Pattern**               | **Category**                     | **Used For**                                    |
|---------------------------|----------------------------------|-------------------------------------------------|
| Prompt Chaining           | Prompt Workflow                  | Copywriting, task sequencing                    |
| Routing                   | Prompt Workflow                  | CRM, decision trees                             |
| Parallel Execution        | Prompt Workflow                  | Ensemble reasoning                              |
| ReAct Pattern             | Agent Behavior                   | Reason + Action agents                          |
| CodeAct Pattern           | Agent Behavior                   | Tool-augmented execution                        |
| Meta-Agent Pattern        | Agent Behavior                   | Modular, scalable agents                        |
| Self-Reflection           | Self-Improving                   | Output critique + adaptation                    |
| Reflexion Loop            | Self-Improving                   | Iterative learning via memory and revision      |
| Evaluator Optimizer       | Self-Improving                   | Output validation + feedback                    |
| Multi-Agent Workflow      | Multi-Agent System               | Collaborative reasoning                         |
| Network Pattern           | Multi-Agent System               | Parallel specialized agents                     |
| Autonomous Agent Loop     | Multi-Agent System               | Goal-seeking systems                            |
| Agentic RAG               | RAG-Based Pattern                | Vector search + LLM memory                      |
| Tool Use Pattern          | Tool Integration                 | API orchestration with cloud/search             |
| ReWoo                     | Symbolic Reasoning               | Structured workflow execution via LLM planning  |


### Architectural Placement of Patterns in System Design

| **System Layer**           | **Design Patterns Used**                                                                 |
|----------------------------|-------------------------------------------------------------------------------------------|
| **Prompt Interface**       | Prompt Chaining, Routing, Parallel Execution, ReAct, CodeAct                             |
| **Agent Orchestrator**     | Routing, Meta-Agent, ReAct, Reflexion Loop, Multi-Agent Workflow, Autonomous Agent Loop  |
| **LLM Inference / Reasoning** | ReAct, Self-Reflection, Evaluator Optimizer, Reflexion Loop, ReWoo                   |
| **Tool Execution Layer**   | CodeAct, Tool Use Pattern, ReWoo                                                          |
| **RAG Layer**              | Agentic RAG, Prompt Chaining                                                              |
| **Memory Layer**           | Reflexion Loop, Self-Reflection, Evaluator Optimizer                                     |
| **Multi-Agent Extension**  | Meta-Agent, Multi-Agent Workflow, Network Pattern, Autonomous Agent Loop                 |
| **Feedback / Eval Layer**  | Self-Reflection, Evaluator Optimizer, Reflexion Loop                                     |
| **Symbolic Planner Layer** | ReWoo                                                                                     | -->
