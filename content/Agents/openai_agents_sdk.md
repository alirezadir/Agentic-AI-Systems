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

### Installation
Install the SDK via pip:
```bash
pip install openai-agents
```

### Hello World Example
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

### Example: Haiku Agent
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

### Context
Agents support dependency injection and shared state via context:
```python
from dataclasses import dataclass
from agents import Agent, RunContextWrapper

@dataclass
class UserContext:
    uid: str
    is_pro_user: bool

    async def fetch_purchases(self) -> list:
        ...

agent = Agent[UserContext](...)
```

#### Output Types
- Default output is plain `str`.
- Specify `output_type` (e.g., Pydantic models, dataclasses, TypedDict, lists) for structured outputs.

```python
from pydantic import BaseModel
from agents import Agent

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
Handoffs allow agents to delegate tasks to specialized sub-agents, enabling modular workflows.

```python
from agents import Agent

booking_agent = Agent(...)
refund_agent = Agent(...)

triage_agent = Agent(
    name="Triage agent",
    instructions=(
        "Help the user with their questions. "
        "If booking-related, hand off to booking_agent. "
        "If refund-related, hand off to refund_agent."
    ),
    handoffs=[booking_agent, refund_agent],
)
```

## 5. Guardrails
Run input/output validations alongside agents for safety and relevance using `@input_guardrail` and `@output_guardrail`.

### Input Guardrail Example
```python
@input_guardrail
async def guard_input(ctx, agent, user_input):
    return GuardrailFunctionOutput(output_info="ok", tripwire_triggered="math" in user_input)

agent = Agent(
    name="Support",
    instructions="Assist the user.",
    input_guardrails=[guard_input],
)
```

### Output Guardrail Example
```python
@output_guardrail
async def guard_output(ctx, agent, output):
    return GuardrailFunctionOutput(output_info=output, tripwire_triggered="badword" in output.text)

agent = Agent(
    name="Chat",
    instructions="Respond courteously.",
    output_guardrails=[guard_output],
    output_type=ResponseModel,
)
```

## 6. Running Agents
### The Agent Loop
Use the `Runner` class to execute agents:
1. `Runner.run()` (async): Returns `RunResult`.
2. `Runner.run_sync()` (sync wrapper): Returns `RunResult`.
3. `Runner.run_streamed()` (async streaming): Returns `RunResultStreaming`.

```python
from agents import Agent, Runner

async def main():
    agent = Agent(name="Assistant", instructions="You’re a concise assistant.")
    result = await Runner.run(agent, "Write a haiku about recursion.")
    print(result.final_output)
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

### Agent Patterns 
- [Agent Patterns Examples ](https://github.com/openai/openai-agents-python/tree/main/examples/agent_patterns)

### Multi-agent orchestration
- [tBa]

### Dynamic Instructions
- `instructions` can be a function (sync or async) receiving `(context, agent)` and returning a prompt string at runtime.

```python
from agents import Agent, RunContextWrapper

def dynamic_instructions(
    ctx: RunContextWrapper[UserContext], agent: Agent[UserContext]
) -> str:
    return f"User ID: {ctx.context.uid}. Tailor your response."

agent = Agent[UserContext](
    name="Dynamic agent",
    instructions=dynamic_instructions,
)
```

### Lifecycle Events (Hooks)
- Subclass AgentHooks to observe per-agent lifecycle events.
- Common AgentHooks methods:

    - **on_start**: Called before this agent is invoked.
    - **on_end**: Called after this agent produces final output.
    - **on_handoff**: Called when this agent receives a handoff.
    - **on_tool_start**: Called before invoking any tool.
    - **on_tool_end**: Called after a tool returns its result.

```python
from agents import Agent, AgentHooks

class LoggingHooks(AgentHooks):
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

### Tracing 
- [openAI Tracing documentation](https://openai.github.io/openai-agents-python/tracing/)
    -  automatically captures MCP operations
- External tracing: 
    - weights and biases
    - logfire 
    - langsmith
    - MLflow
    - etc.