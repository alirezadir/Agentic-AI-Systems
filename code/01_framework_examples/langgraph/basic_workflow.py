from typing import Annotated, Sequence, TypedDict
from langgraph.graph import Graph, StateGraph
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import operator

# Define our state
class AgentState(TypedDict):
    messages: Annotated[Sequence[HumanMessage | AIMessage], operator.add]
    next: str

# Define our nodes
def create_agent_node(name: str, system_prompt: str):
    """Create an agent node with a specific role."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
    ])
    
    chain = prompt | ChatOpenAI(temperature=0) | (lambda x: x.content)
    
    def agent_node(state: AgentState) -> AgentState:
        """Process the state through the agent."""
        messages = state["messages"]
        response = chain.invoke({"messages": messages})
        return {"messages": [AIMessage(content=response)], "next": "end"}
    
    return agent_node

# Create our graph
def create_workflow():
    # Create nodes
    researcher = create_agent_node(
        "researcher",
        "You are a research assistant. Analyze the given text and extract key points."
    )
    
    summarizer = create_agent_node(
        "summarizer",
        "You are a summarization expert. Create a concise summary of the key points."
    )
    
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("researcher", researcher)
    workflow.add_node("summarizer", summarizer)
    
    # Add edges
    workflow.add_edge("researcher", "summarizer")
    workflow.add_edge("summarizer", "end")
    
    # Set entry point
    workflow.set_entry_point("researcher")
    
    # Add end node
    workflow.add_node("end", lambda x: x)
    
    return workflow.compile()

# Example usage
if __name__ == "__main__":
    # Create the workflow
    app = create_workflow()
    
    # Run the workflow
    result = app.invoke({
        "messages": [
            HumanMessage(content="Here's a text about AI: Artificial Intelligence (AI) is transforming various industries through machine learning and deep learning. It enables computers to learn from data and make decisions. Key applications include natural language processing, computer vision, and robotics.")
        ],
        "next": "researcher"
    })
    
    # Print results
    print("\nResearch Analysis:")
    print(result["messages"][0].content)
    print("\nFinal Summary:")
    print(result["messages"][1].content)

    # Save output to a file
    with open("basic_workflow_output.txt", "w") as f:
        f.write("Research Analysis:\n")
        f.write(result["messages"][0].content + "\n\n")
        f.write("Final Summary:\n")
        f.write(result["messages"][1].content + "\n") 