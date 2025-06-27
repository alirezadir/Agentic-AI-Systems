# 1. Gen-AI Evaluation 

 This summary combines **Model Evaluation** and **Application Evaluation** as detailed in *AI Engineering* by Chip Huyen.


## 1. Model Evaluation

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
