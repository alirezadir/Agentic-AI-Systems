import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, handoff
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from agents.run import RunConfig, RunContextWrapper

# Load the environment variables from the .env file
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

# Check if the API key is present
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set. Please ensure it is defined in your .env file.")

# Define Agents, Handoffs, and Run Config on_chat_start
@cl.on_chat_start
async def start():
    model = OpenAIChatCompletionsModel(
        model="gpt-4o",
        openai_client=AsyncOpenAI(api_key=openai_api_key)
    )

    run_config = RunConfig(
        model=model,
        # tracing_disabled=True
    )

    billing_agent = Agent(
        name="Billing Agent",
        instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
        You handle billing-related queries, including invoices, payments, and pricing questions. Be professional and precise.""",
        handoff_description="Specialist agent for Billing questions"
    )

    refund_agent = Agent(
        name="Refund Agent",
        instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
        You handle refund requests and related policies. Be empathetic while following refund guidelines.""",
        handoff_description="Specialist agent for Refund questions"
    )

    # Define a callback function to handle handoffs
    def on_handoff(agent: Agent, ctx: RunContextWrapper[None]):
        print("Handoff called for agent: ", agent.name)
        # Could add more detailed logging or notifications here
        cl.Message(
            content=f"🔄 Handing off to {agent.name}... \n I'm transferring your request to our {agent.name} who will be able to better assist you.",
            author="System"
        ).send()

    triage_agent = Agent(
        name="Triage Agent",
        instructions=(
            "You are the first point of contact. Direct billing questions to the Billing Agent "
            "and refund requests to the Refund Agent. If unsure, handle the query yourself."
        ),
        handoffs=[
            handoff(billing_agent, on_handoff=lambda ctx: on_handoff(billing_agent, ctx)),
            handoff(refund_agent, on_handoff=lambda ctx: on_handoff(refund_agent, ctx))
        ]
    )

    # Set session variables (agents, run config, chat history, etc)
    cl.user_session.set("triage_agent", triage_agent)
    cl.user_session.set("run_config", run_config)
    cl.user_session.set("billing_agent", billing_agent)
    cl.user_session.set("refund_agent", refund_agent)
    cl.user_session.set("chat_history", [])

    await cl.Message(content="Welcome to the billing & refund triage agent! How can I help you today?").send()


@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages and generate responses."""

    # Send a thinking message
    msg = cl.Message(content="Thinking...")
    await msg.send()

    # Get session variables (agents, run config, chat history, etc)
    triage_agent: Agent = cast(Agent, cl.user_session.get("triage_agent"))
    run_config: RunConfig = cast(RunConfig, cl.user_session.get("run_config"))

    # Retrieve the chat history from the session.
    history = cl.user_session.get("chat_history") or []

    # Append the user's message to the history.
    history.append({"role": "user", "content": message.content})

    try:
        result = await Runner.run(triage_agent, history, run_config=run_config)

        response_content = result.final_output

        # Update the thinking message with the actual response
        msg.content = response_content
        await msg.update()

        history.append({"role": "developer", "content": response_content})

        # Update session history
        cl.user_session.set("chat_history", history)
        print(f"History: {history}")

    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")