# General-Purpose Swarm Multi-Agent Demo
# Requires: pip install git+https://github.com/openai/swarm.git

from swarm import Swarm, Agent, Result

def greet(context_variables, language):
    """
    Greet the user in the specified language using context variables.
    """
    user_name = context_variables.get("user_name", "User")
    greeting = "Hola" if language.strip().lower() == "spanish" else "Hello"
    message = f"{greeting}, {user_name}!"
    print(message)
    return message

# --- Agent Definitions ---

sales_agent = Agent(
    name="Sales Agent",
    instructions="You are a sales agent. Help the user with purchases.",
    functions=[],
)

def transfer_to_sales():
    """
    Transfer control to the sales agent.
    """
    return sales_agent

support_agent = Agent(
    name="Support Agent",
    instructions="You are a support agent. Help the user with issues.",
    functions=[transfer_to_sales],
)

def transfer_to_support():
    """
    Transfer control to the support agent.
    """
    return support_agent

def main_instructions(context_variables):
    """
    Generate main agent instructions using context variables.
    """
    user_name = context_variables.get("user_name", "User")
    return f"You are the main assistant. Greet {user_name} and help them with anything."

main_agent = Agent(
    name="Main Agent",
    instructions=main_instructions,
    functions=[greet, transfer_to_support],
)

def main():
    # Create the Swarm client
    client = Swarm()

    # Simulate a conversation
    messages = [
        {"role": "user", "content": "Hi!"},
        {"role": "user", "content": "Can you greet me in Spanish?"},
        {"role": "user", "content": "I need help with my order."},
        {"role": "user", "content": "Actually, I want to buy something."},
    ]

    context_variables = {"user_name": "Alice"}

    response = client.run(
        agent=main_agent,
        messages=messages,
        context_variables=context_variables
    )

    # Print the final agent and context
    print(f"Final agent: {response.agent.name}")
    print("Context variables:", response.context_variables)
    print("Conversation:")
    for msg in response.messages:
        print(f"{msg['role'].capitalize()}: {msg['content']}")

if __name__ == "__main__":
    main()


