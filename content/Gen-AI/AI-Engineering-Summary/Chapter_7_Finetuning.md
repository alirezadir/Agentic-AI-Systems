# Chapter 7: Fine-tuning 

---

## 📘 Structure Overview

1. Why Finetune? When Not To
2. Finetuning Strategies and Architectures
   - Full Finetuning
   - Partial Finetuning
   - Parameter-Efficient Finetuning (PEFT)
   - LoRA and QLoRA
   - Adapter Architectures
3. Finetuning Development Pipelines
   - Dataset Preparation
   - Tokenization and Format
   - Model Scaling and Progression
   - Distillation Paths
4. Training Practices and Optimization
   - Batch Size
   - Epochs
   - Prompt Loss Weights
   - Scheduler & Optimizer Selection
5. Domain Adaptation and Continued Pretraining
6. Advanced Finetuning Topics
   - Model Merging
   - Layer Stacking
   - Mixture-of-Experts Merging
7. Finetuning vs RAG: Use Case Matrix
8. Evaluation, Metrics & Testing
9. Safety, Alignment, and Reinforcement Tuning
10. Code Snippets & Practical Implementation

---

## 🔍 1. Why Finetune? When Not To

- Finetuning gives **precise control** over model behavior.
- Necessary when:
  - Output style/format is crucial
  - Prompts alone don't deliver accuracy
  - Low-latency, high-volume deployments are needed

**Avoid Finetuning When:**
- Data is small or noisy
- You want live updates to data (→ use RAG instead)
- No GPU access for training

---

## 📚 2. Finetuning Strategies & Architectures

### 2.1 Full Finetuning
- Updates **all weights** of a model.
- Pros: Maximum capability.
- Cons: Requires thousands of GPUs for large models (e.g., LLaMA 65B).

### 2.2 Partial Finetuning
- Freeze majority of layers; only finetune top few (e.g., last transformer blocks).
- Pros: Lower memory cost.
- Cons: Limited task transfer.

### 2.3 PEFT: Parameter-Efficient Finetuning

#### Common Methods
- **LoRA**: Insert trainable low-rank matrices in attention layers.
- **Adapters**: Add trainable layers between existing layers.
- **Prefix/Prompt Tuning**: Train only a prefix of input tokens.
- **BitFit**: Finetune only bias terms.

**LoRA Formula:**
\[
W' = W + \frac{\alpha}{r}AB
\]
Where A ∈ ℝ^{d×r}, B ∈ ℝ^{r×k}, r ≪ d, k

### 2.4 Quantization-Aware Finetuning
- e.g., **QLoRA**: Run training on 4-bit weights, then apply LoRA.
- Reduces GPU memory needs 2–4x.
- Use **BitsAndBytesConfig** with Hugging Face.

### 2.5 Adapter Architectures
- e.g., **Houlsby**, **Compacter**, **IA3**
- Plug-in modules that tune behavior without touching base weights.
- Allow multiple task adapters in same model (multi-task efficiency).

---

## ⚙️ 3. Development Pipeline

### 3.1 Dataset Preparation
- Format: instruction → input → output
- Prefer structured, aligned text with clear formatting

```json
{
  "instruction": "Translate English to French",
  "input": "The cat is sleeping",
  "output": "Le chat dort"
}
```

### 3.2 Tokenization and EOS Handling
- Use the tokenizer of the pretrained base model.
- Add special tokens (e.g., BOS, EOS) if model expects them.

### 3.3 Model Scaling Progression
- Start with small models (e.g., 125M, 770M) for debugging
- Move to 7B–13B for production finetuning
- Consider quantized preloading + LoRA for larger models

### 3.4 Distillation Paths
- Use large LLM to generate training pairs
- Finetune smaller, faster model

**Teacher Model** → Output → Becomes Data → Finetune Student Model

---

## 📈 4. Training Practices

### 4.1 Batch Size
- Adjust based on memory availability
- Use **gradient accumulation** if needed

### 4.2 Epochs & Early Stopping
- Common defaults:
  - 3–5 epochs (large datasets)
  - 10+ epochs (small curated datasets)
- Stop when val loss plateaus or increases

### 4.3 Prompt Loss Weight
- Custom dataloader can apply weighted loss:
  - Prompt = 0.1, Response = 0.9
- Helps model focus on response rather than copying prompt

### 4.4 Optimizer Selection
- AdamW is most common
- Schedule: Cosine + Warmup (e.g., 5% of total steps)

---

## 🌐 5. Continued Pretraining (Domain Adaptation)

- Continue training on domain data with unsupervised loss (e.g., next-token prediction).
- Improves vocabulary fit and tokenization performance.
- Use when:
  - You have 10k+ documents in a niche area
  - You need better recall of domain-specific concepts

---

## 🧠 6. Advanced Topics: Merging and Layer Stacking

### 6.1 Model Merging
- Blend finetuned models using weighted averaging
- E.g., base + safety model → safe assistant

**Simple Merge Example:**
```python
merged_weights = (0.7 * base_weights + 0.3 * tuned_weights)
```

### 6.2 Frankenmodels / Layer Stacking
- Compose layers from multiple models
- E.g., first 10 layers from Model A, last 12 from Model B

Used in:
- Solar-10.7B
- DARE/TaskVector merge strategies

---

## 🧩 7. Finetuning vs. RAG Matrix

| Situation                  | Finetuning | RAG |
|---------------------------|------------|-----|
| Static behavior tuning    | ✅         | ❌  |
| Dynamic knowledge         | ❌         | ✅  |
| Safety filters / detox    | ✅         | ❌  |
| Web search integration    | ❌         | ✅  |
| Few-shot fails            | ✅         | ❌  |

**Strategy**: Use finetuning for personality, format, response rules. Use RAG for real-time facts.

---

## 📏 8. Evaluation Metrics

- **Loss (token-level)**: Tracks learning
- **BLEU / ROUGE**: For text generation
- **EM / Accuracy**: For classification tasks
- **Bias/Detox Benchmarks**: e.g., RealToxicityPrompts

Test across slices:
- Short vs long prompts
- Popular vs rare tokens
- Specific topics/domains

---

## 🛡️ 9. Safety and Reinforcement Alignment

- Detox models: Trained with finetuning + reward signal
- OpenAI uses RLHF (Reinforcement Learning from Human Feedback)
- Tools: TRL (Hugging Face), PPOTrainer

**Basic RLHF Pipeline:**
1. SFT (Supervised Fine-tuning)
2. Reward model from ranking data
3. Policy optimization (e.g., PPO)

---

## 💻 10. Code Snippets & Demos

### A. LoRA Setup with PEFT
```python
from peft import get_peft_model, LoraConfig
from transformers import AutoModelForCausalLM

config = LoraConfig(task_type="CAUSAL_LM", r=4, lora_alpha=32, lora_dropout=0.05)
model = AutoModelForCausalLM.from_pretrained("tiiuae/falcon-7b")
model = get_peft_model(model, config)
model.print_trainable_parameters()
```

### B. QLoRA Example
```python
from transformers import BitsAndBytesConfig
bnb_config = BitsAndBytesConfig(load_in_4bit=True)
model = AutoModelForCausalLM.from_pretrained("llama-7b", quantization_config=bnb_config)
```

### C. Training with HF Trainer
```python
from transformers import Trainer, TrainingArguments
args = TrainingArguments(
  output_dir="./outputs",
  per_device_train_batch_size=8,
  gradient_accumulation_steps=4,
  num_train_epochs=3,
  learning_rate=2e-5,
  save_steps=1000,
  logging_dir="./logs"
)
trainer = Trainer(model=model, args=args, train_dataset=train_data)
trainer.train()
```


### D. Data Preprocessing (SFT-style JSON to Tokenized Format)
```python
from datasets import load_dataset
from transformers import AutoTokenizer

dataset = load_dataset("json", data_files="data.json")
tokenizer = AutoTokenizer.from_pretrained("llama-7b")

def tokenize(example):
    return tokenizer(
        f"### Instruction:\n{example['instruction']}\n\n### Input:\n{example['input']}\n\n### Response:\n{example['output']}",
        truncation=True, padding="max_length"
    )
tokenized_dataset = dataset.map(tokenize)
```

### E. Evaluation Script (BLEU Score)
```python
from datasets import load_metric
metric = load_metric("bleu")

predictions = ["The cat is on the mat"]
references = [["The cat sits on the mat"]]
print("BLEU:", metric.compute(predictions=predictions, references=references))
```

### F. Custom LoRA Module in PyTorch
```python
import torch.nn as nn
class LoRALinear(nn.Module):
    def __init__(self, in_features, out_features, r=8):
        super().__init__()
        self.linear = nn.Linear(in_features, out_features)
        self.A = nn.Parameter(torch.randn(in_features, r))
        self.B = nn.Parameter(torch.randn(r, out_features))
        self.alpha = 16

    def forward(self, x):
        return self.linear(x) + (self.alpha / self.A.shape[1]) * (x @ self.A @ self.B)
```

Let me know if you'd like even more advanced scripts (e.g., RLHF loop, SFT dataset generation, multi-GPU setup) or want to continue to Chapter 8!


