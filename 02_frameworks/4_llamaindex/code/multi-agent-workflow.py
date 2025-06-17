# LlamaIndex Multi-Agent Workflow Example
# This file demonstrates how to set up and run a multi-agent workflow using LlamaIndex.

import asyncio
from llama_index.llms.openai import OpenAI
from llama_index.core.agent.workflow import FunctionAgent, AgentWorkflow
from llama_index.core.workflow import Context
from tavily import AsyncTavilyClient

# Set up LLM
llm = OpenAI(model="gpt-4o", api_key="sk-...")  # Replace with your OpenAI API key

# Define tools
async def search_web(query: str) -> str:
    """Useful for using the web to answer questions."""
    client = AsyncTavilyClient(api_key="tvly-...")  # Replace with your Tavily API key
    return str(await client.search(query))

async def record_notes(ctx: Context, notes: str, notes_title: str) -> str:
    """Useful for recording notes on a given topic."""
    current_state = await ctx.get("state")
    if "research_notes" not in current_state:
        current_state["research_notes"] = {}
    current_state["research_notes"][notes_title] = notes
    await ctx.set("state", current_state)
    return "Notes recorded."

async def write_report(ctx: Context, report_content: str) -> str:
    """Useful for writing a report on a given topic."""
    current_state = await ctx.get("state")
    current_state["report_content"] = report_content
    await ctx.set("state", current_state)
    return "Report written."

async def review_report(ctx: Context, review: str) -> str:
    """Useful for reviewing a report and providing feedback."""
    current_state = await ctx.get("state")
    current_state["review"] = review
    await ctx.set("state", current_state)
    return "Report reviewed."

# Agent Definitions
research_agent = FunctionAgent(
    name="ResearchAgent",
    description="Searches the web for information on a given topic.",
    system_prompt="You are a research assistant. Use the web_search tool to find information and record_notes to save it.",
    tools=[search_web, record_notes],
    llm=llm,
    can_handoff_to=["WriteAgent"]
)

write_agent = FunctionAgent(
    name="WriteAgent",
    description="Writes a report using the information found by the ResearchAgent.",
    system_prompt="You are a writer. Use the write_report tool to draft the report based on the research notes.",
    tools=[write_report],
    llm=llm,
    can_handoff_to=["ReviewAgent"]
)

review_agent = FunctionAgent(
    name="ReviewAgent",
    description="Reviews the report and provides feedback.",
    system_prompt="You are a reviewer. Use the review_report tool to critique the report.",
    tools=[review_report],
    llm=llm
)

# AgentWorkflow Initialization
agent_workflow = AgentWorkflow(
    agents=[research_agent, write_agent, review_agent],
    root_agent=research_agent.name,
    initial_state={
        "research_notes": {},
        "report_content": "Not written yet.",
        "review": "Review required.",
    },
)

# Running the Workflow
async def main():
    await agent_workflow.run()

if __name__ == "__main__":
    asyncio.run(main()) 