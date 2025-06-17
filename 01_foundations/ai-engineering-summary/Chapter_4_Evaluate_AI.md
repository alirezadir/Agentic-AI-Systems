# Chapter 4: Evaluating AI Systems 

---

### 📖 Structure Overview

1. Evaluation-Driven Development  
2. Evaluation Criteria  
   - Domain-Specific Capability  
   - Generation Capability  
   - Instruction Following Capability  
   - Cost and Latency  
3. Model Selection  
   - Benchmarks and Leaderboards  
   - Open Source vs. APIs  
4. Designing an Evaluation Pipeline  
   - Define Evaluation Guidelines  
   - Evaluate All Components  
   - Use Mixed Evaluation Methods  
   - Evaluate Evaluation Pipeline

---

### ✅ 1. Evaluation-Driven Development

- Inspired by **Test-Driven Development**: Define evaluation goals before building.
- Use-case examples:
  - **Recommender systems**: evaluated via engagement or purchase rate.
  - **Fraud detection**: dollars saved from fraudulent activity.
  - **Generative code**: functional correctness via pass@k.
- **Why it matters**: Helps avoid deploying apps with unclear ROI.

**Interview Tip**: Always tie model goals to measurable outcomes.

---

### ✅ 2. Evaluation Criteria

#### Domain-Specific Capability
- How well does the model perform in the domain? (e.g., legal, finance, healthcare)
- Metrics: accuracy, task-specific correctness

#### Generation Capability
- Fluency: Is the language grammatically correct?
- Coherence: Does the response follow logical structure?
- Factual Consistency: Does it align with context or source?
  - **Benchmarks**: TruthfulQA
  - **Tools**: GPT-Judge, Claude, Gemini

#### Instruction Following
- Does the model follow formatting, style, constraints?
- Scored via rule-based classifiers, AI judges, or manual reviews.

#### Cost & Latency
- Model response time and inference cost.
- Crucial for production viability and scaling.

---

### ✅ 3. Model Selection

#### Benchmarks & Leaderboards
- **Public Benchmarks**:
  - Pros: Weed out poor models
  - Cons: Contaminated by training data, not task-specific
- **Leaderboards**:
  - LMSYS, HuggingFace, HELM
  - Aggregation not always transparent

**Contamination Example**: GPT-3 had ~40% overlap with common benchmarks【51:7†source】.

#### Open Source vs. Model APIs
- Trade-offs across 7 axes:
  - **Privacy**: Open source = private; API = data leaves boundary
  - **Cost**: APIs may scale cheaper; open source = infra & tuning overhead
  - **Control**: Open source = more tunability; APIs = fixed behavior

**Interview Tip**: Expect to explain "build vs. buy" logic and infrastructure tradeoffs.

---

### ✅ 4. Designing an Evaluation Pipeline

#### Step 1: Define Evaluation Guidelines
- What makes a response "good" or "bad"?
- Use real test queries, generate responses, manually label.
- **Create rubrics**: Binary, 1–5 scale, -1/0/1 for contradiction/neutral/entailment.
- Validate with humans or AI agents.

#### Step 2: Evaluate All Components
- Evaluate per **turn**, **task**, and **component**.
- Example: Resume Parser:
  - Step 1: Extract text (similarity)
  - Step 2: Extract employer (classification accuracy)

#### Step 3: Use Mixed Evaluation Methods
- Combine:
  - **Automatic classifiers** (fast, low-cost)
  - **AI Judges** (nuanced, costly)
  - **Human feedback** (production-ready truth signal)
- Use **logprobs** for model confidence and token-by-token analysis.

#### Step 4: Slice-Based Evaluation
- Analyze model by:
  - User group (free vs. premium)
  - Query source (mobile vs. web)
  - Query type (short vs. long)
- Prevents **Simpson’s Paradox**: Aggregates may hide true performance patterns.

#### Step 5: Estimate Sample Size
- OpenAI guidelines:
  - 10% difference: ~100 samples
  - 3%: ~1,000
  - 1%: ~10,000

---

### ✅ Evaluation Examples & Metrics

- **MCQs**:
  - Great for knowledge and reasoning.
  - Easy to generate, benchmark, and verify.
  - Metrics: accuracy, F1, precision, recall

- **Open-Ended Generation (NLG)**:
  - Metrics: fluency, coherence, faithfulness
  - Evaluation: AI-as-a-Judge, reference similarity, factual consistency

- **Safety Evaluation**:
  - Categories: profanity, self-harm, hate speech, stereotypes, bias
  - Tools: GPT-4/Claude moderation, Meta’s LlamaGuard, Perspective API
  - Benchmarks: RealToxicityPrompts, BOLD

---

### 🔹 Summary Takeaways

- Use **evaluation-first design** to guide AI development.
- Build **multi-tiered evaluation pipelines**: rule-based, statistical, human.
- Apply **data slicing** and **criteria mapping** to uncover weaknesses.
- Tie model scores back to **business metrics**.
- Iterate continuously — even your evaluation needs evaluation.

---

### 🪡 Interview Review Questions (with Answers)

1. **Why is evaluation-driven development important?**  
   → Prevents unclear ROI, ensures measurable business value.

2. **What four categories define evaluation criteria?**  
   → Domain capability, generation quality, instruction following, cost & latency.

3. **Why are public benchmarks insufficient for model selection?**  
   → They may be contaminated, misaligned with your application, or non-transparent.

4. **How should you evaluate a multi-step system?**  
   → Evaluate each component and the full pipeline independently.

5. **What is Simpson’s Paradox, and why does it matter?**  
   → A model may underperform on subgroups even if it looks good on aggregate.

6. **What makes an AI judge unreliable over time?**  
   → Inconsistency due to sampling, prompt phrasing, or underlying model changes.

---

### 💻 Code Examples & Snippets

#### 1. Functional Evaluation Using Prompt + Classifier
```python
# Check if model response follows instruction format
from transformers import pipeline
classifier = pipeline("text-classification", model="typeform/distilbert-base-uncased-mnli")

response = "You are a terrible fit."
result = classifier(response)
print(result)  # {'label': 'CONTRADICTION', 'score': ...}
```
*Purpose*: Detect instruction-violating or unsafe responses.

#### 2. Task-Specific Evaluation with Logprobs
```python
# Estimate confidence in classification
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model.eval()

prompt = "The correct label is:"
inputs = tokenizer(prompt, return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs, labels=inputs["input_ids"])
    logprobs = outputs.loss
print("Model confidence (logprob):", -logprobs.item())
```
*Purpose*: Use logprobs to infer model confidence.

#### 3. AI Judge Prompt Example (Factual Consistency)
```text
Prompt:
"Does the summary contain untruthful or misleading facts not supported by the source text?\n\nSource: {{document}}\nSummary: {{summary}}\nAnswer:"
```
*Purpose*: Evaluate factual consistency using LLM as meta-evaluator.

---

