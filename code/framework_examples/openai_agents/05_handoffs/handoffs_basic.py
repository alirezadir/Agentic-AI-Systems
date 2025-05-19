import asyncio
from agents import Agent, handoff, Runner, RunContextWrapper

# Define specialized agents with clear instructions
billing_agent = Agent(
    name="Billing Agent",
    instructions="You handle billing-related queries, including invoices, payments, and pricing questions. Be professional and precise."
)

refund_agent = Agent(
    name="Refund Agent", 
    instructions="You handle refund requests and related policies. Be empathetic while following refund guidelines."
)

def on_handoff(agent: Agent, ctx: RunContextWrapper[None]):
    print("Handoff called for agent: ", agent.name)
    # Could add more detailed logging or notifications here

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

async def main():
    result = await Runner.run(
        triage_agent,
        "I need help with my billing"
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())