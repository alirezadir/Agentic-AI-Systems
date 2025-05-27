from pydantic import BaseModel
from typing import Optional
from agents import Agent, handoff, RunContextWrapper


# Define the data structure to pass during handoff
class EscalationData(BaseModel):
   reason: str
   priority: Optional[str]
   customer_tier: Optional[str]


# Handoff callback that processes the escalation data
async def process_escalation(ctx: RunContextWrapper, input_data: EscalationData):
   print(f"[ESCALATION] Reason: {input_data.reason}")
   print(f"[ESCALATION] Priority: {input_data.priority}")
   print(f"[ESCALATION] Customer tier: {input_data.customer_tier}")

   # You might use this data to prioritize responses, alert human agents, etc.


# Create an escalation agent
escalation_agent = Agent(
   name="Escalation Agent",
   instructions="""You handle complex or sensitive customer issues that require
   special attention. Always address the customer's concerns with extra care and detail.""",
)

# Create a service agent that can escalate with context
service_agent = Agent(
   name="Service Agent",
   instructions="""You are a customer service agent who handles general inquiries.
  
   For complex issues, escalate to the Escalation Agent and provide:
   - The reason for escalation
   - Priority level (Low, Normal, High, Urgent)
   - Customer tier if mentioned (Standard, Premium, VIP)""",
   handoffs=[
       handoff(
           agent=escalation_agent,
           on_handoff=process_escalation,
           input_type=EscalationData,
       )
   ],
)