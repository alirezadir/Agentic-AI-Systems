# LangGraph Code Examples

This directory contains example implementations using LangGraph, a framework for building stateful, multi-actor applications with LLMs.

## Overview
This folder provides starter code and examples to help you build AI agents with LangGraph. It includes basic and advanced examples covering various aspects of agent development, such as multi-agent orchestration, workflow management, and more.

## Prerequisites
- Python 3.8 or higher
- OpenAI API key (set as an environment variable or in a .env file)

## Usage
1. Install dependencies:
   ```bash
   pip install langgraph openai
   ```
2. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your_api_key_here"
   ```
3. Run the examples:
   ```bash
   python 0_hello_world_graph.py
   ```

## Contents
### Examples
- `0_hello_world_graph.py`: Simple "Hello World" example for LangGraph.
- `0_langgraph_hello_world.py`: Another basic example for LangGraph.
- `1_build_basic_chatbot.py`: Basic chatbot implementation.
- `2_add_tools_chatbot.py`: Chatbot with tool integration.
- `3_add_memory_chatbot.py`: Chatbot with memory and context management.
- `advanced_workflow.py`: Advanced workflow example.
- `basic_workflow.py`: Basic workflow example.
- `complete_chatbot.py`: Full-featured chatbot implementation.
- `customer_support_bot.py`: Customer support bot example. 