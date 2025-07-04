# OpenAI Cookbook: Orchestrating Agents — Routines and Handoffs
**Source:** [OpenAI Cookbook: Orchestrating Agents](https://cookbook.openai.com/examples/orchestrating_agents)

---

## Overview

This guide introduces the concepts of **routines** and **handoffs** for orchestrating multiple agents (LLMs + tools) in a controllable, modular way. It demonstrates how to structure agent workflows, implement routines, and enable agent-to-agent handoffs, with practical code examples throughout.


### Core Concepts

| Concept      | Description                                                                 |
|--------------|-----------------------------------------------------------------------------|
| **Routine**  | A set of natural language instructions (system prompt) + tools to execute   |
| **Handoff**  | Mechanism for transferring control between agents/routines                  |

---

## 1. Routines

A routine is a list of instructions (system prompt) and the tools needed to complete them. Routines can include conditional logic, much like a state machine, but are expressed in natural language for the LLM.

**Example: Customer Service Routine**
```python
system_message = (
    "You are a customer support agent for ACME Inc."
    "Always answer in a sentence or less."
    "Follow the following routine with the user:"
    "1. First, ask probing questions and understand the user's problem deeper.\n"
    " - unless the user has already provided a reason.\n"
    "2. Propose a fix (make one up).\n"
    "3. ONLY if not satisfied, offer a refund.\n"
    "4. If accepted, search for the ID and then execute refund."
)

def look_up_item(search_query):
    """Use to find item ID."""
    return "item_132612938"

def execute_refund(item_id, reason="not provided"):
    print("Summary:", item_id, reason)
    return "success"
```


### 1.1. Executing Routines

A simple loop to execute a routine:
```python
def run_full_turn(system_message, messages):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_message}] + messages,
    )
    message = response.choices[0].message
    messages.append(message)
    if message.content: print("Assistant:", message.content)
    return message

messages = []
while True:
    user = input("User: ")
    messages.append({"role": "user", "content": user})
    run_full_turn(system_message, messages)
```


### 1.2. Tool Use and Function Schemas

To enable function/tool calling, define a schema for each function:
```python
import inspect

def function_to_schema(func) -> dict:
    type_map = {
        str: "string", int: "integer", float: "number", bool: "boolean",    
        list: "array", dict: "object", type(None): "null",
    }
    signature = inspect.signature(func)
    parameters = {}
    for param in signature.parameters.values():
        param_type = type_map.get(param.annotation, "string")
        parameters[param.name] = {"type": param_type}
    required = [
        param.name for param in signature.parameters.values()
        if param.default == inspect._empty
    ]
    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": (func.__doc__ or "").strip(),
            "parameters": {
                "type": "object",
                "properties": parameters,
                "required": required,
            },
        },
    }
```


### 1.3. Handling Tool Calls

Map tool names to functions and execute them as needed:
```python
tools_map = {tool.__name__: tool for tool in tools}

def execute_tool_call(tool_call, tools_map):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    print(f"Assistant: {name}({args})")
    return tools_map[name](**args)
```

### 1.4. Putting it all together:
```python
tools = [execute_refund, look_up_item]


def run_full_turn(system_message, tools, messages):

    num_init_messages = len(messages)
    messages = messages.copy()

    while True:

        # turn python functions into tools and save a reverse map
        tool_schemas = [function_to_schema(tool) for tool in tools]
        tools_map = {tool.__name__: tool for tool in tools}

        # === 1. get openai completion ===
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system_message}] + messages,
            tools=tool_schemas or None,
        )
        message = response.choices[0].message
        messages.append(message)

        if message.content:  # print assistant response
            print("Assistant:", message.content)

        if not message.tool_calls:  # if finished handling tool calls, break
            break

        # === 2. handle tool calls ===

        for tool_call in message.tool_calls:
            result = execute_tool_call(tool_call, tools_map)

            result_message = {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
            messages.append(result_message)

    # ==== 3. return new messages =====
    return messages[num_init_messages:]


def execute_tool_call(tool_call, tools_map):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    print(f"Assistant: {name}({args})")

    # call corresponding function with provided arguments
    return tools_map[name](**args)


messages = []
while True:
    user = input("User: ")
    messages.append({"role": "user", "content": user})

    new_messages = run_full_turn(system_message, tools, messages)
    messages.extend(new_messages)
```

---

## 5. Handoffs Between Agents
- Handoff: an agent (or routine) handing off an active conversation to another agent, like when you get transfered to someone else on a phone call. Except in this case, the agents have complete knowledge of your prior conversation!
- Agents can hand off control by returning an Agent object or calling a transfer function. This enables modular, multi-agent workflows.


**Example: Transfer to Refund Agent**
```python

refund_agent = Agent(
    name="Refund Agent",
    instructions="You are a refund agent. Help the user with refunds.",
    tools=[execute_refund],
)

# Handoff function
def transfer_to_refunds():
    return refund_agent # return an Agent object
```
- Update run_full_turn to take an *Agent* instead of separate system_message and tools
- Update the main loop to check for agent transfers and switch context as needed.


```python

def run_full_turn(agent, messages):

    current_agent = agent
    ...

    while True:

        # turn python functions into tools and save a reverse map
        tool_schemas = [function_to_schema(tool) for tool in current_agent.tools]
        tools_map = {tool.__name__: tool for tool in current_agent.tools}

        # === 1. get openai completion ===
        response = client.chat.completions.create(
            model=agent.model,
            messages=[{"role": "system", "content": current_agent.instructions}]
            + messages,
            tools=tool_schemas or None,
        )
        message = response.choices[0].message
        messages.append(message)

        if message.content:  # print agent response
            print(f"{current_agent.name}:", message.content)

        if not message.tool_calls:  # if finished handling tool calls, break
            break

        # === 2. handle tool calls ===

        for tool_call in message.tool_calls:
            result = execute_tool_call(tool_call, tools, current_agent.name)

            if type(result) is Agent:  # if agent transfer, update current agent
                current_agent = result
                result = (
                    f"Transfered to {current_agent.name}. Adopt persona immediately."
                )

            result_message = {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
            messages.append(result_message)

    # ==== 3. return last agent used and new messages =====
    return Response(agent=current_agent, messages=messages[num_init_messages:])


def execute_tool_call(tool_call, tools, agent_name):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    print(f"{agent_name}:", f"{name}({args})")

    return tools_map[name](**args)  # call corresponding function with provided arguments
```

see [handoffs.py](./code/handoffs.py) for a complete example.

---

## 6. Best Practices
- Keep routines simple and robust
- Use clear, modular function schemas
- Let agents express intent to transfer/handoff
- Log and observe agent behavior for improvement

---

## References
- [OpenAI Cookbook: Orchestrating Agents](https://cookbook.openai.com/examples/orchestrating_agents)

---
