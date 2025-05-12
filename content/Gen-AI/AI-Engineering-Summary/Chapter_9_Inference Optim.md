# Chapter 9: Inference Optimization

---

# Inference Optimization

**inference optimization** aims to improve latency, cost, and throughput across model, hardware, and service levels

## Understanding Inference Optimization

### Inference Overview

* **Inference server** executes models on hardware
* **Inference service** handles request routing, preprocessing, response

### Computational Bottlenecks

#### Compute-bound

* Limited by arithmetic ops
* Example: **prefill step** in transformers

#### Memory bandwidth-bound

* Limited by memory transfer speed
* Example: **decode step** in transformers

#### Memory capacity-bound (a.k.a. OOM)

* Often appears as memory-bound in ML usage
* Can be addressed via model partitioning

```python
# Arithmetic intensity = FLOPs / bytes accessed
# Use Roofline model to diagnose bottlenecks
```

## Online and Batch Inference APIs

* **Online APIs**: optimize for latency
* **Batch APIs**: optimize for cost, allow aggressive batching
* Use cases for batch APIs:

  * Periodic reporting
  * Document ingestion
  * Synthetic data generation
* **Streaming mode**: emits tokens as generated, improves user-perceived latency

## Inference Performance Metrics

### Latency Components

* **TTFT**: Time to First Token (prefill)
* **TPOT**: Time Per Output Token (decode)
* **Total Latency** = `TTFT + TPOT × output_tokens`

### Throughput & Goodput

* **Throughput (TPS)**: tokens/sec system-wide
* **Goodput**: requests/sec meeting latency SLOs
* Tradeoff: Batching ↑ throughput, ↓ latency

### Utilization

#### MFU (Model FLOPs Utilization)

```python
MFU = actual_tokens_per_sec / peak_tokens_per_sec
```

#### MBU (Model Bandwidth Utilization)

```python
MBU = (param_count × bytes/param × tokens/s) / peak_bandwidth
```

* High MFU → compute-bound workload
* High MBU → bandwidth-bound workload

## AI Accelerators

### CPUs vs GPUs

* CPUs: few strong cores
* GPUs: thousands of weak, parallel cores (for **matmul-heavy** workloads)

### Specialized Inference Chips

* Examples: Apple Neural Engine, AWS Inferentia, MTIA, Edge TPU
* Optimized for: low-precision, fast memory, low power

### Chip Metrics

* **FLOPs**, **memory bandwidth**, **memory capacity**, **TDP**

## Model Optimization

### Model Compression

#### Quantization

* Reduces param size, memory bandwidth use
* Popular: **weight-only quantization**

#### Distillation

* Trains smaller model to mimic larger one

#### Pruning

* Removes unimportant params or sets them to zero (sparsity)
* Less adopted due to implementation complexity

### Autoregressive Decoding Optimizations

#### Speculative Decoding

* Use **draft model** for K tokens → verify with **target model**

```python
# Pseudocode
draft_tokens = draft_model(input)
verified_tokens = target_model.verify(draft_tokens)
```

#### Inference with Reference

* Copy repeated tokens directly from context instead of generating

#### Parallel Decoding

* Predict multiple tokens in parallel (e.g., **Medusa**, **Lookahead**)
* Requires token **verification and integration**

### Attention Mechanism Optimizations

#### KV Cache

```python
# KV Cache size
2 × B × S × L × H × bytes
```

* Bottleneck in long-context inference
* Solutions:

  * **Cross-layer attention**
  * **Multi-query/grouped-query attention**
  * **PagedAttention (vLLM)**

#### Attention Kernels

##### FlashAttention

* Fuses attention ops into optimized kernel
* Hardware-specific

## Kernels and Compilers

* Languages: **CUDA**, **Triton**, **ROCm**
* Techniques:

  * Vectorization
  * Parallelization
  * Loop Tiling
  * Operator Fusion
* Compilers: **torch.compile**, **XLA**, **OpenXLA**, **TensorRT**

## Inference Service Optimization

### Batching Techniques

* **Static Batching**: fixed size
* **Dynamic Batching**: fixed window
* **Continuous Batching**: return completed requests early; refill batch

### Decoupling Prefill and Decode

* Allocate different machines for compute-bound (prefill) and bandwidth-bound (decode) stages

### Prompt Caching

* Cache overlapping prompt segments (e.g., system prompts)
* Drastically reduces TTFT and cost
* Tradeoff: additional memory

### Parallelism Strategies

#### Replica Parallelism

* Multiple full-model replicas

#### Model Parallelism

* **Tensor Parallelism**: split operators
* **Pipeline Parallelism**: split model stages

#### Specialized Parallelism

* **Context Parallelism**: split input sequence
* **Sequence Parallelism**: split operations


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


