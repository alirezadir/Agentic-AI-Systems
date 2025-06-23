
# AI Agents Design Patterns (Comprehensive Guide)

---

## Table of Contents

1. [Prompt-Oriented Patterns](#1-prompt-oriented-patterns)
2. [Agent Behavior Patterns](#2-agent-behavior-patterns)
3. [Self-Improving / Reflective Patterns](#3-self-improving--reflective-patterns)
4. [Multi-Agent System Patterns](#4-multi-agent-system-patterns)
5. [Retrieval-Augmented Generation (RAG) Patterns](#5-retrieval-augmented-generation-rag-patterns)
6. [Tool-Use & Execution Environment Patterns](#6-tool-use--execution-environment-patterns)
7. [Symbolic Reasoning Patterns (ReWoo)](#7-symbolic-reasoning-patterns-rewoo)

---

## Agentic Design Patterns
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
  - Collaborative patterns ... 
---

## 1. Prompt-Oriented Patterns

### Prompt Chaining
- **Pattern**: Sequential prompt execution with conditional flow.
- **Flow**:  
  Input → LLM Call 1 → Output → Gate (Fail → Exit, Pass → LLM Call 2) → Final Output
- **Use Case**: Proofreading, Copywriting, Sequential execution logic

### Routing
- **Pattern**: Decision-based branching to different LLMs.
- **Flow**:  
  LLM Call 1 → Output evaluated → Routed to LLM Call 2/3/4 → Output
- **Use Case**: CRM agents, Agentic task delegation

### Parallel Execution
- **Pattern**: Multiple LLMs called in parallel, then aggregated.
- **Flow**:  
  LLM Call 1 → Multiple LLM Call 2s (parallel) → Aggregator → Output
- **Use Case**: Vulnerability analysis, ensemble reasoning

---

## 2. Agent Behavior Patterns

### ReAct Pattern
- **Pattern**: Reasoning (via LLM) and Acting alternate steps.
- **Flow**:  
  Query → LLM 1 (Reason) → Tools → LLM 2 (Action) → Output
- **Use Case**: Used by most AI agents

### CodeAct Pattern
- **Pattern**: Combines planning, acting, and tool-use in a loop using a sandbox.
- **Flow**:  
  User → Agent → Plan (CoT, Reflection) → Execute in CodeAct → Environment → Revised Actions → Outcome
- **Use Case**: Real-time dynamic tool control and Python execution (used by Manus AI)

### Meta-Agent Pattern
- **Pattern**: Delegation from a coordinating meta-agent to sub-agents.
- **Flow**:  
  Input → Meta-Agent → n Sub-Agents → Aggregation → Summarization → Output
- **Use Case**: Modular, compositional agents, scalable reasoning

---

## 3. Self-Improving / Reflective Patterns

### Self-Reflection / Reflexion Pattern
- **Pattern**: Agent critiques and improves its output iteratively.
- **Flow**:
  1. Query → Actor/Responder LLM
  2. Output → Evaluator (LLM)
  3. If unsatisfactory: → Self-Reflection Module
  4. Uses:
     - **Short-Term Memory** (Insights)
     - **Long-Term Memory** (Experience)
     - **Tool Execution** (Google, APIs)
  5. Updated output looped until it passes
- **Used by**: OpenAI’s Reflexion architecture, OpenServe AI
- **Category**: Self-Improving, Reflective Agent

### Reflexion Feedback Loop
- **Pattern**: Full loop with evaluator, responder, and memory integration.
- **Flow**:  
  User Query → LLM Response → Evaluator (needs improvement?) → Self-Reflection → Memory Update → Improved Output
- **Use Case**: Long-term self-learning and output improvement

### Evaluator-Optimizer Pattern
- **Pattern**: Output validated via a second LLM, feedback given if rejected.
- **Flow**:  
  LLM Generator → Validator → (Accepted → Output, Rejected → Feedback Loop to Generator)
- **Use Case**: Personalized agents, search optimization

---

## 4. Multi-Agent System Patterns

### Multi-Agent Workflow
- **Pattern**: Agents with specialized roles coordinated by a main agent.
- **Flow**:  
  Query → Agent → Sub-Agents (S-Agent 1 to n) → Aggregator LLM → Output
- **Use Case**: Collaborative reasoning (used by Gemini Deep Research)

### Network Pattern
- **Pattern**: Meta-agent dispatches tasks to a task-specific mesh of agents.
- **Flow**:  
  Meta-Agent → Parallel agents (e.g., coding, debugging) → Output

### Autonomous Agent Loop
- **Pattern**: Two or more agents interact recursively until goal is achieved.
- **Flow**:  
  Agent 1 ↔ Agent 2 (loop) → Output
- **Use Case**: Closed-loop autonomous goal-seeking systems

---

## 5. Retrieval-Augmented Generation (RAG) Patterns

### Agentic RAG Pattern
- **Pattern**: Agents augment generation with vector-based search + reflection.
- **Flow**:  
  Query → Agent → Tools (Vector Search, Company DBs) → LLM → Reflection → Output
- **Use Case**: Context-aware, factual generation (used by Perplexity AI)

---

## 6. Tool-Use & Execution Environment Patterns

### Tool Use Pattern
- **Pattern**: Agent uses external APIs (e.g., AWS, Kagi) via MCP.
- **Flow**:  
  Query → Agent → MCP Server → Tool APIs → Output
- **Use Case**: Minimal-code integration with SaaS or cloud services

### CodeAct Sandbox (Detailed)
- **Modules**:
  - Planning: Chain-of-Thought, Self-reflection, Improvisation
  - CodeAct Sandbox: Revise or Create Actions
  - Environment: Tools (Gmail, DBs, Memory)
- **Loop**:  
  Observation → Action → Environment → Outcome → Revised Actions → Repeat

---

## 7. Symbolic Reasoning Patterns (ReWoo)

### ReWoo (Reasoning over Workflows)
- **Pattern**: LLM reasons *about* a workflow instead of solving tasks directly.
- **How it Works**:
  - Input → LLM chooses symbolic actions/modules
  - Each module performs a sub-task (e.g., search, calculation, summarization)
  - LLM coordinates these in structured reasoning steps
- **Flow**:
  1. Input → Planner (LLM)
  2. Planner → Symbolic Workflow (API/Tool/Model)
  3. Submodules execute
  4. Results fed back to LLM → Final reasoning/output
- **Key Modules**:
  - Tool executor (API or scripted tools)
  - Reasoning LLM planner
  - Subtask results aggregator
- **Benefits**:
  - **Interpretability** via symbolic steps
  - **Modularity** and low hallucination
- **Used in**: Microsoft’s ReWoo, AutoGPT-style agents with module planners

---

## Summary Table

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


---

## Architectural Placement of Patterns in System Design

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
| **Symbolic Planner Layer** | ReWoo                                                                                     |
