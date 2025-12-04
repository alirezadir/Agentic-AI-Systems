
#  Transformer Architecture Variants

```
              
                       Transformer Family        
              
                          
       
                                            
                                            
Encoder-Only       Decoder-Only       Encoder-Decoder
(e.g., BERT)        (e.g., GPT)         (e.g., T5, BART)
```


##  Encoder-Only Models

- **Examples:** BERT, RoBERTa, DistilBERT  
- **Purpose:** Understanding tasks (classification, QA, embeddings)  
- **Characteristics:**
  - Bidirectional attention (uses context from both left and right)
  - Input is fully visible at once
  - Trained with **Masked Language Modeling (MLM)**


##  Decoder-Only Models

- **Examples:** GPT, GPT-2/3/4, LLaMA  
- **Purpose:** Text generation, completion, chat  
- **Characteristics:**
  - Unidirectional attention (left-to-right only)
  - Only sees past tokens
  - Trained with **Next Token Prediction (CLM)**
  - Great for autoregressive generation


##  Encoder-Decoder (Seq2Seq) Models

- **Examples:** T5, BART, MarianMT, mT5  
- **Purpose:** Translation, summarization, question generation  
- **Characteristics:**
  - Encoder reads and encodes input
  - Decoder generates output based on encoder outputs + past tokens
  - Combines understanding and generation
  - Commonly trained with **Seq2Seq** or **denoising objectives**


##  Quick Comparison Table

| Model Type       | Attention Direction | Main Use                     | Training Objective | Examples            |
|------------------|---------------------|------------------------------|--------------------|---------------------|
| Encoder-Only     | Bidirectional       | Classification, Embedding    | MLM                | BERT, RoBERTa       |
| Decoder-Only     | Unidirectional      | Text Generation, Completion  | CLM                | GPT, LLaMA          |
| Encoder-Decoder  | Bi + Uni-directional| Translation, Summarization   | Seq2Seq / Denoise  | T5, BART, mT5       |


##  Popular Transformer Models (2025)

- **GPT-4o (OpenAI, 2024)**  
  Decoder-only transformer with multimodal capabilities (text, vision, audio); trained autoregressively for next-token prediction. Excels in long-form text generation, coding, reasoning, and computer-using agent tasks.

- **Claude 3.5 Sonnet (Anthropic, 2024)**  
  Decoder-only model optimized for safety, reasoning, and long-context tasks. Strong performance in coding, analysis, and agentic workflows.

- **Gemini 1.5 Pro (Google, 2024)**  
  Multimodal decoder-only model with extremely long context windows (up to 2M tokens). Effective for complex reasoning, code generation, and multimodal tasks.

- **LLaMA 3.1 (Meta, 2024)**  
  Open-source, large-scale decoder-only model optimized for performance, multilingual capabilities, and training efficiency. Strong open-source alternative for agent development.

- **T5 (Text-to-Text Transfer Transformer)**  
  Encoder-decoder model trained on a unified text-to-text format, effective for translation, summarization, and question answering.

- **Mistral Large 2 (Mistral AI, 2024)**  
  Decoder-only model optimized for cost-effectiveness and strong performance. Good balance of capabilities and affordability for agent systems.
