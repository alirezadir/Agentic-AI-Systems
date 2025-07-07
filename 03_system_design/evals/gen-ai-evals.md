# Gen-AI Evaluation

This guide synthesizes best practices for **Model Evaluation** and **System Evaluation** as described in *AI Engineering* book by Chip Huyen.

---

## 1. Model Evaluation

Model evaluation assesses how effectively a model performs its intended tasks, independent of the broader system.

### 1.1 Model Evals: Criteria

- **Domain/Task Performance**: Accuracy in specialized domains (e.g., coding, healthcare, law, finance) via public/private benchmarks (e.g., MMLU for non-coding); include efficiency (runtime, memory).

- **Generation Performance**: Fluency, coherence, and factuality (local/global). Methods: self-verification (SelfCheckGPT), knowledge-augmented checks (SAFE), textual entailment.

- **Instruction-Following**: Adherence to requirements, constraints, and format. Benchmarks: IF-Eval, INFOBench, role-based evals (e.g., RoleLLM).

- **Cost and Latency**: Includes TTFT (Time to First Token), TPS (Tokens Per Second), total latency, and token costs.

##### Core LLM Metrics

- **Entropy**: Measures uncertainty in model prediction ($H(p) = -\sum_{i=1}^{n} p_i \log_2(p_i)$, higher -> more uncertainty.)
- **Cross-Entropy**: Uncertainty of model prediction ($H(p, q) = -\sum_{i=1}^{n} p_i \log_2(q_i)$, p: true, q:predicted).
- **Perplexity**: Exponential of cross-entropy; lower values indicate better prediction ($PPL = 2^{H(p,q)}$).
    - e.g H(p,q) = 3 bits, PPL = 8 possible options to choose from.
    - PPL = 1-10: perfect, 10-100: good, 100-1000: bad, 1000+: terrible.
- **BPC/BPB**: Bits-per-character/byte; relevant for compression-like tasks.
- **BLEU**: Precision-based metric for machine translation.
- **ROUGE**: Recall-based metric for summarization.
- **BERTScore**: Semantic similarity metric for text generation.


**Sample Criteria Table:**
| **Criteria**        | **Metric**        | **Hard** | **Ideal** |
|---------------------|-------------------|----------|-----------|
| Cost                | $/1M tokens       | < $30    | < $15     |
| Scale               | TPM (Tokens/min)  | > 1M     | > 1M      |
| TTFT                | ms (P90)          | < 200    | < 100     |
| Total Latency       | sec (P90)         | < 60     | < 30      |
| Quality             | Elo score         | > 1200   | > 1250    |
| Code Gen            | pass@1 (%)        | > 90     | > 95      |
| Factuality          | Internal metric   | > 0.8    | > 0.9     |


### 1.2 Model Evals: Methods

- **Objective methods**: a clear, measurable, correct answer (e.g., multiple-choice, exact match)
- **Subjective methods**: Open-ended, requires judgment (e.g., essay scoring)
    - e.g. "How would you rate the customer service?"

#### Objective Evaluation

- **Functional Correctness**: Does the output meet requirements? Used for coding, SQL generation, etc.
    - Benchmarks: HumanEval (OpenAI), MBPP (Google Python), BirdSQL, Spider, WikiSQL.

- **Similarity to Reference Data (Ground Truth)**
    - Compare model output to reference answers:
        - *Human Evaluation*
        - *Exact Match*
        - *Lexical Similarity*: BLEU, ROUGE, METEOR
        - *Semantic Similarity*: Embedding-based (e.g., cosine similarity using BERT, CLIP, OpenAI embeddings, sentence transformers)
            - Metrics: BERTScore, etc.
            - Applicable to multimodal data via joint embedding spaces.

- **Embedding Similarity**: Uses vector closeness to assess semantic alignment.

#### Subjective Evaluation

- ##### Comparative Evaluation (Ranking Models)

    - **Pointwise Ranking**: Score models independently, then compare.
    - **Comparative Ranking**: Directly compare models against each other to establish a ranking.
        - Example: LMSYS’s Chatbot Arena leaderboard.
        - Challenges: Scalability, standardization, and quality control.
- ##### AI as a Judge

    - Use LLMs to judge other LLMs via prompt templates (e.g., `{question}, {answer}`).
        - Pros: Fast, scalable, low cost.
        - Cons: Can be inconsistent, may reflect model biases.
        - More robust with chain-of-thought or multiple judges.
        - Modes: score a response, compare to reference, or compare two responses.



- **A/B testing** in production
- **Arena Voting**: voting platforms (e.g., LMSYS's Chatbot Arena)
- **Human-AI ensemble judging**
- **Rubric Scoring**



### 1.3 Model Selection

**Two main steps:**
1. Identify the best achievable performance.
2. Map models on a cost–performance curve; select the model with optimal ROI.

**Workflow:**
1. Filter out models based on hard requirements.
    - Use public benchmarks (e.g., HELM, LMSYS) for initial filtering.
2. Define task-specific metrics and evaluate candidates on internal data using your own evaluation pipeline:
    - Assess quality, latency, and cost.
    - Analyze cost-performance tradeoffs.
    - Select based on total ROI, not just raw performance.
3. Continuously monitor in production and collect feedback.

---

## 2. System Evaluation

System evaluation determines whether the complete AI application performs as intended in real-world scenarios.

### 2.1 System Evals: Pipeline Design

#### Key Steps:
1. **Evaluate All Components**
    - Assess each part (retrieval, orchestration, fallback, guardrails, etc.) at task, turn, and intermediate levels.

2. **Select Metrics, Methods & Datasets**
    - Align metrics to business goals.
    - Combine automatic metrics (classifiers, logprobs), AI judges, and human review as needed.
    - Build diverse datasets (real, synthetic, edge, adversarial); annotate via logs, humans, or AI.
    - Slice results to avoid misleading aggregates; maintain multiple eval sets (e.g., by input type, user, tags, length, etc.).
    - Use larger samples for small improvements; validate and minimize evaluation latency; ensure reproducibility.

3. **Set Clear Guidelines**
    - Define criteria (e.g., relevance, factuality, safety) with rubrics and examples. 
   
#### Notes:
- **Rubrics should include:**
    - Clear success criteria with examples
    - Failure examples, tagged by severity

- **Common Failure Modes:**
    - Misinterpreted input
    - Incoherent or factually incorrect answers
    - Leakage of sensitive data or PII
    - Hallucinated citations or sources

- **Scoring Approaches:**
    - **Binary:** Pass/fail scoring.  
    - Example: JSON format validity.
    - **Ordinal Scale:** Numeric scale, such as 1-5 or 1-10.  
    - Example: Relevance, tone.
    - **Categorical:** Selection from predefined classes.  
    - Example: Offensive / Helpful / Safe.

- **Task-Level vs. Turn-Level Evals**:

    - **Task-Level:** Focuses on the end-to-end outcome.  
    - Example: “Was the ticket booked?”
    - **Turn-Level:** Focuses on intermediate steps in multi-turn workflows.  
    - Example: “Was the user’s intent correctly interpreted?”







- You can scale up by using **multiple raters** or **LLMs-as-judges**.

### 2.2 Monitoring, Logging & Feedback Loops

- Continuously track metrics across time and deployments.
- Use logs to audit and analyze failure cases.
- Integrate **user feedback** into system scoring.

**Metric Axes to Track:**
- Prompt/model version
- User segment
- Query type


### 2.3 Tools & Best Practices

- Use tools like **LangSmith, Phoenix, Promptfoo** for evaluation orchestration.
- Implement prompt versioning and rollback.
- Run A/B tests with real users and human raters.
- Maintain evaluator dashboards to unify model and application views.

**Remember:** Evaluation is not a one-time event. It should be ongoing, systematic, and as automated as possible to ensure your generative AI platform remains safe, reliable, and high-performing in production.
