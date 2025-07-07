# Chapter 10: AI Engineering Architecture and User Feedback

## 1. AI Engineering Architecture

### Step 1: Enhance Context

- **Context Construction**: Supplements model input with additional relevant information (RAG, search, APIs)
  - Retrieval types: text, image, tabular
  - Tools: API wrappers (e.g., news, weather, finance), embeddings with FAISS, Pinecone, Weaviate
  - Consider dynamic context slicing and weighted retrieval (e.g., prioritize recency or semantic similarity)
- **Foundation Analogy**: Context ≈ feature engineering for LLMs
- **Model Provider Capabilities**:
  - Vary in file limits, tool access, parallelism support
  - OpenAI: supports file uploads and function calling
  - Claude: longer context windows, constitutional AI support
  - Gemini: tool-rich, vision/text native, good planning control

**Code Tip:**
```python
from langchain.chains import RetrievalQA
qa = RetrievalQA.from_chain_type(llm=OpenAI(), retriever=my_vectordb.as_retriever())
result = qa.run("Summarize the latest policy on user privacy.")
```

**Interview Tips**
- Know how RAG works: retrieve + augment prompt
- Explain differences between retrieval frameworks (chunking, ranking, execution)

---

### Step 2: Put in Guardrails

| Guardrail Type     | Function                                           | Tools                             |
|-------------------|----------------------------------------------------|-----------------------------------|
| Input Guardrails  | Prevent prompt injection, filter PII               | Azure PyRIT, NeMo, Llama Guardrails |
| Output Guardrails | Catch hallucinations, bias, toxicity               | Perspective API, OpenAI moderation |

- **Implementation Levels**:
  - Model provider: baseline filters
  - Application developer: prompt defenses, scoring layers

**Code Snippet: Output Moderation**
```python
from openai import OpenAI
response = openai.ChatCompletion.create(...)
if 'flagged' in response['usage']:
    log_moderation_issue(response)
```

**Best Practices**
- Always pair input/output guardrails
- Tune for balance: false positives vs. unfiltered risk

---

### Step 3: Add Model Router and Gateway

#### Router
- **Intent Classification**: Route based on user’s need (FAQ vs. billing vs. tech help)
- **Multi-model Serving**: Assign different models per task
- **Cost Optimization**: Light models for simple tasks, heavy models for complex ones

#### Gateway
- **Purpose**: Unified API interface, access control, fallback routing
- **Features**:
  - Monitor and limit usage
  - Retry failed calls
  - Provide caching, guardrails

**Code Example Snippet**: Model Gateway
```python
@app.route('/model', methods=['POST'])
def model_gateway():
    data = request.get_json()
    if data['model_type'] == "openai":
        return openai_model(...)
    elif data['model_type'] == "gemini":
        return gemini_model(...)
```

**Study Tip**: Differentiate routers (intent prediction) vs. gateways (API mgmt)

---

### Step 4: Reduce Latency with Caches

#### Types of Caching
| Type              | Description                                           | Pros/Cons                       |
|-------------------|--------------------------------------------------------|---------------------------------|
| Exact Caching     | Match full queries, use in-memory/DB stores           | Fast, but limited reuse scope   |
| Semantic Caching  | Match via vector similarity threshold                 | Reusable but error-prone        |
| Prompt Caching    | Cache system prompts, long doc prompts                | Great for repeated prompts      |
| KV Caching        | Model-level optimization for autoregressive decoding  | Speeds up decode, low latency   |

**Security Alert**: Never cache user-personalized or PII-rich outputs!

**Caching Tools**: Redis, PostgreSQL, FAISS, pgvector

**Code Snippet: Prompt Caching Layer**
```python
prompt_hash = hash(user_prompt)
if prompt_hash in redis_cache:
    return redis_cache[prompt_hash]
else:
    response = generate_response(user_prompt)
    redis_cache[prompt_hash] = response
```

---

### Step 5: Add Agent Patterns

- **Agentic Workflows**: Enable loops, conditionals, multi-tool execution
- **Use Cases**:
  - Email composition, dynamic retrieval, bank transfers, form auto-fill
- **Execution Flow**: Generation → Review → Tool Call → Re-gen (loop)

#### Write Actions
- **Risky**: Directly modifies external systems (e.g., sends email)
- **Needs Safeguards**: Verification, guardrails, user confirmation

**Code Snippet: LangChain Agent Executor**
```python
from langchain.agents import initialize_agent
agent = initialize_agent(tools, llm, agent="zero-shot-react-description")
agent.run("Check weather and send a summary email.")
```

**Interview Takeaway**:
- Understand how agents differ from basic LLM usage: planning, memory, tool invocation

---

### 6. Monitoring and Observability

- **Goals**:
  - Detect failures early (malformed outputs, silence, bias)
  - Track usage patterns, model response types, latency
- **Approaches**:
  - Logs, traces, metrics via Prometheus, Grafana, OpenTelemetry
  - Alerting + A/B test metrics (TTFT, success rate)

**Code Snippet: Basic Request Logging**
```python
@app.after_request
def log_request(response):
    logger.info(f"{request.path} - {response.status_code} - {time.time()}")
    return response
```

---

### 7. AI Pipeline Orchestration

- **Purpose**: Coordinate RAG, agents, caching, scoring in sequence
- **Orchestration Tools**: LangChain, Haystack, DSPy, Airflow, Prefect

| Component       | Task                                         |
|------------------|----------------------------------------------|
| Retriever        | Pull context                                 |
| Generator        | Create candidate response                    |
| Scorer           | Rank or validate response                    |
| Action/Tool Call | Perform real-world action (optional)         |
| Logger           | Store metadata for future evaluation         |

**Code Snippet: LangChain DAG Composition**
```python
from langchain.chains import SequentialChain
chain = SequentialChain(
    chains=[retriever_chain, generation_chain, scoring_chain],
    input_variables=["query"],
    output_variables=["response"]
)
```

---

## 2. User Feedback

### Extracting Conversational Feedback
- **Challenge**: Feedback is often implicit
- **Types**:
  - Explicit: Thumbs up/down, comments
  - Implicit: User retry, edit, stop

#### Techniques
- Classify messages as positive/negative/neutral
- Use NLU to infer sentiment, frustration, satisfaction

**Example**:
```python
if "again" in user_input.lower():
    feedback_label = "possible dissatisfaction"
```

---

### Feedback Design

| Principle           | Description                                       |
|--------------------|---------------------------------------------------|
| Minimize Friction  | Inline, non-intrusive UI elements                 |
| Actionability      | Collect feedback that can improve the system     |
| Granularity        | Capture component-specific feedback              |
| Privacy-Safe       | Avoid PII in logging and analysis                 |

**Design Tip**: Use microinteractions, emoji responses, comment tagging

---

### Feedback Limitations

- **Biases**: Early users ≠ general users; feedback ≠ objective truth
- **Misinterpretation Risk**: Negative feedback ≠ model failure
- **Volume Tradeoff**: High-volume feedback might be low-signal

**Recommendation**:
- Combine user feedback with automated metrics for robustness
- Use feedback to guide exploration, not directly optimize

---

## Chapter Summary
- Gradually evolve system from basic model calls to full-fledged orchestration
- Enhance input with context, secure with guardrails, manage cost/latency with routers + caches
- Use agents and orchestration to increase capability
- Collect and interpret feedback for continuous improvement

---

## Additional Coding Snippets & Prototypes

### Full Feedback Loop Pipeline
```python
class FeedbackLoop:
    def __init__(self, generator, scorer, logger):
        self.generator = generator
        self.scorer = scorer
        self.logger = logger

    def process(self, query):
        response = self.generator(query)
        score = self.scorer(response)
        self.logger(query, response, score)
        return response
```

### OpenAI Moderation + Semantic Caching Combo
```python
from openai import OpenAI
from sentence_transformers import SentenceTransformer
import faiss

# Load models
embed_model = SentenceTransformer('all-MiniLM-L6-v2')
response = openai.ChatCompletion.create(...)
embedding = embed_model.encode([response['content']])

# Store in FAISS index
faiss_index.add(embedding)
```

### Agentic Planning with DSPy
```python
import dsp
@dsp.transformation()
def plan_and_execute(user_query):
    plan = dsp.llm("Plan steps to answer: " + user_query)
    result = dsp.execute(plan)
    return result
```

---

### 🧠 Comprehensive End-to-End AI Workflow Example

This prototype integrates context retrieval, moderation, scoring, logging, and caching in one modular pipeline.
```python 
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import faiss, openai
import logging

# Init
embedder = SentenceTransformer('all-MiniLM-L6-v2')
moderator = pipeline("text-classification", model="unitary/unbiased-toxic-roberta")
scorer = pipeline("text-classification", model="cross-encoder/nli-deberta-v3-base")
faiss_index = faiss.IndexFlatL2(384)
cache = {}
logging.basicConfig(level=logging.INFO)

# Workflow function
def ai_pipeline(user_input):
    # 1. Check cache
    input_embed = embedder.encode([user_input])[0]
    D, I = faiss_index.search([input_embed], k=1)
    if D[0][0] < 0.5:
        cached_response = cache.get(I[0][0])
        if cached_response:
            return cached_response

    # 2. Moderation
    toxicity = moderator(user_input)[0]
    if toxicity['label'] == 'toxic' and toxicity['score'] > 0.7:
        return "Input flagged as toxic."

    # 3. Call model
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[{"role": "user", "content": user_input}])
    content = response['choices'][0]['message']['content']

    # 4. Scoring
    feedback_score = scorer(f"User: {user_input} \n Bot: {content}")[0]['score']

    # 5. Cache and log
    cache[len(cache)] = content
    faiss_index.add([input_embed])
    logging.info(f"Input: {user_input} | Score: {feedback_score:.2f}")

    return content
```
