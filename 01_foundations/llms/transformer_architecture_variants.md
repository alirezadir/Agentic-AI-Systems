
# 🔧 Transformer Architecture Variants

```
              ┌───────────────────────────────────┐
              │         Transformer Family        │
              └───────────────────────────────────┘
                          ▲
       ┌──────────────────┼───────────────────┐
       │                  │                   │
       ▼                  ▼                   ▼
Encoder-Only       Decoder-Only       Encoder-Decoder
(e.g., BERT)        (e.g., GPT)         (e.g., T5, BART)
```

---

## 🔹 Encoder-Only Models

- **Examples:** BERT, RoBERTa, DistilBERT  
- **Purpose:** Understanding tasks (classification, QA, embeddings)  
- **Characteristics:**
  - Bidirectional attention (uses context from both left and right)
  - Input is fully visible at once
  - Trained with **Masked Language Modeling (MLM)**

---

## 🔹 Decoder-Only Models

- **Examples:** GPT, GPT-2/3/4, LLaMA  
- **Purpose:** Text generation, completion, chat  
- **Characteristics:**
  - Unidirectional attention (left-to-right only)
  - Only sees past tokens
  - Trained with **Next Token Prediction (CLM)**
  - Great for autoregressive generation

---

## 🔹 Encoder-Decoder (Seq2Seq) Models

- **Examples:** T5, BART, MarianMT, mT5  
- **Purpose:** Translation, summarization, question generation  
- **Characteristics:**
  - Encoder reads and encodes input
  - Decoder generates output based on encoder outputs + past tokens
  - Combines understanding and generation
  - Commonly trained with **Seq2Seq** or **denoising objectives**

---

## ✅ Quick Comparison Table

| Model Type       | Attention Direction | Main Use                     | Training Objective | Examples            |
|------------------|---------------------|------------------------------|--------------------|---------------------|
| Encoder-Only     | Bidirectional       | Classification, Embedding    | MLM                | BERT, RoBERTa       |
| Decoder-Only     | Unidirectional      | Text Generation, Completion  | CLM                | GPT, LLaMA          |
| Encoder-Decoder  | Bi + Uni-directional| Translation, Summarization   | Seq2Seq / Denoise  | T5, BART, mT5       |

---

## 🌟 Popular Transformer Models

- **GPT-3 / GPT-4**  
  Decoder-only transformers trained autoregressively for next-token prediction; excel in long-form text generation, coding, and reasoning.

- **T5 (Text-to-Text Transfer Transformer)**  
  Encoder-decoder model trained on a unified text-to-text format, effective for translation, summarization, and question answering.

- **PaLM, LLaMA**  
  Large-scale, decoder-only models optimized for performance, multilingual capabilities, and training efficiency at scale.
