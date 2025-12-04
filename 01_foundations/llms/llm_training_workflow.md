
#  LLM Training Workflow


##  1. Pretraining Phase

```
Raw Text Corpus
      
Tokenization (e.g., BPE, WordPiece, SentencePiece)
      
Self-Supervised Objective
       Next Token Prediction (Autoregressive)
       Masked Token Prediction (Autoencoding)
      
Model Training
       Huge compute (TPUs/GPUs)
       Billions of parameters
      
Trained Foundation Model
```

###  Key Concepts in Pretraining

- **Objective:** Learn general language understanding from large-scale unstructured data.
- **Data:** Web crawl, books, code, Wikipedia, forums, etc.
- **Labels:** No human annotation  labels are generated from the data itself.
- **Model Types:** Decoder-only (e.g., GPT), Encoder-only (e.g., BERT), or Encoder-Decoder (e.g., T5).
- **Scale:** Trillions of tokens, massive compute, days to weeks of training.

###  Interview Takeaways

-  Pretraining is *not task-specific*  it's about broad language modeling.
-  Most LLM capabilities (reasoning, summarization, etc.) emerge during this stage.
-  Tokenization choice affects model efficiency and generalization.
-  Self-supervision enables learning at massive scale without labeled datasets.


##  2. Supervised Fine-Tuning (SFT)

```
Pretrained LLM
      
Curated Labeled Data
(e.g., input-output pairs, instruction-response)
      
Supervised Learning Objective
(e.g., Cross-Entropy Loss on expected output)
      
Fine-Tuned LLM
(Specialized on following instructions or tasks)
```

###  Key Concepts in Supervised Fine-Tuning

- **Objective:** Teach the pretrained LLM to follow specific instructions, complete tasks, or mimic ideal behavior using high-quality, labeled datasets.
- **Data:** Instruction-response pairs (e.g., "Summarize this article"  summary), sometimes crowd-sourced or written by experts.
- **Process:**
  - Reuse the pretrained model weights
  - Add specific task or instruction-following data
  - Optimize with **supervised learning (cross-entropy loss)**
- **Output:** A model that performs better on **instruction-based tasks** or more aligned generation.

###  Common Datasets for SFT

- **OpenAIs InstructGPT dataset**
- **FLAN collection** (Google)
- **Alpaca / Dolly-style datasets** (open-source)

###  Interview Takeaways

-  SFT helps models learn to **follow instructions**, not just generate fluent text.
-  Quality of fine-tuning data is more important than quantity.
-  This phase can drastically improve performance on downstream tasks with much smaller compute than pretraining.
-  Often used before RLHF to "shape" base behavior.


##  3. Alignment Phase (RLHF  Reinforcement Learning with Human Feedback)

```
Supervised Fine-Tuned LLM
      
Generate Multiple Responses
      
Human Preference Data
(Pairs ranked by human annotators)
      
Reward Model Training
      
Reinforcement Learning (PPO)
      
Aligned LLM
(More helpful, harmless, honest)
```

###  Concept Overview

- **Goal:** Align model outputs with human values and preferences  making it more helpful, harmless, safe, and trustworthy.
- **RLHF:** A multi-step process that fine-tunes LLM behavior based on human preference rankings.
- **Reward Model:** Trained to predict which model output a human would prefer based on ranked samples.
- **PPO (Proximal Policy Optimization):** The most common RL algorithm used to optimize model responses via feedback signals.


###  RLHF Pipeline Breakdown

1. Pretrained/SFT model generates multiple responses to a prompt.  
2. Human annotators rank or score the outputs.  
3. A **reward model** is trained to predict preferences.  
4. The base model is fine-tuned using **PPO** to maximize the reward signal.

```math
\nabla_\theta J(\theta) = \mathbb{E}_\pi[\nabla_\theta \log \pi_\theta(a|s) R(a)]
```

> This equation represents the PPO update rule, where actions leading to preferred outputs are reinforced based on reward estimates.


###  Challenges and Considerations

- **Reward Overfitting / Hacking:** Model learns to exploit flaws in the reward model.  
- **Model Drift:** Fine-tuned model may deviate from intended behavior over time.  
- **Human Feedback Cost:** Gathering high-quality annotations is labor-intensive and expensive.  
- **Scalability:** Preference data is hard to scale across languages, domains, and user types.


###  Tools & Frameworks

- **HuggingFace TRL (PPOTrainer)**  Easy-to-use RLHF training loop.  
- **OpenAIs RLHF stack**  Used in InstructGPT and ChatGPT.  
- **Anthropics Constitutional AI**  An alternative approach using AI-written feedback instead of human labels.
