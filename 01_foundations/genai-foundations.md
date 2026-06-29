# GenAI Foundations

This subchapter is a compact review of the core generative AI concepts needed before studying system design and production agentic systems.

## Mental Model

A production GenAI system is rarely just a model call. It is usually:

```text
user/task -> context construction -> model/tool call -> validation -> response/action -> trace/eval
```

The model is the reasoning or generation engine, but system quality comes from the full loop: data, prompts, retrieval, tools, state, evals, latency, cost, and guardrails.

## 1. Foundation Models

Foundation models are large pretrained models that can be adapted to many downstream tasks.

Key concepts:

- **Pretraining**: learns general patterns from large-scale data.
- **Post-training**: improves instruction following, tool use, safety, and preference alignment.
- **Inference-time adaptation**: prompting, retrieval, examples, tool calls, routing, and structured output.
- **Weight adaptation**: fine-tuning, adapters, LoRA, preference tuning, distillation, and quantization.

Common model families:

- **LLMs**: text and code generation, extraction, reasoning, planning, tool calling.
- **VLMs and multimodal models**: image, document, screenshot, video, audio, and UI understanding.
- **Embedding models**: semantic representations for retrieval, clustering, reranking, memory, and recommendations.
- **Diffusion and media models**: image, video, audio, 3D, and design generation or editing.

Read more:

- [AI Engineering: Foundation Models](./ai-engineering-summary/Chapter_2_FMs.md)
- [LLM training workflow](./llms/llm_training_workflow.md)

## 2. LLMs

LLMs turn a sequence of tokens into a probability distribution over next tokens. In applications, they are used as flexible language, reasoning, and interface components.

Important dimensions:

| Dimension | Why It Matters |
|-----------|----------------|
| Quality | Task accuracy, reasoning reliability, instruction following, and domain fit. |
| Latency | Interactive UX, tool loops, streaming, and multi-step agent speed. |
| Cost | Token volume, context length, retries, tool loops, and background jobs. |
| Context window | How much task state, retrieved evidence, tool output, and history can fit. |
| Tool support | Native function calling, structured outputs, computer use, code execution, and web/search tools. |
| Modality | Text-only vs image, audio, video, document, and UI understanding. |
| Privacy and deployment | API vs self-hosted, data retention, compliance, and tenant isolation. |
| Licensing | Open-weight usage rights, commercial restrictions, redistribution, and fine-tuning rules. |

Useful design rule: choose the cheapest and fastest model that meets the product's quality, safety, and reliability bar. Use routing when different requests need different model tiers.

Read more:

- [LLM frameworks and model selection](./llms/llms-frameworks.md)
- [Transformer architecture variants](./llms/transformer_architecture_variants.md)

## 3. Transformers and Context

Transformers are the dominant architecture behind modern LLMs and many multimodal models. The key practical idea is that a model call only sees what is inside its current context.

Context can include:

- System and developer instructions.
- User request.
- Conversation history.
- Retrieved documents.
- Tool outputs.
- Examples.
- Memory summaries.
- Output schema.

Context engineering means deciding what to include, omit, compress, order, and validate.

Common failure modes:

- Too much irrelevant context.
- Missing source-of-truth data.
- Stale retrieval results.
- Contradictory instructions.
- Overlong tool outputs.
- Hidden assumptions in conversation history.
- Prompt injection inside retrieved or user-provided content.

## 4. VLMs and Multimodal Models

Vision-language and multimodal models allow systems to reason over screenshots, diagrams, documents, photos, charts, audio, and video.

Use cases:

- Document extraction and layout-aware understanding.
- Chart, table, and dashboard interpretation.
- Computer-use agents that inspect and operate GUIs.
- Design review, visual QA, and creative workflows.
- Multimodal search and retrieval.
- Medical, industrial, robotics, and geospatial analysis with domain controls.

Design considerations:

- Separate perception errors from reasoning errors.
- Preserve source artifacts and coordinates when possible.
- Use OCR/layout extraction when deterministic parsing is more reliable than pure vision reasoning.
- Evaluate on realistic visual clutter, partial information, and low-quality inputs.
- Treat screenshots and documents as potential prompt-injection carriers.

## 5. Diffusion and Generative Media

Diffusion models generate data by learning how to denoise. In practice they power text-to-image, image editing, video generation, audio generation, and design workflows.

Key concepts:

- **Conditioning**: prompts, image references, masks, layout, pose, depth, style, or audio cues guide the output.
- **Sampling**: generation quality and latency depend on sampling strategy and number of steps.
- **Editing**: inpainting, outpainting, style transfer, image-to-image, and region-specific modification.
- **Personalization**: LoRA, textual inversion, reference images, and style adapters.
- **Safety and provenance**: content filters, watermarking/provenance, copyright policy, and human review.

Production constraints:

- GPU cost and queue latency.
- Asset storage and lifecycle management.
- Abuse prevention and moderation.
- Brand consistency.
- Repeatability and seed control.
- Evaluation of subjective quality.

## 6. Embeddings and Retrieval

Embeddings map content into vectors so similar items are near each other. They are the foundation of semantic search, RAG, clustering, recommendations, and memory retrieval.

Retrieval stack:

```text
documents -> chunking -> embeddings/indexing -> retrieval -> reranking -> context packing -> generation
```

Common retrieval patterns:

- **Keyword search**: fast, exact, strong for IDs, names, rare terms, and legal/technical references.
- **Vector search**: semantic similarity over chunks, documents, images, audio, code, or records.
- **Hybrid search**: combines keyword and vector retrieval.
- **Reranking**: reorders candidates with a stronger model.
- **Graph retrieval**: follows relationships between entities, documents, users, or actions.
- **Agentic retrieval**: lets an agent reformulate queries, select tools, inspect results, and retrieve iteratively.

Read more:

- [RAG](./ai-engineering-summary/Chapter_6_1_RAG.md)
- [Building a Generative AI Platform](./gen-AI/huyen-Gen-AI-Platform.md)

## 7. Prompting and Structured Outputs

Prompting is the most accessible way to steer model behavior.

Prompt elements:

- Task and success criteria.
- Relevant context.
- Constraints and policies.
- Examples.
- Output format.
- Tool-use instructions.
- Refusal or escalation rules.

Structured outputs make GenAI systems easier to integrate and test. Prefer schemas for extraction, classification, tool calls, plans, and API-facing outputs.

Read more:

- [Prompt Engineering](./ai-engineering-summary/Chapter_5_Prompt_Eng.md)

## 8. Evaluation

Evaluation gives you a way to change prompts, models, retrieval, tools, and guardrails without guessing.

Evaluation layers:

- **Unit-style checks**: schema validity, deterministic functions, parsers, tool wrappers.
- **Golden datasets**: representative requests with expected outputs or rubrics.
- **Retrieval evals**: recall, precision, freshness, source quality, and reranker quality.
- **Generation evals**: correctness, completeness, groundedness, tone, format, and safety.
- **Agent evals**: task success, tool-call quality, recovery, cost, latency, and trace quality.
- **Online monitoring**: drift, incidents, user feedback, escalation rate, and cost anomalies.

Read more:

- [Evaluation of Generative Systems](./ai-engineering-summary/Chapter_3_Evaluation.md)
- [Evaluating AI Models and Agents](./ai-engineering-summary/Chapter_4_Evaluate_AI.md)

## 9. Fine-Tuning and Adaptation

Fine-tuning is not always the first answer. Start with prompting, retrieval, tools, and evals. Fine-tune when you need consistent behavior that is hard, expensive, or slow to achieve at inference time.

Good reasons to fine-tune:

- Domain-specific style or structure.
- Repeated task behavior.
- Lower latency or lower token usage.
- Better extraction/classification consistency.
- Distillation from a stronger model.
- Specialized coding, reasoning, or tool-call behavior.

Bad reasons to fine-tune:

- Missing external knowledge that should live in retrieval.
- Unclear product requirements.
- No evaluation set.
- Problems caused by bad prompts, poor chunking, or weak tool design.

Read more:

- [Fine-tuning and annotation](./llms/fine_tuning+annotation.md)
- [Finetuning and Model Adaptation](./ai-engineering-summary/Chapter_7_Finetuning.md)

## 10. What Moves to Later Chapters

Keep the boundaries clear:

- System architectures move to [System Design](../03_system_design/README.md).
- Production runtime, deployment, security, observability, and cost controls move to the new Prototype to Production chapter.
- Framework tutorials and runnable code move to the hands-on appendix.
- Curated links move to [Resources](../RESOURCES.md).
