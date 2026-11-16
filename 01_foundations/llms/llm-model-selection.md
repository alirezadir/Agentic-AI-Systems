# LLM Model Selection

This note keeps model selection inside the foundations chapter. Framework comparisons and build-stack decisions belong in later production and hands-on chapters.

## Selection Criteria

Choosing a model is a system-design trade-off, not a leaderboard-only decision.

| Criterion | Questions to Ask |
|-----------|------------------|
| Quality | Does it meet the task's accuracy, reasoning, instruction-following, and robustness bar? |
| Latency | Is it fast enough for interactive, streaming, batch, or background use? |
| Cost | What is the expected cost per request, session, workflow, or user? |
| Context window | Can it fit the needed instructions, user input, retrieved data, history, and tool outputs? |
| Modality | Does the task require text, code, image, audio, video, documents, or UI understanding? |
| Tool use | Does it support structured outputs, function calling, code execution, web/search, or computer use? |
| Reliability | How often does it follow schemas, call valid tools, and recover from errors? |
| Privacy | What data is sent to the provider, stored, logged, or used for improvement? |
| Deployment | Is the model API-based, self-hosted, private cloud, edge, or hybrid? |
| Licensing | Are model weights, outputs, fine-tuning, and commercial use allowed for the product? |
| Operations | Can the team monitor, evaluate, version, rate-limit, and fall back safely? |

## Use-Case Fit

### General Chat and Reasoning

Prioritize:

- Instruction following.
- Reasoning quality.
- Long-context reliability.
- Low hallucination rate.
- Tool-call quality if the assistant acts.

### Coding

Prioritize:

- Repository-scale context handling.
- Patch quality.
- Test-running and debugging behavior.
- Tool and shell safety.
- Deterministic formatting and schema adherence.

### RAG and Knowledge Assistants

Prioritize:

- Grounded answer quality.
- Citation/source handling.
- Long-context synthesis.
- Resistance to prompt injection in retrieved text.
- Cost for repeated retrieval and generation loops.

### Structured Extraction

Prioritize:

- JSON/schema reliability.
- Low temperature consistency.
- Good handling of noisy documents.
- Field-level evaluation.
- Ability to abstain or mark uncertainty.

### Agentic Workflows

Prioritize:

- Tool selection accuracy.
- Valid argument generation.
- Multi-step recovery.
- Cost and latency across loops.
- Human approval support.
- Traceability.

### Multimodal Tasks

Prioritize:

- Vision/document/audio quality for the target input.
- Layout and coordinate grounding.
- OCR and chart/table robustness.
- Safety around screenshots and documents.
- Ability to cite page, region, frame, or timestamp.

## Model Routing

Most production systems should not use one model for everything.

Common routing patterns:

- **Task router**: classify request type, then select model/workflow.
- **Cost router**: start with a cheaper model; escalate when confidence is low.
- **Capability router**: send multimodal, coding, long-context, or tool-heavy tasks to specialized models.
- **Latency router**: choose fast models for interactive turns and stronger models for background work.
- **Fallback router**: retry with another provider/model after failures or rate limits.

Routing needs evals. Without evals, routing can silently reduce quality.

## Cost and Latency Drivers

Costs usually come from more than the final answer.

Drivers:

- Input tokens.
- Output tokens.
- Retrieved context size.
- Tool loop iterations.
- Retries and fallbacks.
- Long conversation history.
- Multimodal inputs.
- Background jobs.
- Fine-tuned or premium models.

Controls:

- Summarize or compress state.
- Retrieve less but better context.
- Use rerankers.
- Cache stable prompt/context segments.
- Route simple tasks to smaller models.
- Stream interactive responses.
- Batch offline work.
- Add stop conditions to agents.

## Embedding Model Selection

Embedding models should be selected by retrieval quality on your data, not generic scores alone.

Consider:

- Domain vocabulary.
- Multilingual support.
- Code/document/image/audio support.
- Vector dimension and storage cost.
- Query/document asymmetry.
- Reranker compatibility.
- Latency and batch throughput.
- Privacy and deployment constraints.

Evaluate:

- Recall at k.
- Precision at k.
- Mean reciprocal rank.
- Source freshness.
- Downstream answer quality.
- Failure cases by document type.

## Fine-Tuning Decision

Use fine-tuning when prompting and retrieval are not enough.

Good fit:

- Repeated structured behavior.
- Domain style or taxonomy.
- Lower latency through shorter prompts.
- Lower cost through smaller specialized models.
- Tool-call or extraction consistency.
- Distillation from a stronger model.

Poor fit:

- Missing external knowledge.
- Weak eval set.
- Unclear product behavior.
- Retrieval, chunking, or prompt issues.
- Rapidly changing facts.

## Practical Model Selection Process

1. Define task classes and success metrics.
2. Build a small representative eval set.
3. Test a baseline model with simple prompts.
4. Add retrieval/tools only when needed.
5. Compare quality, latency, and cost on real examples.
6. Add routing if task classes have different requirements.
7. Add fallbacks and monitoring before production.
8. Re-run evals whenever prompts, context, tools, models, or providers change.

## What Moves Elsewhere

- Agent framework comparisons move to the production/build-stack chapter.
- Runnable framework tutorials move to the hands-on appendix.
- Current model leaderboards and market rankings belong in [Resources](../../RESOURCES.md), not this foundation note.
