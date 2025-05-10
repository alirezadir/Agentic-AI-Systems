# 1. Evaluation 

Evaluation is foundational to developing production-grade generative AI systems. It spans model-level assessment and holistic application-level performance. This section combines **Model Evaluation** and **Application Evaluation** as detailed in *AI Engineering* by Chip Huyen.

---

## 1.1 Model Evaluation

Model evaluation measures how well a model performs specific tasks, independent of system integration.

## 1.1 Evaluation Criteria

- **Domain-Specific Capability**  Accuracy within fields like coding, healthcare, law, finance
    - domain specific benchmarks  (private, public); usually exact correctness (e.g. functional)
    - multiple-choice questions for non-coding tasks; e.g. MMLU (Massive Multitask Language Understanding): math, STEM, social, legal (57 areas)
    - efficieny: runtime, memory usage 

-  **Generation Capability**: Fluency, coherence, and factuality of generated responses
    - Factual consistency: local (against context); global (open knowledge) 
        - self-verification (e.g. selfcheckGPT), Knowledge-augmented verification (e.g. Google's SAFE: Search-Augmented Factuality Evaluator: reasoning -> Google API); 
        - Textual Entailment: Decides two statements if, Entailment, Contradiction, Neutral
- **Instruction-Following**: Adherence to task requirements, constraints, and formatting 
    - Benchmarks: IF-Eval (Google, focus on expected format), INFOBench
    - Role-playing: RoleLLM (AI Judge)
- **Cost and Latency**: TTFT (Time to First Token), TPS, total latency, token costs 

Example: 
| **Criteria**        | **Metric**        | **Hard**       | **Ideal**     |
|---------------------|-------------------|----------------|---------------|
| Cost                | $/1M tokens       | < $30          | < $15         |
| Scale               | Tokens/min (TPM)  | > 1M           | > 1M          |
| Latency (TTFT)      | P90               | < 200 ms       | < 100 ms      |
| Latency (Total)     | P90               | < 1 min        | < 30 sec      |
| Model Quality       | Elo score         | > 1200         | > 1250        |
| Code Generation     | pass@1 (HumanEval)| > 90%          | > 95%         |
| Factual Consistency | Internal metric   | > 0.8          | > 0.9         |

Model Benchmarks
	•	Use public benchmarks for model filtering, not selection.
	•	For real usage, private leaderboards and application-specific tests work better.
	•	Combine automated and human feedback (e.g. AI-as-a-judge) for robustness 


### 1.1.2 Language Modeling Metrics

| Metric            | Description                                                           |
| ----------------- | --------------------------------------------------------------------- |
| **Entropy**       | Measures uncertainty in predictions                                   |
| **Cross-Entropy** | Average bits needed to encode output given the model                  |
| **Perplexity**    | Exponential of cross-entropy; lower values indicate better prediction; measures how difficult it is for a model to predict a given text. |
| **BPC/BPB**       | Bits-per-character / bits-per-byte for compression-like tasks         |

## 1.3 Model Evaluation Methods
- **Exact vs Subjective evaluation methods**
    - Exact: no ambiguity (e.g. MCQ)
    - Subjective: e.g. essay score 
### 1.3.1 Exact Evaluation

These rely on comparison with reference outputs.

- ##### Functional Correctness

    - Does it meet functional requirements, and correctness?
    - Tasks like coding and structured queries (e.g. SQL generation).
    - Benchmarks: HumanEval (OpenAI) & MBPP(Google python) for coding; BirdSQL, Spider, Wii=kiSQL for text-to-SQL
    

- ##### Similarity to Reference Data (GT)
    * Data: (Input, reference GT), e.g. in Translation
    * similarity between two open-ended texts:
        * **Human Eval**
        * **Exact Match**
        * **Lexical Similarity**: BLEU, ROUGE, METEOR
        * **Semantic Similarity**: Cosine similarity of sentence embeddings A.B/(|A|.|B|)
            - Embeddings: BERT, CLIP, OpenAI text-embedding, sentence transformer
            - metrics e.g. BERTScore, etc 
            - used for any modaility: 
                - Mutlimodal embeddings space: joint embeddings space: e.g. `[text_embedding x text_proj_matrix + vision_embedding x vision_proj_matrix]`

- ##### Embedding Similarity

    *  Leverages vector closeness to assess semantic correctness


### 1.3.2 AI as a Judge

* Using LLMs to evaluate LLMs (using AI to evaluate
AI)
* prompt template ({question}, {answer}) + LLM model
* Pros: Fast, easy, cheap; Scalable (e.g. 58% of LangChain evals), 
* Limits: consistency; may inherit biases 
* Use Chain-of-Thought or multiple judge models for robustness
* Ai as a Judge methods: 
    - Evaluate  quality of a response by itself `Given the following question and answer, evaluate how good the answer is
for the question. Use the score from 1 to 5.`
    - compare w/ reference response
    - compare two responses 


### 1.3.3  Comparative Evaluation (Model Ranking)

* Ranking models: **pointwise**  vs **comparative evaluation.**
* **Pointwise Ranking** eval independently; compare scores                         |
* **Comparative Ranking:**: eval models against each other; compute a ranking from comparison results.
    - Benchmarks: popular LMSYS’s Chatbot Arena leaderboard
    - Challenges: Scalability bottlenecks, Lack of standardization and quality control
<!-- | **Relative Scoring** | Rate models against each other rather than absolute metrics |
| **Blind Testing**    | Prevent rater bias by anonymizing model source              | -->

#### Future Trends

* Live A/B testing in production
* Community voting platforms
* Human-AI ensemble judging

---

### 1.4 Model Selection Workflow

**Two-steps for model selection**: 
1. Best achievable performance
2. Map models on cost–performance axes; choose a model that
gives the best performance for bucks 

**Model Selection Workflow**:
1. Filter out models with hard attributes
2. **Public model eval:** Filter with public benchmarks (e.g. HELM, LMSYS)
3. **Task specific eval**: Define task-specific metrics & evaluate candidate models on internal data and own eval pipeline:            
    - Objectives: quality, latency, and cost.
    - Run cost-performance tradeoff analysis
    - Select based on total ROI, not just raw performance
4. Online eval: monitor, and collect feedback 

---

## 1.2 Application (System) Evaluation

Application evaluation measures whether the full AI system performs its intended function in realistic use cases.

### 1.2.1 Evaluation Pipeline Design

**System Eval Pipeline Steps:**

1. **Evaluate All Components**: 
    - Many components: Retrieval, orchestration, fallback, guardrails
    - levels: per task, per turn, and per intermediate output.
2. **Create Evaluation Guidelines**: 
    - *A correct response is not always a good response* 
    - Good response criteria: e.g.: Relevance (to query), Factual consistency (to context), Safety
    - Define criteria, 
    - Rubric scores with (positive/negative) examples
    - Tie metrics to business metrics: 
        - e.g. Factual consistency of 80%: we can automate 30%
3. **Select Evaluation Methods & Datasets**: 
    - Select Evaluation methods: 
        - e.g. toxicity classifier(toxicity) + semantic similarity (relevance) + AI judge (factual consistency)
        - Mix & match: small classifier for 100% of data + expensive judge for 1% 
        - use logprobs if available (esp for classification)
        - use automatic metrics when posssible, 
    - Select Evaluation Data: 
        - Mix of real, synthetic, edge-case, and adversarial inputs
        - Annotate eval data: prod data or label with human / AI
        - slice based evaluation: based on input type, user tiers, tags, length, etc (prevents misinterpretation due to Simpson’s paradox)
        - multiple evaluation sets: behavior across usage types, devices, error types
        - estimate sample size needs: larger samples needed to confirm small performance gains (e.g. ~100 for 10% gain, ~1,000 for 3%,)
        - evaluate your evaluation pipeline (high quality high score, business metrics)
        - ensure reproducibility (consistent judge configs (e.g. temperature = 0), fixed prompts, sampling)
        - ontrol evaluation overhead (for latency)



#### Scoring Approaches

| Score Type        | Description        | Example                    |
| ----------------- | ------------------ | -------------------------- |
| **Binary**        | Pass/fail          | JSON format validity       |
| **Ordinal Scale** | 1-5 or 1-10        | Relevance, tone            |
| **Categorical**   | Predefined classes | Offensive / Helpful / Safe |

Use **multiple raters** or **LLMs-as-judges** for scale.


#### Task-Level vs Turn-Level Evaluation

| Level          | Focus                                                                                            |
| -------------- | ------------------------------------------------------------------------------------------------ |
| **Task-Level** | End-to-end outcome (e.g. "was the ticket booked?")                                               |
| **Turn-Level** | Intermediate steps in multi-turn workflows (e.g. "was the user's intent correctly interpreted?") |

---

### 1.2.4 Evaluation Rubrics and Fail Modes

**Key Failure Modes:**

* Misinterpretation of input
* Incoherent or factually incorrect answers
* Leaking sensitive data or PII
* Hallucinated citations or sources

Rubrics should contain both:

* Success criteria with examples
* Failure examples with severity tagging

---

### 1.2.5 Monitoring, Logging & Feedback Loops

* Track metrics over time and deployments
* Use logs to audit failure cases
* Integrate **user feedback** with system scoring

**Metric Axes**:

* Prompt/model version
* User segment
* Query type

---

### 1.2.6 Tools & Practices

* **LangSmith, Phoenix, Promptfoo** for evaluation orchestration
* Prompt versioning + rollback support
* A/B testing with real users and human raters
* Evaluator dashboards to unify model & app views

---

Evaluation isn’t a one-time task—it must be ongoing, systematic, and automated wherever possible to ensure a safe, performant generative AI platform in production.

---

# 2. Prompt Engineering
- Prompt: instructions (+ context) given to a model to perform a task
    - e.g. Task description, Example(s), Output format
- Prompt engineering: frames input instructions + context to guide a model’s behavior; 
 - often serving as the first step in models adaptation.

## 2.1 Core Concepts

* **In-Context Learning**:

  * Zero-shot: no examples
  * Few-shot: include examples in prompt

* **Prompt Types**:

  * **System Prompt**: configures base behavior
  * **User Prompt**: direct user instruction

* **Context Length and Efficiency**:

  * Use only relevant parts
  * Token limit = cost + latency bottleneck

---

## 2.2 Prompt Engineering Best Practices

1. **Write Clear and Explicit Instructions**
2. **Provide Sufficient Context**: from RAG or knowledge base
3. **Break Complex Tasks into Simpler Subtasks**
4. **Give the Model Time to Think**: Chain-of-Thought
5. **Iterate on Prompts**: test, revise, repeat
6. **Evaluate Prompt Tools**: Promptfoo, DSPy, LangChain
7. **Organize and Version Prompts**: for rollback and reproducibility

---

## 2.3 Defensive Prompt Engineering

| Threat                        | Description                                  |
| ----------------------------- | -------------------------------------------- |
| **Reverse Prompting**         | Extracting proprietary prompts from outputs  |
| **Jailbreaking / Injection**  | Bypassing constraints with adversarial input |
| **Sensitive Info Extraction** | Prompt-crafted info leaks                    |

**Mitigations**:

* Prompt filtering and sanitization
* Guardrails for unsafe completions
* Monitor inputs and outputs

---

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
