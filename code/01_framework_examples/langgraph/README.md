# LangGraph Sample Projects

This directory contains example implementations using LangGraph, a framework for building stateful, multi-actor applications with LLMs. Each example demonstrates different features and capabilities of LangGraph.

## Prerequisites

- Python 3.9+
- OpenAI API key
- Required packages (install using `pip install -r requirements.txt`):
  - langgraph>=0.0.15
  - langchain>=0.1.0
  - langchain-openai>=0.0.5
  - langchain-core>=0.1.10
  - openai>=1.12.0
  - python-dotenv>=1.0.1
  - pydantic>=2.6.1

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set your OpenAI API key:
```bash
export OPENAI_API_KEY=your_api_key_here
```

## Example Projects

### 1. Basic Workflow (`basic_workflow.py`)

A simple example demonstrating the core concepts of LangGraph:
- Basic graph creation and node definition
- Simple workflow with two agents (researcher and summarizer)
- State management and message passing
- Output saving to file

Run it with:
```bash
python basic_workflow.py
```

### 2. Advanced Workflow (`advanced_workflow.py`)

A more complex example showcasing advanced LangGraph features:
- Conditional routing based on message content
- Tool integration and function calling
- Multiple agent types with different roles
- State management with multiple fields
- Error handling and edge cases

Run it with:
```bash
python advanced_workflow.py
```

### 3. Complete Chatbot (`complete_chatbot.py`)

A full-featured chatbot implementation demonstrating:
- Human-in-the-loop interaction
- Conversation memory and context management
- Custom tool integration (knowledge base search, user profile lookup)
- Conditional routing and state management
- Output logging to file

Run it with:
```bash
python complete_chatbot.py
```

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