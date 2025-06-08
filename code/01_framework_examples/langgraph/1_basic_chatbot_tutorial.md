**LangGraph Tutorial Summary: Build a Basic Chatbot**

**Setup**
- `pip install -U langgraph langsmith`
- Requires access to an LLM (`OpenAI`, `Anthropic`, `Gemini`, etc.)

**Core Components**

**State**
- Defined as a `TypedDict`:
  `class State(TypedDict): messages: Annotated[list, add_messages]`
- Uses `Annotated[list, add_messages]` to append messages (not overwrite)

**StateGraph**
- Core LangGraph construct for building state machines
- Created with `graph_builder = StateGraph(State)` using your state schema

**Nodes**
- Functions that take the current `State` and return an updated `State`
- Added with: `graph_builder.add_node("chatbot", chatbot)`

**Edges**
- Define control flow between nodes
- Entry edge: `graph_builder.add_edge(START, "chatbot")`

**Types & Reducers**
- `TypedDict` defines state schema
- `Annotated[...]` attaches a reducer function like `add_messages`
  (reducers define how state updates: append, replace, etc.)

**LLM Integration**
- A node typically invokes the LLM using the current messages:
  `def chatbot(state: State): return {"messages": [llm.invoke(state["messages"])]}`

**Compile & Run**

**Compile Graph**
- `graph = graph_builder.compile()`

**Run Chatbot**
- `graph.stream({"messages": [{"role": "user", "content": user_input}]})`

**Explanation of key lines**

`return {"messages": [llm.invoke(state["messages"])]}`
- `state["messages"]`: current chat history
- `llm.invoke(...)`: calls the LLM to generate a reply
- `[ ... ]`: wraps response in a list (required by `add_messages`)
- `{"messages": [...]}`: returns a state update with new messages

`graph.stream({"messages": [{"role": "user", "content": user_input}]})`
- Starts the graph execution
- Sends `user_input` as a message
- Streams updates as nodes run and state changes