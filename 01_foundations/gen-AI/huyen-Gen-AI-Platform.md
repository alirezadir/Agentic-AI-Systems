Suammary of **Building A Generative AI Platform**
*Chip Huyen, Jul 25, 2024*
Source: [huyenchip.com](https://huyenchip.com/2024/07/25/genai-platform.html)

---

## Overview

- **Gen-AI platform**: a modular architecture for production-ready generative AI appplications

* Extensible: 
    - simplest form: user requery -> app -> model -> response -> user 
    - progressively adds components like context, guardrails, routing, caching, orchestration
    - Both self-hosted and API-based models

**A common order of components to add**:

1. Enhance **Context** (external data + Tools)
2. **Guardrails** (protect system + users)
3. **Router** and gateway (pipelines + security)
4. **Optimizie** latency + costs (cache)
5. Add complex **logic** 
6. **Observability**: visibility into the system for monitoring and debugging
7. **Orchestration**: chaining all the components together


- **Notes**: 
    - **evals** are necessary in every step
    - More topics (not covered here): model evaluation, application evaluation, prompt engineering, finetuning, data annotation guidelines, chunking strategies (for RAGs)


---

## Step 1: Enhance Context

**Context construction**: 
- enriches queries with *relevant (external) data* before model inference
- equivalent to feature engineering in classical ML 

- **Goals**: 

    * Reduces hallucinations + more detailed response
    * Enables up-to-date knowledge injection
    * In-context learning (learning from the context), a form of continual learning

### RAG: Retrieval-Augmented Generation

- Most well-know pattern: **Retriever + Generator** uses external memory (documents, tables)
    - Retriever: similar to Retrieval for search engines, recommender systems, log analytics
    - unstructured data (documents) or structured (tables); short or long 
    - **Chunking**  required: for long documents (model's max context length e.g. 8k-32k tokens + latency requirements)
        - chunking size: depending on type of document, 100-1000 tokens 
        - use Text splitters (e.g. langchain char, token, md, code, etc splitters)
- Augmentation techniques: term-based & embedding-based retrieval, SQL execution, and web search


#### Retrieval Types

* **Term-Based retrieval**: e.g. keyword search, BM25 (TF-IDF), Elasticsearch (inverted index)
    - faster & cheaper 
* **Embedding-based retrieval** (aka vector search): 
    - **Embeddings**: sentence-transformers, OpenAI embeddings; 
    - **Vector search**: ANN e.g. FAISS, ScaNN (Spotify), ANNOY (Spotify)
    - **Metrics**: Recall, QPS, Build time, Index size 

* **Hybrid Search**: use both 
    - sequential: term based → reranking  w/ vectors (ANN)
    - ensemble: use multiple candid gen → re-rank

**Evaluation Metrics**

* Recall
* Query Per Second (QPS)
* Build Time
* Index Size

#### RAG with Tabular (Structured) Data
* SQL data: different from unstructured data 
* Text-to-SQL → SQL Execution (query result) → Generation (response)
    * same or different models for Text-to-SQL & Generation 
* Large databases: Schema prediction (what tables to use for each query) 
#### Agentic RAG

**agentic  = workflow of models with tool access**

* Actions: Callable Functions  
* Tools (one or more actions): RAG, web search, SQL, APIs 
* Supports **read-only** and **write** actions

#### Query Rewriting

* Converts ambiguous queries to explicit (e.g. entity resolution): `what about his wife?` -> `when was the last time John did ...`
* May require DB lookups for identity resolution

---

## Step 2: Guardrails

**Guardrails**: mitigate risk via input/output validation; protect both users & developers 

### Input Guardrails

* **Risks** to protect against: **Private/Sesntivie information** leakag to external APIS, executing bad prompts (jailbraking)
* **Leaking private information**
    * Personal information (PII) e.g. ID, address, phone; faces; company IP or secrets ...  
    * PII Detection & Blocing or Masking
* **Model Jailbreak**
    - Especially dangerous for AI with tool access (e.g. run a SQL query) 
    - Jailbreak Detection
    - Harmful actions guardrails (e.g. no SQL insert w/o human approval)
    * Scope Filtering: block out-of-domain topics
    * Anomaly Detection: for rare/harmful prompts

### Output Guardrails
* AI models are probabilistic: 
    * Unreliable outputs -> **Output Quality** measurements
        - **Output quality policies** (e.g. output format)
        - **Security & Safety policies** (sensitive info, toxic, etc)
* **Output Failure Modes**:
    * Empty, malformed (e.g. invalid JSON)
    * Toxic (e.g, sexist, racist), 
    * Hallucination: Hallucination detection & mitigation (sufficient context, CoT prompting, etc) 
    * Sensitive info: trained or retrieved  
    * Brand-risk (e.g. response that Grok by X was trained by OpenAI)
    * General bad responses: e.g. a recipe full of sugar (use AI-as-a-judge)
* **Detection Tools**: regex, toxicity classifiers, SAFE, SelfCheckGPT, AI as a Judge, etc
* **Failure Mangement**: 
    * **Retry Policies**: retry on failure (until pass), added latency -> retry in parallel (redundancy)
    * **Human Escalation**: hand off based on sentiment or complexity

---

## Step 3: Add Model Router and Gateway

* **Router + Gateway**: Work with **multiple models**; enable dynamic model dispatch and secure model API usage

### Router
* Benefits of **Multiple models**: specialized solution; cost saving (simpler queries to cheaper models) 
* typically consists of **Intent Classification** → route to appropriate model/handler (e.g. ordering, troubleshooting, refund models, human agent in customer service)
    - Also avoid out-of-scope conversations
* **Next Action Prediction** for ambiguous queries (e.g. freezing, account or weather)
* **Routing based on model capabilities or cost**
* **Context resizing** for different models' conext limits: e.g. query: 1000 tokens + 8k tokens web search: truncate or use larger context model

### Gateway

* A Unified interface to access multiple LLM APIs
    * Easy maintanence: only need to update gateway if models' API change
* Fine-grained access control + Cost management (usage limits)
* Fallback (rate limit, API failures) policies: (Retry, route to different model) 
* load balancing, logging, and analytics integration
* Caching and guardrails integration

```python
# Example model gateway (simplified)
def openai_model(input_data, model_name, max_tokens):
    openai.api_key = os.environ["OPENAI_API_KEY"]
    response = openai.Completion.create(
        ...
        )
...        
@app.route('/model', methods=['POST'])
def model_gateway():
    ...
    if model_type == "openai":
        result = openai_model(input_data, model_name, max_tokens)
    elif model_type == "gemini":
        result = gemini_model(...)
    return jsonify(result)
```

---

## Step 4: Reduce Latency with Cache

- **cache systems** cut cost and response time by reusing work
    - Both in training & deployment 

### Types of Cache

* **Prompt Cache**: stores overlapping segments of  prompts; process it only once 
    * overlapping / multiple runs of system prompts;
    * long documents 
    * incorporated into model APIs w/ some cost
* **Exact Cache**: stores full output for exact queries; e.g. a product summary; embedding retreival 
    - Implementatoin: In-memory storage (fast; limited); DBs like Postgres, Redis, etc
    - need eviction policy (LRU, LFU, FIFO)
* **Semantic Cache**: reuse based on vector similarity of queries
    * query embedding -> vector search in query cache -> use if score above a threshold
* KV cache for attention (implemented by model provider; out of scope)

### Tradeoffs

* Prompt cache: high token savings
* Semantic cache: compute-intensive, brittle to bad similarity thresholds
* Tools: PostgreSQL, Redis, FAISS

---

## Step 5: Add Complex Logic and Write Actions

- **Complex logic**: multi-step, loops, conditional task flows
    - e.g. outputs from a model (conditionally) -> same/another model until task completed
- **Write actions** allow the model to change external state
    - e.g. make changes to DB, or the world (send an email/message)
    - enable to automate a whole (customer) workflow 
        - e.g. research customers, find their contacts, draft emails, send first emails, read responses, follow up, extract orders, update DB with new orders
        - Automatic alteration of lives by AI: Trust in AI system & its security; protect from bad actors 
        - **prompt injection** is a weakness: manipulate input prompts to access undesired behavior 
            - e.g. access to a DB and corrupt data 
            - serious safety & security need

### Complex Logic

* Looped or conditional workflows
* Example: plan → decompose → resolve → generate

### Write Actions

* Can send emails, place orders, update DBs
* Risks: prompt injection, unintended writes
* Must enforce strict access and review policies

---

## 6. Observability

- **Observability**:  **Monitor & track** system health and performance at all levels; projects with all sizes  
- Three pillars of monitoring: **Metrics, logs, and traces**

### Metrics
* Metrics are application-specific; but two types: 
    * **System Metrics**: Latency, throughput(QPS), memory usage, hardware util,  service availability/uptime.
    * **Model Metrics**:

        * Accuracy, hallucination rate, toxicity
        * RAG metrics: Retrieval relevance & precision
        * Vector DB metrics: storage size, Query time (latency)
        * Output failure metrics: time-out, empty, malformated outout rate
        * Length-related metrics: Token and length stats for query, context, and response 
            - track model behavior + track latency & cost 
    * **Latency Metrics**:

        * TTFT (Time to First Token), 
        - TBT (Time Between Tokens), 
        - TPS (Tokens Per Second), 
        - TPOT (Time Per Output Token), 
        - Total Latency
    * **Cost Metrics**: Input/output token usage, queries/sec
* Metric axes:  users, releases, prompt/chain versions, prompt/chain types, and time
* *spot checks* (sampling a subset of data to quickly identify issues) vs *exhaustive checks* 

### Logs

* **Logging philosophy**: Log everything: configs, querys/inputs, (intermediate) outputs, Events (starts, ends, errors) 
* Use tags/IDs for traceability
* Automated log analysis and log anomaly detection: by AI 
* Manual daily inspection: get an idea of user usages & refine evaluation

### Traces

* Detailed step-by-step request execution lifecycle tracking (from query -> final response)
* Entire process including: actions, documents, prompts
* Time + Cost: Needed for debugging and cost attribution
* Example Tool: LangSmith 

---

## 7. AI Pipeline Orchestration
- AI Applications: multiple models, multiple DBs, many tools
- **Orchestrators**: Define & chain components (pipelining) of an end-to-end workflow

### Components Definition
* Define components 
    * Models (generation, routing, scoring)
    * Databases
    * Actions (tools) 
* integration with gateways (or act as gateway)
* integration with eval and monitoring tools

### Chaining (Pipelining)
* Sequence of steps for the system (function composition)
* Pipeline example: 
    ```text
    process (raw) query → retrieve (rel. data) → construct prompt (query + data) → generate → evaluate → return/fallback
    ```
* do as much in parallel as possible (latency): e.g. routing & guardrail 


### Orchestrator Tools

* LangChain, LlamaIndex, Flowise, Langflow, Haystack
* Support branching, parallel steps, retries

### Evaluation Criteria

* Integration & extensibility
* Support for complex pipelines
* Developer experience
* Performance and scalability

---

## Best Practices

* Build without orchestrators first to reduce complexity
* Use hybrid retrieval for precision and coverage
* Secure write actions carefully
* Evaluate caching value based on hit rate and redundancy
* Log and trace every step for visibility
* Route based on intent and cost for scalability
* Use model-specific prompt caches to save tokens
