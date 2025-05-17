# OpenAI's Agents Overview

This document provides an overview of OpenAI's Agents, based on the [official documentation](https://platform.openai.com/docs/guides/agents) and the [OpenAI Agents Python SDK](https://openai.github.io/openai-agents-python/).

## 1. Overview

### Agent Components
- **Models**: Handle reasoning, decision-making, and process various modalities.
- **Tools**: Extend agent capabilities using hosted tools, function tools, or other agents.
- **Knowledge and Memory**: Provide external or persistent knowledge to agents.
- **Audio and Speech**: Enable audio or speech-based interactions.
- **Guardrails**: Ensure safety and relevance through input/output validations.
- **Orchestration**: Manage workflows and task delegation across multiple agents.

### Agents SDK
The **Agents SDK** offers a minimal set of primitives:
- **Agents**: Models with instructions and tools for specific tasks.
    - Models: `o1`, `o3-mini`, `GPT-4.5`, `GPT-4o`, `GPT-4o-mini`.
    - Tools: `Function Calling`, `WebSearchTool`, `FileSearchTool`, `ComputerTool`.
    - Knowledge: `VectorStore`, `Semantic Search`, `Embedding`.
- **Handoffs**: Delegate tasks to specialized agents.
- **Guardrails**: Validate inputs and outputs for safety.
    - Includes a free Moderation API and instruction hierarchy for prompt prioritization.
- **Orchestration Tools**:
    - **Runner**: Executes agents and manages their lifecycle.
    - **Tracing**: Visualize and debug agent workflows.
    - **Evaluation**: Assess agent performance.
- **Other Components**:
    - Fine-tuning: `SFT`, `DPO`, `RLT`.
    - Model Context Protocol (MCP): Standardizes tool/context provisioning for LLMs.
    - Agent Hooks: Customize agent behavior at lifecycle stages.
    - [Voice Agents](https://platform.openai.com/docs/guides/voice-agents): Enable speech-to-speech or chained architectures.

- Install the SDK via pip:
```bash
pip install openai-agents
```

##### Hello World Example
```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)
```

## 2. Basic Agent Configuration

### Key Components
A basic agent consists of:
- **Instructions**: Developer-defined prompts.
- **Model**: LLM and optional settings (e.g., temperature).
- **Tools**: Callable functions or external tools.

##### Example: Haiku Agent
```python
from agents import Agent, function_tool

@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny"

agent = Agent(
    name="Haiku agent",
    instructions="Always respond in haiku form",
    model="o3-mini",
    tools=[get_weather],
)
```



#### Output Types
- Default output is plain `str`.
- Specify `output_type` (e.g., Pydantic models, dataclasses, TypedDict, lists) for structured outputs.

```python
from pydantic import BaseModel

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

agent = Agent(
    name="Calendar extractor",
    instructions="Extract calendar events from text",
    output_type=CalendarEvent,
)
```

## 3. Models 
- Built-in models: 
    - Text models (generation, reasoning), 
    - Image models (generation, analysis), 
    - Audio models (tts, transcribe, whisper, real-time) 
    - `o1`, `o3-mini`, `GPT-4.5`, `GPT-4o`, `GPT-4o-mini`, etc 
    -  Just pass the model name to the agent `model`. Internally uses `OpenAIResponsesModel` or `OpenAIChatCompletionsModel`.
    - List and pricing of models [here](https://platform.openai.com/docs/pricing#other-models)
- Custom models: 
    - Using littlellm 
    ```python
        # We prefix with litellm/ to tell the Runner to use the LitellmModel    
        Agent(... model="litellm/anthropic/claude-3-5-sonnet-20240620", ...)
        # or 
        model_name = "anthropic/claude-3-5-sonnet-20240620"
        Agent( ... model=LitellmModel(model=model_name, api_key=api_key) , ...)
    ```
    or
    - Global: using ``AsyncOpenAI`` as client and `OpenAIChatCompletionsModel` as model
    ```python
        client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)
        model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client)
    ```
    - `Runner.run` level: using `ModelProvider`: `run_config=RunConfig(model_provider=CUSTOM_MODEL_PROVIDER)`
    - Agent level: using `Agent.model`
    - examples [here](https://github.com/openai/openai-agents-python/tree/main/examples/model_providers)
## 3. Tools
### Tool Types
- **Hosted tools**: Run on LLM servers (e.g., `WebSearchTool`, `FileSearchTool`, `ComputerTool`).
- **Function tools**: Python functions decorated with `@function_tool` for schema generation and doc parsing.
- **Agents as tools**: Convert an agent into a tool using `.as_tool()` for multi-agent orchestration.

```python
from agents import Agent, WebSearchTool, FileSearchTool

agent = Agent(
    name="Locator",
    tools=[
        WebSearchTool(),
        FileSearchTool(max_num_results=2, vector_store_ids=["VEC_ID"]),
    ],
)
```

### Function Tools
- Use the `@function_tool` decorator to create function tools.
- Functions can be sync or async and accept Python types as arguments.

```python
from agents import Agent, function_tool

@function_tool
async def get_weather(city: str) -> str:
    """
    Fetch the weather for a given location.

    Args:
        city: The city to fetch the weather for.
    """
    return f"The weather in {city} is sunny."

agent = Agent(
    name="Hello world",
    instructions="You are a helpful agent.",
    tools=[get_weather],
)
```

#### Tool Use Options
Control tool invocation via `ModelSettings.tool_choice`:
- `"auto"`: Let the LLM decide whether to use a tool.
- `"required"`: Must call at least one tool.
- `"none"`: No tool calls allowed.
- `"<tool_name>"`: Must call the named tool.

```python
from agents import Agent, function_tool, ModelSettings

@function_tool
def get_news(topic: str) -> str:
    return fetch_latest_news(topic)

agent = Agent(
    name="NewsBot",
    instructions="Fetch the latest news on a topic.",
    tools=[get_news],
    model_settings=ModelSettings(tool_choice="required"),
)
agent.tool_use_behavior = "stop_on_first_tool"
```

### Agents as Tools
Use `.as_tool()` to turn an agent into a tool for multi-agent orchestration.

```python
spanish_agent = Agent(...)
french_agent = Agent(...)

orchestrator_agent = Agent(
    name="Orchestrator",
    instructions="Translate messages using the appropriate tools.",
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message to Spanish",
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate the user's message to French",
        ),
    ],
)
async def main():
    result = await Runner.run(orchestrator_agent, input="Say 'Hello, how are you?' in Spanish.")
```

## 4. Handoffs
- Handoffs allow agents to delegate tasks to other agents (e.g.specialized sub-agents), enabling modular workflows.
- Handoffs are defined in the agent's `handoffs` property.
- Can take an `agent` directly, or a Handoff object (e.g. `Handoff(agent, input_guardrails=...)`)



```python
from agents import Agent

billing_agent = Agent(name="Billing agent", instructions="...")
refund_agent = Agent(name="Refund agent", instructions="...")

triage_agent = Agent(
    name="Triage agent",
    instructions=(
        "... "
        "If billing-related, hand off to billing_agent. "
        "If refund-related, hand off to refund_agent."
    ),
    handoffs=[billing_agent, handoff(refund_agent)],
)
```
-  Customizing handoffs using the `handoff()` function
    ```python
    from agents import handoff

    def on_handoff(agent, ctx):
        print(f"Handing off to {agent.name}")

    handoffs = [handoff(agent=refund_agent, on_handoff=on_handoff(agent, ctx))]
    ```



## 5. Running Agents
### The Agent Loop
Use the `Runner` class to execute agents:
1. `Runner.run()` (async): Returns `RunResult`.
2. `Runner.run_sync()` (sync wrapper): Returns `RunResult`.
3. `Runner.run_streamed()` (async streaming): Returns `RunResultStreaming`.
- Parameters:
    - `starting_agent`: starting agent (required)
    - `input`:  input to the agent (required)
    - `context`
    - `run_config`
    - `hooks`
    - `previous_response_id` 
#### Example: Basic Run
```python
from agents import Agent, Runner
import asyncio

async def main():
    agent = Agent(name="Assistant", instructions="You're a concise assistant.")
    result = await Runner.run(agent, "Write a haiku about recursion.")
    print(result.final_output)
```
### Example: streamed Run
```python
    async def main():
        agent = Agent(...)
        result = Runner.run_streamed(agent, input="Please tell me 5 jokes.")

        async for event in result.stream_events():
            if event.item.type == "message_output_item":
                print(ItemHelpers.text_message_output(event.item))

    asyncio.run(main())
```
- `stream_events()` types: 
    - tool_call_output_item
    - tool_call_item
    - message_output_item

#### Run Config
- Global settings for the agent run:
    - `model`, `model_provider`
    - `model_settings` (e.g. temperature, top_p, etc)
    - `tracing_disabled`, `trace_metadata`, etc
    - `input_guardrails`, `output_guardrails`
    - `workflow_name, trace_id, group_id`:
```python
    from agents.run import RunConfig

    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )
    
    agent: Agent = Agent(name="Assistant", instructions=...)
    result = Runner.run_sync(agent, "Hello, how are you.", run_config=config)
```
### Multi-turn Conversation
Each run represents a single logical turn in a conversation. Use `RunResult.to_input_list()` for the next turn.

```python
async def main():
    agent = Agent(name="Assistant", instructions="Reply very concisely.")

    # First turn
    result = await Runner.run(agent, "What city is the Golden Gate Bridge in?")
    print(result.final_output)  # San Francisco

    # Second turn
    new_input = result.to_input_list() + [{"role": "user", "content": "What state is it in?"}]
    result = await Runner.run(agent, new_input)
    print(result.final_output)  # California
```
## 6. Guardrails
Run input/output validations alongside agents for safety and relevance using `@input_guardrail` and `@output_guardrail`.
- Input guardrails: run on the initial user input
- Output guardrails: run on the final agent output
- Guardrails run in 3 steps:
    - guardrail receives the same input passed to the agent.
    - guardrail function runs to produce a `GuardrailFunctionOutput`.
    - check if `.tripwire_triggered` is true. If true, an `InputGuardrailTripwireTriggered` exception is raised

### Input Guardrail Example
```python
@input_guardrail
async def guard_input(ctx, agent, user_input):
    # typically Runner.run(guardrail_agent, user_input, ctx)
    return GuardrailFunctionOutput(output_info="ok", tripwire_triggered="math" in user_input)

agent = Agent(
    name="Support",
    instructions="Assist the user.",
    input_guardrails=[guard_input],
)

async def main():
    # This should trip the guardrail
    try:
        await Runner.run(agent, "can you solve my math homework?")

    except InputGuardrailTripwireTriggered:
        print("Math homework guardrail tripped")
```

### Output Guardrail Example
```python
@output_guardrail
async def guard_output(ctx, agent, output):
    # typically Runner.run(guardrail_agent, output.response, ctx.context)
    return GuardrailFunctionOutput(output_info=output, tripwire_triggered="badword" in output.text)

agent = Agent(
    name="Chat",
    instructions="Respond courteously.",
    output_guardrails=[guard_output],
    output_type=ResponseModel,
)
async def main():
    # This should trip the guardrail
    try:
        await Runner.run(agent, "Hello, can you help me with *badword*?")

    except OutputGuardrailTripwireTriggered:
        print("Badword output guardrail tripped")
```

## 7. Other Features
### Model Context Protocol (MCP)
MCP standardizes how applications provide tools/context to LLMs.

```python
from agents import Agent
from agents.mcp import MCPServerStdio

async with MCPServerStdio(params={
    "command": "npx",
    "args": ["@modelcontextprotocol/server-filesystem", "samples"],
}) as server:
    agent = Agent(
        name="MCP Agent",
        instructions="Use MCP tools to complete tasks",
        mcp_servers=[server],
    )
```
### Context
Agents support dependency injection and shared state via context:
- Local context: 
    - via context wrapper (`wrapper: RunContextWrapper[TContext]`) and the `wrapper.context` property
- Global context:
    - Agent instructions ("`system/developer`" prompt).
    - `input` when calling the Runner.run
    - Expose it via function tools
    - retrieval or web search
```python

from dataclasses import dataclass
from agents import Agent, RunContextWrapper, Runner, function_tool

# A simple context object (using a dataclass)
@dataclass
class UserInfo:  
    name: str
    uid: int

# Tool: takes context wrapper: RunContextWrapper[UserInfo]
# reads context via: wrapper.context
@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:  
    return f"User {wrapper.context.name} is 47 years old"

async def main():
    # Create your context object
    user_info = UserInfo(name="John", uid=123)  

    # pass the context type to the Agent constructor (type check)
    agent = Agent[UserInfo](  
        name="Assistant",
        tools=[fetch_user_age],
    )

    # Passing the local context to the Runner
    result = await Runner.run(
        starting_agent=agent,
        input="What is the age of the user?",
        context=user_info,
    )

    print(result.final_output) 
    # The user John is 47 years old.

if __name__ == "__main__":
    asyncio.run(main())

agent = Agent[UserContext](...)
```
### Tracing 
- **Agents Tracing**: to monitor and debug agentic workflow execution, including:  
    - **logging**: fcn_calls, input/output, decisions, etc
    - **visualization**: workflow, performance
    - **debugging & error tracking**
    - **workflow & performance monitoring**
    - **agent interactions**
    - (Also automatically captures MCP operations)
- **Traces** vs Spans:  
    - Trace: single end-to-end operation of a "workflow". The entire `Runner.run()` is wrapped in a trace.
    - Span: operations with a start and end time: `agent_span(), generation_span(), fucntion_span(), guardrail_span()`, etc.
- Enabling Tracing: tracing is enabled by default. 
    - to disbale: `tracing_disabled=True` in `RunConfig`
- Default Tracing: 
    - default trace is named "`Agent trace`"
- [OpenAI Traces Dashboard](https://platform.openai.com/traces)
- Higher level Tracing 
    - multiple run() calls in a single trace
        - include different runs in `with trace("workflow_name")`: 
    ```python
    from agents import Agent, Runner, trace

    async def main():
        agent = Agent(name="Joke generator", instructions="Tell funny jokes.")

    with trace("Joke workflow"): 
        first_result = await Runner.run(agent, "Tell me a joke")
        second_result = await Runner.run(agent, f"Rate this joke: {first_result.final_output}")
        print(f"Joke: {first_result.final_output}")
        print(f"Rating: {second_result.final_output}")
    ```
- **Tracing Processors**: 
    - Open AI Tracing Processors: 
        ```python
        # Set up the custom trace processor
        local_processor = LocalTraceProcessor()
        set_trace_processors([local_processor])
        ```
    - External tracing processors: 
        - Weights & biases, logfire, braintrust, agentops, langsmith, MLflow, etc.
        - Example: 
            ```python
            class AgentLogEntry(BaseModel):
                agent_name: str, 
                ...
            log_entry = AgentLogEntry(...)
            with trace("workflow_name"):
                # do some work 
                # ...
                # Log the entry
                await logfire.log(log_entry)
                # Log metrics 
                # agentops
                agentops.log_metric("code_complexity", "low")
                # keywords_ai
                keywords_ai.log_metric("keyword_count", 10)
                # scorecard
                scorecard.log_metric("quality_score", evaluation.quality_score)
                # ...
            
                ```

src: [openAI Tracing documentation](https://openai.github.io/openai-agents-python/tracing/)

### Lifecycle Events (Hooks)
- Subclass AgentHooks to observe per-agent lifecycle events.
    - **Run-Level Lifecycle** (`RunHooks`)
    - **Agent-Level Lifecycle** (`AgentHooks`)
- Common `AgentHooks` methods:
    - **on_start**: Called before this agent is invoked.
    - **on_end**: Called after this agent produces final output.
    - **on_handoff**: Called when this agent receives a handoff.
    - **on_tool_start**: Called before invoking any tool.
    - **on_tool_end**: Called after a tool returns its result.
- `RunHooks`: are similarly defined `(on_agent_start, on_agent_end, on_handoff, on_tool_start, on_tool_end)`

    ```python
    from agents import Agent, AgentHooks

    class LoggingHooks(AgentHooks):

        async def on_agent_start(self, context: RunContextWrapper, agent: Agent) -> None:
            print(f"Agent {agent.name} started.")

        async def on_tool_start(self, context, agent, tool):
            print(f"Invoking tool: {tool.name}")

        async def on_tool_end(self, context, agent, tool, result):
            print(f"Tool {tool.name} returned: {result}")

    agent = Agent(
        name="Logger",
        instructions="Do something",
        hooks=LoggingHooks(),
    )
    ```

### Agent Patterns 
- [Agent Patterns Examples ](https://github.com/openai/openai-agents-python/tree/main/examples/agent_patterns)
    - agents_as_tools
    - deterministic
    - forcing_tool_use
    - input_guardrails
    - llm_as_a_judge
    - output_guardrails
    - parallelization   
    - routing

### Multi-agent orchestration
- Orchestrating via LLM: 
    - [Orchestrating via LLM](https://github.com/openai/openai-agents-python/tree/main/examples/agent_patterns/orchestration)
- Orchestrating via code: 
    - [Orchestrating via code](https://github.com/openai/openai-agents-python/tree/main/examples/agent_patterns/orchestration)

### Voice Agents
- [Voice Agents](https://openai.github.io/openai-agents-python/voice/)
- Main concept is a "Voice Pipeline", including 3 stages (chained):  
    - `TTS [audio -> text] -> agent -> [text -> audio] STT`
    - `VoicePipeline` is a wrapper around the 3 stages.
- Install: 
    - `pip install openai-agents[voice]`
- Example: 
    - [Voice Agents Example](https://github.com/openai/openai-agents-python/tree/main/examples/voice)
    ```python
    from agents.voice import AudioInput, VoicePipeline, SingleAgentVoiceWorkflow
    
    # create an agent
    agent = Agent(name="Assistant", instructions="You're a helpful assistant.")

    async def main():
        # set the VoicePipeline with the workflow (SingleAgentVoiceWorkflow)
        pipeline = VoicePipeline(workflow=SingleAgentVoiceWorkflow(agent))
        # create an audio input buffer
        buffer = np.zeros(24000 * 3, dtype=np.int16)
        audio_input = AudioInput(buffer=buffer)
        
        # run the pipeline
        result = await pipeline.run(audio_input)

        # Create an audio player using `sounddevice`
        player = sd.OutputStream(samplerate=24000, channels=1, dtype=np.int16)
        player.start()
        ```


## 8. Advanced topics 
### Other types of Memory 
- **Types of Memory** in Agentic Frameworks: 
    - Short Term  Memory (STM)  
        - **Working Memory** 
        - **Cache Memory**
    - [Long Term Memory (LTM)](https://langchain-ai.github.io/langmem/concepts/conceptual_guide/)
        - Episodic Memory (EM): Past Experiences & interactions e.g. summaries of past conversations
        - Semantic Memory: Facts & Knowledge e.g. User preferences, Paris <> France
        - Procedural Memory: Learned tasks, System Behavior  e.g. personality and response patterns
        <!-- - Conceptual Memory (CM) -->
- **External Long Term Memory Tools**:
    - Persistent memory stores (e.g. vector stores, databases)
    - [LangMem](https://blog.langchain.dev/langmem-sdk-launch/) (LangChain SDK for LTM): 
        - LangGraph LTM [Course](https://www.deeplearning.ai/short-courses/long-term-agentic-memory-with-langgraph/)
    - [Letta](https://github.com/letta-ai/letta) (MemGPT)
    - [Zep](https://github.com/getzep/graphiti) graph-base memory Grafiti
    - [Pinecone](https://www.pinecone.io/learn/agentic-memory/)
    - [Pinecone](https://www.pinecone.io/learn/agentic-memory/)
- Sources: 
    - [Different types of memories in agentic framework](https://www.linkedin.com/pulse/different-types-memories-agentic-framework-gourav-g--shdxc/)
    - [AI Agent Memory Types Simplified](https://www.linkedin.com/posts/rakeshgohel01_these-explanations-will-clarify-your-ai-agent-activity-7313175951243190273-hZl_/)

### Dynamic Instructions
- `instructions` can be a function (sync or async) receiving `(context, agent)` and returning a prompt string at runtime.

    ```python

    def dynamic_instructions(ctx, agent) -> str:
        return f"User ID: {ctx.context.uid}. Tailor your response."

    agent = Agent(
        name="Dynamic agent",
        instructions=dynamic_instructions,
    )
    ```

<!-- ### Payment Tools 
- [stripe for agents SDK](https://docs.stripe.com/agents) -->