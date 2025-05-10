
# OpenAI API QuickStart Guide (from Official Developer Docs)

This guide synthesizes the technical details and code examples from the official OpenAI API Guides across ten key areas:
Text and Prompting, Images and Vision, Audio and Speech, Structured Outputs, Function Calling, Conversation State,
Streaming, File Inputs, Reasoning, and Evals.

---

## 1. Text and Prompting

### Core Concepts
- The Completions API accepts a single prompt string, while the Chat Completions API uses a list of messages with roles
  (`system`, `user`, `assistant`) to preserve conversational context.
- Sampling controls like `temperature` (0–2) and `top_p` (0–1) let you balance randomness and coherence in generated text.
- Message roles enable prompt engineering patterns: use a `system` message for global instructions, few-shot examples
  to demonstrate format, and chain-of-thought cues like “Let’s think step by step”.

### Examples
```python
import openai
openai.api_key = "YOUR_API_KEY"

resp = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a medieval history expert."},
        {"role": "user", "content": "Explain the significance of the Magna Carta."}
    ],
    temperature=0.3,
    max_tokens=150
)
print(resp.choices[0].message.content)
```

```bash
curl https://api.openai.com/v1/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "text-davinci-003",
    "prompt": "Input: 2+2\nOutput: 4\n\nInput: 3+5\nOutput:",
    "max_tokens": 5,
    "temperature": 0
  }'
```

---

## 2. Images and Vision

### Examples
```python
from openai import OpenAI
client = OpenAI()

gen = client.images.generate(
    prompt="A futuristic city skyline at dusk", 
    n=2, 
    size="512x512"
)
for img in gen.data:
    print(img.url)
```

```bash
curl https://api.openai.com/v1/images/edits \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F image="@face.png" \
  -F mask="@mask.png" \
  -F prompt="Add round spectacles" \
  -F n=1 \
  -F size="256x256"
```

---

## 3. Audio and Speech

### Examples
```python
import openai

with open("interview.wav", "rb") as f:
    transcript = openai.Audio.transcribe("whisper-1", f)
print(transcript["text"])
```

```bash
curl https://api.openai.com/v1/audio/translations \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F file="@spanish_speech.mp3" \
  -F model="whisper-1"
```

---

## 4. Structured Outputs

### Examples
```python
from openai import OpenAI
import json

schema = {
  "type": "object",
  "properties": {
    "title": {"type": "string"},
    "year": {"type": "integer"}
  },
  "required": ["title","year"],
  "additionalProperties": False
}

resp = OpenAI().chat.completions.create(
  model="gpt-4",
  messages=[{"role":"user","content":"Give me details on Inception"}],
  functions=[{"name":"get_movie_info","parameters":schema}],
  function_call={"name":"get_movie_info"}
)
info = json.loads(resp.choices[0].message.function_call.arguments)
print(info)
```

---

## 5. Function Calling

### Examples
```python
import openai, json

functions = [{
  "name": "get_weather",
  "description": "Fetch current weather by city",
  "parameters": {
    "type": "object",
    "properties": {"city":{"type":"string"}},
    "required":["city"]
  }
}]

resp = openai.ChatCompletion.create(
  model="gpt-4",
  messages=[{"role":"user","content":"What's the weather in Tokyo?"}],
  functions=functions
)
args = json.loads(resp.choices[0].message.function_call.arguments)
print("Calling get_weather with", args)
```

```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model":"gpt-4",
    "messages":[{"role":"user","content":"Get me stock price for AAPL"}],
    "functions":[{"name":"get_stock","parameters":{/*...*/}}],
    "function_call":{"name":"get_stock"}
  }'
```

---

## 6. Conversation State

### Examples
```python
history = [
  {"role":"system","content":"You are a finance assistant."},
  {"role":"user","content":"Summarize Q1 earnings of Apple."}
]
history.append({"role":"user","content":"And what about Q2?"})
resp = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=history
)
print(resp.choices[0].message.content)
```

---

## 7. Streaming

### Examples
```python
import openai, sys
stream = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[{"role":"user","content":"Write a poem about sunsets."}],
  stream=True
)
for chunk in stream:
    sys.stdout.write(chunk.choices[0].delta.get("content",""))
```

---

## 8. File Inputs (PDFs and Vision)

### Core Concepts
- Models like `gpt-4-vision-preview` can directly process PDFs and images.
- Upload PDFs via the **Files API**, then pass them using `file_id` for multimodal processing.
- Files should be under 20MB and under 100 pages for optimal performance.

### Examples
```python
# Upload a PDF
pdf = openai.Files.create(file=open("report.pdf", "rb"), purpose="assistants")

# Use file in a vision model request
response = openai.ChatCompletion.create(
    model="gpt-4-vision-preview",
    messages=[
        {"role": "user", "content": [
            {"type": "text", "text": "Summarize the key findings from this document."},
            {"type": "file", "file_id": pdf.id}
        ]}
    ]
)
print(response.choices[0].message.content)
```

---

## 9. Reasoning

### Core Concepts
- Use **chain-of-thought prompting** (“Let's think step by step”) to improve accuracy in tasks requiring multi-step reasoning.
- Combine with **function calling** or **tool use** for exact answers (math, code execution, API results).
- Apply **self-verification prompts** to have the model critique or improve its own reasoning.

### Examples
```python
messages = [
    {"role": "user", "content": "What is the square root of 144, divided by 3? Think step by step."}
]
response = openai.ChatCompletion.create(
    model="o4",
    messages=messages,
    temperature=0
)
print(response.choices[0].message.content)
```

```python
# Self-verification
follow_up = [
    *messages,
    {"role": "assistant", "content": response.choices[0].message.content},
    {"role": "user", "content": "Can you verify and explain if this answer is correct?"}
]
check = openai.ChatCompletion.create(model="gpt-4", messages=follow_up)
print(check.choices[0].message.content)
```

---

## 10. Evals

### Core Concepts
- OpenAI **Evals framework** lets you define structured test cases (prompt + expected output) to benchmark models.
- Supports built-in eval templates or custom YAML tasks with accuracy, match, or embedding-based metrics.
- Integrate into CI/CD to catch regressions when switching models or modifying prompts.

### Examples
```bash
# Run an existing eval suite
openai evals run math:addition --model gpt-4 --record
```

```yaml
# yaml file: math_eval.yaml
id: math_eval
metrics: [accuracy]
tasks:
  - input: "What is 12 + 15?"
    ideal_output: "27"
```

```bash
# Run your custom suite
openai evals run math_eval --model gpt-4 --registry ./evals/registry --record
```
