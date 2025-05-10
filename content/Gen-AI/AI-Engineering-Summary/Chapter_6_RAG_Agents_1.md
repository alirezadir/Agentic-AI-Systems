# Chapter 6 : RAG and Agents

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

## 🔍 1. Introduction

- LLMs are powerful but **context-limited**.
- RAG provides **dynamic context augmentation**.
- Agents enable **multi-step reasoning** with tools.

**Key Terms**:
- **Context construction** = the process of providing input that guides model reasoning.
- **External memory** = databases, APIs, or documents external to the model.

---

## 📚 2. Retrieval-Augmented Generation (RAG)

### 2.1 Architecture

- **Retriever**:
  - Encodes user query.
  - Finds relevant documents (term or embedding-based).

- **Generator**:
  - Receives query + top-K context.
  - Produces a grounded response.

**Architecture Types:**
- **Standard RAG**: Single-pass retrieval → generation.
- **Multi-hop RAG**: Iterative document chaining.
- **FiD (Fusion-in-Decoder)**: Encoder per chunk → concatenate hidden states → generate.

### 2.2 Retrieval Algorithms

#### Term-Based:
- Uses keyword overlap (BM25, TF-IDF).
- ✅ Simple, fast
- ❌ No semantic understanding

#### Embedding-Based:
- Uses dense vector embeddings (OpenAI, MiniLM, BGE).
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

### 2.3 Retrieval Optimization

- **Chunking**:
```python
def chunk_text(text, size=500, overlap=100):
    return [text[i:i+size] for i in range(0, len(text), size - overlap)]
```
- **Reranking**: Use cross-encoder to reorder top-K.
- **Hybrid Search**: Combine BM25 + embeddings.
- **Metadata Filtering**: Filter by tag, source, or topic.

### 2.4 Beyond Text (Multimodal + SQL + Tables)

#### Multimodal RAG:
- Images: Use CLIP to embed images + queries.
- Audio: Use Whisper or HuBERT for transcript indexing.

#### Tabular RAG (Text-to-SQL):
```sql
SELECT product, SUM(units)
FROM Sales
WHERE date > NOW() - INTERVAL 7 DAY
GROUP BY product
ORDER BY SUM(units) DESC
```

### 2.5 Evaluation

- **Recall@K**: Are retrieved docs relevant?
- **Groundedness**: Are claims supported by retrieved content?
- **Factual Consistency**: Hallucination rate?
- **Latency**: Response time impact of retrieval.

### 2.6 Pitfalls & Best Practices

✅ Ensure chunk overlap covers query ambiguity.
✅ Use summaries for long docs.
❌ Avoid injecting too many irrelevant chunks.
❌ Avoid mixing similar but conflicting docs.

---

## 🤖 3. Agents

### 3.1 Overview

- **Agent = model + memory + tool access + control flow**.
- Agents can:
  - Interact with environments.
  - Select tools.
  - Reflect and adapt.

**Example Use Cases:**
- File QA agents
- Web scraping + summarizing bots
- Developer agents (e.g., SWE-Agent)

### 3.2 Tools

- Implemented as callable functions or APIs.

```python
def search_tool(query):
    return web_search(query)

def run_sql(query):
    return sql_engine.execute(query)
```

- Tools can be language-specific (Python, Bash), or service wrappers (APIs).

### 3.3 Planning & Control Flows

#### Common Plans:
- **Sequential**: fetch_data → process → summarize
- **Conditional**: IF API_fails THEN retry()
- **Looped**: Repeat scraping until all pages processed

**Plan Prompting Format**:
```text
Task: Summarize top news.
Plan: [search_news, extract_titles, summarize]
```

### 3.4 Failure Modes & Evaluation

- **Tool Misuse**: Wrong tool for task
- **Timeouts**: Tool doesn’t return in time
- **Stuck Loops**: Plan never terminates

**Evaluate Agents By:**
- Task completion rate
- Steps taken vs optimal
- Reflection/adjustment quality

### 3.5 Reflection and Iteration

#### ReAct Pattern:
```text
Thought: I need data.
Action: fetch_sales_data
Observation: Found 1 week of sales
Thought: I need 4 weeks. Retry...
```

#### Reflexion Pattern:
- After step failure, critique reasoning.
- Rerun with adjusted plan.

### 3.6 Security

- Limit tools exposed.
- Validate input params (e.g., SQL injection).
- Use audit logs and sandboxing.

---

## 🧠 4. Memory in RAG & Agents

- **Short-Term**: Local to one run; limited to context window.
- **Long-Term**:
  - Vector DB (e.g., ChromaDB, Weaviate)
  - SQL logs
  - Session histories

**Use Case**: Personalized tutor agent using persistent memory of past answers.

---

## ✅ 5. Review Questions

1. What are the roles of retriever and generator in RAG?
2. Name three control flow patterns in agents.
3. How do ReAct and Reflexion differ?
4. What metrics can evaluate agent quality?
5. How is memory handled across RAG and agent systems?

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

# Tool definitions
def get_weather(location):
    return f"Weather in {location} is sunny."

def search(query):
    return f"Search results for {query}."

tools = [
    Tool(name="get_weather", func=get_weather, description="Gets weather"),
    Tool(name="search", func=search, description="Web search")
]

# Initialize Agent
agent = initialize_agent(tools, OpenAI(), agent="zero-shot-react-description", verbose=True)
result = agent.run("What’s the weather in Paris and top 3 tourist spots?")
```

### 🔹 Agent Memory Store
```python
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory(memory_key="chat_history")
agent_chain = initialize_agent(..., memory=memory)
```

Let me know if you’d like this exported or if you want to dive into Chapter 7 next!

### Agent with SQL + Planning
```python
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.utilities import SQLDatabase
from langchain.llms import OpenAI

# Define SQL tool
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