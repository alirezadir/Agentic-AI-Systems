from agents import Agent, Runner
from pydantic import BaseModel
import asyncio


class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str


def on_handoff(agent: Agent):
    print("Handoff called for agent: ", agent.name)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions=(
        "You are a history tutor who helps students understand historical topics. "
        "Explain important events, provide relevant context, and break down complex topics "
        "into understandable pieces."
    ),
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions", 
    instructions=(
        "You are a math tutor who helps students solve mathematical problems. "
        "Break down complex problems into steps, explain your reasoning clearly, "
        "and provide relevant examples to illustrate concepts."
    ),
)

triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "You are a triage agent who determines which specialist tutor can best help "
        "the student. For history questions, hand off to the History Tutor. For math "
        "questions, hand off to the Math Tutor."
    ),
    handoffs=[history_tutor_agent, math_tutor_agent],
)


async def main():
    # Example query to demonstrate handoff behavior
    result = await Runner.run(triage_agent, "What is the capital of France?")

    
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())