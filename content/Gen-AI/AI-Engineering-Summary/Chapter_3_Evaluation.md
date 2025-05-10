# Chapter 3: Evaluation Methodology

---

### 📚 Structure Overview

1. **Challenges of Evaluating Foundation Models**  
2. **Understanding Language Modeling Metrics**  
   - Entropy  
   - Cross Entropy  
   - Bits-per-Character and Bits-per-Byte  
   - Perplexity & Interpretation  
3. **Exact Evaluation**  
   - Functional Correctness  
   - Similarity Measurements  
   - Embedding-Based Similarity  
4. **AI as a Judge**  
   - Use Cases, Setup, Limitations  
5. **Comparative Evaluation**  
   - Ranking Models  
   - Challenges  
   - Future Directions

---

### ✅ 1. Challenges of Evaluating Foundation Models

- Foundation models are **open-ended** → hard to evaluate with fixed labels.
- Evaluation now includes:
  - Accuracy & alignment
  - Safety, usefulness, creativity
- **Why it's hard**:
  - More intelligent outputs require **expert review**
  - Human evaluation is slow, expensive
  - Existing benchmarks quickly become obsolete
  - Quality varies by **domain, format, and task complexity**
- **Underinvestment**: Evaluation lags behind modeling in tooling and R&D.

**Interview Tip**: Know why eyeballing results is insufficient in production.

---

### ✅ 2. Understanding Language Modeling Metrics

#### Entropy (Shannon)
- Measures uncertainty in a distribution.
- Higher entropy = more randomness.
- “How many bits are needed to encode a message?”

#### Cross Entropy
- Measures distance between true label distribution \(P\) and predicted \(Q\).
\[ H(P, Q) = - \sum P(x) \log Q(x) \]

#### Bits-per-Character (BPC), Bits-per-Byte (BPB)
- Used to normalize cross entropy across token granularities (char/byte).

#### Perplexity
- \( PP = 2^{H(P, Q)} \) or \( e^{H(P, Q)} \)
- Lower is better. Indicates model “confidence”.
- Used in training diagnostics and benchmarking (e.g., LLaMA, PaLM).

**Interview Tip**: Perplexity is only valid when labels are available. Doesn’t always reflect downstream task quality.

---

### ✅ 3. Exact Evaluation

#### Functional Correctness
- Checks if model output **satisfies task requirements**.
- Best for deterministic tasks: code, SQL, math, data pipelines.
- **pass@k** in coding: if one of k generated solutions passes all test cases, count as correct.
- Common in benchmarks like HumanEval, MBPP, Spider.

#### Similarity Against References
- Used when gold-standard outputs exist.
- Types:
  - **Exact match**
  - **Lexical similarity** (BLEU, ROUGE)
  - **Semantic similarity** (BERTScore, cosine in embedding space)
- **Reference-free eval** growing in popularity (e.g., with AI judges).

#### Embedding Similarity
- Convert text to vector and compute distance (cosine similarity).
- E.g., CLIP for image-text pairs, BERT or OpenAI embeddings for text.

**Interview Tip**: Know when exact match breaks (e.g., paraphrasing) and when embedding-based similarity is better.

---

### ✅ 4. AI as a Judge

#### Concept
- Use LLMs to score or evaluate outputs.
- AI model = "meta-evaluator"

#### Benefits
- Scalable, cheap, no reference data required.
- More nuanced than hardcoded metrics.

#### Setup
- Define evaluation rubric.
- Prompt the LLM to score outputs or choose between completions.

#### Limitations
- Scores vary by **model version and prompt phrasing**.
- Not consistent over time; can't benchmark longitudinally.
- Need calibration with human evaluation.

#### What Models Can Be Judges?
- GPT-4 (most used), Claude, PaLM-2

**Interview Tip**: Know pros/cons of LLM-based eval vs traditional metrics.

---

### ✅ 5. Ranking Models with Comparative Evaluation

#### Pointwise vs. Comparative
- **Pointwise**: score each model independently.
- **Comparative**: pairwise comparison (A vs B) → better signal for subjective tasks.

#### Use Cases
- LMSYS Chatbot Arena, Anthropic RLHF datasets

#### Process
1. Generate outputs from multiple models.
2. Present pairs to human or AI judges.
3. Tally win rates.
4. Use ranking algorithm (e.g., Elo, Bradley-Terry).

#### Challenges
- **Scalability**: Pairwise comparisons grow quadratically.
- **Transitivity issues**: Human preference may not be transitive.
- **Noisy signals**: Non-experts may introduce noise.

#### Future Trends
- Embedding feedback loops into products.
- Use AI to triage, then humans for hard cases.

**Interview Tip**: Understand difference between comparative eval and A/B testing. Comparative = side-by-side.

---

### 🔹 Summary Takeaways

- Evaluation is essential to deploy safe, useful Gen-AI systems.
- Combine **exact + subjective** methods for robust pipelines.
- Use **perplexity & entropy** for training eval, **functional correctness** for tasks, and **AI judges** for nuance.
- Comparative evaluation is growing but requires care in design.

---

### 🪡 Interview Review Questions (with Answers)

1. **Why is evaluating foundation models harder than classic ML?**  
   → Open-ended outputs, subjective quality, fast model evolution, lack of labels.

2. **What are the key language modeling metrics?**  
   → Entropy, cross-entropy, perplexity, BPC/BPB.

3. **When should you use AI as a judge?**  
   → When you lack references, need subjective judgment, or want scalable evaluation.

4. **What are pitfalls of using perplexity?**  
   → Doesn’t align with human preference, invalid for non-language outputs.

5. **How does comparative evaluation differ from A/B testing?**  
   → Comparative = multiple outputs shown side-by-side; A/B = one-at-a-time.

---

### 💻 Code Examples & Snippets

#### 1. Perplexity Calculation with HuggingFace Transformers
```python
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
import math

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
model.eval()

input = "The future of AI is exciting."
inputs = tokenizer(input, return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs, labels=inputs['input_ids'])
    loss = outputs.loss
    perplexity = math.exp(loss.item())
print(f"Perplexity: {perplexity:.2f}")
```
*Purpose*: Estimate how confidently the model predicts the next token.

#### 2. Semantic Similarity with Sentence Transformers
```python
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')

s1 = "The cat sits on the mat."
s2 = "A feline is on a rug."
emb1 = model.encode(s1, convert_to_tensor=True)
emb2 = model.encode(s2, convert_to_tensor=True)
similarity = util.pytorch_cos_sim(emb1, emb2)
print("Cosine similarity:", similarity.item())
```
*Purpose*: Compute semantic similarity between two texts.

#### 3. Prompt for AI-as-a-Judge Evaluation
```python
prompt = """
Evaluate the helpfulness of the following response on a scale of 1-10:

Question: How do I fix a bug in my React app?

Response: Have you tried turning it off and on again?

Score:
"""
response = openai.Completion.create(model="gpt-4", prompt=prompt)
print(response['choices'][0]['text'])
```
*Purpose*: Use GPT as a judge by asking for a rating.

---


