
## LlamaIndex FunctionAgent / AgentWorkflow Basic Introduction

- **AgentWorkflow**: is an orchestrator for running a system of one or more agents. 
- **FunctionAgent**: a lightweight agent in LlamaIndex with LLM and a set of tools
- we use a simple workflow with a single FunctionAgent.
- we use `llama_index.core.workflow`
- Full code example: [agent-workflow.py](./code/agent-workflow.py)
    

### Agent Setup

#### LLM Model

* Utilizes OpenAI's `gpt-4o-mini` model

```python
from llama_index.llms.openai import OpenAI

llm = OpenAI(model="gpt-4o-mini", api_key="sk-...")
```

#### Define tool

* Defines an async web search tool using Tavily

```python
from tavily import AsyncTavilyClient

# async function tool
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

* Run a single agent with a user message (`agent.run`)

```python
user_msg = "What is the weather in San Francisco?"
response = await agent.run(user_msg=user_msg) # async
print(str(response))
```
or, 
* Wrap the agent in an `AgentWorkflow` with a single `FunctionAgent` (`workflow.run`)

```python
from llama_index.core.agent.workflow import AgentWorkflow

workflow = AgentWorkflow(agents=[agent])
user_msg = "What is the weather in San Francisco?"
response = await workflow.run(user_msg=user_msg) # async
```

* The `AgentWorkflow` is an orchestrator for running a system of one or more agents. In this example, we create a simple workflow with a single `FunctionAgent`, and use it to cover basic functionality.

### Maintaining State

* Uses `Context` to preserve state across agent runs

```python
from llama_index.core.workflow import Context

ctx = Context(agent)
```
 * Runs the agent with context to maintain conversation history

```python
response = await agent.run(user_msg="My name is Logan, nice to meet you!", ctx=ctx)
print(str(response))

response = await agent.run(user_msg="What is my name?", ctx=ctx)
print(str(response))
```
<!--
* Serializes and deserializes context using `JsonSerializer` or `JsonPickleSerializer`

```python
from llama_index.core.workflow import JsonPickleSerializer, JsonSerializer

ctx_dict = ctx.to_dict(serializer=JsonSerializer())
restored_ctx = Context.from_dict(agent, ctx_dict, serializer=JsonSerializer())
``` -->

* Allows saving and loading context from storage, using `JsonSerializer`

```python
restored_ctx = Context.from_dict(agent, ctx_dict, serializer=JsonSerializer()) # context is a serialized dict

response = await agent.run(user_msg="Do you still remember my name?", ctx=restored_ctx)
```

### Streaming

* workflows support streaming responses
* Streaming handled via event handlers returned from the workflow
* To stream only the LLM output, use `AgentStream` events

```python
from llama_index.core.agent.workflow import AgentStream

handler = agent.run(user_msg="What is the weather in Saskatoon?")

async for event in handler.stream():
    if isinstance(event, AgentStream):
        print(event.response) # the current full response
        # print(event.delta, end="", flush=True)
        # print(event.raw)  # the raw llm api response
        # print(event.current_agent_name)  # the current agent name
    # other event types: AgentInput, AgentOutput, ToolCall, ToolCallResult, etc
```

### Tools and State

* Tools can access the workflow context using `ctx`
* set and retrieve (set/get) `state` from the context 
* Implement tools asynchronously for efficiency

```python
async def set_name(ctx: Context, name: str) -> str:
    state = await ctx.store.get("state")
    state["name"] = name
    await ctx.store.set("state", state)
    return f"Name set to {name}"


agent = FunctionAgent(
    tools=[set_name],
    llm=llm,
    system_prompt="You are a helpful assistant that can set a name.",
    initial_state={"name": "unset"},
)

ctx = Context(agent)

response = await agent.run(user_msg="My name is Logan", ctx=ctx)

state = await ctx.store.get("state")
print(state["name"]) # Logan
```

### Human in the Loop

* Tools support human feedback/intervention 
    * e.g. confirming a tool call or providing feedback.
* we use `ctx.wait_for_event` to wait for an event, and use event types`InputRequiredEvent` and `HumanResponseEvent` to handle the events.

```python

# define tool with human in the loop
async def dangerous_task(ctx: Context) -> str:
    """A dangerous task that requires human confirmation."""

    question = "Are you sure you want to proceed?"
    response = await ctx.wait_for_event( # wait for an event
        HumanResponseEvent, # event type (human response) to wait for 
        waiter_id=question, # id of waiter
        waiter_event=InputRequiredEvent( # waiter (input) event to send 
            prefix=question, # event prefix (question)
            user_name="Logan", # user name
        ),
        requirements={"user_name": "Logan"}, # requirements for the event
    )
    if response.response == "yes":
        return "Dangerous task completed successfully."
    else:
        return "Dangerous task aborted."

# create agent
agent = FunctionAgent(
    tools=[dangerous_task],
    llm=llm,
    system_prompt="You are a helpful assistant that can perform dangerous tasks.",
)

# run agent
handler = agent.run(user_msg="I want to proceed with the dangerous task.")

# stream events from the handler
async for event in handler.stream_events():
    if isinstance(event, InputRequiredEvent): # if the event is an input event
        response = input(event.prefix).strip().lower() # get response from user
        handler.ctx.send_event( # send the response to the agent ctx
            HumanResponseEvent( # event type (human response) to send
                response=response, # response
                user_name=event.user_name, # user name
            )
        )

response = await handler # get the response from the agent
print(str(response)) # print the response

```

**Notes**:
- In production scenarios, you might handle HITL over a websocket or multiple API requests. 
- Context object is serializable, so we can also save the workflow mid-run and restore it later
