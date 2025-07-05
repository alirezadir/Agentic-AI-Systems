"""
LlamaIndex Custom Planning Multi-Agent System

A multi-agent system where a top-level LLM plans and orchestrates sub-agents to generate, refine, and review a report.

Agents:
- ResearchAgent: Searches the web and records notes.
- WriteAgent: Writes a markdown report based on research notes.
- ReviewAgent: Reviews the report and provides feedback.

The planner LLM creates and executes a plan, calling each agent as needed.
"""

import re
import xml.etree.ElementTree as ET
from typing import Any, Optional, List, Dict

from pydantic import BaseModel, Field

from llama_index.llms.openai import OpenAI
from tavily import AsyncTavilyClient
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.workflow import Context
from llama_index.core.llms import ChatMessage
from llama_index.core.workflow import (
    Event, StartEvent, StopEvent, Workflow, step
)

# --- LLM setup for sub-agents ---
sub_agent_llm = OpenAI(model="gpt-4.1-mini", api_key="sk-...")

# --- Tool definition: Web search tool for research agent ---
async def search_web(query: str) -> str:
    """Use the web to answer questions."""
    client = AsyncTavilyClient(api_key="tvly-...")
    return str(await client.search(query))

# --- Sub-agent definitions ---
research_agent = FunctionAgent(
    name="ResearchAgent",
    description="Records research notes based on a specific prompt.",
    system_prompt=(
        "You are the ResearchAgent. Search the web for information on a given topic and record notes in a structured format."
    ),
    llm=sub_agent_llm,
    tools=[search_web],
)

write_agent = FunctionAgent(
    name="WriteAgent",
    description="Writes a report based on research notes or revises the report based on feedback.",
    system_prompt=(
        "You are the WriteAgent. Write a markdown report on a given topic, grounded in the research notes. "
        "Return your markdown report surrounded by <report>...</report> tags."
    ),
    llm=sub_agent_llm,
    tools=[],
)

review_agent = FunctionAgent(
    name="ReviewAgent",
    description="Reviews a report and provides feedback.",
    system_prompt=(
        "You are the ReviewAgent. Review the written report and provide feedback. "
        "Your review should either approve the current report or request changes."
    ),
    llm=sub_agent_llm,
    tools=[],
)

# --- Tool wrappers for sub-agents (used by planner) ---
async def call_research_agent(ctx: Context, prompt: str) -> str:
    """Record research notes based on a specific prompt."""
    result = await research_agent.run(
        user_msg=f"Write some notes about the following: {prompt}"
    )
    state = await ctx.store.get("state")
    state["research_notes"].append(str(result))
    await ctx.store.set("state", state)
    return str(result)

async def call_write_agent(ctx: Context) -> str:
    """Write or revise a report based on research notes and feedback."""
    state = await ctx.store.get("state")
    notes = state.get("research_notes", None)
    if not notes:
        return "No research notes to write from."
    user_msg = (
        "Write a markdown report from the following notes. "
        "Be sure to output the report in the following format: <report>...</report>:\n\n"
    )
    feedback = state.get("review", None)
    if feedback:
        user_msg += f"<feedback>{feedback}</feedback>\n\n"
    notes_str = "\n\n".join(notes)
    user_msg += f"<research_notes>{notes_str}</research_notes>\n\n"
    result = await write_agent.run(user_msg=user_msg)
    match = re.search(r"<report>(.*)</report>", str(result), re.DOTALL)
    report = match.group(1) if match else str(result)
    state["report_content"] = report
    await ctx.store.set("state", state)
    return report

async def call_review_agent(ctx: Context) -> str:
    """Review the report and provide feedback."""
    state = await ctx.store.get("state")
    report = state.get("report_content", None)
    if not report:
        return "No report content to review."
    result = await review_agent.run(
        user_msg=f"Review the following report: {report}"
    )
    state["review"] = result
    await ctx.store.set("state", state)
    return result

# --- Planner Workflow and event models ---

PLANNER_PROMPT = """You are a planner chatbot.

Given a user request and the current state, break the solution into ordered <step> blocks. Each step must specify the agent to call and the message to send, e.g.
<plan>
  <step agent="ResearchAgent">search for …</step>
  <step agent="WriteAgent">draft a report …</step>
  ...
</plan>

<state>
{state}
</state>

<available_agents>
{available_agents}
</available_agents>

The general flow should be:
- Record research notes
- Write a report
- Review the report
- Write the report again if the review is not positive enough

If the user request does not require any steps, you can skip the <plan> block and respond directly.
"""

class InputEvent(StartEvent):
    user_msg: Optional[str] = Field(default=None)
    chat_history: List[ChatMessage]
    state: Optional[Dict[str, Any]] = Field(default=None)

class OutputEvent(StopEvent):
    response: str
    chat_history: List[ChatMessage]
    state: Dict[str, Any]

class StreamEvent(Event):
    delta: str

class PlanEvent(Event):
    step_info: str

class PlanStep(BaseModel):
    agent_name: str
    agent_input: str

class Plan(BaseModel):
    steps: List[PlanStep]

class ExecuteEvent(Event):
    plan: Plan
    chat_history: List[ChatMessage]

class PlannerWorkflow(Workflow):
    llm: OpenAI = OpenAI(
        model="o3-mini",
        api_key="sk-...",
    )
    agents: Dict[str, FunctionAgent] = {
        "ResearchAgent": research_agent,
        "WriteAgent": write_agent,
        "ReviewAgent": review_agent,
    }

    @step
    async def plan(self, ctx: Context, ev: InputEvent) -> 'ExecuteEvent | OutputEvent':
        if ev.state:
            await ctx.store.set("state", ev.state)
        chat_history = ev.chat_history
        if ev.user_msg:
            chat_history.append(ChatMessage(role="user", content=ev.user_msg))
        state = await ctx.store.get("state")
        available_agents_str = "\n".join(
            f'<agent name="{agent.name}">{agent.description}</agent>'
            for agent in self.agents.values()
        )
        system_prompt = ChatMessage(
            role="system",
            content=PLANNER_PROMPT.format(
                state=str(state),
                available_agents=available_agents_str,
            ),
        )
        response = await self.llm.astream_chat(messages=[system_prompt] + chat_history)
        full_response = ""
        async for chunk in response:
            full_response += chunk.delta or ""
            if chunk.delta:
                ctx.write_event_to_stream(StreamEvent(delta=chunk.delta))
        xml_match = re.search(r"(<plan>.*</plan>)", full_response, re.DOTALL)
        if not xml_match:
            chat_history.append(ChatMessage(role="assistant", content=full_response))
            return OutputEvent(response=full_response, chat_history=chat_history, state=state)
        xml_str = xml_match.group(1)
        root = ET.fromstring(xml_str)
        plan = Plan(steps=[])
        for step in root.findall("step"):
            plan.steps.append(PlanStep(
                agent_name=step.attrib["agent"],
                agent_input=step.text.strip() if step.text else "",
            ))
        return ExecuteEvent(plan=plan, chat_history=chat_history)

    @step
    async def execute(self, ctx: Context, ev: ExecuteEvent) -> InputEvent:
        chat_history = ev.chat_history
        plan = ev.plan
        for step in plan.steps:
            ctx.write_event_to_stream(
                PlanEvent(step_info=f'<step agent="{step.agent_name}">{step.agent_input}</step>')
            )
            if step.agent_name == "ResearchAgent":
                await call_research_agent(ctx, step.agent_input)
            elif step.agent_name == "WriteAgent":
                await call_write_agent(ctx)
            elif step.agent_name == "ReviewAgent":
                await call_review_agent(ctx)
        state = await ctx.store.get("state")
        chat_history.append(ChatMessage(
            role="user",
            content=(
                "I've completed the previous steps, here's the updated state:\n\n"
                f"<state>\n{state}\n</state>\n\n"
                "Do you need to continue and plan more steps? If not, write a final response."
            )
        ))
        return InputEvent(chat_history=chat_history)

# --- Running the workflow ---
import asyncio

async def main():
    planner_workflow = PlannerWorkflow(timeout=None)
    handler = planner_workflow.run(
        user_msg=(
            "Write me a report on the history of the internet. "
            "Briefly describe the history of the internet, including the development of the internet, the development of the web, "
            "and the development of the internet in the 21st century."
        ),
        chat_history=[],
        state={
            "research_notes": [],
            "report_content": "Not written yet.",
            "review": "Review required.",
        },
    )
    async for event in handler.stream_events():
        if isinstance(event, PlanEvent):
            print("Executing plan step: ", event.step_info)
    result = await handler
    print("\n\nFinal Response:\n")
    print(result.response)
    state = await handler.ctx.get("state")
    print("\n\nFinal Report Content:\n")
    print(state["report_content"])
    print("\n\nFinal Review:\n")
    print(state["review"])

if __name__ == "__main__":
    asyncio.run(main()) 