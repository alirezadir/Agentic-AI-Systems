# Chapter 8: Dataset Engineering 

---

## 📘 Section Structure

1. Data Curation  
   - Data Quality  
   - Data Coverage  
   - Data Quantity  
   - Data Acquisition and Annotation

2. Data Augmentation and Synthesis  
   - Why Data Synthesis  
   - Traditional Data Synthesis Techniques  
   - AI-Powered Data Synthesis  
   - Model Distillation

3. Data Processing  
   - Inspect Data  
   - Deduplicate Data  
   - Clean and Filter Data  
   - Format Data

---

## 🧩 Data Curation

### ✅ Data Quality
- Measures how well data supports safe, aligned model behavior.
- Poor quality leads to:
  - Hallucinations
  - Inconsistent formatting
  - Unsafe outputs (toxicity, bias)

🧠 *Tips*:
- Use reasoning templates for complex tasks.
- Build curated CoT datasets for math, logic, multi-hop QA.

**Example CoT Response:**
```text
I start with 50 apples, then give away 20. So 50 - 20 = 30. Final answer: 30.
```

---

### ✅ Data Coverage
- Broader coverage improves generalization and robustness.
- Include a mix of:
  - Question types: factual, creative, reasoning, coding
  - Tones: formal, friendly, expert, explanatory
  - Languages and regional phrasing

📚 *Interview Example*: “How would you scale an assistant from healthcare to finance domains?”

---

### ✅ Data Quantity
- Bigger is not always better: quality governs learning.
- Recommended: Start with 5k–10k curated examples → scale with synthetic generation
- Use cross-validation to detect saturation point (when more data stops helping)

🔁 *Metrics to track*:
- BLEU/ROUGE for NLG
- Exact match or F1 for QA
- Perplexity during training

---

### ✅ Data Acquisition and Annotation
- **Internal data**: Requires cleaning, anonymization, and formatting
- **External public datasets**:
  - Alpaca, Dolly, OpenAssistant
  - Helpful-Harmless, ShareGPT, Anthropic HH

Annotation types:
- Classification: Binary/multi-label
- Extraction: Named entities, relations
- Rating: 1–5, or win/loss comparisons

🛠️ *Best Practice*: Use double annotation (2+ reviewers) with reconciliation

---

## 🔁 Data Augmentation and Synthesis

### ✅ Why Data Synthesis
- Useful when:
  - Real data is scarce
  - Privacy limits real-user collection
  - Edge case examples are needed (e.g., rare diseases, uncommon languages)

Benefits:
- Boosts diversity
- Prepares model for unseen instructions
- Enables synthetic safety training

---

### ✅ Traditional Data Synthesis Techniques

**Text-Based Techniques**:
- Back-translation (EN→DE→EN)
- Word swaps (synonyms, hypernyms)
- Tense/gender/number flipping

**Bias Mitigation Example**:
```text
Original: He is a great engineer.
Augmented: She is a great engineer.
```

**Image Analogs**:
- Corruptions (blur, occlusion, rotation)
- Language → replace entities (location, profession)

---

### ✅ AI-Powered Data Synthesis

**LLM-Powered Augmentation**:
- Generate examples with step-by-step reasoning, JSON outputs, tool usage
- Mix prompt styles:
  - Concise instruction
  - Roleplay format
  - Explanation followed by a request

**Tools**:
- OpenAI GPT-4, Claude, Mistral
- HuggingFace `datasets`, `promptsource`
- LangChain agents for chaining instructions

**Generation Strategy**:
- Prompt → Instruction → Completion → Score → Filter → Store

---

### ✅ Model Distillation

- Use a large model to label data → train smaller model (e.g., GPT-4 → Phi)
- Can be used for instruction-tuning or reward modeling

🧠 *Caution*: Ensure no verbatim copying across models (esp. with API ToS)

**Filtering synthetic generations**:
- Length filter
- Prompt/response coherence score
- GPT judge model for helpfulness/safety

---

## 🧹 Data Processing

### ✅ Inspect Data

**Metrics to Inspect**:
- Avg/max/min token lengths
- Token entropy (low = repetitive)
- Topic diversity
- Valid JSON/code percentage

Tools: `matplotlib`, `wordcloud`, `pandas-profiling`, `spaCy`

---

### ✅ Deduplicate Data

**Methods**:
- Exact match removal
- Cosine similarity over embeddings (e.g., using `sentence-transformers`)
- MinHash for fast approximate duplicates

**Why it matters**:
- Reduces overfitting
- Prevents reward hacking (same instruction, seen multiple times)

---

### ✅ Clean and Filter Data

Remove:
- Repetitive outputs (e.g., “I’m sorry, I can’t help with that.”)
- Incomplete JSONs or broken markdown
- Language drift (English prompt, French response)

**Filter Types**:
- Regex-based profanity detection
- Entropy threshold
- Validator functions

---

### ✅ Format Data

Structure for chat-based LLMs:
```json
{
  "messages": [
    {"role": "user", "content": "What is the Pythagorean theorem?"},
    {"role": "assistant", "content": "It states that a^2 + b^2 = c^2..."}
  ]
}
```

Tips:
- Escape symbols correctly
- Avoid unnecessary padding in prompt
- Use consistent quotation, spacing

---

## 💻 Code Examples (Expanded)

### A. GPT-Based Instruction Generation
```python
from openai import OpenAI
client = OpenAI()
topics = ["carbon neutrality", "circular economy"]
for t in topics:
    prompt = f"Write an instruction and detailed response about {t}."
    out = client.chat.completions.create(
      model="gpt-4",
      messages=[{"role": "user", "content": prompt}]
    )
    print(out.choices[0].message.content)
```

### B. Deduplication via Embedding Similarity
```python
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer('all-MiniLM-L6-v2')
embs = model.encode(df["instruction"].tolist(), convert_to_tensor=True)
scores = util.cos_sim(embs, embs)
mask = scores > 0.99  # filter high similarity
```

### C. Token Distribution Check
```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")
token_counts = [len(tokenizer.encode(text)) for text in df["response"]]
plt.hist(token_counts, bins=40)
```

### D. Toxicity Detection and Filtering
```python
from detoxify import Detoxify
model = Detoxify("original")

scores = model.predict(df["response"].tolist())
df["toxicity"] = scores["toxicity"]
df = df[df["toxicity"] < 0.2]
```

Let me know if you'd like visuals added, or export as PDF/Notion/Markdown!

