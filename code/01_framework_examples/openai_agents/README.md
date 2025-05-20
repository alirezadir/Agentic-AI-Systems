# OpenAI Agents Examples

This directory contains examples and templates for building AI agents using the OpenAI Agents SDK.

## Contents

### Examples
#### Basic
- [`01_basic/`](./01_basic/): Simple "Hello World" examples showing basic agent setup and interaction
- [`02_models/`](./02_models/): Working with external model providers and configurations
- [`03_tools/`](./03_tools/): Building and integrating different types oftools for agents
- [`04_context/`](./04_context/): Managing context and history in agent interactions
- [`05_handoffs/`](./05_handoffs/): Demonstrates agent-to-agent task delegation
- [`06_guardrails/`](./06_guardrails/): Adding input/output validation and safety guardrails
- [`07_run_stream/`](./07_run_stream/): Working with streaming responses from agents
- [`08_lifecycle/`](./08_lifecycle/): Understanding and managing agent lifecycles and hooks
- [`09_outputs/`](./09_outputs/): Handling different types of agent outputs
- [`10_tracing/`](./10_tracing/): Implementing tracing and logging for agent actions
#### Advanced
- [`11_mcp/`](./11_mcp/): Using the Model Context Protocol
- [`12_prompting/`](./12_prompting/): Advanced prompting techniques (e.g. dynamic prompting)
- [`13_voice_agents/`](./13_voice_agents/): Building voice-enabled agents

## Getting Started

1. Install dependencies:
```bash
pip install openai-agents
```

2. Set your OpenAI API key in the environment variable `OPENAI_API_KEY` or in the `.env` file:
```bash
export OPENAI_API_KEY="your_api_key_here"
```

3. Run the examples:
```bash
python 01_basic/hello_world.py
```
