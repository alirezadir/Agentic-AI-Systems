
# Foundation Models as Planners

## Can Foundation Models Plan?

There is ongoing debate about whether large language models (LLMs), especially autoregressive ones, are capable of effective planning.

- **Yann LeCun** argues that autoregressive LLMs can't plan.
- **Kambhampati (2023)** states that while LLMs are good at retrieving knowledge, they struggle with producing executable plans.
- Generated plans may appear coherent but often fail at execution.
- It's unclear whether this limitation is inherent or due to lack of proper prompting and tooling.

## Planning as a Search Problem

Planning is fundamentally a **search problem**: finding paths to a goal, predicting their outcomes, and selecting the most promising one.

- Backtracking is often needed (e.g., trying path A, failing, then trying path B).
- Critics say autoregressive models can't backtrack. However:
  - LLMs can restart and revise paths, effectively simulating backtracking.
  - Planning requires knowing the **effects of actions** and the **environmental context**.

## Tooling and Outcome Prediction

Planning needs:
- Awareness of **available actions**.
- Prediction of **state transitions** after an action.
  
Paper: _"Reasoning with Language Model is Planning with World Model"_ (Hao et al., 2023) proposes that LLMs can internally simulate outcomes, making coherent planning possible.

Even if LLMs can't plan alone, they can assist as components in larger planning systems (e.g., integrated with search or state tracking).

---

## FM vs RL Planners

| Feature                | Foundation Model (FM) Agents                | Reinforcement Learning (RL) Agents         |
|------------------------|---------------------------------------------|--------------------------------------------|
| Planning Approach      | Prompting or fine-tuning                    | Learning policies via reward feedback      |
| Resource Intensity     | Lower                                        | High (training-heavy)                      |
| Adaptability           | High                                         | Moderate                                   |
| Hybridization          | Can integrate RL algorithms                 | FM+RL agents may converge in the future    |

---

## Plan Generation via Prompting

The simplest method to make a model generate plans is via **prompt engineering**.

### Example Prompt:
```
Propose a plan to solve the task. You have access to 5 actions:
- get_today_date()
- fetch_top_products(start_date, end_date, num_products)
- fetch_product_info(product_name)
- generate_query(task_history, tool_output)
- generate_response(query)
```

### Example Plan Outputs:

| Task                                 | Generated Plan                                                       |
|--------------------------------------|----------------------------------------------------------------------|
| Tell me about Fruity Fedora          | [fetch_product_info, generate_query, generate_response]             |
| Best-selling product last week       | [fetch_top_products, generate_query, generate_response]             |
| Price of best-selling product        | [get_time, fetch_top_products, fetch_product_info, generate_query, generate_response] |

### Parameter Resolution:

- Plans are generated **without fixed parameters**.
- Parameters (e.g., dates, quantities) are inferred from tool outputs or context.

### Common Challenges:
- **Missing information** in user queries (e.g., timeframe).
- **Hallucinations** in action names or parameters.
- **Tool mismatches** or invalid sequences.

---

## How to Improve Planning

Here are some approaches to enhance planning reliability:

- Improve system prompts (more structured examples).
- Write detailed descriptions for tools/functions.
- Simplify complex tools by breaking them down.
- Use stronger base models.
- Fine-tune a model specifically for plan generation.

---

## Summary

Foundation models have **potential as planners**, but current limitations around:
- Backtracking
- Parameter handling
- Tool integration
- Action outcome prediction

...require thoughtful design of agent workflows and hybrid systems. Improvements in prompting, tool use, and model fine-tuning can lead to more reliable, executable plans in agentic systems.
