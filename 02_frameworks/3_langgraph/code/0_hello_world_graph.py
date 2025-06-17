from langgraph.graph import StateGraph
from typing import TypedDict

# Define a minimal state
class SimpleState(TypedDict):
    message: str

# Define a single node that always returns a fixed message
def greet_node(state: SimpleState) -> SimpleState:
    return {"message": "Hello, World!"}

# Build the graph
workflow = StateGraph(SimpleState)
workflow.add_node("greet", greet_node)
workflow.set_entry_point("greet")
workflow.add_node("end", lambda x: x)
workflow.add_edge("greet", "end")
app = workflow.compile()

if __name__ == "__main__":
    # Run the graph with a dummy input
    result = app.invoke({"message": ""})
    print(result["message"])  # Should print 'Hello, World!' 