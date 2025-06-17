from typing import Annotated, Sequence, TypedDict, List
from langgraph.graph import Graph, StateGraph
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage, FunctionMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
import operator
import json

# =====================
# State Definition
# =====================
# AgentState will keep track of the conversation messages, next node, topic, and sentiment
class AgentState(TypedDict):
    messages: Annotated[Sequence[HumanMessage | AIMessage | FunctionMessage], operator.add]
    next: str
    topic: str
    sentiment: str

# =====================
# Tool Definitions
# =====================
# Define tools for sentiment analysis and topic information
@tool
def analyze_sentiment(text: str) -> str:
    """Analyze the sentiment of the given text."""
    # In a real application, you would use a proper sentiment analysis model
    positive_words = ["good", "great", "excellent", "positive", "happy"]
    negative_words = ["bad", "poor", "terrible", "negative", "sad"]
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        return "positive"
    elif negative_count > positive_count:
        return "negative"
    else:
        return "neutral"

@tool
def get_topic_info(topic: str) -> str:
    """Get information about a specific topic."""
    # In a real application, you would fetch this from a knowledge base or API
    topics = {
        "ai": "Artificial Intelligence is the simulation of human intelligence by machines.",
        "ml": "Machine Learning is a subset of AI that focuses on learning from data.",
        "nlp": "Natural Language Processing deals with the interaction between computers and human language."
    }
    return topics.get(topic.lower(), "Topic not found in knowledge base.")

# =====================
# Node Definitions
# =====================
# This function creates an agent node with a specific role and optional tools
def create_agent_node(name: str, system_prompt: str, tools: List = None):
    """Create an agent node with a specific role and tools."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),  # System prompt for the agent's role
        MessagesPlaceholder(variable_name="messages"),  # Placeholder for conversation history
    ])
    
    chain = prompt | ChatOpenAI(temperature=0)
    
    def agent_node(state: AgentState) -> AgentState:
        """Process the state through the agent."""
        messages = state["messages"]  # Get current messages
        response = chain.invoke({"messages": messages})  # Get agent's response
        
        # Handle function calls if any
        if hasattr(response, "additional_kwargs") and "function_call" in response.additional_kwargs:
            function_call = response.additional_kwargs["function_call"]
            function_name = function_call["name"]
            function_args = json.loads(function_call["arguments"])
            
            # Execute the function based on the function name
            if function_name == "analyze_sentiment":
                result = analyze_sentiment(function_args["text"])
                return {
                    "messages": [FunctionMessage(content=result, name=function_name)],
                    "next": "sentiment_analyzer",
                    "sentiment": result
                }
            elif function_name == "get_topic_info":
                result = get_topic_info(function_args["topic"])
                return {
                    "messages": [FunctionMessage(content=result, name=function_name)],
                    "next": "topic_researcher",
                    "topic": function_args["topic"]
                }
        
        # Default: return the response and go to end
        return {"messages": [response], "next": "end"}
    
    return agent_node  # Return the node function

# =====================
# Workflow Graph Construction
# =====================
# This function sets up the workflow graph with nodes and conditional edges
def create_workflow():
    # Create nodes for each agent role
    initial_agent = create_agent_node(
        "initial_agent",
        "You are an AI assistant. Analyze the user's input and determine if you need to analyze sentiment or get topic information.",
        tools=[analyze_sentiment, get_topic_info]
    )
    
    sentiment_analyzer = create_agent_node(
        "sentiment_analyzer",
        "You are a sentiment analysis expert. Provide insights based on the sentiment analysis."
    )
    
    topic_researcher = create_agent_node(
        "topic_researcher",
        "You are a topic research expert. Provide detailed information about the given topic."
    )
    
    # Create the graph structure
    workflow = StateGraph(AgentState)
    
    # Add nodes to the graph
    workflow.add_node("initial_agent", initial_agent)
    workflow.add_node("sentiment_analyzer", sentiment_analyzer)
    workflow.add_node("topic_researcher", topic_researcher)
    
    # Add conditional edges to route based on the 'next' value in state
    workflow.add_conditional_edges(
        "initial_agent",
        lambda x: x["next"],
        {
            "sentiment_analyzer": "sentiment_analyzer",
            "topic_researcher": "topic_researcher",
            "end": "end"
        }
    )
    
    workflow.add_edge("sentiment_analyzer", "end")
    workflow.add_edge("topic_researcher", "end")
    
    # Set entry point for the workflow
    workflow.set_entry_point("initial_agent")
    
    # Add end node (no-op)
    workflow.add_node("end", lambda x: x)
    
    return workflow.compile()  # Compile the workflow

# =====================
# Example Usage and Testing
# =====================
if __name__ == "__main__":
    # Create the workflow
    app = create_workflow()
    
    # Test cases to demonstrate the workflow
    test_cases = [
        "I'm really happy with the new AI features!",
        "Tell me more about machine learning.",
        "This product is terrible and I'm very disappointed."
    ]

    # Open output file to save results
    with open("advanced_workflow_output.txt", "w") as f:
        for test_input in test_cases:
            print(f"\nProcessing: {test_input}")
            result = app.invoke({
                "messages": [HumanMessage(content=test_input)],
                "next": "initial_agent",
                "topic": "",
                "sentiment": ""
            })
            
            print("\nFinal Response:")
            print(result["messages"][-1].content)
            if "sentiment" in result and result["sentiment"]:
                print(f"Detected Sentiment: {result['sentiment']}")
            if "topic" in result and result["topic"]:
                print(f"Researched Topic: {result['topic']}")

            # Save output to file
            f.write(f"Input: {test_input}\n")
            f.write(f"Final Response: {result['messages'][-1].content}\n")
            if "sentiment" in result and result["sentiment"]:
                f.write(f"Detected Sentiment: {result['sentiment']}\n")
            if "topic" in result and result["topic"]:
                f.write(f"Researched Topic: {result['topic']}\n")
            f.write("\n") 