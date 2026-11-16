# RAG and Knowledge System Design

Retrieval-Augmented Generation (RAG) grounds model outputs in external knowledge. In system design, RAG is not just "vector DB plus prompt"; it is a data, retrieval, permission, context, evaluation, and product-trust subsystem.

Use this page as the system-design guide for enterprise search, document assistants, knowledge copilots, agentic retrieval, multimodal RAG, and cited-answer systems.

## Core Architecture

```text
documents / data sources
  -> ingestion
  -> parsing and normalization
  -> chunking and metadata extraction
  -> embeddings, lexical indexes, graph indexes
  -> access-control filters

query
  -> auth and policy checks
  -> query understanding / rewriting
  -> retrieval
  -> reranking
  -> context packing
  -> model generation
  -> citation and groundedness checks
  -> answer, abstention, or escalation
  -> traces, feedback, and evals
```

## Why Use RAG

Use RAG when the system needs:

- Fresh or frequently changing knowledge.
- Private or proprietary knowledge.
- Source-grounded answers.
- Citations and auditability.
- Access-control-aware retrieval.
- Domain-specific facts that should not be baked into model weights.
- Deletion, retention, or compliance controls.

Do not use RAG as a reflex. If a task needs stable style, format, or behavior rather than external facts, prompting or fine-tuning may be a better lever.

## RAG Components

| Component | Responsibility | Design Questions |
|-----------|----------------|------------------|
| Source connectors | Pull data from docs, wikis, databases, tickets, emails, code, media, or APIs. | What is the source of truth? How fresh must data be? |
| Parser | Convert files into text, tables, layout, images, metadata, and structured records. | Is deterministic parsing needed before model reasoning? |
| Chunker | Split content into retrievable units. | What chunk size, overlap, hierarchy, and metadata preserve meaning? |
| Indexes | Store lexical, vector, graph, or multimodal representations. | Which retrieval modes are needed? |
| Retriever | Fetch candidate evidence. | How are query rewriting, filters, and top-k chosen? |
| Reranker | Reorder candidates with a stronger relevance signal. | What is the latency and quality trade-off? |
| Context packer | Fit evidence into the model context. | What gets included, compressed, cited, or dropped? |
| Generator | Produce grounded answer or structured output. | How does the model cite, abstain, or ask follow-up questions? |
| Verifier | Check faithfulness, policy, format, and citations. | What failures require retry, fallback, or escalation? |
| Eval/observability | Measure retrieval and answer quality. | Which traces and metrics prove the system works? |

## Retrieval Patterns

### 1. Basic RAG

```text
query -> retrieve -> augment prompt -> generate answer
```

Use for simple document Q&A, FAQ assistants, and internal knowledge search.

Strengths:

- Simple architecture.
- Fast to prototype.
- Works well when documents are clean and questions are direct.

Limits:

- Weak on ambiguous, multi-hop, or cross-source questions.
- Sensitive to chunking and retrieval quality.
- Can produce grounded-looking answers from irrelevant chunks.

### 2. Hybrid Search

```text
query -> keyword search + vector search -> merge/rerank -> answer
```

Use when exact terms, IDs, names, error codes, legal clauses, or technical vocabulary matter.

Design note: hybrid search is often better than pure vector search for enterprise systems because real user queries mix semantic intent with exact identifiers.

### 3. Reranked RAG

```text
retrieve broad candidates -> rerank -> pack top evidence -> answer
```

Use when first-stage retrieval has acceptable recall but poor ordering.

Trade-off: better quality at the cost of extra latency and compute.

### 4. Multi-Hop RAG

```text
query -> retrieve evidence -> derive next query -> retrieve more -> synthesize
```

Use when answers require connecting facts across documents, entities, or time.

Risks:

- More steps increase cost and latency.
- Each retrieval step can compound errors.
- Requires stronger traceability and evals.

### 5. Agentic RAG

```text
query -> agent decides source/tool/query -> retrieve/search/query -> inspect evidence -> continue or answer
```

Use when the system must decide:

- Whether retrieval is needed.
- Which source to query.
- Whether to use vector search, keyword search, SQL, graph, web, or API tools.
- Whether evidence is sufficient.
- Whether to retrieve again, ask a follow-up, or abstain.

Agentic RAG is useful for complex research and operational assistants, but it needs budget caps, loop detection, traceability, and tool permissions.

### 6. Graph RAG

```text
query -> entity/relation extraction -> graph traversal + document retrieval -> synthesis
```

Use when relationships are central: organizations, people, transactions, dependencies, legal clauses, incidents, code ownership, or supply chains.

### 7. Multimodal RAG

```text
documents/images/audio/video -> multimodal parsing/indexing -> retrieval -> multimodal or text synthesis
```

Use when knowledge lives in charts, screenshots, scanned documents, diagrams, images, videos, or audio.

Common options:

- Embed text and images into a shared multimodal space.
- Summarize images/tables/charts into text and retrieve summaries.
- Store image summaries with pointers to raw artifacts.
- Retrieve text plus raw images and pass both to a multimodal model.

See runnable examples in [`code/`](./code/).

## Data and Index Design

Chunk metadata matters as much as chunk text.

Useful metadata:

- Document ID and version.
- Source URL or storage path.
- Author/owner.
- Tenant/user/group ACL.
- Timestamp and freshness.
- Section/page/paragraph/table/figure.
- Chunk hierarchy.
- Language.
- Data classification.
- Deletion/retention policy.

Example record shape:

```json
{
  "chunk_id": "policy_v4_page12_chunk03",
  "document_id": "refund_policy",
  "document_version": "v4",
  "text": "Refunds require approval after 30 days...",
  "metadata": {
    "source": "support_policy_pdf",
    "page": 12,
    "section": "Refund exceptions",
    "tenant": "global",
    "acl": ["support_agents"],
    "updated_at": "2026-06-01"
  }
}
```

## Access Control and Privacy

Enterprise RAG must filter before generation.

Controls:

- Enforce ACLs at retrieval time, not only after generation.
- Keep tenant indexes isolated when risk is high.
- Filter by user, group, role, region, and data classification.
- Prevent citations to unauthorized sources.
- Redact PII when context leaves the trusted boundary.
- Support deletion and re-indexing.
- Log which sources were retrieved and shown to the model.

Failure mode: the final answer can leak information even if the cited source is hidden. Retrieval and generation both need policy checks.

## Context Packing

Retrieved chunks are not automatically good context.

Packing decisions:

- Top-k evidence.
- Diversity across sources.
- Recency and authority.
- Redundancy removal.
- Compression/summarization.
- Source ordering.
- Citation format.
- Token budget.
- Conflict handling.

Useful pattern:

```text
query
  -> candidates
  -> rerank
  -> remove duplicates
  -> group by source
  -> include citations and metadata
  -> generate with explicit grounding instructions
```

## Evaluation

Evaluate retrieval and generation separately.

Retrieval metrics:

- Recall@k.
- Precision@k.
- MRR.
- nDCG.
- Source freshness.
- ACL correctness.

Generation metrics:

- Groundedness.
- Faithfulness.
- Citation accuracy.
- Completeness.
- Abstention quality.
- Format validity.
- Safety and PII handling.

End-to-end metrics:

- Task success.
- User satisfaction.
- Escalation rate.
- Time to answer.
- Cost per answered question.
- Human correction rate.

Golden eval cases should include:

- Easy direct facts.
- Multi-hop questions.
- Ambiguous queries.
- Questions with no answer.
- Outdated documents.
- Conflicting sources.
- Unauthorized sources.
- Prompt injection inside retrieved text.
- Tables, charts, images, and scanned PDFs if multimodal.

## Common Failure Modes

- Bad chunking loses context.
- Retrieval misses exact IDs or rare terms.
- Reranker over-prioritizes semantically similar but wrong chunks.
- Context includes too much irrelevant text.
- Model answers from prior knowledge instead of evidence.
- Citations point to sources that do not support the claim.
- ACL filters are applied too late.
- Index is stale after document changes.
- Prompt injection inside retrieved content changes behavior.
- Agentic RAG loops or overspends.

## Design Checklist

- What is the source of truth?
- How fresh must the index be?
- What document types and modalities are supported?
- What chunking strategy preserves meaning?
- Which retrieval modes are needed?
- How are ACLs enforced?
- How are citations generated and verified?
- What happens when evidence is insufficient?
- How are retrieval and answer quality evaluated?
- How are stale, deleted, or conflicting sources handled?
- What is the latency and cost budget?

## Runnable Examples

Current examples live under [`code/`](./code/) and will move to the hands-on appendix later:

- Basic LangChain RAG.
- LangGraph RAG.
- Multimodal RAG with CLIP.
- Multimodal multi-vector retrieval.
- Agentic RAG.
