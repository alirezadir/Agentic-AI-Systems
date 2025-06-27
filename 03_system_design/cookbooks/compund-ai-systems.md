# Compound AI Systems
Source: [Compound AI Systems](https://bair.berkeley.edu/blog/2024/02/18/compound-ai-systems/)

## 1. Compound AI Systems: Introduction

- Traditional focus in AI was on building ever-larger, more capable models (e.g., LLMs).
- State-of-the-art results are now increasingly achieved by **compound systems**—AI applications composed of **multiple interacting components** (e.g., multiple model calls, retrievers, external tools).
- Examples: AlphaCode 2 (LLM + code execution + clustering), AlphaGeometry (LLM + symbolic solver), RAG pipelines, multi-step chains, and enterprise applications.
- Compound systems enable higher performance, flexibility, and reliability than monolithic models alone.

**Why Compound AI Systems?**
1. **System design can yield bigger improvements than model scaling** (e.g., sampling, filtering, chaining).
2. **Dynamic knowledge and access control**: Models are static; systems can incorporate up-to-date data and enforce access.
3. **Control and trust**: Systems can filter, verify, and cite outputs, increasing reliability.
4. **Performance and cost optimization**: Systems can mix models and strategies to meet diverse application needs.

## 2. Compound AI System Design

### System Components:
- **Models**: LLMs or other AI models for core reasoning or generation.
- **Retrievers**: Systems for fetching relevant data (e.g., search, RAG).
- **External Tools**: APIs, code execution, symbolic solvers, plugins.
- **Control Logic**: Orchestration via traditional code or agent frameworks.

### Example Systems:
| System         | Components & Design                                                                                  | Results/Notes                                      |
|----------------|-----------------------------------------------------------------------------------------------------|----------------------------------------------------|
| AlphaCode 2    | LLMs, code execution, clustering, solution filtering                                                | 85th percentile in coding contests                 |
| AlphaGeometry  | LLM + symbolic math engine, iterative construction and checking                                     | Olympiad-level geometry performance                |
| Medprompt      | LLM, retrieval, chain-of-thought, ensembling                                                        | Outperforms specialized medical models             |
| Gemini (MMLU)  | LLM, custom inference logic (CoT@32)                                                                | 90% on MMLU, surpassing GPT-4 5-shot               |
| ChatGPT Plus   | LLM, web browser, code interpreter, image generator plugins                                         | Multi-tool consumer AI product                     |
| RAG, ORQA, etc | LLM(s), retrieval system, multi-step query and answer generation                                    | Widely used in search and enterprise apps          |

## 3. Key Challenges

- **Design Space**: Many possible combinations of models, retrievers, tools, and orchestration strategies. Resource allocation (latency, cost) is complex.
- **Optimization**: Components are often non-differentiable; end-to-end optimization is an open research area (e.g., DSPy for pipeline optimization).
- **Operation (MLOps/DataOps)**: Monitoring, debugging, and securing compound systems is more complex than for single models. New tools are emerging for trace analysis, data quality, and security.

## 4. Emerging Paradigms & Tools

- **Composition Frameworks**: LangChain, LlamaIndex, agent frameworks (AutoGPT, BabyAGI), and prompt control tools (Guardrails, Outlines, LMQL, SGLang).
- **Automated Optimization**: DSPy (pipeline optimization), FrugalGPT (cost-quality routing), AI gateways (Databricks AI Gateway, OpenRouter, Martian).
- **LLMOps/DataOps**: LangSmith, Phoenix Traces, Databricks Inference Tables for monitoring and evaluation; DSPy Assertions, MT-Bench, FAVA, ARES for automated quality checks.

## 5. Conclusion

- Compound AI systems—composed of multiple models, tools, and orchestration logic—are now the leading paradigm for achieving state-of-the-art results in AI applications.
- Best practices for design, optimization, and operation are still evolving, but frameworks and tools are rapidly emerging.
- Compound systems are expected to remain a key trend in AI, enabling higher quality, reliability, and flexibility than monolithic models alone.

---

**Reference:**  
[The Shift from Models to Compound AI Systems – BAIR Blog, Feb 2024](https://bair.berkeley.edu/blog/2024/02/18/compound-ai-systems/)
