**LangGraph Tutorial Summary: Add Memory to Chatbot**

**Purpose**

* Enable multi-turn conversations by persisting conversation state.
* Use LangGraph's checkpointing system to store and resume `State` across calls.

**Checkpointing Setup**

* Use in-memory saver for tutorial purposes:

  ```python
  from langgraph.checkpoint.memory import MemorySaver
  memory = MemorySaver()
  ```

**Compile with Checkpointer**

* Add `checkpointer=memory` during graph compilation:

  ```python
  graph = graph_builder.compile(checkpointer=memory)
  ```

**Running with Memory**

* Supply a `thread_id` inside `config` to identify conversation thread:

  ```python
  config = {"configurable": {"thread_id": "1"}}
  ```
* Call the chatbot with the thread-aware config:

  ```python
  events = graph.stream(
      {"messages": [{"role": "user", "content": "Hi there! My name is Will."}]},
      config,
      stream_mode="values",
  )
  ```

**Follow-up with Context**

* Ask follow-up using the same config:

  ```python
  user_input = "Remember my name?"
  events = graph.stream(
      {"messages": [{"role": "user", "content": user_input}]},
      config,
      stream_mode="values",
  )
  ```
* The assistant remembers "Will" due to persistent `State`.

**Test with New Thread**

* Switch to a different `thread_id` to test stateless run:

  ```python
  config = {"configurable": {"thread_id": "2"}}
  ```
* Assistant forgets name since no prior history is stored for this ID.

**Inspect State**

* Call `graph.get_state(config)` to check saved messages and metadata:

  ```python
  snapshot = graph.get_state(config)
  snapshot.values
  snapshot.next
  ```

**Summary**

* Persistent memory works via LangGraph checkpointing.
* No external memory management needed.
* Enables coherent, contextual chatbot conversations across sessions.

**Next Step**

* Extend chatbot with human-in-the-loop capabilities for fallback and verification.
