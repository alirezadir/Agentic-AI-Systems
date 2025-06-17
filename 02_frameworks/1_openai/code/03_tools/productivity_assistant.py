from agents import Agent, Runner
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Specialist agents
note_taking_agent = Agent(
   name="Note Manager",
   instructions="You help users take and organize notes efficiently.",
   # In a real application, this agent would have note-taking tools
)

task_management_agent = Agent(
   name="Task Manager",
   instructions="You help users manage tasks, deadlines, and priorities.",
   # In a real application, this agent would have task management tools
)

# Coordinator agent that uses specialists as tools
productivity_assistant = Agent(
   name="Productivity Assistant",
   instructions="""You are a productivity assistant that helps users organize their work and personal life.
  
   For note-taking questions or requests, use the note_taking tool.
   For task and deadline management, use the task_management tool.
  
   Help the user decide which tool is appropriate based on their request,
   and coordinate between different aspects of productivity.
   """,
   tools=[
       note_taking_agent.as_tool(
           tool_name="note_taking",
           tool_description="For taking, organizing, and retrieving notes and information"
       ),
       task_management_agent.as_tool(
           tool_name="task_management",
           tool_description="For managing tasks, setting deadlines, and tracking priorities"
       )
   ]
)

async def run_productivity_assistant(user_input: str) -> str:
    """Run the productivity assistant with user input."""
    result = await Runner.run(productivity_assistant, user_input)
    return result.final_output

async def main():
    # Example user requests
    requests = [
        "I need to take notes about my meeting with the marketing team",
        "Set a reminder for my project deadline next Friday",
        "Help me organize my daily tasks"
    ]
    
    for request in requests:
        try:
            print(f"\nUser Request: {request}")
            print("-" * 50)
            response = await run_productivity_assistant(request)
            print(f"Assistant Response:\n{response}")
            print("=" * 50)
        except Exception as e:
            print(f"Error processing request: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())