
# Transformer Architecture Variants

```
              
                       Transformer Family        
              
                          
       
                                            
                                            
Encoder-Only       Decoder-Only       Encoder-Decoder
(e.g., BERT)        (e.g., GPT)         (e.g., T5, BART)
```


## Encoder-Only Models

- **Examples:** BERT-style and embedding-focused models
- **Purpose:** Understanding tasks such as classification, retrieval, reranking, and embeddings
- **Characteristics:**
  - Bidirectional attention (uses context from both left and right)
  - Input is fully visible at once
  - Trained with **Masked Language Modeling (MLM)**


## Decoder-Only Models

- **Examples:** GPT-style and Llama-style models
- **Purpose:** Text generation, chat, coding, reasoning, and tool calling
- **Characteristics:**
  - Unidirectional attention (left-to-right only)
  - Only sees past tokens
  - Trained with **Next Token Prediction (CLM)**
  - Great for autoregressive generation


## Encoder-Decoder (Seq2Seq) Models

- **Examples:** T5-style and BART-style models
- **Purpose:** Translation, summarization, transformation, and constrained generation
- **Characteristics:**
  - Encoder reads and encodes input
  - Decoder generates output based on encoder outputs + past tokens
  - Combines understanding and generation
  - Commonly trained with **Seq2Seq** or **denoising objectives**


## Quick Comparison Table

| Model Type       | Attention Direction | Main Use                     | Training Objective | Examples            |
|------------------|---------------------|------------------------------|--------------------|---------------------|
| Encoder-only     | Bidirectional       | Classification, embeddings, reranking | MLM | BERT-style models |
| Decoder-only     | Unidirectional      | Chat, generation, coding, tool use | CLM | GPT/Llama-style models |
| Encoder-decoder  | Bi + uni-directional | Translation, summarization, transformation | Seq2Seq / denoising | T5/BART-style models |


## Practical Notes

- Most modern chat, coding, and agentic LLMs are decoder-only or decoder-dominant systems.
- Encoder-only models remain important for embeddings, reranking, classification, and retrieval.
- Encoder-decoder models remain useful for transformation-heavy tasks, though many product systems now use general instruction-following decoder models.
- Architecture alone does not determine product quality. Post-training, tool support, context handling, inference stack, evals, and system design often matter more.

## Related Notes

- [LLM Model Selection](./llm-model-selection.md)
- [GenAI Foundations](../genai-foundations.md)
