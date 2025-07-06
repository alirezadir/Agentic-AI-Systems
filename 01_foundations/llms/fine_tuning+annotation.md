
# 3. Finetuning

Finetuning adapts models by updating weights based on task-specific data.

### 3.1 When to Finetune

**Reasons To:**

* Need consistent tone/format/voice
* Repetitive prompts required
* Few-shot prompting fails

**Reasons Not To:**

* High cost (GPU + engineering)
* Frequent data drift → retraining
* Can solve with prompt/context updates

**Finetuning vs. RAG:**

* Use RAG when external knowledge varies rapidly
* Combine both in advanced pipelines

### 3.1.1 When to Finetune, RAG, or Prompt Engineer


| Scenario                                                     | Recommendation                                        |
| ------------------------------------------------------------ | ----------------------------------------------------- |
| Repeated task with limited variability                       | **Prompt Engineering**                                |
| Tasks requiring up-to-date or external knowledge             | **RAG**                                               |
| Need to inject style, format, tone or structure consistently | **PEFT (e.g. LoRA)**                                  |
| When prompt engineering fails or is too verbose              | **PEFT or Full Finetuning**                           |
| Performance bottleneck due to retrieval latency              | **Finetuning over RAG**                               |
| Low-resource environments (edge, mobile)                     | **Finetune lightweight models**                       |
| High-stakes or regulated domains                             | **PEFT + Strict evaluation + Optional Full Finetune** |

---

## 3.2 Memory Bottlenecks

1. **Trainable Parameter Load**: full models = 10s of GB
2. **Memory Math**: 4 bytes x 2 (optimizer) x params
3. **Precision Tricks**:

   * BF16, FP8, quantization for reduced memory

---

## 3.3 Finetuning Techniques

| Technique                 | Notes                                         |
| ------------------------- | --------------------------------------------- |
| **Full Finetuning**       | All weights, most powerful but costly         |
| **PEFT (e.g. LoRA)**      | Train small adapter layers only               |
| **Model Merging**         | Combine checkpoints with task-specific models |
| **Multi-task Finetuning** | Jointly optimize across datasets              |

---

## 3.4 Finetuning Tactics

* Use clean, task-aligned, diverse data
* Monitor overfitting with validation samples
* Use checkpointing and eval hooks during training
* Consider post-finetuning eval + prompt tuning

---

Finetuning should be used strategically and not by default. Prompt engineering and RAG are often lower-lift and can achieve comparable gains.

# 5. Data Annotation Guidelines

High-quality annotations are critical to building effective AI systems. Poor annotation leads to noisy training data, low-quality evaluations, and flawed deployment decisions.

## 5.1 Principles of Good Annotation

| Principle                   | Description                                                     |
| --------------------------- | --------------------------------------------------------------- |
| **Clarity**                 | Guidelines must clearly define each class or scoring dimension  |
| **Consistency**             | Same input yields the same annotation across annotators/time    |
| **Coverage**                | Guidelines should include both canonical and edge-case examples |
| **Alignment with Use Case** | Scoring should reflect application needs, not academic goals    |

---

## 5.2 Guidelines Structure

* **Task Definition**: Describe the objective in plain language
* **Scope Specification**: Define what’s in and out of scope
* **Annotation Rubrics**: Provide rating scales or labels, with definitions
* **Examples & Counterexamples**: Real, synthetic, and adversarial samples

---

## 5.3 Avoid Common Pitfalls

| Pitfall                        | Risk                                     |
| ------------------------------ | ---------------------------------------- |
| Vague definitions              | Annotators interpret labels differently  |
| Missing negative examples      | Unclear boundary between success/failure |
| Overly complex scoring schemes | Inconsistency, fatigue, noise            |
| One-size-fits-all criteria     | Misalignment with product behavior       |

---

## 5.4 Evaluator Feedback Loop

* Let annotators flag ambiguous cases
* Regularly revise guidelines based on annotation disagreements
* Integrate evaluator disagreement as a signal in modeling

---

# 6. Chunking Strategies (for RAGs)

Chunking determines how documents are segmented into retrievable units for RAG pipelines. Well-chunked data improves both **retrieval recall** and **generation quality**.

## 6.1 Why Chunking Matters

* LLMs have fixed context limits (e.g. 4k–32k tokens)
* Small chunks = higher retrieval recall, but may miss context
* Large chunks = more context, but worse recall and latency

---

## 6.2 Chunking Strategies

| Strategy              | Description                                                 |
| --------------------- | ----------------------------------------------------------- |
| **Fixed-Length**      | Break at uniform token/window size (e.g. every 512 tokens)  |
| **Semantic-Based**    | Use paragraph/sentence boundaries, meaning-aware splitting  |
| **Document-Aware**    | Maintain markdown/code structure, tables, headers           |
| **Adaptive Chunking** | Dynamically size chunks based on importance or section role |

---

## 6.3 Best Practices

* Avoid splitting entities or references mid-sentence
* Optimize for **retrieval unit granularity**:

  * Legal docs → larger chunks
  * FAQs/emails → smaller chunks
* Include metadata (e.g. source, title, headers) for re-ranking and grounding

---

## 6.4 Tools & Implementations

* **LangChain TextSplitters**: character, token, recursive, markdown, code
* **LlamaIndex Node Parsers**: hierarchical document parsing
* Consider windowed chunk overlap (stride) to retain cross-chunk coherence

---

Chunking is both a preprocessing and architectural decision in retrieval systems. Tailor it to document type, query style, and latency constraints.
