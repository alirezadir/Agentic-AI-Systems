# From Models to Compound AI Systems
Reference: [The Shift from Models to Compound AI Systems  BAIR Blog, Feb 2024](https://bair.berkeley.edu/blog/2024/02/18/compound-ai-systems/)

## 1. Compound AI Systems

- **Pre-2023:** Traditional focus in AI:building ever-larger, more capable models (e.g., LLMs).
- **2024:** SOA results are now increasingly achieved by **compound systems**: 
    - AI applications composed of **multiple interacting components** (e.g., multiple model calls, retrievers, external tools).
- Examples: 
    - AlphaCode 2 (LLM + code execution + clustering), AlphaGeometry (LLM + symbolic solver), 
    - RAG pipelines, 
    - multi-step chains (e.g. CoT@32)
- Compound systems enable higher performance, flexibility, and reliability than monolithic models alone.
- **2025:** Agents and agentic AI systems have become the dominant paradigm, with standardized frameworks, evaluation practices, and production-ready patterns


**Why Compound AI Systems?**
- No clear end in sight to the scaling of AI models; more state-of-the-art results are obtained using compound systems. Why?
1. **System design scaling can yield bigger improvements than model scaling** (e.g., sampling, filtering, chaining).
    - higher returns-to-cost ratio of system design scaling than model scaling (e.g. 30% vs 5%).
    - faster to iterate on system design than model scaling.
2. **Dynamic knowledge and access control**: Models are static (knowledge and access); systems can incorporate up-to-date data and enforce access.
3. **Control and trust**: models are hard to control (e.g. certain behavior, hallucinations); systems can filter, retrive,verify, and cite outputs, increasing trust.
4. **Performance and cost optimization**: Models have fixed performance and cost; systems can mix models and strategies to meet diverse application needs. 

**Agents and agentic AI systems**: 
- Agents are compound systems that can dynamically select and combine components based on the task at hand.
- Agentic AI systems are compound systems that can learn and adapt to the task at hand.

## 2. Compound AI System Design
- On the surface, an AI system is a combination of traditional software and AI models.
- Interesting design questions, e.g.:
    - Control Logic: should it be in traditional code (e.g., Python LLM calls), or driven by an AI model (e.g. agents with external tool calls)?
    - Orchestration: how to orchestrate the components to achieve the desired goal?
    - Optimization: where to invest resources?
        - where to invest resources? e.g. in retrievers, or in models? or tools? or use multiple models?
        - how to do end-to-end end-to-end to maximize a metric?
    - Monitoring: how to monitor the system for the desired goal?
    - Security: how to secure the system for the desired goal?

**Core System Components**:
- **Models**: LLMs or other AI models for core reasoning or generation.
- **Retrievers**: Systems for fetching relevant data (e.g., search, RAG).
- **External Tools**: APIs, code execution, symbolic solvers, plugins.
- **Control Logic**: Orchestration via traditional code or agent frameworks.

### 2.1. Key Challenges

- **Design Space**: Vast possible combinations of models, retrievers, tools, and orchestration strategies. Resource allocation (latency, cost) is complex.
    - Examples: in a simple RAG system: 
        - many retrieval and models to choose from, 
        - techniques to improve retrieval quality (e.g. query expansion or reranking models), 
        - techniques to improve the LLMs generated output (e.g., running another LLM to check that the output relates to the retrieved passages)

- **Optimization**: 
    - Requires co-optimizing the components (e.g. a model that wored well for a retrievr, and a retriver that works well for a model)
    - Components are often non-differentiable (e.g. search engines or code interpreters)
    - end-to-end optimization is an open research area (e.g., DSPy for pipeline optimization).

- **Operation (MLOps/DataOps)**: 
    - MLOps more challenging: 
        - e.g. track and debug the performance of a classifer agent: variable number of reflection steps or external API calls
    - Monitoring, debugging, and securing compound systems is more complex than for single models. 
    - New tools are emerging for trace analysis, data quality, and security.

### 2.3. Emerging Paradigms & Tools

- **Composition Frameworks and Strategies**: 
    - LLM frameworks: (LangChain, LlamaIndex), 
    - Agent frameworks (AutoGPT, BabyAGI), 
    - prompt control tools (Guardrails, Outlines, LMQL, SGLang).
    - Inference strategies: CoT, self-consistency, RAG, etc
- **Automated Optimization**: 
    - **Quality Opimization**: DSPy (pipeline optimization given a quality metric), 
    - **Cost Opimization**: **AI gateways** or routers: FrugalGPT (cost-quality routing), Databricks AI Gateway, OpenRouter, Martian.
- **LLMOps/DataOps**: 
    - **Monitoring**: required for both model outputs and data pipelines
        - **Tracing**: Need to track all the steps taken by the application and intermediate outputs
    - LangSmith, Phoenix Traces, Databricks Inference Tables for monitoring and evaluation; 
    - DSPy Assertions (research), MT-Bench, FAVA, ARES for automated quality checks.

### 2.4. Example Systems:
- **AlphaCode 2**
  - *Components & Design*: LLMs, code execution, clustering, solution filtering
  - *Results/Notes*: 85th percentile in coding contests

- **AlphaGeometry**
  - *Components & Design*: LLM + symbolic math engine, iterative construction and checking
  - *Results/Notes*: Olympiad-level geometry performance

- **Medprompt**
  - *Components & Design*: LLM, retrieval, chain-of-thought, ensembling
  - *Results/Notes*: Outperforms specialized medical models

- **Gemini (MMLU)**
  - *Components & Design*: LLM, custom inference logic (CoT@32)
  - *Results/Notes*: 90% on MMLU, surpassing GPT-4 5-shot

- **ChatGPT Plus**
  - *Components & Design*: LLM, web browser, code interpreter, image generator plugins
  - *Results/Notes*: Multi-tool consumer AI product

- **RAG, ORQA, etc**
  - *Components & Design*: LLM(s), retrieval system, multi-step query and answer generation
  - *Results/Notes*: Widely used in search and enterprise apps




## 5. Conclusion

- Compound AI systemscomposed of multiple models, tools, and orchestration logicare now the leading paradigm for achieving state-of-the-art results in AI applications.
- Best practices for design, optimization, and operation are still evolving, but frameworks and tools are rapidly emerging.
- Compound systems are expected to remain a key trend in AI, enabling higher quality, reliability, and flexibility than monolithic models alone.



