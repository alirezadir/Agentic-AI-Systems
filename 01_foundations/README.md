# Chapter 1: Foundations of GenAI and Agentic AI

This chapter is the conceptual base for the rest of the repo. Treat it like the first chapter of a short technical book: compact, practical, and self-contained enough that a reader can review the core ideas before moving into system design and production.

The chapter has two major parts:

1. **Generative AI foundations**: foundation models, LLMs, VLMs, diffusion models, embeddings, prompting, RAG, fine-tuning, evaluation, and AI engineering basics.
2. **Agentic AI foundations**: agents, tools, memory, planning, control flow, human-in-the-loop, multi-agent systems, protocols, and agentic application patterns.

## Learning Path

Read this chapter in order if you are building intuition from scratch. Skip around if you are using it as an interview or design reference.

| Order | Topic | What to Know | Current Notes |
|-------|-------|--------------|---------------|
| 1 | Foundation models | Pretraining, adaptation, model families, scaling, capabilities, and limits. | [AI Engineering: Foundation Models](./ai-engineering-summary/Chapter_2_FMs.md) |
| 2 | LLM architecture | Transformer variants, context windows, tokenization, reasoning behavior, and model selection. | [LLM architecture variants](./llms/transformer_architecture_variants.md), [LLM model selection](./llms/llm-model-selection.md) |
| 3 | Multimodal models | VLMs, image/video/audio inputs, multimodal embeddings, computer-use models, and UI grounding. | [Multimodal and VLM Foundations](./multimodal-vlm-foundations.md) |
| 4 | Diffusion and generative media | Denoising diffusion, text-to-image/video systems, conditioning, controllability, and evaluation. | [Diffusion and Generative Media Foundations](./diffusion-foundations.md) |
| 5 | Prompting and context | Instructions, examples, structured outputs, context construction, prompt caching, and failure modes. | [Prompt Engineering](./ai-engineering-summary/Chapter_5_Prompt_Eng.md) |
| 6 | Retrieval and knowledge | Embeddings, chunking, hybrid retrieval, reranking, RAG, agentic RAG, and freshness. | [RAG](./ai-engineering-summary/Chapter_6_1_RAG.md), [GenAI platform](./gen-AI/huyen-Gen-AI-Platform.md) |
| 7 | Evaluation | Model evals, application evals, agent evals, human review, AI-as-judge, and regression suites. | [Evaluation of Generative Systems](./ai-engineering-summary/Chapter_3_Evaluation.md), [Evaluating AI Models and Agents](./ai-engineering-summary/Chapter_4_Evaluate_AI.md) |
| 8 | Adaptation | Fine-tuning, instruction tuning, preference tuning, synthetic data, annotation, and when not to fine-tune. | [Fine-tuning and annotation](./llms/fine_tuning+annotation.md), [Finetuning and Model Adaptation](./ai-engineering-summary/Chapter_7_Finetuning.md) |
| 9 | Agents | Agent definitions, workflows vs agents, tools, actions, planning, memory, reflection, and autonomy. | [Agents and Agentic AI](./agents/README.md), [Agents in AI Engineering](./ai-engineering-summary/Chapter_6_2_Agents.md) |
| 10 | AI engineering | Data, inference, latency, cost, system boundaries, and full-stack engineering concerns. | [Data Engineering](./ai-engineering-summary/Chapter_8_Data_Eng.md), [Full-Stack AI Engineering](./ai-engineering-summary/Chapter_10_AI_Engineering.md) |
| 11 | Developer foundations | Modern Python, repo hygiene, dependency management, scripts, notebooks, and AI-assisted coding practice. | [Modern Python](./python/modern_python.md) |

## Part A: Generative AI Foundations

Start with the compact subchapter: [GenAI Foundations](./genai-foundations.md).

Use these focused notes for missing model families:

- [Multimodal and VLM Foundations](./multimodal-vlm-foundations.md)
- [Diffusion and Generative Media Foundations](./diffusion-foundations.md)

### 1. Foundation Models

Foundation models are large pretrained models adapted to many tasks through prompting, retrieval, fine-tuning, tool use, or product-specific orchestration.

Core ideas:

- **Pretraining** learns broad statistical structure from large-scale data.
- **Post-training** aligns the model toward instruction following, tool use, safety, and preferences.
- **Adaptation** can happen through prompts, retrieval, fine-tuning, adapters, or distillation.
- **Capability is system-dependent**: model quality matters, but the surrounding context, tools, evals, and runtime controls often decide product quality.

Read:

- [AI Engineering: Foundation Models](./ai-engineering-summary/Chapter_2_FMs.md)
- [LLM training workflow](./llms/llm_training_workflow.md)

### 2. LLMs

LLMs are the default reasoning and language layer in most GenAI systems. They are used for generation, extraction, classification, planning, coding, tool calling, and conversational interfaces.

Core ideas:

- **Model selection is a product trade-off**, not a leaderboard exercise: quality, latency, cost, context length, tool support, privacy, licensing, and reliability all matter.
- **Context is the runtime memory** of the model call: system prompt, user input, retrieved data, tool results, prior state, and examples.
- **Structured outputs make systems testable**: JSON schemas, function calls, and constrained decoding reduce integration risk.
- **Small models still matter** for routing, classification, extraction, eval assistance, and cost-sensitive background work.

Read:

- [LLM model selection](./llms/llm-model-selection.md)
- [Transformer architecture variants](./llms/transformer_architecture_variants.md)

### 3. VLMs and Multimodal Models

Vision-language and multimodal models extend the interface from text-only inputs to images, screenshots, video, audio, documents, and UI state. They are central to computer-use agents, document agents, robotics interfaces, medical/media workflows, and design/code assistants.

Core ideas:

- **VLMs connect perception to reasoning**: OCR, layout understanding, object recognition, chart understanding, and UI grounding.
- **Multimodal retrieval** uses embeddings over text, images, audio, or document layout.
- **Computer-use agents depend on visual grounding** plus action APIs such as browser control, desktop control, or mobile automation.
- **Evaluation is harder** because errors can come from perception, reasoning, tool choice, or action execution.

Read:

- [Multimodal and VLM Foundations](./multimodal-vlm-foundations.md)

### 4. Diffusion and Generative Media

Diffusion models and related generative media systems are the foundation for modern image, video, audio, and design-generation workflows.

Core ideas:

- **Diffusion models learn denoising**: generation starts from noise and iteratively moves toward a sample conditioned on text, image, layout, style, or other signals.
- **Control mechanisms** include text prompts, image references, masks, depth/pose/layout conditions, LoRAs, adapters, and editing constraints.
- **Production constraints** include latency, GPU cost, content safety, provenance, copyright risk, and human review.
- **Evaluation mixes objective and subjective signals**: prompt adherence, visual quality, identity consistency, brand fit, safety, and downstream task success.

Read:

- [Diffusion and Generative Media Foundations](./diffusion-foundations.md)

### 5. Prompting, Context, and RAG

Prompting is the simplest control surface, but production systems usually need context construction and retrieval.

Core ideas:

- **Prompting**: instructions, examples, output contracts, role/task framing, and decomposition.
- **Context engineering**: choose what information enters the model call, in what order, at what granularity, and with what constraints.
- **RAG**: retrieve external information, ground generation, and reduce stale or hallucinated answers.
- **Agentic RAG**: let the system decide when to retrieve, how to reformulate queries, which sources to inspect, and whether more evidence is needed.

Read:

- [Prompt Engineering](./ai-engineering-summary/Chapter_5_Prompt_Eng.md)
- [RAG](./ai-engineering-summary/Chapter_6_1_RAG.md)
- [Building a Generative AI Platform](./gen-AI/huyen-Gen-AI-Platform.md)

### 6. Evaluation and Adaptation

Evaluation is not a final QA step. It is the feedback loop for prompt changes, model changes, retrieval changes, tool changes, and product releases.

Core ideas:

- **Model evals** measure isolated model behavior.
- **Application evals** measure end-to-end task success.
- **Agent evals** inspect plans, tool calls, traces, memory writes, retries, and final outcomes.
- **Fine-tuning** is useful when behavior needs to become cheaper, faster, more consistent, or domain-specific than prompting alone can achieve.

Read:

- [Evaluation of Generative Systems](./ai-engineering-summary/Chapter_3_Evaluation.md)
- [Evaluating AI Models and Agents](./ai-engineering-summary/Chapter_4_Evaluate_AI.md)
- [Fine-tuning and annotation](./llms/fine_tuning+annotation.md)
- [Finetuning and Model Adaptation](./ai-engineering-summary/Chapter_7_Finetuning.md)

## Part B: Agentic AI Foundations

Start with the compact subchapter: [Agentic AI Foundations](./agentic-ai-foundations.md).

### 1. What Is an Agent?

An AI agent is a model-centered system that can use context, tools, memory, and control flow to pursue a goal. The important distinction is not branding; it is whether the system can decide actions based on intermediate feedback.

Core ideas:

- **Workflow**: predefined path; the system follows known steps.
- **Agent**: dynamic path; the system chooses next actions based on state, observations, and tool results.
- **Agentic system**: a broader product architecture that may include one or more agents, deterministic services, retrieval, queues, approvals, evals, observability, and policy controls.

Read:

- [Agents and Agentic AI](./agents/README.md)
- [Agents in AI Engineering](./ai-engineering-summary/Chapter_6_2_Agents.md)

### 2. Agent Building Blocks

Most agentic systems are composed from a small set of primitives.

| Primitive | Role |
|-----------|------|
| Model | Reasons, plans, extracts, writes, decides, or calls tools. |
| Tools | Let the system read or act through APIs, files, databases, browsers, code, or services. |
| Memory | Preserves task state, user preferences, facts, summaries, or learned experience. |
| Planner | Breaks goals into steps, chooses strategy, and updates based on observations. |
| Controller | Runs the loop, enforces limits, handles retries, and decides when to stop. |
| Guardrails | Constrain inputs, outputs, tool calls, permissions, and policy-sensitive actions. |
| Human checkpoints | Add approval, correction, escalation, or judgment when automation is risky. |
| Evals and traces | Make behavior observable, testable, and debuggable. |

### 3. Tool Use and Control Flow

Tool use is where agentic systems become useful and risky. A read-only retrieval tool has a different risk profile from a tool that sends emails, writes code, changes infrastructure, or moves money.

Design questions:

- What tools are available?
- What permissions does each tool have?
- Which tools require approval?
- How are tool inputs validated?
- What state is logged?
- What happens on failure, timeout, or partial completion?
- Can the user cancel, rewind, or inspect the task?

### 4. Memory and State

Agent memory is not a single component. It includes conversation history, task state, user profile, retrieved knowledge, tool results, execution traces, and long-term learned facts.

Useful distinction:

- **Context**: information passed into the current model call.
- **State**: durable task/session data used by the application.
- **Memory**: selected information persisted for future turns, sessions, users, or agents.
- **Knowledge**: external source of truth, usually retrieved rather than memorized.

### 5. Multi-Agent Systems

Multi-agent systems are useful when the task naturally decomposes across roles, tools, permissions, or evaluation perspectives. They are not automatically better than a single well-scoped agent.

Use multi-agent designs when:

- Different roles need different tools or permissions.
- Independent critique or verification improves quality.
- Work can run in parallel.
- Specialized agents reduce prompt complexity.
- Organizational boundaries matter, such as planner, researcher, coder, reviewer, and operator.

Avoid multi-agent designs when a deterministic workflow, single agent, or simple tool call is enough.

### 6. Protocols and Interoperability

Agentic systems increasingly depend on standard interfaces for tools, data, and agent communication.

Key ideas:

- **MCP** standardizes how models and agents connect to tools and external context.
- **A2A-style patterns** standardize task handoff, delegation, and agent-to-agent communication.
- **Tool registries and gateways** help teams govern which tools are approved, discoverable, versioned, and observable.

## Chapter Boundaries

This chapter explains the foundations. It should not become a framework tutorial or production runbook.

- Detailed architectures belong in [System Design](../03_system_design/README.md).
- Framework comparisons and hands-on examples currently live in [Frameworks](../02_frameworks/README.md) and will move into the hands-on appendix.
- Production runtime, deployment, security, data governance, and cost controls will move into the new Prototype to Production chapter.
- Resource links belong in [Resources](../RESOURCES.md).

## Migration Notes

Completed in this phase:

- Added compact GenAI and Agentic AI foundations subchapters.
- Added focused multimodal/VLM and diffusion foundations notes.
- Cleaned the agents reference page into a concise visual/reference index.
- Split build-stack guidance out of foundation notes and left it for production/hands-on chapters.

Future chapter work:

1. Move framework/build-stack decisions into the Prototype to Production chapter.
2. Move detailed system-design diagrams and production patterns into the System Design chapter.
3. Keep only compact inline examples in this chapter; move full tutorials to the hands-on appendix.
