## 1. Agents Intro 
### 1.1 What is an agent?
- Agent: AI model capable of **reasoning**, **planning**, and **interacting** with its environment, in order to achieve a user-defined objective. 
- **request -> think and plan -> act (using tools)**
- combines **reasoning**, **planning**, and the execution of **actions** (often via external **tools**)
- spectrum of increasing agency: 
    - Simple processor (no impact on program flow)
    - Router (basic control flow)
    - Tool Caller (fcn execution)
    - Multi-step agent ( controls iteration and program continuation)
    - Multi-agent (agentic workflow can start another agentic workflow)
- Agent perform tasks via Tools to perform actions 
    - actions can involve one / multiple tools 
    - e.g. tools `send_message_to(recipient, message)`, `web_search(input)`
- Example: Customer Service Chatbots
    - answer questions, 
    - guide through troubleshooting steps, 
    - open issues in internal databases, 
    - complete transactions.
    - Objectives: improving user satisfaction, reducing wait times, or increasing sales conversion rate
### 1.2 LLMs
- agents' brain: AI models (LLMs), bodies (Tools)
- LLMs: predict the next token, given a sequence of previous tokens.
- token: unit of info (word, sub-word) + special characters (e.g. EOS)
- next token prediction: autoregressive; 
    - decode text until it predicts the EOS
- 3 types of transformers: 
    - Encoders: Encode to embeddings (millions of params); e.g. BERT
    - Decoders: Generate text; Billions of params: LLMs: e.g. Llama/ GPT-3 
    - Encoder-decoders: (seq-to-seq); e.g. T5
- decoding: token w/ max score or *beam search*: explore multiple candidate sequences;find the one with the maximum total score
- attention: identifying the most relevant words ->  attention span -> context length
- LLMs training:  self-supervised (masked language modeling objective)
### Messages 
- Agens' user interface: chat interface: 
    - exchange of **messages** (concatenated and formatted into a specific prompt
- System messages: persistent instructions;  how the model should behave; info on tools, actions, thought process; User messages, 
- Conversations: User and Assistant Messages
- Chat Templates: messages <-> specific formatting +  handle  multi-turn conversations while maintaining context (chat history)
    - prevoius messages + special tokens concatenated to each message 
    - message exchanges -> into a single prompt
    - use the chat_template from the model’s tokenizer (`tokenizer.apply_chat_template`)
- ChatML format: list of JSON messages `[{"role": "system", "content": "..."}, ...]`
- ChatML to chat Template format: 
    ```
    [
    {"role": "system", "content": "You are a helpful chatbot."},
    {"role": "user", "content": "Hi there!"},
    {"role": "assistant", "content": "Hello, human!"},
    ]
    ```
    -> formatted 
    ```
    <|begin_of_text|><|start_header_id|>system<|end_header_id|>

    You are a helpful chatbot.<|eot_id|><|start_header_id|>user<|end_header_id|>

    Hi there!<|eot_id|><|start_header_id|>assistant<|end_header_id|>

    Hello, human!<|eot_id|>
    ```
### 1.3 Tools 
- Actions executed via Tools 
- Tool: a callabale fucntion, w/ a clear objective 
- Tool should include: 
    - textual description, 
    - callable, 
    - arguments & their types
- Example tools: Web Search, Image Generation, Retrieval, external API (youtube, github, etc)
- How tools work?
    - LLMs only receive text inputs and generate text outputs
    - LLMs generate text that represents a tool call, e.g. `call weather_tool(‘Paris’).`
    - Tool calling by Agent:  reads response, identifies tool call is required, executes the tool, and retrieves the actual data.
    - Tools given to LLMs via system prompt description of avaiable tools 
    - Tool's textual description includes: 
        - Tool name: , Descrition: , Arguments (with typings) , Outputs
    - Auto-formatting Tools
        - in python, using `@tool` decorator before function 
        ```python 
        @tool
        def calculator(a: int, b: int) -> int:
            """Multiply two integers."""
            return a * b

        print(calculator.to_string())
        ```
        - `to_string()` output:
        `Tool Name: calculator, Description: Multiply two integers., Arguments: a: int, b: int, Outputs: int`
    - Generic Tool implementation
        ```python 
        class Tool:
        def __init__(self, ...):
            self.name = ... 
            self.description= 
            self.func 
            self.arguments 
            self.outputs   
        def to_string(self) -> str:
            ...
        def __call__(self, *args, **kwargs):
            ...      
        ```
### 1.4  AI Agent Workflow
- Agents work in a continuous cycle of: thinking (**Thought**) → acting (**Act**) → observing (**Observe**)
    - thought: decide next step 
    - act: take action (call tools w/ arguments)
    - observe: reflect on output 
- **Thought-Action-Observation Cycle**: 
    - a while loop: until the objective fulfilled.
    - example:
        - Query: "`What’s the current weather in New York?`"?
        - Thought: `The user needs current weather info for New York. I have access to a tool that fetches weather data. First, I need to call the weather API to get up-to-date details. `
        - Action: JSON-formatted command that calls the weather API tool:
            ```
            {
            "action": "get_weather",
            "action_input": {
            "location": "New York"
                }
            }
             ``` 
        - Observation: `Current weather in New York: partly cloudy, 15°C, 60% humidity.`
        - Thought (reflection): `“Now that I have the weather data for New York, I can compile an answer for the user.”`
        - Action (final): `The current weather in New York is partly cloudy with a temperature of 15°C and 60% humidity` 
- **1.4.1 Thoughts (Reasoning) & ReAct**
    - **Thoughts**: Agent’s internal reasoning and planning processes
    - Types of Thoughts: 
        - Analysis: e.g. intent classification 
        - planning: breaking task into multiple steps 
        - decision making: e.g. recommendation 
        - memory integration: e.g. using chat context 
        - self-reflection: e.g. if the strategy worked
        - goal setting 
        - Prioritization: e.g. security before new feature 
    - **ReAct** = Reason (Think) + Act 
        - ReAct is a prompting technique 
        - appends `“Let’s think step by step”` (CoT) 
        - encourages the model to generate a plan (decompose the problem into sub-tasks)
        - some models fine-tuned to "think before answering": e.g. Deepseek R1 or OpenAI's o1
            - trained to always include specific thinking sections `<think> ... </think>`

- **1.4.2 Action**
    - **Actions**:  to interact with its environment (web, DB, physical)
    - **Action Types**: 
        - Information Retrieval: e.g. web search, DB query, document retrieval
        - Tool  Execution: e.g. API call, function execution
        - Environment Interaction: e.g. digital interface or physical device
        - communication: e.g. chat with user, message othe agents 
    - Agent types (based on actions): 
        - Tool-calling agents 
        - JSON agents: uses JSON to format the action
        - Code agents: writes code 
            - JSON agents: The Stop and Parse Approach: 
                - LLMs generate a JSON-formatted action
                - Agent stops execution
                - Agent parses the JSON to extract the action and its arguments
                - Agent executes the action and retrieves the result
                    ```
                        {
                        "action": "get_weather",
                        "action_input": {
                            "location": "New York"
                        }
                    ```
            - Code agents: 
                - LLMs generate code snippets
                - Agent executes the code & retrieves the result
                - pros: Expressiveness, modularity, and reusability
                - Example: 
                    ```python
                    def get_weather(location):
                        # Call weather API
                        return weather_data
                    ```

- **1.4.3 Observe: Reflect & Adapt**
    -   **Observation**: Agent’s perception on the results of its actions
    -   **Reflection**: Agent’s ability to analyze the outcome of its actions
    -   **Adaptation**: Agent’s ability to adjust its strategy based on observations
    - **observation** phase: 
        - **collect** feedback from the environment
        - **analyze** the results / make decisions (success/failure, next action)
        - **append** the observation to the chat history
    - Types of Observations: 
        - system feedback: e.g. success/failure
        - user feedback: e.g. user rating
        - environment feedback: e.g. API response
        - self-reflection: e.g. if the strategy worked
        - analysis of the results
## 2. Agentic Frameworks
-  **Agentic frameworks**:  provide a set of tools, libraries, and practices for building agents
- not always needed when building an application with LLMs
- when not to ise them?
    - simple applications with a single tool
    - agents that require simple workflows (e.g. chain of prompts)
    - using a single agent
- when to use them?
    - complex applications that require multiple tools
    - agents that require complex workflows
    - using multiple agents 
- Agentic Frameworks Examples: 
    - **langgraph**
    - **llama_index**
    - **smolagents**: focuses on codeAgent (performs “Actions” through code blocks, and then “Observes” results by executing the code.)
    - openai's agents 
- Components of Agentic Frameworks: 
    - An *LLM* engine 
    - A list of *tools*
    - A *parser* for extracting tool calls from the LLM output.
    - A *system prompt* synced with the parser.
    - A *memory system*.
    - *Error logging and retry* mechanisms to control LLM mistakes