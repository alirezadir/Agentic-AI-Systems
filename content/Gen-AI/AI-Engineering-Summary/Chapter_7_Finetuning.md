# Chapter 7: Fine-tuning 

#### Keywords 

* **Transfer learning** reuses pre-trained model knowledge for new tasks/domains
  - Improves sample efficiency
  - Types of transfer learning:
    - **Fine-tuning**: full or partial update of model weights
    - **Feature-based transfer**: freeze base model, use it as feature extractor
    - **Linear probing**: train only a linear classifier on frozen embeddings
    - **Prompt tuning**: learn soft prompts; model remains frozen
    - **Adapter tuning**: train lightweight modules (e.g., LoRA); base model frozen
    - **Model distillation / merging**: compress or combine models
    - **Multi-task learning**: shared model backbone across multiple tasks

* **Model adaptation**: subset of transfer learning, adapt a model to new domains/languages/tasks; often with limited data
* **Finet-uning**: update model weights to improve task-specific performance
* **PEFT** (Parameter-Efficient Finetuning) updating only subsets of model weights

## 1. Stages of Training for LLMs

*Training pipeline for modern LLMs typically follows these stages:*


- **1. Pre-training**  
  - Self-supervised learning (e.g., next-token prediction)  
  - Data: Massive unlabeled text corpus  
  - Goal: Build general world and language understanding

- **2. Continued Pre-training**  
  - Further self-supervised learning on domain/language-specific corpora  
  - Data: Raw domain-specific text (e.g., legal, medical, multilingual)  
  - Goal: Improve domain familiarity and specialization

- **3. Supervised Finetuning (SFT)**  
  - Train on (input, output) pairs for task alignment  
  - Data: Labeled instruction-response data  
  - Goal: Adapt to instruction-following tasks and formats

- **4. Preference Finetuning (RLHF, DPO)**  
  - Learn from human preferences using ranked responses  
  - Data: Ranked outputs (e.g., winner vs. loser completions)  
  - Goal: Optimize model behavior for safety, helpfulness, alignment

- **5. PEFT (Parameter-Efficient Finetuning)**  
  - Update only small, targeted parts of the model (e.g., adapters in LoRA)  
  - Data: Any of the above  
  - Goal: Efficient specialization with minimal memory/compute overhead

- **6. Model Merging / Distillation**  
  - Combine or compress models (e.g., distill large into small)  
  - Data: Outputs or weights of finetuned models  
  - Goal: Support multi-tasking or low-resource deployment






## 2. Finetuning Overview
* **Goal**: Adapt a base model to a specific task
* **Forms**: Full, partial, PEFT (e.g., LoRA), supervised, preference, long-context
* **Supervised finetuning**: (input, output) pairs to align with task-specific objectives
* **Preference finetuning**: Learn to generate preferred responses using comparative data

## 3. When to Finetune

### Reasons to Finetune

* Improve instruction-following & structured output (e.g., JSON, YAML)
* Domain adaptation: SQL dialects, customer-specific queries
* Bias mitigation: finetune on curated data to reduce learned biases
* Distillation: train small models to mimic large ones
* Finetuned small models can outperform larger base models (e.g., Grammarly’s Flan-T5 > GPT-3 on editing tasks)

### Reasons Not to Finetune

* High cost: (annotated) data, compute, ML knowledge (training, serving) needed
  * Evaluation pipeline and iterative experimentation required
* Can degrade performance on other tasks (catastrophic forgetting)-> consider separate models 
* Not experimented with prompting (+Tools) 
* May not outperform strong prompt+RAG setups


### Finetuning vs RAG
- **Fine-Tuning or Retrieve?** after prompt engineering? if Failures are 
  - **Information-based** (facts)-> **RAG** (term based then embeddings),
  - **Behavior-based** (forms)-> **Fine-tune**
  - **Both**: **RAG first,** then Fine-tune  

| Scenario                 | Best Choice    | Explanation                                                         |
| ------------------------ | -------------- | ------------------------------------------------------------------- |
| Missing / outdated information | **RAG**        | Connect model to external sources (BM25, embedding-based retrieval) |
| Behavior-based (Output format issues)     | **Finetuning** | Reinforce syntax/styles with labeled data                           |
| Hallucinations           | **RAG first**  | RAG reduces hallucination via grounding                             |
| Both info & behavior | **RAG then Fine** | RAG addresses info gaps, finetuning aligns outputs                  |

## 4. Memory Bottlenecks
* **Memory** is a bottleneck for working with FMs (both inference & finetuning)
  - Fine-tuning memory: f (N of parameters + numerical representations)
* **Inference Memory**:
  `Total = N × M × 1.2` where N = parameters, M = bytes/param (e.g., 2 bytes for FP16)
    - 20% for activation and key-value vectors
    - Example: 13B params × 2B × 1.2 = **\~31.2 GB**

* **Training Memory**:

  - Additional memory for:
    * **Gradients**: 1 per trainable param
    * **Optimizer state**: up to 2 per param (e.g., Adam)
    * **Activations** (can exceed weights)
    * Estimate: `Training Mem ≈ N x M x 3 ` (for Adam)

* **Gradient checkpointing**: Recomputes activations to save memory

* **Numerical formats**:

  * **Floating Point**: FP32 (4B, High precision), FP16 (2B, Lower precision; inference / mixed precision), 
  * **Brain Float**: BF16, (2B, Training on TPUs/GPUs)
  * **Normal Float**: NF4 (Weight quantization)
  * **Integer**: INT8, INT4 (Inference quantization)
  * **Mixed precision** (AMP): common for training
  * Note: Training is more sensitive to numerical precision; some Ops in 32, some 16, 8 bits; for inference, use 16, 8, 4 bits

* **Quantization**: reduce bits per param (precision)
    - mostly on weights 
    - post-training (PTQ), or inference quantization (<=16)
  

## 5. FineTuning Techniques
- finetuning large-scale models is memory-intensive
- Reducing model’s memory footprint: finetuning more accessible
- partial fine-tuning (e.g. only last layer) is parameter inefficient -> PEFT: inserting additional parameters into the model in the right places (parameter efficient)
### 5.1 PEFT Techniques
#### Adapter-Based Methods
- Add trainable parameters to the model’s architecture,
- Examples: 
  - **LoRA** Low-rank adapters (W → W + α/r AB); **BitFit** Only  bias terms, **IA3**: Inject  per layer (multi-task efficient), **LongLoRA** long-context adaptation                                

#### Soft Prompt-Based Methods
- modify how the model processes the input 
- **Soft prompt**: insert special trainable tokens (soft tokens)
- e.g. Prompt Tuning, P-Tuning, Prefix-Tuning

#### LoRA
- LoRA is the most popular & dominant PEFT technique 
  - No extra inference latency; 
* **Low-rank update**:

  ```math
  W' = W + \frac{α}{r} * W_{AB}
  ```
  * `W_{AB} = A(n x r). B(r x m)` is a low rank decomposition (factorization)
  * Only A and B are trainable (reduced memory); W kept intact
  * Typically applied to Wq, Wv, Wk, Wo matrices
  * why it works? pre-training implicitly minimizes the model’s intrinsic dimension.
* **LoRA configs**:
    - rank parameter r  
      -  r = 2, 4, 8, ...
      - e.g. GPT-3(750B ~ 350GB w/ 16FP) -> with r = 2 -> 18M (0.01%)
      - 4 < r < 64, usually sufficient for many use cases
    - LoRA Serving: 
      * Merge LoRA weights (A,B) into weights before serving 
      * Modular serving: merge during inference; load different adapters on same base model (multi-LoRA); adds latency
      



<!-- | LoRA Rank (r) | α/r Ratio | Memory  | Performance Notes              |
| ------------- | --------- | ------- | ------------------------------ |
| 2             | \~1       | 6–37 MB | Good results on Wq, Wv, Wk, Wo |
| 64+           | varies    | higher  | May lead to overfitting        | -->

#### Quantized LoRA (QLoRA)

* 4-bit NF4 quantization + LoRA
* Uses **paged optimizers** for CPU-GPU memory swap
* Finetunes 65B models on single 48GB GPU
* Trade-off: More memory-efficient, slower training due to dequantization
* **Guanaco** models: competitive with GPT-3.5 tier

### 5.2 Model Merging
- ensemble methods: combine outputs of different models
- model merging: goal: create a single model from multiple models
- with or without fine-tuning 
- model 1 on task 1, model 2 on task 2 -> merged model better at both
- use case: multi-task finetuning (paralel fine-tuning -> merge)
  - one way to do federated learning
- Model merging approaches:how model parameters are combined: 
  - summing, layer stacking, and concatenation.

| Approach             | Summary                                                       |
| -------------------- | ------------------------------------------------------------- |
| **Summing (linear)** | Weighted average of task vectors or layers                    |
| **SLERP**            | Spherical interpolation (geodesic path between model vectors) |
| **Layer Stacking**   | Take layers from different models (frankenmerging, MoE)       |
| **Concatenation**    | Merge LoRA adapters; total rank = r1 + r2                     |

* **Task Vectors**: Δ = Finetuned - Base
* **Pruning**: Reset redundant parameters to base (improves merge quality)

## 6. Finetuning Tactics

### Model Choice Strategy

* **Progression path**: start small (cheapest and fastest), test, scale up
* **Distillation path**: strong → small model via synthetic data

### Frameworks

* Hugging Face `peft`, `LLaMA-Factory`; more in Llama Police
* Use inference APIs for quick tests; frameworks for control & tuning

### Hyperparameters

| Hyperparameter         | Typical Range | Notes                                      |
| ---------------------- | ------------- | ------------------------------------------ |
| **Learning rate**      | 1e-7 – 1e-3   | Stable loss = good; adjust with scheduler  |
| **Batch size**         | ≥ 8           | Gradient accumulation if memory-bound      |
| **Epochs**             | 1 (millions)–10 (thousands)        | Small data = more epochs; monitor val loss |
| **Prompt loss weight** | 0.1 (default) | Tune contribution from prompt vs. response |
