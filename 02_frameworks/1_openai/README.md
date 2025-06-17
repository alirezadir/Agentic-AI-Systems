# OpenAI 
This directory contains comprehensive docs and examples for building AI agents using the OpenAI Agents SDK.

## Overview
This folder provides documentation and code examples for building AI agents with the OpenAI Agents SDK. It includes guides, tutorials, and starter code to help you get started quickly.

## Prerequisites
- Python 3.8 or higher
- OpenAI API key (set as an environment variable or in a .env file)

## Usage
1. Install dependencies:
   ```bash
   pip install openai openai-agents
   ```
2. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```
3. Explore the docs and code examples to build your own agents.

## Contents
### Docs
- [OpenAI Agents (Concepts and Setup)](./docs/openai_agents_overview.md): Key concepts and basic setup for OpenAI agentic systems.
- [OpenAI Agents SDK (Comprehensive Guide)](./docs/openai_agents_sdk.md): Comprehensive guide and code examples for building agents with the OpenAI Agents SDK.
- [OpenAI API Quickstart](./docs/openai_api_quickstart.md): Fast start guide for using the OpenAI API for generative tasks.
- [OpenAI Agents Design Guide (Summary)](./docs/openai-agents-design-guide.md): Design principles and structure for OpenAI agents.

### Code
- Starter codes for building agents with the OpenAI Agents SDK can be found in the [code](./code/README.md) including: 
    - basics, models, tools, context, handoffs, guardrails, run_stream, lifecycle, outputs, tracing, mcp, prompting, voice_agents. 

- #### Basic Examples
    - [`01_basic/`](./code/01_basic/): Simple "Hello World" examples showing basic agent setup and interaction
    - [`02_models/`](./code/02_models/): Working with external model providers and configurations
    - [`03_tools/`](./code/03_tools/): Building and integrating different types of tools for agents
    - [`04_context/`](./code/04_context/): Managing context and history in agent interactions 
    - [`05_handoffs/`](./code/05_handoffs/): Demonstrates agent-to-agent task delegation
    - [`06_guardrails/`](./code/06_guardrails/): Adding input/output validation and safety guardrails
    - [`07_run_stream/`](./code/07_run_stream/): Working with streaming responses from agents
    - [`08_lifecycle/`](./code/08_lifecycle/): Understanding and managing agent lifecycles and hooks
    - [`09_outputs/`](./code/09_outputs/): Handling different types of agent outputs
    - [`10_tracing/`](./code/10_tracing/): Implementing tracing and logging for agent actions

- #### Advanced Examples
    - [`11_mcp/`](./code/11_mcp/): Using the Model Context Protocol
    - [`12_prompting/`](./code/12_prompting/): Advanced prompting techniques (e.g. dynamic prompting)
    - [`13_voice_agents/`](./code/13_voice_agents/): Building voice-enabled agents
