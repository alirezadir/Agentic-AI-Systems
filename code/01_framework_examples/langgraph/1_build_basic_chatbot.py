# 1_build_basic_chatbot.py
# LangGraph Basic Chatbot Example

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model


# =========================
# SECTION 1: State Definition
# =========================
class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

# =========================
# SECTION 2: Graph Builder
# =========================
graph_builder = StateGraph(State)

# =========================
# SECTION 3: LLM Setup
# =========================
llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")

# =========================
# SECTION 4: Node Definition
# =========================
def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

# Add the chatbot node to the graph
# The first argument is the unique node name
# The second argument is the function or object that will be called whenever the node is used.
graph_builder.add_node("chatbot", chatbot)

# =========================
# SECTION 5: Add Entry Edge
# =========================
graph_builder.add_edge(START, "chatbot")

# =========================
# SECTION 6: Compile the Graph
# =========================
graph = graph_builder.compile()

# =========================
# SECTION 7: Main Chat Loop
# =========================
def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

if __name__ == "__main__":
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            stream_graph_updates(user_input)
        except:
            # fallback if input() is not available
            user_input = "What do you know about LangGraph?"
            print("User: " + user_input)
            stream_graph_updates(user_input)
            break 