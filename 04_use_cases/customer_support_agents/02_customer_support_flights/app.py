import os
import chainlit as cl
from agents import Runner, MessageOutputItem, HandoffOutputItem, ToolCallItem, ToolCallOutputItem, ItemHelpers
from main import triage_agent, AirlineAgentContext

@cl.on_chat_start
async def start():
    await cl.Message(
        content="✈️ Welcome to Airline Customer Support!\n\nYou can ask questions about baggage, seats, wifi, or request seat changes.\nType your message below.",
        author="Airline Bot"
    ).send()
    cl.user_session.set("input_items", [])
    cl.user_session.set("context", AirlineAgentContext())
    cl.user_session.set("current_agent", triage_agent)

@cl.on_message
async def main(message: cl.Message):
    input_items = cl.user_session.get("input_items") or []
    context = cl.user_session.get("context") or AirlineAgentContext()
    current_agent = cl.user_session.get("current_agent") or triage_agent

    # Add user message
    input_items.append({"content": message.content, "role": "user"})

    try:
        result = await Runner.run(current_agent, input_items, context=context)
        response_chunks = []
        for new_item in result.new_items:
            agent_name = getattr(new_item.agent, "name", "Agent")
            if isinstance(new_item, MessageOutputItem):
                response_chunks.append(f"**{agent_name}:** {ItemHelpers.text_message_output(new_item)}")
            elif isinstance(new_item, HandoffOutputItem):
                response_chunks.append(
                    f"Handed off from {new_item.source_agent.name} to {new_item.target_agent.name}"
                )
            elif isinstance(new_item, ToolCallItem):
                response_chunks.append(f"{agent_name}: Calling a tool")
            elif isinstance(new_item, ToolCallOutputItem):
                response_chunks.append(f"{agent_name}: Tool call output: {getattr(new_item, 'output', '')}")
            else:
                response_chunks.append(f"{agent_name}: Skipping item: {new_item.__class__.__name__}")
        response = "\n".join(response_chunks) if response_chunks else "No response from agent."
        await cl.Message(content=response, author="Airline Bot").send()
        # Update session state
        cl.user_session.set("input_items", result.to_input_list())
        cl.user_session.set("current_agent", result.last_agent)
        cl.user_session.set("context", context)
    except Exception as e:
        await cl.Message(content=f"Sorry, an error occurred: {e}", author="Airline Bot").send() 