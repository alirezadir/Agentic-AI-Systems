from agents import Agent, handoff, Runner, RunContextWrapper
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Create specialist agents
billing_agent = Agent(
   name="Billing Agent",
   instructions="""You are a billing specialist who helps customers with payment issues.
   Focus on resolving billing inquiries, subscription changes, and refund requests.
   If asked about technical problems or account settings, explain that you specialize
   in billing and payment matters only.""",
)

technical_agent = Agent(
   name="Technical Agent",
   instructions="""You are a technical support specialist who helps with product issues.
   Assist users with troubleshooting, error messages, and how-to questions.
   Focus on resolving technical problems only.""",
)


# Create an agent that handles account-related questions
account_agent = Agent(
   name="Account Management",
   instructions="""You help customers with account-related issues such as
   password resets, account settings, and profile updates.""",
)

# Create a triage agent that can hand off to specialists
triage_agent = Agent(
   name="Customer Service",
   instructions="""You are the initial customer service contact who helps direct
   customers to the right specialist.
  
   If the customer has billing or payment questions, hand off to the Billing Agent.
   If the customer has technical problems or how-to questions, hand off to the Technical Agent.
   For general inquiries or questions about products, you can answer directly.
  
   Always be polite and helpful, and ensure a smooth transition when handing off to specialists.""",
   handoffs=[billing_agent, technical_agent],  # Direct handoff to specialist agents
)

# Custom handoff callback function
async def log_account_handoff(ctx: RunContextWrapper[None]):
   print(
       f"[LOG] Account handoff triggered at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
   )
   # In a real app, you might log to a database or alert a human supervisor


# Create a triage agent with customized handoffs
enhanced_triage_agent = Agent(
   name="Enhanced Customer Service",
   instructions="""You are the initial customer service contact who directs
   customers to the right specialist.
  
   If the customer has billing or payment questions, hand off to the Billing Agent.
   If the customer has technical problems, hand off to the Technical Agent.
   If the customer needs to change account settings, hand off to the Account Management agent.
   For general inquiries, you can answer directly.""",
   handoffs=[
       billing_agent,  # Basic handoff
       handoff(  # Customized handoff
           agent=account_agent,
           on_handoff=log_account_handoff,  # Callback function
           tool_name_override="escalate_to_account_team",  # Custom tool name
           tool_description_override="Transfer the customer to the account management team for help with account settings, password resets, etc.",
       ),
       technical_agent,  # Basic handoff
   ],
)

async def handle_customer_request(request):
   runner = Runner()
   result = await runner.run(triage_agent, request)
   return result


# Example customer inquiries
billing_inquiry = (
   "I was charged twice for my subscription last month. Can I get a refund?"
)
technical_inquiry = (
   "The app keeps crashing when I try to upload photos. How can I fix this? Give me the shortest solution possible."
)
general_inquiry = "What are your business hours?"

import asyncio

async def main():
    # Process the different types of inquiries
    billing_response = await handle_customer_request(billing_inquiry)
    print(f"Billing inquiry response:\n{billing_response.final_output}\n")

    technical_response = await handle_customer_request(technical_inquiry)
    print(f"Technical inquiry response:\n{technical_response.final_output}\n")

    general_response = await handle_customer_request(general_inquiry)
    print(f"General inquiry response:\n{general_response.final_output}")

    result = await Runner.run(
        enhanced_triage_agent, "I need to change my password."
    )
    print(f"Account management inquiry response:\n{result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())