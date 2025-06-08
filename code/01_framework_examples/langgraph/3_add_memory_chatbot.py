# 3_add_memory_chatbot.py
# LangGraph Chatbot with Web Search Tool and Persistent Memory

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch

# =========================
# SECTION 1: State Definition
# =========================
class State(TypedDict):
    messages: Annotated[list, add_messages]

# =========================
# SECTION 2: Graph Builder
# =========================
graph_builder = StateGraph(State)

# =========================
# SECTION 3: LLM and Tool Setup
# =========================

llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")
tool = TavilySearch(max_results=2)
tools = [tool]
llm_with_tools = llm.bind_tools(tools)

# =========================
# SECTION 4: Node Definitions
# =========================
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)
tool_node = ToolNode(tools=[tool])
graph_builder.add_node("tools", tool_node)

# =========================
# SECTION 5: Edges and Compilation
# =========================
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.set_entry_point("chatbot")
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

# =========================
# SECTION 6: Main Chat Loop with Memory
# =========================
def stream_graph_updates(user_input: str, config):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}, config, stream_mode="values"):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

if __name__ == "__main__":
    print("Welcome to the LangGraph chatbot with memory!")
    thread_id = input("Enter a thread id for your conversation (e.g. '1'): ").strip() or "1"
    config = {"configurable": {"thread_id": thread_id}}
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            stream_graph_updates(user_input, config)
        except:
            # fallback if input() is not available
            user_input = "What do you know about LangGraph?"
            print("User: " + user_input)
            stream_graph_updates(user_input, config)
            break 