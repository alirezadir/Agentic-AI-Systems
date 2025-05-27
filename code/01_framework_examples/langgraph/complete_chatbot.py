from typing import Annotated, Sequence, TypedDict, List, Dict, Any
from langgraph.graph import Graph, StateGraph
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage, FunctionMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain.memory import ConversationBufferMemory
import operator
import json

# Define our state
class AgentState(TypedDict):
    messages: Annotated[Sequence[HumanMessage | AIMessage | FunctionMessage], operator.add]
    next: str
    memory: Dict[str, Any]
    needs_human_input: bool
    human_input: str

# Define tools
@tool
def search_knowledge_base(query: str) -> str:
    """Search the knowledge base for information."""
    # In a real application, this would query a vector store or database
    knowledge_base = {
        "company_policy": "Our company policy states that all employees must complete training annually.",
        "product_info": "Our main product is an AI-powered chatbot that helps with customer service.",
        "pricing": "Basic plan: $10/month, Pro plan: $25/month, Enterprise: Custom pricing."
    }
    return knowledge_base.get(query.lower(), "Information not found in knowledge base.")

@tool
def get_user_profile(user_id: str) -> str:
    """Get user profile information."""
    # In a real application, this would query a user database
    profiles = {
        "user1": "Premium user, active for 2 years",
        "user2": "Basic user, active for 6 months",
        "user3": "Enterprise user, active for 1 year"
    }
    return profiles.get(user_id, "User not found.")

# Define our nodes
def create_agent_node(name: str, system_prompt: str, tools: List = None):
    """Create an agent node with a specific role and tools."""
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
    ])
    
    chain = prompt | ChatOpenAI(temperature=0)
    
    def agent_node(state: AgentState) -> AgentState:
        """Process the state through the agent."""
        messages = state["messages"]
        memory = state["memory"]
        
        # Add memory context to messages
        if memory and "chat_history" in memory:
            messages = list(memory["chat_history"]) + list(messages)
        
        response = chain.invoke({"messages": messages})
        
        # Handle function calls if any
        if hasattr(response, "additional_kwargs") and "function_call" in response.additional_kwargs:
            function_call = response.additional_kwargs["function_call"]
            function_name = function_call["name"]
            function_args = json.loads(function_call["arguments"])
            
            # Execute the function
            if function_name == "search_knowledge_base":
                result = search_knowledge_base(function_args["query"])
                return {
                    "messages": [FunctionMessage(content=result, name=function_name)],
                    "next": "assistant",
                    "memory": memory,
                    "needs_human_input": False,
                    "human_input": ""
                }
            elif function_name == "get_user_profile":
                result = get_user_profile(function_args["user_id"])
                return {
                    "messages": [FunctionMessage(content=result, name=function_name)],
                    "next": "assistant",
                    "memory": memory,
                    "needs_human_input": False,
                    "human_input": ""
                }
        
        # Check if human input is needed
        if "needs_human_input" in state and state["needs_human_input"]:
            return {
                "messages": [response],
                "next": "human_input",
                "memory": memory,
                "needs_human_input": True,
                "human_input": state["human_input"]
            }
        
        return {
            "messages": [response],
            "next": "end",
            "memory": memory,
            "needs_human_input": False,
            "human_input": ""
        }
    
    return agent_node

def human_input_node(state: AgentState) -> AgentState:
    """Handle human input in the workflow."""
    print("\nHuman Input Required:")
    print(state["messages"][-1].content)
    human_response = input("Your response: ")
    
    return {
        "messages": [HumanMessage(content=human_response)],
        "next": "assistant",
        "memory": state["memory"],
        "needs_human_input": False,
        "human_input": human_response
    }

def end_node(state: AgentState) -> AgentState:
    """Handle the end of the conversation."""
    return state

# Create our graph
def create_workflow():
    # Create memory
    memory = ConversationBufferMemory(return_messages=True)
    
    # Create nodes
    assistant = create_agent_node(
        "assistant",
        """You are a helpful AI assistant. You can:
        1. Answer general questions
        2. Search the knowledge base for specific information
        3. Look up user profiles
        4. Ask for human input when needed
        
        Always be polite and professional. If you need more information, use the appropriate tool or ask for human input.""",
        tools=[search_knowledge_base, get_user_profile]
    )
    
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("assistant", assistant)
    workflow.add_node("human_input_handler", human_input_node)
    workflow.add_node("end", end_node)
    
    # Add edges with conditional routing
    workflow.add_conditional_edges(
        "assistant",
        lambda x: x["next"],
        {
            "human_input": "human_input_handler",
            "end": "end"
        }
    )
    
    workflow.add_edge("human_input_handler", "assistant")
    
    # Set entry point
    workflow.set_entry_point("assistant")
    
    return workflow.compile()

# Example usage
if __name__ == "__main__":
    # Create the workflow
    app = create_workflow()
    
    # Initialize memory
    memory = {"chat_history": []}
    
    # Test conversation
    test_inputs = [
        "What is your company policy?",
        "Tell me about user1's profile",
        "What are your pricing plans?"
    ]
    
    with open("complete_chatbot_output.txt", "w") as f:
        for user_input in test_inputs:
            print(f"\nUser: {user_input}")
            result = app.invoke({
                "messages": [HumanMessage(content=user_input)],
                "next": "assistant",
                "memory": memory,
                "needs_human_input": False,
                "human_input": ""
            })
            
            # Update memory with the conversation
            memory["chat_history"].extend([
                HumanMessage(content=user_input),
                result["messages"][-1]
            ])
            
            print("\nAssistant:", result["messages"][-1].content)
            
            # Save output to file
            f.write(f"User: {user_input}\n")
            f.write(f"Assistant: {result['messages'][-1].content}\n\n")
            # If human input was needed, it would have been handled in the workflow
            if result["needs_human_input"]:
                print("Human input was requested and handled in the workflow.")
                f.write("Human input was requested and handled in the workflow.\n\n") 