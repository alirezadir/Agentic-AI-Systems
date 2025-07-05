"""
LlamaIndex AgentQL Research Assistant

A streamlined research agent using LlamaIndex, AgentQL, Playwright, and DuckDuckGo.
# use DuckDuckGo to search the web for information.
# use AgentQL to parse HTML and extract information from the web, 
# use Playwright to click on links and extract information from the web.
"""

import os
from llama_index.tools.playwright.base import PlaywrightToolSpec
from llama_index.tools.agentql import AgentQLBrowserToolSpec
from llama_index.tools.duckduckgo import DuckDuckGoSearchToolSpec
from llama_index.llms.openai import OpenAI
from llama_index.core.agent.workflow import AgentWorkflow, AgentStream

async def create_workflow():
    # setup playwright tools (click on links)
    async_browser = await PlaywrightToolSpec.create_async_playwright_browser(headless=True)
    playwright_tools = PlaywrightToolSpec(async_browser=async_browser).to_tool_list()
    browser_tools = [
        tool for tool in playwright_tools
        if tool.metadata.name in ["click", "get_current_page", "navigate_to"]
    ]
    # setup agentql tools (parse HTML)
    agentql_tools = AgentQLBrowserToolSpec(async_browser=async_browser).to_tool_list()
    
    # setup duckduckgo tools (search the web)
    duckduckgo_tools = [
        tool for tool in DuckDuckGoSearchToolSpec().to_tool_list()
        if tool.metadata.name == "duckduckgo_full_search"
    ]
    llm = OpenAI(model="gpt-4o")

    workflow = AgentWorkflow.from_tools_or_functions(
        browser_tools + agentql_tools + duckduckgo_tools,
        llm=llm,
        system_prompt=(
            "You are an expert in browser automation, data extraction, and summarization "
            "for research resources."
        ),
    )
    return workflow

async def main():
    workflow = await create_workflow()
    handler = workflow.run(
        user_msg=(
            "Use DuckDuckGoSearch to find URL resources on the web that are relevant to the research topic: "
            "What is the relationship between exercise and stress levels?\n"
            "Go through each resource found. For each different resource, use Playwright to click on link to the resource, "
            "then use AgentQL to extract information, including the name of the resource, author name(s), link to the resource, "
            "publishing date, journal name, volume number, issue number, and the abstract.\n"
            "Find more resources until there are two different resources that can be successfully extracted from."
        )
    )
    async for event in handler.stream_events():
        if isinstance(event, AgentStream):
            print(event.delta, end="", flush=True)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())