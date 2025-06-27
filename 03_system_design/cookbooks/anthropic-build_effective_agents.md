
# Anthropic's Building Effective Agents Summary
**Published:** Dec 19, 2024  
**Source:** 
- [Anthropic Blog](https://www.anthropic.com/engineering/building-effective-agents)
- [Anthropic Cookbook (patterns/agents)](https://github.com/anthropics/anthropic-cookbook/tree/main/patterns/agents)


## Workflow Patterns Overview

1. **Basic Workflows**  
    - **Prompt Chaining**: Sequentially process tasks using predefined prompts.  
    - **Routing**: Classify input and route to appropriate workflows or tools (via handoffs).  
    - **Parallelization**: Execute multiple sub-tasks simultaneously and aggregate results.  

2. **Evaluator-Optimizer Workflow**  
    - Iteratively refine outputs by generating, evaluating, and optimizing via feedback loops and an evulator agent.  

3. **Orchestrator-Workers Workflow**  
    - An orchestrator agent dynamically decomposes tasks into subtasks, delegates to specialized workers, and synthesizes results.  

---

## Core Concepts

| Type        | Description                                                                 |
|-------------|-----------------------------------------------------------------------------|
| **Workflow**| Predefined sequence of LLM + tool steps, predictable, controlled logic      |
| **Agent**   | LLM-driven reasoning and control over tools, memory, and task flow          |



### When to Use What
> Use workflows when predictability matters  
> Use agents when flexibility and adaptability are required

#### Workflow
- Use **Workflow** for static processes with predefined steps.
- Use **Workflow** for tool usage with human oversight.

#### Agents
- Use **Agent** when planning and dynamic adaptation are required.
- Use **Agent** for tasks that may require retries or reasoning.

---

## Workflow Patterns 

## 1. Basic Workflows 
#### 1.1 Prompt Chaining

**Example: Email generation**
```
Step 1: Summarize user input →  
Step 2: Generate subject line →  
Step 3: Write full email based on summary & subject
```


```python 
def chain(input_text, prompts):
    output = input_text
    for prompt in prompts:
        output = llm.invoke(prompt.format(output))
    return output
```
usage: 
```python 
prompts = [
    "Summarize: {}",
    "Generate subject line: {}",
    "Compose email using: {}"
]
result = chain("User input text here", prompts)
```
---

#### 1.2. 🔀 Routing

**Example: Customer support**
```
Step 1: Classify query ("refund", "technical", "shipping") →  
Step 2: Route to relevant prompt/tool
```

```python
if "refund" in query:
    run_refund_workflow()
elif "tech" in query:
    run_tech_support()
```

```python 
def routing(input_text, routes):
    classification = llm.invoke("Classify: {}".format(input_text))
    handler = routes.get(classification, default_handler)
    return handler(input_text)
```

usage 
```python 
routes = {
    "refund": handle_refund,
    "technical": handle_technical_support,
    "shipping": handle_shipping
}
response = routing("I need help with my order", routes)
```
---

#### 1.3. Parallelization

**Example: Product description generation**
```
Run 3 different styles →  
Compare outputs →  
Pick best or combine
```

```python
def parallel(prompt_template, inputs):
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(llm.invoke, prompt_template.format(i)) for i in inputs]
        return [f.result() for f in futures]
```

usage 
```python 
inputs = ["Input A", "Input B", "Input C"]
prompt = "Process this input: {}"
results = parallel(prompt, inputs)
```
---
### 2. 🔁 Evaluator-Optimizer Workflow

- Iteratively refine outputs by generating responses and evaluating them in a feedback loop. ￼

Key Characteristics:
	•	**Generation**: An LLM produces an initial output based on the task.
	•	**Evaluation**: Another LLM assesses the output against predefined criteria.
	•	**Optimization**: Feedback from the evaluator is used to refine the output in subsequent iterations. ￼

Ideal Use Cases:
	•	Tasks with clear evaluation metrics.
	•	Scenarios where iterative refinement enhances quality.
	•	Literary translations capturing nuanced meanings.
	•	Complex searches requiring multiple rounds of information gathering. ￼ ￼

```python 
def generate(prompt: str, context: str = "") -> str:
    # Generate initial response
    return llm.invoke(f"{context}\n\n{prompt}")

def evaluate(task: str, content: str) -> str:
    # Evaluate the generated content
    return llm.invoke(f"Evaluate the following {task}:\n\n{content}")

def loop(task: str, max_iters: int = 5) -> str:
    context = ""
    for _ in range(max_iters):
        output = generate(task, context)
        feedback = evaluate(task, output)
        if "PASS" in feedback:
            return output
        context += f"\n\nFeedback: {feedback}"
    return output
```

<!-- Example:
Translating a poem where the initial translation is evaluated for tone and rhythm, and feedback is used to produce a more faithful rendition. -->
---

### 3.  Orchestrator-Workers Workflow

Purpose: Dynamically decompose complex tasks into subtasks, delegate them to worker LLMs, and synthesize the results. ￼

Key Characteristics:
	•	Dynamic Task Decomposition: The orchestrator LLM analyzes the input and determines the necessary subtasks.
	•	Delegation: Each subtask is assigned to a specialized worker LLM.
	•	Synthesis: Results from worker LLMs are aggregated to form the final output. ￼

Ideal Use Cases:
	•	Tasks where subtasks can’t be predefined and vary based on input.
	•	Complex coding tasks involving multiple file changes.
	•	Search tasks requiring information gathering from diverse sources. ￼ ￼

```python 
class Orchestrator:
    def __init__(self, prompt: str):
        self.prompt = prompt

    def parse(self) -> List[str]:
        # Decompose the main task into subtasks
        return llm.invoke(f"Break down the task: {self.prompt}").splitlines()

    def process_tasks(self, tasks: List[str]) -> List[str]:
        # Assign each subtask to a worker LLM
        return [llm.invoke(f"Execute subtask: {task}") for task in tasks]

    def synthesize(self, results: List[str]) -> str:
        # Combine the results from all workers
        return llm.invoke(f"Combine the following results:\n\n{results}")
```
usage
```python 
orchestrator = Orchestrator("Generate a comprehensive report on climate change impacts.")
subtasks = orchestrator.parse()
results = orchestrator.process_tasks(subtasks)
final_report = orchestrator.synthesize(results)
```

Example:

A coding assistant that, upon receiving a feature request, identifies affected files, delegates code modifications to worker LLMs, and integrates the changes into a cohesive codebase. ￼




## Agent Pattern & Loop

### Agent Loop Example
```
1. Decide: "I need to look up a fact"
2. Act: Call web search API
3. Observe: Retrieve result
4. Decide: "Now I can answer"
5. Output final answer
```

```python
while not done:
    action = agent.plan(state)
    result = tools[action](input)
    state.update(result)
```

###  Tools & Enhancements

**Example**: Retrieval-augmented generation
```python
query = "Explain Claude AI"
docs = vector_search(query)
response = llm(prompt + docs)
```

##  Frameworks: Use Carefully

| Framework        | Role                                |
|------------------|--------------------------------------|
| **LangGraph**    | Graph-based control flow (agents, loops) |
| **LangChain**    | Chains, memory, tools, agents         |
| **Rivet**        | GUI builder for workflows             |
| **Vellum**       | Workflow UI with evaluation           |
| **Amazon Bedrock** | Framework for agent orchestration   |


### Best Practices

- Start simple – don’t over-engineer
- Use workflows first, agents when needed
- Design reusable, modular prompts
- Observe, log, and evaluate results often

---
###  Appendix 1: Agents in Practice

#### A. Customer Support Agent

**Why agents work well:**
- Conversational interface matches natural support flow
- Requires access to external tools (order history, customer data)
- Agents can programmatically perform actions (refunds, ticket updates)
- Clear success criteria (resolved/unresolved)
- Human oversight + feedback loops enhance performance

**Business viability:**
- Real-world implementations show success-based billing (e.g. charge per resolution)

#### B. 💻 Coding Agents

**Why agents work well:**
- Code is verifiable via automated tests
- Feedback loop: test → fix → re-test
- Well-structured problem space
- Output is objectively measurable

**Example:**
- Claude agents solving real GitHub issues on SWE-bench Verified
- Agents use PR descriptions to implement fixes
- Human review still required for broader integration


#### C.🧾 Document Processing Agent

**Workflow**:
- Upload document
- Extract + segment text
- Summarize segments
- Compile overview
---

### Appendix 2: Prompt Engineering Your Tools

**Tools are essential to agentic systems. Good tool prompting = better agent behavior.**

#### Key Guidelines

- Let model "think" before committing to output
- Use familiar formats (e.g., markdown over JSON for code)
- Avoid formats with high overhead (e.g., line-count diffs)

####  Agent-Computer Interface (ACI) Tips

| Tip                                  | Description                                                                 |
|--------------------------------------|-----------------------------------------------------------------------------|
| **Think like the model**             | Is tool usage obvious? Add examples, format specs                           |
| **Improve naming**                   | Clear, intuitive parameter names help LLMs interpret tool APIs              |
| **Test iteratively**                 | Use real input cases, analyze mistakes, refine tools                        |
| **Poka-yoke design**                 | Prevent misuse through tool constraints (e.g., enforce absolute paths)      |

<!-- #### 🛠 Claude Example:
- Issue: Agents failed with relative paths after changing directories
- Fix: Required absolute paths → success rate improved -->

> “We spent more time optimizing tools than the prompt.”

---

