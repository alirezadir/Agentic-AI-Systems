
# Agents SDK Overview

## Basic Configuration  
- `instructions`: Developer message or system prompt.  
- `model`: LLM choice and optional `model_settings` (e.g., temperature, top_p).  
- `tools`: List of function-decorated callables the agent can invoke.  

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

## Context
- Agents are generic on their context type for dependency injection and shared state, passed into every agent, tool, and handoff via Runner.run().  

```python
from dataclasses import dataclass
from agents import Agent, RunContextWrapper

@dataclass
class UserContext:
    uid: str
    is_pro_user: bool

    async def fetch_purchases(self) -> list[Purchase]:
        ...

agent = Agent[UserContext](...)
```

## Output Types
- Default output is plain str.
- Specify output_type (Pydantic models, dataclasses, TypedDict, lists, etc.) for structured outputs.

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

## Handoffs
- Sub-agents listed in handoffs let the main agent delegate specialized tasks, enabling modular workflows.

```python
from agents import Agent

booking_agent = Agent(...)
refund_agent  = Agent(...)

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

## Dynamic Instructions
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

## Lifecycle Events (Hooks)
- Subclass AgentHooks to observe per-agent lifecycle events.  
- Common AgentHooks methods:

| Method         | When Called                         |
|----------------|--------------------------------------|
| on_start       | Before this agent is invoked         |
| on_end         | After this agent produces final output |
| on_handoff     | When this agent receives a handoff   |
| on_tool_start  | Before invoking any tool             |
| on_tool_end    | After a tool returns its result      |

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

## Running Agents  
- Use the `Runner` class to execute agents:  
  1. `Runner.run()` (async → `RunResult`)  
  2. `Runner.run_sync()` (sync wrapper)  
  3. `Runner.run_streamed()` (async streaming → `RunResultStreaming`)  

```python
from agents import Agent, Runner

async def main():
    agent = Agent(name="Assistant", instructions="You’re concise.")
    result = await Runner.run(agent, "Write a haiku about recursion.")
    print(result.final_output)
```

## Tool Types
- **Hosted tools** (run on LLM servers): **WebSearchTool, FileSearchTool, ComputerTool**.
- **Function tools**: Any Python function via @function_tool, with auto-generated schema and doc parsing.
- **Agents as tools**: Turn an Agent into a tool via .as_tool() for multi-agent orchestration.

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

## Model Context Protocol (MCP)
- MCP standardizes how applications provide tools/context to LLMs (“USB-C port for AI”).
- Two server types: MCPServerStdio (local subprocess) and MCPServerSse (HTTP/SSE).

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


## Guardrails
- Run input/output validations alongside agents for safety and relevance.

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
## Forcing Tool Use  
- Control tool invocation via `ModelSettings.tool_choice`:  

| Value           | Behavior                                          |
|-----------------|---------------------------------------------------|
| `"auto"`        | Let the LLM decide whether to use a tool          |
| `"required"`    | Must call at least one tool                       |
| `"none"`        | No tool calls allowed                             |
| `"<tool_name>"` | Must call the named tool                          |

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
