
# OpenAI API QuickStart Guide (from Official Developer Docs)

This guide synthesizes the technical details and code examples from the official OpenAI API Guides across ten key areas:
Text and Prompting, Images and Vision, Audio and Speech, Structured Outputs, Function Calling, Conversation State,
Streaming, File Inputs, Reasoning, and Evals.

---

## 1. Text and Prompting
- **APIs Overview**: `Completions`, `Chat Completions`, `Responses`
  - **Completions API**: Original, stateless, accepts a single prompt string.
  - **Chat Completions API**: Uses a list of messages (`developer`, `user`, `assistant`) to maintain conversational context.
  - **Responses API**: Latest, stateful, supports tools like web search, file access, and multi-step reasoning.

- **Sampling Controls**: Adjust `temperature` (0–2) and `top_p` (0–1) for randomness vs coherence.
- Tips: 
  - Use **Message Roles**: (`system/developer` for global instructions.)
  - Add few-shot examples for format guidance.
  - Include chain-of-thought (CoT) cues like “Let’s think step by step.”
- Responses vs Chat Completions: 
  - responses: stateless, single input-output
    - input: `messages` (list of messages)
    - output content: ``choices[0].message.content``
  - chat completions: stateful, multi-turn conversations
    - input: `input` (list of messages)
    - output content: ``response.output_text``
### Examples
```python
from openai import OpenAI
client = OpenAI()
client.api_key = "YOUR_API_KEY"

resp = client.chat.completions.create(
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
```python 

response = client.responses.create(
  model="gpt-4.1",
  input=[
      {
          "role": "user",
          "content": "Write a one-sentence bedtime story about a unicorn."
      }
  ]
)

print(response.output_text)
```

- Read prompts from a file:
```python
with open("prompt.txt", "r") as f:
    prompt = f.read()
response = client.responses.create( 
  model="gpt-4.1",
  input=prompt
) 
```

<!-- ```bash
curl https://api.openai.com/v1/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "text-davinci-003",
    "prompt": "Input: 2+2\nOutput: 4\n\nInput: 3+5\nOutput:",
    "max_tokens": 5,
    "temperature": 0
  }'
``` -->

---

## 2. Images
- **Image Generation**: Use  DALL-E or GPT Image (`images` API, e.g. `gpt-image-1` model) for generating/Editing images from text prompts.
- **Image Analysis**: Use `Responses` / `chat completions` for analyzing images and extracting information.

**Examples**
- Image Generation
```python
gen = client.images.generate(
    model="gpt-image-1",
    prompt="A futuristic city skyline at dusk", 
    n=2, 
    size="512x512"
)
for img in gen.data:
    print(img.url)
```
- Image analysis (from url)

```python
response = client.responses.create(
    model="gpt-4.1-mini",
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "what's in this image?"},
            {
                "type": "input_image",
                "image_url": "https://example.com/image.png",
            },
        ],
    }],
)
print(response.output_text)
```
- Image analysis (from file): encode into base64
```python
import base64

with open("./image.png", "rb") as f:
    image_data = f.read()
    encoded_image = base64.b64encode(image_data).decode("utf-8")

response = client.responses.create(
    model="gpt-4.1-mini",
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "what's in this image?"},
            {
                "type": "input_image",
                "image_url": f"data:image/png;base64,{encoded_image}",
            },
        ],
    }],
)
```


## Structured Outputs
- Use JSON mode or Structured Outputs (e.g. json schema or a `BaseModel` subclass) to define structured outputs for:
  - response format 
  - function calling
- Response format: use `response_format` (chat completions) or ``text_format``(responses) 

**Examples:**
- example: JSON schema for response format
``` python
schema = {
  "type": "object",
  "properties": {
    "name": {"type": "string"},
    "year": {"type": "integer"}
  },
  "required": ["name","year"],
  "additionalProperties": False
}

response = client.beta.chat.completions.parse(
  model="gpt-4",
  messages=[{"role":"user","content":"Give me details on Inception movie"}],
  response_format: { type: "json_schema", json_schema: {"strict": true, "schema": schema} }
)
info = json.loads(response.choices[0].message.content)
print(info["name"], info["year"])
# or 
obj = response.choices[0].message.parsed
print(obj.name, obj.year)
```
- example: using Pydantic BaseModel
```python 
  from pydantic import BaseModel

  class CalendarEvent(BaseModel):
      name: str
      date: str
      participants: list[str]

  response = client.beta.chat.completions.parse(
      model="gpt-4o-2024-08-06",
      messages=[
          {"role": "system", "content": "Extract the event information."},
          {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."},
      ],
      text_format=CalendarEvent,
  )

  event = response.output_parsed
  ```
---

## 5. Function Calling
- Calling functions using `tools`
- Define function object **schema**, including:
  - `type=function`, `name`, `description`, and `parameters`.
    - `parameters` is a JSON schema object with `type`, `properties`, and `required` fields.
  - Example function schema:
    ```json
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "A short description of the function",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The location to ..",
                    },
                },
            },
            "required": ["location"],
        },
      ```
**Function Calling Steps:**

1. **Define Function Schema**: Create a schema for the function(s) with details such as `name`, `description`, and `parameters`.
2. **Call the Model with Tools**: Pass the function(s) as tools to the model. The model determines when to invoke the function based on the input.
    - **Function Call** in Response: The model's response includes a function call message with the function name and input arguments (e.g., `completion.choices[0].message.tool_calls`).
3. **Execute the Function**: Run the function code using the provided arguments.
4. **Append the Result** & Call model again: Send the function's output back to the model.
5. **Model Responds**: The model generates a final response incorporating the function's output.

**Tool choice:**
  - `auto`, `required`, `forced_function`

**Example**:
```python
  def get_weather(city: str) -> str:
    # dummy weather function
    # In practice, this would call an external API
      return f"The weather in {city} is sunny"

  # 1. Define the function schema in JSON format in the tools list
  tools = [{
      "type": "function",
      "name": "get_weather",
      "description": "Get current temperature for provided coordinates in celsius.",
      "parameters": {
          "type": "object",
          "properties": {
              "latitude": {"type": "number"},
              "longitude": {"type": "number"}
          },
          "required": ["latitude", "longitude"],
          "additionalProperties": False
      },
      "strict": True
  }]

  input_messages = [{"role": "user", "content": "What's the weather like in Paris today?"}]

  # 2. Call the model with the tools
  response = client.responses.create(
      model="gpt-4.1",
      input=input_messages,
      tools=tools,
  )

  # The model's response includes a function call message (with name and args)
  print(response.output)

  tool_call = response.output[0]
  args = json.loads(tool_call.arguments)
  print("Calling get_weather with", args)

  # 3. Execute the function
  result = get_weather(args["latitude"], args["longitude"])

  # 4. Append the result (function call message + result) message & call the model 
  input_messages.append(tool_call)  # append model's function call message
  input_messages.append({           # append result 
      "type": "function_call_output",
      "call_id": tool_call.call_id,
      "output": str(result)
  })

  response_2 = client.responses.create(
      model="gpt-4.1",
      input=input_messages,
      tools=tools,
  )
  print(response_2.output_text)
  "The current temperature in Paris is 14°C (57.2°F)."

  ```
- Handling multiple function calls:
  ```python
  for tool_call in response.output:
    if tool_call.type == "function_call":
      name = tool_call.name
      args = json.loads(tool_call.arguments)

      # Execute the function
      result = call_function(name, args)

      # Append the result back to the input messages
      input_messages.append({
        "type": "function_call_output",
        "call_id": tool_call.call_id,
        "output": str(result)
      })

    def call_function(name, args):
      if name == "get_weather":
          return get_weather(**args)
      if name == "send_email":
          return send_email(**args)
  ```


---

## 6. Conversation State
- Manual management of conversation state
  - Use `messages`  & append them manually to the  history.
    ```python
    history = [
      {"role":"system","content":"You are a finance assistant."},
      {"role":"user","content":"Summarize Q1 earnings of Apple."}
    ]
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=history
    )

    history.append({"role":"assistant","content":resp.choices[0].message.content})
    history.append({"role":"user","content":"And what about Q2?"})

    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=history
    )
    print(resp.choices[0].message.content)
    ```
- OpenAI APIs for conversation state
  - use `previous_response_id` parameter (only for `responses` API)
    ```python 

      response = client.responses.create(
          model="gpt-4o-mini",
          input="tell me a joke",
      )
      print(response.output_text)

      second_response = client.responses.create(
          model="gpt-4o-mini",
          previous_response_id=response.id, # use the previous response id 
          input=[{"role": "user", "content": "explain why this is funny."}],
      )
      print(second_response.output_text)
    ```


---

## 7. Streaming
- Use `stream=True` to receive partial responses in real-time.
- Each chunk has a `type` field indicating the content type.
  <!-- - `response.created`
  - `response.output_text.delta`
  - `response.completed`
  - `error` -->
### Examples
```python
stream = openai.responses.create(
  model="gpt-3.5-turbo",
  input=[{"role":"user","content":"Write a poem about sunsets."}],
  stream=True
)

response = ""
for chunk in stream:
    print(chunk.type)
    if chunk.type == "response.output_text.delta":
            response += chunk.delta
print(response)
```

---

## 8. File Inputs (PDFs and Vision)

- Models like `gpt-4-vision-preview` can directly process PDFs and images.
- Upload PDFs via the **Files API**, then pass them using `file_id = file.id` 
- Files should be under 20MB and under 100 pages for optimal performance.

### Examples

```python
# Upload a PDF using Files API
file = openai.Files.create(file=open("report.pdf", "rb"), purpose="assistants")

response = openai.ChatCompletion.create(
  model="gpt-4-vision-preview",
  messages=[
    {"role": "user", "content": [
      {"type": "text", 
      "text": "Summarize the key findings from this document."},
      {"type": "file", 
      "file_id": file.id} # use file_id
      # for responses API use: "type": "input_text" , "input_file"
    ]}
  ]
)
print(response.choices[0].message.content)
```

---

## 9. Reasoning

- Use **Reasoning models** (like o3 and o4-mini) for complex tasks:
  - e.g. complex problem solving, coding, scientific reasoning, and multi-step planning for agentic workflows
  - **Reasoning models** trained with RL to perform reasoning. They think before they answer.
  - Reasoning models introduce reasoning tokens in addition to input and output tokens.
- Combine with **function calling** or **tool use** for exact answers (math, code execution, API results).
<!-- - Apply **self-verification prompts** to have the model critique or improve its own reasoning. -->
- context window management: 
  - Use `max_completion_tokens parameter` parameter, check `completion_tokens_details`

### Examples
```python
messages = [
    {"role": "user", "content": "What is the square root of 144, divided by 3? Think step by step."}
]
response = client.responses.create(
    model="o4-mini",
    reasoning={"effort": "medium"}, # low, medium, high; use reasoning_effort="medium" in chat completions API
    messages=messages,
     max_output_tokens=300
)
print(response.status
print(response.output_text)
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
## OpenAI Built-in Tools 
### Web Search 

- Use the `web_search_preview` tool to fetch real-time information from the web.
- Specify user location for localized search results.

##### Example
```python
response = client.responses.create(
  model="gpt-4.1",
  tools=[{
    "type": "web_search_preview",
    "search_context_size": "low",
    "user_location": {
      "type": "approximate",
      "country": "GB",
      "city": "London",
      "region": "London",
    }
  }],
  input="What are the best restaurants around Granary Square?",
)

print(response.output_text)
```
## File Search
- Use the `file_search` tool to search for specific content in a list of `vector_stores` (of the files).
- supported file types: .pdf, .txt, .doc(x), .json, and coding files (.py, .js, .java, etc.).
- size limit: 512MB per file, 10k for total vector stores; project limit: 100GB all files

```python
response = client.responses.create(
  model="gpt-4o-mini",
  input="What is deep research by OpenAI?",
  tools=[{
    "type": "file_search",
    "vector_store_ids": ["<vector_store_id>"],
    "max_num_results": 2
  }]
)
print(response.output_text)
```
## computer use 
-  Computer-Using Agent (CUA) models (e.g. `computer_use_preview`)
- details here: [Computer use](https://platform.openai.com/docs/guides/tools-computer-use)
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
