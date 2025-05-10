# Chapter 9: Inference Optimization

---

## Understanding Inference Optimization

### Inference Overview

- **Inference Server**: Executes models using available hardware. Handles incoming requests and returns predictions.
- **Inference Service**: Includes request routing, preprocessing, and the inference server.
- **API Types**:
  - **Online APIs**: Low latency, good for real-time use (chatbots, code gen).
  - **Batch APIs**: Cost-effective, suited for high-throughput (summaries, recommendations).

#### Bottlenecks
| Type                    | Definition                                          | Examples                            |
|-------------------------|-----------------------------------------------------|-------------------------------------|
| Compute-bound          | Limited by raw computation power                    | Image generation                    |
| Memory bandwidth-bound | Limited by data transfer rate (GPU <-> memory)     | Autoregressive LLM inference        |

**Prefill & Decode Phases**:
- **Prefill**: Input tokens processed in parallel → compute-bound
- **Decode**: One token at a time, dependent on memory load → bandwidth-bound

### Interview Tips
- Know the distinction between prefill and decode
- Discuss trade-offs in batching latency vs. throughput

---

### Inference Performance Metrics

| Metric     | Meaning                                                  | Tips for Use Cases                  |
|------------|----------------------------------------------------------|------------------------------------|
| TTFT       | Time to First Token — affected by prefill step           | Important for conversational bots  |
| TPOT       | Time Per Output Token — affected by decoding            | Critical for large outputs         |
| TBT / ITL  | Time Between Tokens / Inter-Token Latency               | Monitors smoothness in generation  |
| Throughput | Queries processed per second                            | Optimize for cost-efficiency       |
| Goodput    | Useful throughput (removes failed/incomplete queries)   | Evaluates real system effectiveness|
| Utilization| MFU/MBU show model/memory usage                         | Helps diagnose underused hardware  |

**Interview Takeaways**:
- Know trade-offs: reducing latency may increase cost.
- Discuss metrics for both user experience and infra planning.

---

### AI Accelerators

| Accelerator | Key Feature                     | When to Use                             |
|-------------|----------------------------------|------------------------------------------|
| GPU         | Parallel processing, flexible   | Standard for training & inference        |
| TPU         | Google’s matrix-op optimized   | Cost-effective for batch jobs            |
| Gaudi (Intel)| Memory/compute tuned chips     | Efficient LLM workloads                  |
| Cerebras    | Wafer-scale engine             | Extreme scale models                     |

**Memory Hierarchy Optimization**:
- **FlashAttention, Triton, ROCm**: Improve bandwidth-sensitive ops
- **Power Consumption Consideration**: Choose chips with optimal TDP/FLOPs balance

**Study Tip**: Review FLOPs, memory size, and bandwidth to match hardware to workload (compute-bound vs. bandwidth-bound).

---

## Inference Optimization

### Model Optimization

#### Compression Techniques
| Technique   | Description                                      | Use Case                             |
|-------------|--------------------------------------------------|--------------------------------------|
| Quantization| Reduce bit precision (e.g., float32 → int8)     | Faster inference, smaller models     |
| Distillation| Small model trained to mimic large one           | Edge deployment                      |
| Pruning     | Remove unimportant weights                      | Speed & memory gain without retrain |

#### Decoder Optimization
- **Autoregressive Decoding Bottlenecks**: Sequential generation delays output
- **KV Cache**: Helps skip recomputation for past tokens
- **Speculative Decoding**: Generate multiple tokens in parallel, verify correctness

#### Attention Mechanism Optimization
- **Grouped-Query Attention**: Reduces quadratic complexity
- **FlashAttention**: Efficient GPU kernel for attention

#### Kernels & Compilers
| Concept           | Purpose                                  | Tools                        |
|------------------|------------------------------------------|------------------------------|
| Vectorization     | Process multiple elements at once         | Torch, TensorRT              |
| Parallelization   | Chunk work across cores                   | CUDA, Triton                 |
| Loop Tiling       | Cache-efficient iteration order           | Hardware-specific tuning     |
| Operator Fusion   | Combine ops to minimize memory overhead   | TVM, MLIR, OpenXLA           |

---

### Inference Service Optimization

#### Batching
| Method             | Description                                  | Pros / Cons                          |
|--------------------|----------------------------------------------|--------------------------------------|
| Static Batching    | Wait for full batch                          | Efficient but high initial latency   |
| Dynamic Batching   | Timeout-based batching                       | Good latency-cost tradeoff           |
| Continuous Batching| Replace completed requests mid-batch         | Optimal throughput, lower latency    |

#### Parallelism
| Type                | How it Works                                          | Best For                  |
|---------------------|--------------------------------------------------------|---------------------------|
| Pipeline            | Each layer on diff machine (adds comm. overhead)       | Training large models     |
| Replica             | Same model, replicated to serve in parallel            | Low-latency apps          |
| Context             | Input split across devices                             | Long-context handling     |
| Sequence            | Ops split across machines (attention vs FF)            | Specialized workloads     |

#### Prompt Caching
- Cache frequent prompts or prefixes to reduce compute load

#### Decoupled Prefill & Decode
- Prefill on one machine, decode on another
- Separates compute and bandwidth bottlenecks

---

## Summary
- Optimize **latency**, **throughput**, **utilization** based on workload needs.
- Leverage model-level techniques (quantization, pruning, attention optimization) for size/speed.
- Service-level techniques (batching, caching, parallelism) keep model quality intact.

---

## Coding Examples & Snippets

### 1. Quantization with `transformers` and `bitsandbytes`
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
model_id = "facebook/opt-1.3b"
model = AutoModelForCausalLM.from_pretrained(model_id, load_in_8bit=True, device_map='auto')
tokenizer = AutoTokenizer.from_pretrained(model_id)
```
*Loads a model with 8-bit quantization for faster inference on supported GPUs.*

### 2. Speculative Decoding (Simplified Demo)
```python
def speculative_decode(model, tokenizer, input_text, num_predictions=4):
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    predictions = [model.generate(input_ids) for _ in range(num_predictions)]
    return [tokenizer.decode(p[0], skip_special_tokens=True) for p in predictions]
```
*Generates multiple possible outputs and allows verification logic externally.*

### 3. Simple Dynamic Batching Queue
```python
import time
from queue import Queue

queue = Queue()
BATCH_SIZE = 4
TIMEOUT = 0.1

batch = []
start = time.time()
while True:
    if not queue.empty():
        batch.append(queue.get())
    if len(batch) >= BATCH_SIZE or time.time() - start >= TIMEOUT:
        process_batch(batch)
        batch = []
        start = time.time()
```
*Implements timeout-based batching logic to simulate dynamic batching.*

### 4. Prompt Caching with LangChain
```python
from langchain.cache import InMemoryCache
from langchain.llms import OpenAI
from langchain import LLMChain

llm = OpenAI(cache=InMemoryCache())
prompt = "Explain autoregressive decoding."
chain = LLMChain(llm=llm, prompt=prompt)
response = chain.run({})
```
*Adds caching to reduce recomputation for repeated prompts.*

---


