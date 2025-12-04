# LangGraph Examples

**Updated 2025**: This directory contains examples and templates for building AI agents using LangGraph, a framework for orchestrating multi-agent workflows.

**LangGraph v1.0 (October 22, 2025)**: LangGraph reached v1.0, marking the first stable major release in the durable agent framework space. It offers node-based architecture for building multi-agent systems with structured state management, durable state persistence, built-in persistence for saving/resuming workflows, and human-in-the-loop patterns. The **LangGraph Platform** enables teams to run agent workflows at scale with tools to track, debug, and manage them in production.

## Overview
This folder provides starter code and examples to help you build AI agents with LangGraph. It includes basic and advanced examples covering various aspects of agent development, such as multi-agent orchestration, workflow management, and more.

**2025 Features**:
- Production-ready platform for running agent workflows at scale
- Advanced tracing and debugging tools
- Structured state management for complex multi-agent systems
- Visual workflow debugging and monitoring

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
3. Explore the docs and code examples to build your own agents.

## Contents
### Docs
- [Basic Chatbot Tutorial](./1_basic_chatbot_tutorial.md): Key concepts and basic setup for LangGraph.
- [Add Tools Tutorial](./2_add_tools_tutorial.md): Fast start guide for using the LangGraph API.
- [Add Memory Tutorial](./3_add_memory_tutorial.md): Design principles and structure for LangGraph agents.
- [Human-in-the-Loop Tutorial](./4_human_in_the_loop_tutorial.md): Advanced tutorial for human-in-the-loop interactions.

### Code
- Starter codes for building agents with LangGraph can be found in the [code](./code/README.md) including:
    - `0_hello_world_graph.py`: Simple "Hello World" example for LangGraph.
    - `0_langgraph_hello_world.py`: Another basic example for LangGraph.
    - `1_build_basic_chatbot.py`: Basic chatbot implementation.
    - `2_add_tools_chatbot.py`: Chatbot with tool integration.
    - `3_add_memory_chatbot.py`: Chatbot with memory and context management.
    - `advanced_workflow.py`: Advanced workflow example.
    - `basic_workflow.py`: Basic workflow example.
    - `complete_chatbot.py`: Full-featured chatbot implementation.
    - `customer_support_bot.py`: Customer support bot example.

## Key Concepts Demonstrated

### State Management
- Using TypedDict for type-safe state
- Managing conversation history
- Handling multiple state fields

### Graph Structure
- Node creation and connection
- Conditional routing
- Entry point definition
- Edge management

### Tool Integration
- Custom tool definition with @tool decorator
- Function calling from agents
- Tool result handling

### Memory and Context
- Conversation history management
- Context preservation between turns
- State persistence

### Human Interaction
- Human-in-the-loop capabilities
- Input handling
- Interactive conversation flow

## Output Files

Each example generates an output file:
- `basic_workflow_output.txt`
- `advanced_workflow_output.txt`
- `complete_chatbot_output.txt`

These files contain the conversation history and results of each run.

## Best Practices

1. **State Management**
   - Use TypedDict for type-safe state
   - Keep state minimal and focused
   - Handle state updates carefully

2. **Tool Design**
   - Make tools focused and specific
   - Include clear documentation
   - Handle errors gracefully

3. **Graph Structure**
   - Keep the graph simple and clear
   - Use meaningful node names
   - Document the flow between nodes

4. **Error Handling**
   - Implement proper error handling
   - Provide meaningful error messages
   - Handle edge cases appropriately

## Resources

- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)

## Contributing

Feel free to:
1. Add new examples
2. Improve existing examples
3. Add more documentation
4. Report issues or suggest improvements

## License

This project is licensed under the MIT License - see the LICENSE file for details. 