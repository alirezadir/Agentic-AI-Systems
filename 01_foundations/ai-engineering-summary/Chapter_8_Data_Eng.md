# Chapter 8: Dataset Engineering 


## Overview 

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

# Dataset Engineering

## A Data-Centric View of AI

* **Model-centric AI**: Enhances model architecture, scale, training techniques
* **Data-centric AI**: Enhances data quality, diversity, and relevance
* Shift in benchmarks:

  * 2021: Andrew Ng's data-centric competition
  * 20232024: DataComp, DataPerf, dcbench

## Data Curation

### What Data You Need

* Depends on task type:

  * Self-supervised: sequences
  * Instruction: (instruction, response)
  * Preference: (instruction, winning, losing)
  * Reward modeling: ((instruction, response), score)

### Chain-of-Thought (CoT)

* CoT requires data with step-by-step reasoning

```text
Instruction: Boiling point of Nitrogen?
Response (no CoT): -320.4F
Response (CoT): 23 - 20 + 6 = 9 apples
```

### Tool Use

* Human methods not optimal for AI
* Simulated tool use common (e.g., API over GUI)
* LLaMA 3: multi-message chat format for tool use

### Data Types

* Single-turn: simple, easier to obtain
* Multi-turn: richer context, real-world interactions

### Three Pillars

| Aspect   | Description                                                 |
| -------- | ----------------------------------------------------------- |
| Quality  | Relevant, aligned, consistent, formatted, unique, compliant |
| Coverage | Broad task/topic/format/turn/language diversity             |
| Quantity | Task, model size, method (PEFT vs full finetuning)          |

## Data Quality

* High-quality > High-quantity (Yi, LIMA models)
* Key traits: relevant, aligned, consistent, formatted, unique, compliant

## Data Coverage

| Phase               | General | Math/Reasoning | Code   | Multilingual | Exam  | Long Context |
| ------------------- | ------- | -------------- | ------ | ------------ | ----- | ------------ |
| Pre-training        | 50%     | 25%            | 17%    | 8%           |      |             |
| Supervised Finetune | 52.66%  | 21.19%         | 14.89% | 3.01%        | 8.14% | 0.11%        |
| Preference Finetune | 81.99%  | 5.89%          | 6.93%  | 5.19%        |      |             |

* Annealing code/math boosts reasoning

## Data Quantity

* Millions for SFT < Trillions for pre-training
* Ossification: pretraining can reduce finetuning adaptability
* Small data: PEFT, Large data: full finetuning

### Scaling Curve

* Plot accuracy vs. dataset size to determine ROI

### Pre-finetuning

* Use:

  * Self-supervised  Supervised
  * Less relevant  Relevant
  * Synthetic  Real

## Data Acquisition

* Best data source: your application
* Curation pipeline: filter  annotate  synthesize  validate

## Public Dataset Repositories

* Hugging Face, Kaggle, Google Dataset Search, ICPSR, UCI, OpenML, Data.gov, EleutherAI

## Data Synthesis

### Use Cases

| Goal         | Example                                          |
| ------------ | ------------------------------------------------ |
| Quantity     | Simulate rare events (e.g., crashes, edge cases) |
| Coverage     | Generate toxic/safe/adversarial/rare class data  |
| Quality      | Tool use, math, preference ratings               |
| Privacy      | Replace PII with synthetic records               |
| Distillation | Train a small model from larger model's output   |

### Traditional Techniques

* Rule-based: templates, procedural generation (e.g., Faker)
* Simulation: CARLA, virtual robotics, rare-event emulation

### AI-Powered Techniques

* Self-play (Dota, Go, negotiation)
* Back-translation
* Instruction synthesis from outputs
* Multi-turn synthesis (UltraChat, Alpaca)
* Long-context: chunk  QA  full context finetune

## Instruction Data Synthesis

* Reverse instruction: derive prompt from long content
* AI-human hybrid pipelines for balance
* LLaMA 3:

  * Code problem gen  solution gen  test gen  validate/fix  translate  document
  * 2.7M examples

## Data Verification

* Functionally evaluate (e.g., execute code)
* AI judges: score, classify, detect topics/anomalies

## Synthetic Data Limitations

| Limitation        | Risk                                             |
| ----------------- | ------------------------------------------------ |
| Quality Control   | Garbage in  Garbage out                         |
| Imitation Issues  | Superficial mimicry, hallucination risk          |
| Model Collapse    | Recursive synthesis degrades rare-case coverage  |
| Lineage Obscurity | Legal, license, contamination, benchmark leakage |

## Model Distillation

* Student mimics teacher (e.g., DistilBERT)
* Often paired with LoRA or PEFT
* LLaMA, Alpaca, Nemotron pipelines

## Data Processing

### Key Steps

| Step        | Description                                        |
| ----------- | -------------------------------------------------- |
| **Inspect**     | Plot tokens, lengths, topics; manual spot checks   |
| **Deduplicate** | Hashing, vector similarity, MinHash, Bloom filters |
| **Clean**       | Remove PII, sensitive, low-quality, redundant data |
| **Format**      | Match tokenizer, chat format, example length, etc. |

## Summary

* Data quality, diversity, and relevance are mission-critical
* Synthesis is useful but needs strong validation
* Most dataset steps are not easily automatable
* Creativity is key to dataset curation and validation


##  Code Examples (Expanded)

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



