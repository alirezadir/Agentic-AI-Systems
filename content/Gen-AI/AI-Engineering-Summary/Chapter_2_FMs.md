**Chapter 2: Understanding Foundation Models — Study Guide for Gen-AI Engineering Interviews**

---

### 📚 Structure Overview

1. **Training Data**
   - Multilingual Models
   - Domain-Specific Models
2. **Modeling**
   - Model Architecture
   - Model Size
3. **Post-Training**
   - Supervised Finetuning
   - Preference Finetuning
4. **Sampling**
   - Sampling Fundamentals
   - Sampling Strategies
   - Test Time Compute
   - Structured Outputs
   - The Probabilistic Nature of AI

---

### ✅ 1. Training Data

#### Key Concepts
- FMs are only as good as the data they're trained on. Data defines **model capabilities and limitations**.
- Data sources: **Common Crawl**, Reddit links, C4, domain-specific corpora.
- Data problems: **bias**, misinformation, coverage gaps (e.g., rare languages).

#### Subsections:
- **Multilingual Models**: Training on English-rich data causes poor generalization for low-resource languages. Need for **language-specific datasets**.
- **Domain-Specific Models**:
  - E.g., **AlphaFold**, **BioNeMo**, **Med-PaLM2**.
  - Key idea: **Generalist models underperform in specialized domains**.
  - Trade-off: More data != better performance if quality is low.

#### Interview Tips
- Emphasize **data curation** skills and sourcing awareness.
- Be ready to discuss **domain adaptation strategies**.

---

### ✅ 2. Modeling

#### Model Architecture
- **Transformer (Vaswani et al., 2017)**:
  - Core of most FMs.
  - Modules: embedding layer → multiple transformer blocks → output layer (unembedding).
  - Strength: self-attention scales well.
  - Limitation: **quadratic complexity** with sequence length.

- **Alternatives to Transformers**:
  - **Mamba**: Linear-time SSMs with competitive performance.
  - **Jamba**: Hybrid of Mamba and Transformers with Mixture-of-Experts (MoE) architecture.

#### Model Size
- Performance increases with:
  - Number of parameters (e.g., LLaMA-13B)
  - Training tokens
  - Training compute (FLOPs)
- **Scaling laws** predict performance vs. compute tradeoffs.
- Model size affects:
  - **Latency, memory use, deployment cost**
  - Feasibility of on-device vs. cloud serving

#### Formulas
- ReLU(x) = max(0, x)
- Scaling Law (simplified): Performance ∝ (params × tokens)^α under compute constraint

#### Interview Tips
- Know the **trade-offs between model size and inference cost**.
- Mention **emerging architectures** like Mamba if asked about future trends.

---

### ✅ 3. Post-Training

#### Supervised Finetuning (SFT)
- Uses human-annotated task-specific datasets.
- Purpose: align model to desired output behavior.
- Example: Finetuning LLM on customer support dialogues.

#### Preference Finetuning
- Uses **comparison data**: (prompt, better response, worse response)
- Trains a **reward model (RM)**:
  - Objective: Maximize \( r_\theta(x, y_w) - r_\theta(x, y_l) \)
  - Algorithm: PPO (Proximal Policy Optimization)

#### Alternatives
- **Best-of-N Sampling**: Generate N completions, select best via RM.
- Used by: Stitch Fix, Grab

#### Interview Tips
- Understand RLHF and why it matters.
- Be able to explain when **SFT alone suffices** vs. when **RLHF is needed**.

---

### ✅ 4. Sampling

#### Sampling Fundamentals
- Sampling = converting output logits into text.
- Core of **model creativity vs. determinism**.
- Source of **hallucinations, variability, creativity**.

#### Sampling Strategies
- **Temperature**: controls randomness. T=0 is greedy; T>1 is exploratory.
- **Top-k Sampling**: Sample from top-k likely tokens.
- **Top-p (Nucleus)**: Sample from minimal set with cumulative probability > p.

#### Structured Output
- Ensure outputs conform to format (e.g., JSON, SQL):
  - Prompting techniques
  - Output parsers / validators

#### Probabilistic Nature
- Models aren't deterministic.
- Prompt like: “Answer truthfully; say 'I don’t know' if unsure”
- Mitigation: Use RAG, prompt strategies, response filtering.

#### Interview Tips
- Know how **temperature, top-k, top-p affect model behavior**.
- Be ready to write prompts for **structured outputs**.

---

### 🔹 Summary

- Foundation models are shaped by **data, architecture, size, and sampling**.
- Most production use cases use **pretrained + finetuned** models.
- Core trade-offs:
  - Accuracy vs. Latency
  - Generalization vs. Specialization
  - Cost vs. Capability

---

### 🪡 Interview Review Questions (with Answers)

1. **What defines a foundation model's capabilities?**
   - Primarily its training data — quantity, quality, and domain coverage.

2. **What are the dominant architecture types in Gen-AI today?**
   - Transformers, with emerging alternatives like Mamba and Jamba.

3. **Why is post-training necessary?**
   - Pretrained models lack alignment; post-training helps with safety, usefulness, and human preference adherence.

4. **Explain the role of sampling in generation.**
   - Converts logits to tokens. Affects randomness, diversity, and likelihood of hallucination.

5. **What are common ways to align models to tasks?**
   - SFT, Preference Finetuning (RLHF, DPO), Best-of-N Sampling.

---

### 💻 Code Examples & Snippets (~1.5 Pages)

#### 1. Top-k and Top-p Sampling (transformers)
```python
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
input_text = "The future of AI is"
inputs = tokenizer(input_text, return_tensors="pt")

# Generate with top-k and top-p sampling
sample_output = model.generate(
    inputs['input_ids'],
    do_sample=True,
    max_length=50,
    top_k=50,
    top_p=0.95,
    temperature=0.8
)
print(tokenizer.decode(sample_output[0], skip_special_tokens=True))
```
*Purpose*: Demonstrates probabilistic text generation.

#### 2. Best-of-N Sampling (pseudo strategy)
```python
def best_of_n_sampling(prompt, model, tokenizer, n=5):
    candidates = []
    for _ in range(n):
        output = model.generate(...)
        score = reward_model.score(output)
        candidates.append((score, output))
    return max(candidates)[1]
```
*Purpose*: Apply reward model to multiple completions.

#### 3. Structured JSON Output with Guardrails
```python
import json
response = model.generate(prompt="Return JSON with name and age")
try:
    data = json.loads(response)
    assert 'name' in data and 'age' in data
except (ValueError, AssertionError):
    print("Invalid structured output")
```
*Purpose*: Postprocess outputs to ensure structure.

---

Let me know if you want this adapted to a Notion doc, PDF, or followed up with Chapter 3!

