# Chapter 5: Prompt Engineering 

---

<!-- ### Overview -->

<!-- 1. Introduction to Prompting and Its Importance
2. In-Context Learning: Zero-Shot and Few-Shot Prompting
3. Prompt Design: System vs. User Prompts
4. Managing Context Length and Prompt Efficiency
5. Prompt Engineering Best Practices
6. Defensive Prompt Engineering and Safety Strategies
7. Evaluation Techniques for Prompt Robustness
8. Interview Review Questions
9. Code & Prompt Snippets -->

* **Prompt**: instructions (+ context) given to a model to perform a task

  * e.g. Task description, Example(s), Output format
  * context: information given to a model to perform the prompt's requested task 
* **Prompt engineering**: frames input instructions + context to guide a model’s behavior; often serving as the first step in model adaptation.



* **In-Context Learning**: learn the desirable behavior from examples (shots) in the prompt 
  * **Zero-shot**: no examples; best for simple and generic tasks
    *Example:*

    ```text
    Summarize the following paragraph in three bullet points: 
    Paragraph: lorem ipsun .. 
    ```
  * **Few-shot**: embed examples in prompt; useful for formatting, reasoning, or nuance
    *Example:*

    ```text
    Correct grammar:
    Input: she go to school → Output: She goes to school
    Input: they is playing → Output: They are playing
    ```

* **Prompt Types**:

  * **System Prompt**: configures base behavior, tone, safety boundaries, task domain
    *Example:*

    ```text
    {"role": "system", "content": "You are a helpful assistant
      who avoids harmful or illegal content."}
    ```
  * **User Prompt**: direct user instruction or query
    *Example:*

    ```text
    Question: Explain how gravity works in simple terms.
    Answer: 
    ```
  * Combine both for layered control
  * The model combines system & user into a single prompt, typically following a template.

* **Context Length**: Amount of information can be included in a prompt
   * Models have **maximum context length** limits
      * e.g. GPT-3: 2K, GPT-4: 32-128K, Gemini 1.5 pro: 2M
      * scale: 100K words (~130K tokens) ~ a moderate book;  2M ~ 2000 wiki pages, or PyTorch code
   * Models are much better at understanding the beginning and the end of a prompt than the middle
  * Efficient prompting: 
      * Use only relevant parts of input
      * Token limit affects both cost and latency
      * Use compression techniques: structured formats (e.g., JSON > prose), eliminate redundancy or verbose phrasing
      ```text
      Can you please summarize this user complaint and highlight any urgent problems?  
      -> Summarize & flag urgent: 'The device caught fire while charging.'
      ```

## 2.2 Prompt Engineering Best Practices

1. **Write Clear and Explicit Instructions**
   * Explain the task without ambiguity
   * Give the model to adopt a persona (role)
   * Provide examples
   * Specify  output format
   ```text
   `You are a high-school teacher. List five advantages of solar energy. Use bullet points.`
   ```
2. **Provide Sufficient Context**
   ```text
   Context: [disclosure.pdf]
   Question: Summarize the noise complaints,
   ```
   * restricting a model to only the context is tricky: Clear instructions, e.g. `answer using only the provided context`
3. **Break Complex Tasks into Simpler Subtasks**
   ```text
   Step 1: Summarize the content. Step 2: Identify tone. Step 3: Generate a title.
   ```
   * prompt decomposition: each subtask having its own prompt 
      * e.g. for a customer service bot: 
         * Prompt 1 (intent classification), 
         * Prompt 2 (response to a troubleshooting request)
      * pros: monitoring, Debugging, Parallelization
      * cons: increased latency & costs
4. **Give the Model Time to Think**: 
   * Chain-of-Thought (CoT) and self-critique prompting
   * **Chain-of-Thought (CoT)**
      * explicitly asking the model to think step by step
      * simple CoT: add `think step by step` or `explain your decision`

      ```text
      Which animal is faster: cats or dogs? Think step by step before arriving at an answer.
      ```
   * **self-critique prompting**
      * asking the model to check its own outputs.
5. **Iterate on Prompts**
   * Use versioning, A/B testing, and maintain a prompt registry
6. **Automate Prompting with Tools / AI**
   * Manual prompt engineering is time-consuming
   * Use prompt engineering automation tools (OpenPrompt, DSPy), or AI models: 
      * e.g. `Help me write a concise prompt for an application that grades ...`
   * AI-powered prompt optimization tools: Promptbreeder
   * Tools for structurd output: Guidance, Outlines, Instructor
   * Caution: be aware of hidden model API calls (e.g. 30 variations of a prompt = 30X API calls)
   * Use Promptfoo, DSPy, LangChain to test and debug prompt performance
7. **Organize and Version Prompts**
   * Separate prompts from code (e.g. in `prompts.py`)
   ```python 
   # prompts.py
   GPT4o_ENTITY_EXTRACTION_PROMPT = [YOUR PROMPT]
   ```
      * Reusability, Testing, Collab
   * Use prompt metadata for scaling prompts in applications 
      * e.g. wrap in an object 
      ```python 
         from pydantic import BaseModel
         class Prompt(BaseModel):
         model_name: str
         date_created: datetime
         prompt_text: str
         application: str
         creator: str
      ```
   * Annotate prompts in production; track changes and usage outcomes
   * Prompt templates: .prompt file format: Tools e.g. Firebase’s Dotprompt

*Additional Patterns:*

* **Structured Output Prompt**

  ```text
  Extract the following from the text: name, age, issue. Return JSON.
  ```
* **Role-Based Prompt**

  ```text
  You are a career advisor helping a user switch from finance to UX design.
  ```
* **Safety Classifier Prompt**

  ```text
  Analyze this response and classify as SAFE, RISKY, or UNSAFE.
  ```

---

## 2.3 Defensive Prompt Engineering

| Threat                        | Description                                  |
| ----------------------------- | -------------------------------------------- |
| **Reverse Prompting**         | Extracting proprietary prompts from outputs  |
| **Jailbreaking / Injection**  | Bypassing constraints with adversarial input |
| **Sensitive Info Extraction** | Prompt-crafted info leaks                    |

**Mitigations**:

* Prompt filtering and sanitization
* Add refusal constraints (e.g., "Do not generate unsafe content")
* Reinforce system identity in prompts (e.g., "You are a safe assistant")
* Monitor for known injection vectors: "ignore", "bypass", "as DAN"

*Code Example: Regex Guard in Python*

```python
import re
injection_phrases = ["ignore instructions", "override", "simulate DAN"]
if any(re.search(p, input, re.IGNORECASE) for p in injection_phrases):
    raise ValueError("Unsafe prompt detected")
```

---
