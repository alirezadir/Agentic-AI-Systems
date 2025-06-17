
## LlamaIndex FunctionAgent / AgentWorkflow Basic Introduction

- **AgentWorkflow** is an orchestrator for running a system of one or more agents. 
    - we use a simple workflow with a single FunctionAgent 

- **FunctionAgent**: a lightweight agent in LlamaIndex with LLM and a set of tools


### Setup

#### Set up LLM

* Utilizes OpenAI's `gpt-4o-mini` model

```python
from llama_index.llms.openai import OpenAI

llm = OpenAI(model="gpt-4o-mini", api_key="sk-...")
```

#### Define tool

* Defines an async web search tool using Tavily

```python
from tavily import AsyncTavilyClient

async def search_web(query: str) -> str:
    """Useful for using the web to answer questions."""
    client = AsyncTavilyClient(api_key="tvly-...")
    return str(await client.search(query))
```

#### Create agent

* Instantiates a `FunctionAgent` with the defined tool and LLM

```python
from llama_index.core.agent.workflow import FunctionAgent

agent = FunctionAgent(
    tools=[search_web],
    llm=llm,
    system_prompt="You are a helpful assistant that can search the web for information."
)
```

### Running the Agent

* Executes the agent with a user message

```python
response = await agent.run(user_msg="What is the weather in San Francisco?")
print(str(response))
```

* Wraps the agent in an `AgentWorkflow` for execution

```python
from llama_index.core.agent.workflow import AgentWorkflow

workflow = AgentWorkflow(agents=[agent])
response = await workflow.run(user_msg="What is the weather in San Francisco?")
```

* The `AgentWorkflow` is an orchestrator for running a system of one or more agents. In this example, we create a simple workflow with a single `FunctionAgent`, and use it to cover basic functionality.

### Maintaining State

* Uses `Context` to preserve state across agent runs

```python
from llama_index.core.workflow import Context

ctx = Context(agent)
```

<!-- * Runs the agent with context to maintain conversation history

```python
response = await agent.run(user_msg="My name is Logan, nice to meet you!", ctx=ctx)
print(str(response))

response = await agent.run(user_msg="What is my name?", ctx=ctx)
print(str(response))
```

* Serializes and deserializes context using `JsonSerializer` or `JsonPickleSerializer`

```python
from llama_index.core.workflow import JsonPickleSerializer, JsonSerializer

ctx_dict = ctx.to_dict(serializer=JsonSerializer())
restored_ctx = Context.from_dict(agent, ctx_dict, serializer=JsonSerializer())
``` -->

* Allows saving and loading context from storage

```python
response = await agent.run(user_msg="Do you still remember my name?", ctx=restored_ctx)
print(str(response))
```

### Streaming

* `AgentWorkflow` and `FunctionAgent` support streaming responses
* Streaming handled via event handlers returned from the workflow
* To stream only the LLM output, use `AgentStream` events

```python
from llama_index.core.agent.workflow import AgentStream

async for event in workflow.stream(user_msg="Tell me a joke"):
    if isinstance(event, AgentStream):
        print(event.output)
```

### Tools and State

* Provide clear names and docstrings for tools
* Annotate input/output types for tools
* Implement tools asynchronously for efficiency

### Human in the Loop

* Supports human feedback/intervention using callback events

```python
from llama_index.core.agent.callback import BaseAgentCallback

class HumanApprovalCallback(BaseAgentCallback):
    async def on_tool_start(self, tool_name, input):
        print(f"About to run tool: {tool_name} with input: {input}")
        approval = input("Do you want to continue? (y/n): ")
        if approval.lower() != 'y':
            raise Exception("Tool execution cancelled by human.")

agent_with_callback = FunctionAgent(
    tools=[search_web],
    llm=llm,
    system_prompt="You are a helpful assistant that can search the web for information.",
    callbacks=[HumanApprovalCallback()]
)

response = await agent_with_callback.run(user_msg="Search the current news")
print(response)
```

## Best Practices

* Provide clear names and docstrings for tools
* Annotate input and output types for tools
* Implement tools asynchronously to enhance workflow efficiency
* Use Context to maintain state and history across agent interactions
* Serialize context using `JsonSerializer` or `JsonPickleSerializer` for persistence
