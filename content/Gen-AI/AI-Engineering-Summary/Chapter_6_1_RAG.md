# Chapter 6.1 : RAG

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

## 💻 3. Code Snippets

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