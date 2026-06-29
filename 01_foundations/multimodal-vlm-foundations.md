# Multimodal and VLM Foundations

Multimodal models extend GenAI systems beyond text. They can process or generate combinations of text, images, screenshots, documents, audio, video, charts, code, and UI state.

## Mental Model

```text
artifact -> perception/encoding -> reasoning -> grounded output or action
```

The model does not just "see" an image. A production system usually combines model perception with deterministic extraction, metadata, retrieval, tool calls, and validation.

## 1. Modalities

Common modalities:

- **Text**: natural language, code, logs, structured records.
- **Images**: photos, scans, diagrams, product images, medical/industrial images.
- **Documents**: PDFs, forms, contracts, slides, spreadsheets, reports.
- **Screenshots and UI state**: browser pages, desktop apps, mobile apps, IDEs.
- **Audio**: speech, meetings, calls, sound events.
- **Video**: temporal visual/audio streams, demos, inspections, surveillance, generated media.
- **3D/spatial data**: robotics, AR/VR, CAD, geospatial, simulation.

## 2. Vision-Language Models

Vision-language models connect visual perception to language reasoning.

Typical capabilities:

- OCR and text-in-image understanding.
- Layout and document structure understanding.
- Object, scene, and relationship recognition.
- Chart and table interpretation.
- Screenshot and UI reasoning.
- Visual question answering.
- Image-grounded summarization and extraction.

Important limitation: VLMs can appear confident while missing small visual details. Use deterministic parsers, OCR, bounding boxes, source coordinates, and human review when precision matters.

## 3. Multimodal System Patterns

### Document Understanding

```text
document -> parse/OCR/layout -> chunk -> retrieve -> reason -> structured output
```

Use when building contract review, invoice processing, compliance review, research assistants, and enterprise search.

Design notes:

- Preserve page number, section, table, and coordinate metadata.
- Use OCR/layout tools when exact text matters.
- Treat scanned documents differently from native PDFs.
- Evaluate extraction fields separately from final summary quality.

### Screenshot and Computer Use

```text
screenshot/UI state -> model interpretation -> action proposal -> validated browser/desktop action
```

Use for web automation, QA, data entry, coding tools, workflow automation, and computer-use agents.

Design notes:

- Prefer structured DOM/API access when available.
- Use screenshots when the UI is the source of truth or no API exists.
- Validate coordinates, selectors, and destructive actions.
- Keep a trace of screenshots, actions, observations, and failures.

### Multimodal RAG

```text
text/images/audio/video -> embeddings/indexes -> retrieval -> reranking -> grounded answer
```

Use for media libraries, design systems, product catalogs, knowledge bases, diagrams, and meeting archives.

Design notes:

- Store original artifact links and thumbnails.
- Use modality-specific chunking.
- Rerank with a model that understands the target modality.
- Evaluate retrieval separately from generation.

### Audio and Voice Agents

```text
speech -> transcription -> reasoning/tool use -> response text -> speech
```

Use for support, sales, coaching, interviewing, meeting assistants, and accessibility.

Design notes:

- Separate speech recognition errors from reasoning errors.
- Track latency budget across ASR, model, tools, and TTS.
- Add interruption, barge-in, silence handling, and escalation policies.
- Be explicit about recording, consent, retention, and PII.

## 4. Data Representation

A multimodal system often stores several representations of the same artifact:

- Raw file.
- Extracted text.
- OCR output.
- Layout metadata.
- Bounding boxes or timestamps.
- Thumbnails or keyframes.
- Embeddings.
- Human labels or review notes.
- Derived summaries.

Keep references back to the source. Grounded answers should cite page, timestamp, region, frame, or artifact ID where possible.

## 5. Evaluation

Multimodal evaluation needs to isolate where the error came from.

Evaluate:

- Perception accuracy: OCR, object detection, chart reading, layout parsing.
- Retrieval quality: did the system fetch the right artifact/region/time span?
- Reasoning quality: did the model correctly use the evidence?
- Action quality: did the agent click, type, edit, or submit correctly?
- Safety: did it avoid unsafe content, privacy leakage, or destructive actions?
- UX: was latency acceptable and were uncertainty/escalation states clear?

Useful test sets:

- Low-quality scans.
- Cropped screenshots.
- Dense tables.
- Ambiguous charts.
- Multi-page documents.
- UI states with similar buttons.
- Domain-specific images.
- Adversarial prompt text embedded in images or documents.

## 6. Security and Privacy

Multimodal inputs can carry hidden or non-obvious risk.

Risks:

- Prompt injection inside documents, screenshots, captions, or OCR text.
- PII in images, forms, voices, transcripts, or metadata.
- Copyright or licensing issues for generated media.
- Sensitive screenshots containing credentials, customer data, or internal systems.
- Cross-tenant leakage through shared indexes or memory.

Controls:

- Treat extracted text as untrusted input.
- Separate user-provided content from system instructions.
- Apply PII detection to OCR/transcripts when needed.
- Scope tool permissions tightly.
- Keep audit trails for computer-use actions.
- Add human approval for external or irreversible actions.

## 7. Design Checklist

- What modalities are input and output?
- Is the model expected to perceive, reason, generate, or act?
- What deterministic parsers should run before the model?
- What metadata is needed for grounding?
- What source citations should be returned?
- How will errors be attributed to perception, retrieval, reasoning, or action?
- What privacy and retention rules apply to raw artifacts?
- What actions require approval?

## Related Notes

- [GenAI Foundations](./genai-foundations.md)
- [Agentic AI Foundations](./agentic-ai-foundations.md)
- [RAG](./ai-engineering-summary/Chapter_6_1_RAG.md)
