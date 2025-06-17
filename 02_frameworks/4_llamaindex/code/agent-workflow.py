# LlamaIndex FunctionAgent / AgentWorkflow Example
# This file demonstrates how to set up and run a FunctionAgent with an AgentWorkflow.

import asyncio
from llama_index.llms.openai import OpenAI
from llama_index.core.agent.workflow import FunctionAgent, AgentWorkflow, AgentStream
from llama_index.core.workflow import Context
from llama_index.core.agent.callback import BaseAgentCallback
from tavily import AsyncTavilyClient

# Set up LLM
llm = OpenAI(model="gpt-4o-mini", api_key="sk-...")  # Replace with your OpenAI API key

# Define tool
async def search_web(query: str) -> str:
    """Useful for using the web to answer questions."""
    client = AsyncTavilyClient(api_key="tvly-...")  # Replace with your Tavily API key
    return str(await client.search(query))

# Create agent
agent = FunctionAgent(
    tools=[search_web],
    llm=llm,
    system_prompt="You are a helpful assistant that can search the web for information."
)

# Running the Agent
async def run_agent():
    response = await agent.run(user_msg="What is the weather in San Francisco?")
    print(str(response))

# Wrapping the agent in an AgentWorkflow
workflow = AgentWorkflow(agents=[agent])

async def run_workflow():
    response = await workflow.run(user_msg="What is the weather in San Francisco?")
    print(str(response))

# Maintaining State
ctx = Context(agent)

async def run_with_context():
    response = await agent.run(user_msg="My name is Logan, nice to meet you!", ctx=ctx)
    print(str(response))

    response = await agent.run(user_msg="What is my name?", ctx=ctx)
    print(str(response))

# Streaming
async def stream_workflow():
    async for event in workflow.stream(user_msg="Tell me a joke"):
        if isinstance(event, AgentStream):
            print(event.output)

# Human in the Loop
class HumanApprovalCallback(BaseAgentCallback):
    async def on_tool_start(self, tool_name, input):
        print(f"About to run tool: {tool_name} with input: {input}")
        approval = input("Do you want to continue? (y/n): ")
        if approval.lower() != 'y':
            raise Exception("Tool execution cancelled by human.")

agent_with_callback = FunctionAgent(
    tools=[search_web],
    llm=llm,
    system_prompt="You are a helpful assistant that can search the web for information.",
    callbacks=[HumanApprovalCallback()]
)

async def run_with_callback():
    response = await agent_with_callback.run(user_msg="Search the current news")
    print(response)

# Main function to run all examples
async def main():
    print("Running agent...")
    await run_agent()

    print("\nRunning workflow...")
    await run_workflow()

    print("\nRunning with context...")
    await run_with_context()

    print("\nStreaming workflow...")
    await stream_workflow()

    print("\nRunning with human approval callback...")
    await run_with_callback()

if __name__ == "__main__":
    asyncio.run(main()) 