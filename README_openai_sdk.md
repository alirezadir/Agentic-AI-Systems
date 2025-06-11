# OpenAI Agents SDK Reference
```Usage Prompt: Please refer to the OpenAI Agents SDK documentation at: GitHub/Gen-AI-Engineering/README_openai_sdk.md``` 

For implementation details, please check the OpenAI Agents SDK documentation which includes:
- Core primitives and design principles
- Agent configuration and tools
- Best practices for agent design
- Model selection guidelines
- Guardrails and safety considerations

For this implementation, I'm following the best practices from the SDK documentation, specifically:
- Agent design patterns
- Tool implementation guidelines
- Guardrails setup

This implementation follows the patterns shown in the SDK documentation's examples, particularly:
- Basic agent setup
- Tool integration
- Multi-agent orchestration

## Official Resources
- [GitHub Repository](https://github.com/openai/openai-agents-python)
- [Documentation](https://openai.github.io/openai-agents-python/)
- [Examples](https://github.com/openai/openai-agents-python/tree/main/examples)
- [API Reference](https://openai.github.io/openai-agents-python/api_reference/)

## Core Primitives

The SDK has a very small set of primitives:

1. **Agents**: LLMs equipped with instructions and tools
2. **Handoffs**: Allow agents to delegate to other agents for specific tasks
3. **Guardrails**: Enable input validation for agents
4. **Tracing**: Built-in visualization and debugging of agentic flows

## Design Principles

The SDK follows two main design principles:
1. Enough features to be worth using, but few enough primitives to make it quick to learn
2. Works great out of the box, but you can customize exactly what happens

## Key Features

- **Agent Loop**: Built-in handling of tool calls, LLM responses, and looping
- **Python-first**: Use built-in language features for orchestration
- **Handoffs**: Powerful coordination between multiple agents
- **Guardrails**: Parallel input validations and checks
- **Function Tools**: Turn Python functions into tools with automatic schema generation
- **Tracing**: Built-in visualization, debugging, and monitoring

## Quick Start

1. **Installation**
```bash
pip install openai-agents
```

2. **Hello World Example**
```python
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Write a haiku about programming.")
print(result.final_output)
```

3. **Environment Setup**
```bash
export OPENAI_API_KEY=sk-...
```

## Key Components

### 1. Basic Agent
```python
from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant"
)
```

### 2. Agent with Handoffs
```python
spanish_agent = Agent(
    name="Spanish agent",
    instructions="You only speak Spanish.",
)

english_agent = Agent(
    name="English agent",
    instructions="You only speak English",
)

triage_agent = Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[spanish_agent, english_agent],
)
```

### 3. Agent with Tools
```python
from agents import function_tool

@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."

agent = Agent(
    name="Weather Assistant",
    instructions="You are a helpful weather assistant.",
    tools=[get_weather],
)
```

### 4. Data Models
```python
from pydantic import BaseModel
from typing import List, Optional

class Person(BaseModel):
    name: str
    role: Optional[str]
    contact: Optional[str]

class Meeting(BaseModel):
    date: str
    time: str
    location: Optional[str]
    duration: Optional[str]

class Task(BaseModel):
    description: str
    assignee: Optional[str]
    deadline: Optional[str]
    priority: Optional[str]

class EmailData(BaseModel):
    subject: str
    sender: Person
    recipients: List[Person]
    main_points: List[str]
    meetings: List[Meeting]
    tasks: List[Task]
    next_steps: Optional[str]
```

## The Agent Loop

When you call `Runner.run()`, the SDK runs a loop until it gets a final output:

1. Call the LLM with model settings and message history
2. Process the LLM response (may include tool calls)
3. If response has final output, return it and end loop
4. If response has handoff, switch to new agent and continue
5. Process tool calls and append responses, then continue

## Best Practices

1. **Agent Instructions**
   - Be specific and detailed in agent instructions
   - Include examples when possible
   - Specify output format requirements

2. **Error Handling**
   - Always wrap agent execution in try-except blocks
   - Handle potential API errors gracefully
   - Provide meaningful error messages

3. **Async Operations**
   - Use async/await for agent operations
   - Handle concurrent requests appropriately
   - Use asyncio.run() for main execution

4. **Data Models**
   - Use Pydantic models for structured data
   - Include type hints for better code clarity
   - Make optional fields explicit

## Requirements

```
openai>=1.12.0
python-dotenv>=1.0.1
pydantic>=2.6.1
```

## Additional Resources

### Documentation Sections
- [Agents](https://openai.github.io/openai-agents-python/agents/)
- [Running Agents](https://openai.github.io/openai-agents-python/running_agents/)
- [Tools](https://openai.github.io/openai-agents-python/tools/)
- [Handoffs](https://openai.github.io/openai-agents-python/handoffs/)
- [Tracing](https://openai.github.io/openai-agents-python/tracing/)
- [Guardrails](https://openai.github.io/openai-agents-python/guardrails/)
- [Orchestrating Multiple Agents](https://openai.github.io/openai-agents-python/orchestrating_multiple_agents/)

### Example Categories
- [Basic Examples](https://github.com/openai/openai-agents-python/tree/main/examples/basic)
- [Advanced Examples](https://github.com/openai/openai-agents-python/tree/main/examples/advanced)
- [Integration Examples](https://github.com/openai/openai-agents-python/tree/main/examples/integrations)
