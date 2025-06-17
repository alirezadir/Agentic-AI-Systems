**LangGraph Tutorial Summary: Add Tools to Chatbot**

**Purpose**

* Extend the chatbot with external tools like web search.
* Enables the agent to answer questions beyond its training data.

**Setup**

* `pip install -U langchain-tavily`
* Set your API key: `_set_env("TAVILY_API_KEY")`

**Tool Definition**

* Define the tool:

  ```python
  from langchain_tavily import TavilySearch
  tool = TavilySearch(max_results=2)
  tools = [tool]
  ```
* Optional test call:
  `tool.invoke("What's a 'node' in LangGraph?")`

**Bind Tools to LLM**

* Required so the LLM knows how to call tools:

  ```python
  llm_with_tools = llm.bind_tools(tools)
  ```

**Chatbot Node**

* Updated to use the tool-aware LLM:

  ```python
  def chatbot(state: State):
      return {"messages": [llm_with_tools.invoke(state["messages\])]}

  graph_builder.add_node("chatbot", chatbot)
  ```

**Tool Execution Node**

* Use prebuilt:

  ```python
  from langgraph.prebuilt import ToolNode
  tool_node = ToolNode(tools=[tool])
  graph_builder.add_node("tools", tool_node)
  ```

**Conditional Routing**

* Add dynamic routing between `chatbot` → `tools`:

  ```python
  from langgraph.prebuilt import tools_condition
  graph_builder.add_conditional_edges("chatbot", tools_condition)
  graph_builder.add_edge("tools", "chatbot")
  graph_builder.add_edge(START, "chatbot")
  ```

**Graph Behavior**

* If LLM response includes `tool_calls`, graph routes to `tools` node.
* Tool executes and appends result as new message.
* Loop returns to `chatbot` to process result or continue conversation.

**Compile**

* Compile final graph:

  ```python
  graph = graph_builder.compile()
  ```

**Stream Execution**

* Run as before using:

  ```python
  graph.stream({"messages": [{"role": "user", "content": user_input}]})
  ```
