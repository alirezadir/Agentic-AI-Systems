# Chapter 6.1 : RAG and Agents

<!-- ---

## Overview 

1. Introduction: Context Needs and Patterns
2. RAG (Retrieval-Augmented Generation)
   - Architecture
   - Retrieval Algorithms
   - Retrieval Optimization
   - Beyond Text (Multimodal, Tabular)
   - Evaluation
   - Pitfalls & Best Practices
3. Agents
   - Overview
   - Tools
   - Planning & Control Flows
   - Failure Modes & Evaluation
   - Reflection & Iteration
   - Security
4. Memory in RAG & Agents
5. Summary & Review Questions
6. Code Snippets & Practical Examples

--- -->

## 1. Introduction

- LLMs are powerful but **context-limited**.
- **Context construction** = providing relevant information for each input, that guides model reasoning.
- RAG provides **context augmentation**: retrieve relevant information from external data sources
- Agents enable **multi-step reasoning** with Tools.

**Key Terms**:
- **External memory** = internal databases, internet, APIs, or documents (external to the model).

---

## 2. Retrieval-Augmented Generation (RAG)

### 2.1 Architecture

- **Retriever**:
  - Encodes user query & Finds relevant documents 
  - Term-based or Embedding-based retrieval
  - Two functions: **Indexing** and **Querying**.

- **Generator**:
  - Receives query + top-K context.
  - Produces a response.

**Architecture Types:**
- **Standard RAG**: Single-pass retrieval → generation.
- **Multi-hop RAG**: Iterative document chaining.
- **FiD (Fusion-in-Decoder)**: Encoder per chunk → concatenate hidden states → generate.

### 2.2 Retrieval Algorithms

#### Term-Based:
- Uses keyword overlap (TF-IDF, BM25, elasticsearch).
- ✅ Simple, fast
- ❌ No semantic understanding

#### Embedding-Based:
- Uses dense vector embeddings (OpenAI embeddings, BERT, BGE).
- Two steps: 
  - Embedding model: query -> embedding (same embedding used for indexing)
  - Retriever: fetch k data chunks whose embeddings are closest to the query embedding (ANN)
- Architecture: 
  - Indexing: `[External Memory] -> [Splitter] -> [Embedding Model] -> Vector DB`
  - Querying: `[Query] -> [Embedding Model] + [Vector DB] -> retriever`
- Vector DB: stores embeddings as vectors -> Vector search (KNN -> ANN)
  - Efficient vector search: store in buckets, trees, or graphs.
  - Vector serach algorithms: 
    - LSH (hash into buckets), HNSW(graph), IVF, quantization, etc
- Tools: FAISS, Qdrant, Weaviate

**Example FAISS Setup:**
```python
from sentence_transformers import SentenceTransformer
import faiss

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(documents)
index = faiss.IndexFlatL2(384)
index.add(embeddings)
```
### 2.3 Evaluation Metrics

- **Recall@K**: what percentage are relevant
- **Speed**: Queries per second (QPS)
- **Build Time** to index data
- **Index Size**
- **Cost**

<!-- - **Groundedness**: Are claims supported by retrieved content?
- **Factual Consistency**: Hallucination rate?
- **Latency**: Response time impact of retrieval. -->

### 2.4 Retrieval Optimization

- **Chunking**: using splitters 
  - **Chunking Size and Strategy** matters
  * **Chunk units**: characters, words, sentences, paragraphs, or tokens  
    * Choose based on data type and tokenizer compatibility

  * **Recursive chunking**: split sections → paragraphs → sentences  
    * Preserves structure, reduces context loss

  * **Specialized chunking**: 
    * Code → by function/block  
    * Q&A → by question-answer pair  
    * Language-aware for non-English (e.g. Chinese)

  * **Overlapping**:  
    * Add buffer (e.g. 20 chars) to preserve boundary context

  <!-- * **Token-based chunking**:  
    * Align with model tokenizer; reindex if switching models -->

  * **Chunk Size Tradeoffs**:  
    * **Small chunks**: more diverse context (fit more chunks into the model), higher cost (more vectors to index), potential info loss  
    * **Large chunks**: better coherence, faster search, risk of cutoff

  * **Guideline**:  
    * Stay within model’s context limit & embedding's context limit
    * Tune based on retrieval quality and performance needs


<!-- ```python
def chunk_text(text, size=500, overlap=100):
    return [text[i:i+size] for i in range(0, len(text), size - overlap)]
``` -->
- **Reranking**: Use cross-encoder to reorder top-K.
- **Hybrid Search**: Combine e.g. BM25 + embeddings.
  - reciprocal rank fusion (RRF) = sum (1/k + r_i(doc))
- **Metadata Augmentation**: Augment & Filter chunks by Metadata 
  - e.g. tags, keywords, source; description or reviews (product), titles or captions (image, video).
  - **chunk conext augmentation**: generated & augment short context (50-100) for each chunk (e.g. title & description)
- **Query rewriting**

### 2.5 Beyond Text (Multimodal + SQL + Tables)

#### Multimodal RAG:
- Retrieving other modalities: metadata or content 
  - e.g. images can be retried using their descriptions (if relevant)
- **multi-modal embeddings** to retrive from content (compare text to image e.g.)
  - Images: Use CLIP to embed images + queries.
  - Audio: Use Whisper or HuBERT for transcript indexing.

#### RAG with Tabular Data (Text-to-SQL):
- Query: `“How many units of X were sold in the last 7 days`
  - SQL: 
    ```sql
    SELECT SUM(units)
    FROM Sales
    WHERE date > NOW() - INTERVAL 7 DAY
    AND product_name = 'X'
    ORDER BY SUM(units) DESC
    ```
- Pipeline: 
  - Text-to-SQL
  - SQL Execution 
  - Response Generation 
---
## 🤖 3. Agents

### 3.1 Agents Overview

* **Agents**: autonomous systems that:  a) **perceive an environment** and 2) **take actions** upon the environment, to achieve goals.
  - *Environmnet*: e.g. a game, computer, files, interet, road, etc
  - *Set of Actions*: via **Tools** that agents have access to
    - Set of Actions depend on the environment: e.g. actions a chess player agent can take (limited to chess game) 
* **AI Agents**: accompolish tasks provided by a user input: 
  - AI: perceive information (task, feedback from environment), plan a sequence actions 
  * **AI Agent = model + memory + tools access + control flow**

  * Key capabilities:

    * Interact with digital / physical environments.
    * Invoke & combine tools to augment abilities.
    * Plan, reflect, and iterate based on feedback.
    * Support both read (perceive) and write (act) actions (e.g., send emails, execute code).

**Example Use Cases:**
* Assistants, coworkers, and coaches
<!-- * create a website, gather data, plan a trip, do market research, manage a customer account, automate data entry, prepare for
interviews, interview our candidates, negotiate a deal, -->
  * QA agents
  * Research assistants
  * Data analysts
  * Coding agents (e.g., SWE-Agent)
  * Customer support bots
  * Web scraping + summarizing bots
  * Interview preparation 
  * Negotiaion agent 
  * Website creation 

* Example: RAG agent with Tabular data 
  - Task: `Project the sales revenue for product X over the next three months`
  - Sequence of Actions: 
    ```text 
    - Reasoning (sequnce of actions): first need sales data from past 5 years for product X
    - SQL query generation (using text-to-SQL) 
    - SQL query execution 
    - Reasoning (on SQL output): insufficient data -> need past marketing campaigns 
    - SQL query generation (for past campaigns)
    - SQL query execution 
    - Reasoning (on new info): data is sufficient -> make a projection 
    - Reasoning: Task completed 
    ```
* Models: agents need more accurate models: 
  - Compound mistakes: overall accuracy drops with # of steps (0.95)^10 = 0.6, (0.95)^100 = 0.06!
  - Higher stakes: due to tool access, and severe consequences of failures 

---
### 3.2 Tools

* Agents take *actions* via Tools = External *APIs* or *functions* that agents can call.
* *Read-only actions*: perception;  *write actions*: acting upon environment 
* Types:

  * **Knowledge augmentation**: retrievers, SQL executors, web browsing tools, Slack/email access tools
    - Web browsing tools: search APIs, news APIs, GitHub
APIs, social media APIS, etc 
  * **Capability extension**: calculators, calendars, translators, code interpreters
    * **Multimodal**: OCR, captioners, text-to-image, speech-to-text
  * **Write actions**: SQL executor, email API (send), Bank API

    ```python
    # Example tools
    def search_tool(query):
        return web_search(query)

    def run_sql(query):
        return sql_engine.execute(query)
    ```

* Agents require function schemas and metadata to use tools correctly.
* Tool selection depends on environment, task, and model strength.
---
### 3.3 Planning & Control Flows

#### Planning Principles:
* Task: An objective + constraints: plan a trip from LA to SF with a budget of $500
* Planning: Decomposing a task into actionable steps considering constraints.
* Plans must be **valid** & **efficient**
<!-- * Task decomposition (e.g., high-level → subtask) is central. -->
* Agents can be prompted to plan using formats such as CoT ("think step by step").
* **Planning** should be decoupled from **Execution** and only executed after **Validation**. 
* **Multi-Agent Planning**:Planning may involve:

  * A **planner** generates plan: includes *intent classification* (can be separate agent)
  * A **validator** checks feasibility & efficiency (if a bad plan -> generate a new plan); also checks executed output validity & task completion 
  * An **executor** (runs actions)

  ```text 
                                [Tools]   -   |
                                  |        [Executor]
  Query -> [Planner] -> Plan -> [Validator]  -|  -> <Finish>
  ```
* **Planning Granularity**:

  * Plans can be generated at:

    * **High-level** (e.g., quarter to quarter plan)
    * **Low-level** (e.g., week to week plan, `fetch_product_info()`)
  * planning/execution trade-off: more detailed plan is harder to generate, but easier to execute.
  * user hierarchical planing (high level -> low level)

*Example:*

```text
Task: What’s the price of the best-selling product last week?
Plan: [get_today_date, fetch_top_products, fetch_product_info, generate_query, generate_response]
```
#### LLMs as Planners

- **Can Foundation Models Plan?**
  - Onngoing debate about whether autoregressive LLMs are capable of effective planning.

    - Yann LeCun: autoregressive LLMs can't plan.
    - Kambhampati: LLMs are good at retrieving knowledge, they struggle with producing executable plans.
  - Generated plans may appear coherent but often fail at execution.
    - It's unclear if this is inherent or due to lack of proper prompting or tooling.

 * **Planning as a Search Problem**

    - Planning is a **search problem**: finding paths to a goal, predicting their outcomes (rewards), and selecting the best one.

    - Backtracking is often needed (e.g., trying path A, failing, then trying path B).
    - Critics say autoregressive models can't backtrack. However:
      - LLMs can simulating backtracking (restart and revise paths).
    - Planning requires knowing the **outcomes of actions (state)**   
      - LLMs can simulate outcomes
    - LLMs can assist in  planning systems (e.g., integrated with search or state tracking).

- **FM vs RL Planners**
  - RL agent: planner is trained by an RL algorithm (time and resource consuming). 
  - FM agent: prompting & fine-tuning 
  - FM agents and RL agents will merge in future 
#### Plan generation 
- **Plan Generation via Prompting**

    *Example Prompt:*
    ```
    Propose a plan to solve the task. You have access to 5 actions:
    - get_today_date()
    - fetch_top_products(start_date, end_date, num_products)
    - fetch_product_info(product_name)
    - generate_query(task_history, tool_output)
    - generate_response(query)
    The plan must be a sequence of valid actions.
    Examples
    Task: "Tell me about Fruity Fedora"
    Plan: [fetch_product_info, generate_query, generate_response]
    ...
    ```
  - Parameter Resolution
    - List of functions **without fixed parameters**.
    - Parameters (e.g., dates, quantities) are inferred from tool outputs or context.
  - Common Challenges:
    - *Missing information* in user queries (e.g., timeframe).
    - *Hallucinations* or guessing in action names or parameters.
    - *Tool mismatches* or invalid sequences.


* How to Improve Planning

  - Improve system prompts (more structured examples).
  - Write detailed descriptions for tools/functions.
  - Simplify complex tools by breaking them down.
  - Use stronger base models.
  - Fine-tune a model specifically for plan generation.

##### **Function Calling**: 
  - Invoking tools = function calling 
    - Create a tool inventory: Declare tools (`fcn name, parameters, description`)
    - Specify what tools the agent can use (`reqired, none, auto`) 
#### **Reflection and error correction**: 
  - Reflection: 
    - think about what / why sth went wrong 
    - necessary for agent success (not operation)
    - self-critique agent, or a separate scorer 
  - Refelction on: 
    - query feasible 
    - plan makes sense 
    - every step of execution 
    - task completed  
##### ReAct (Reason + Act) Pattern:
  - 3 steps: 
    - **Reason** (Thought): plan, reflect
    - **Act** 
    - **Observe** (reflect)
  - Best for complex/multi-hop tasks:
    ```
    Thought 1
    Act 1 
    Obs 1 
    ...
    Thought N
    Act N
    ```

    ```text
    Thought: I need data.
    Action: fetch_sales_data
    Observation: Found 1 week of sales
    Thought: I need 4 weeks. Retry...
    ```

##### Reflexion Pattern:
- Reflection in two modules: 
  * Evaluator module (assess plan outcome (*what*))
  * Self-Reflection module (diagnoses failure (*why*))
* Generates improved plan/trajectory

#### Tool selection 
- Depends on Task requirements, environmnet + model prefs 
- ablation study: 
  - how agents perform with a set of tools, what happens if you drop tools 
  - plot tool usage 
  - tools frequently used together can be combined 

#### Control Flows:
* Control Flow: order in which actions can be executed
* Common Control Flows: 
  * **Sequential**: A → B → C
  * **Conditional**: IF X THEN A ELSE B
  * **Parallel**: A and B run together
  * **Looped**: Repeat A until condition

- Control Flow Evaluation:

  * Enables efficient execution (e.g., batch or parallel tasks)
  * Must be translated into executable commands with correct parameters

<!-- #### Planning Challenges:

* Models may **hallucinate** functions or **guess** parameters.
* Must manage **tool changes**, **parameter extraction**, and **tool use errors**.
* **Heuristics** and **AI judges** can validate plan steps.
* Humans can assist in providing or approving plans. -->


---
### 3.4 Agent Failure Modes & Evaluation
- Agent evaluation: detecting failures 
* **Tool Misuse**: Wrong or invalid tool invoked
* **Timeouts**: Tool fails to return
* **Stuck Loops**: No termination
* **Invalid plans**: Too long, missing steps, wrong order

**Evaluate Agents By:**

* Valid plan rate
* Steps to completion
* Reflection/adjustment quality
* Tool call validity (tools, parameters)
* Task success vs constraints




* Can be done by same or separate agents
* Example from Reflexion: revise code after test failure

### 3.6 Security

* Limit tools exposed to agent
* Validate all inputs (e.g., prevent SQL injection)
* Use sandboxing and audit logs

---

## 🧠 4. Memory 

* **Internal Memory**: Knowledge from training.
* **Short-Term Memory**: Context window; ephemeral per session.
* **Long-Term Memory**:

  * Vector DBs (e.g., Chroma, Weaviate)
  * SQL logs, file systems, memory buffers

**Use Cases:**

* Personalized tutors
* Consistent conversations
* Storing tool outputs and plans

**Memory Ops:**

* Add/delete memory chunks
* Summarize and compress for space
* Detect contradictions

**Strategies:**

* FIFO, redundancy removal, reflection-based memory curation

---

## ✅ 5. Review Questions

1. What defines an AI agent?
2. Name 3 categories of tools.
3. How do hierarchical plans work?
4. Describe a planning failure vs a tool failure.
5. What types of memory can agents use?

---

## 💻 6. Code Snippets & Practical Examples

### 🔹 LangChain RAG Pipeline

```python
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

embedding = HuggingFaceEmbeddings("all-MiniLM-L6-v2")
vectorstore = FAISS.load_local("my_docs", embedding)
retriever = vectorstore.as_retriever()
llm = OpenAI(model="gpt-4")
rag = RetrievalQA(llm=llm, retriever=retriever)
answer = rag.run("What are AI safety principles?")
```

### 🔹 Agent with Tool Registry

```python
from langchain.agents import Tool, initialize_agent
from langchain.llms import OpenAI

def get_weather(location):
    return f"Weather in {location} is sunny."

def search(query):
    return f"Search results for {query}."

tools = [
    Tool(name="get_weather", func=get_weather, description="Gets weather"),
    Tool(name="search", func=search, description="Web search")
]

agent = initialize_agent(tools, OpenAI(), agent="zero-shot-react-description", verbose=True)
result = agent.run("What’s the weather in Paris and top 3 tourist spots?")
```

### 🔹 Agent Memory Store

```python
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory(memory_key="chat_history")
agent_chain = initialize_agent(..., memory=memory)
```

### 🔹 Agent with SQL + Planning

```python
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.utilities import SQLDatabase
from langchain.llms import OpenAI

db = SQLDatabase.from_uri("sqlite:///sales.db")
toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI())

agent = initialize_agent(
    tools=toolkit.get_tools(),
    llm=OpenAI(),
    agent="zero-shot-react-description",
    verbose=True
)

response = agent.run("Show top 3 products by revenue in Q2")
```

Let me know if you'd like a diagram version or dive deeper into memory optimization!
