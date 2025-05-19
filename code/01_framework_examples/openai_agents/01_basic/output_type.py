from pydantic import BaseModel
from agents import Agent, Runner
import asyncio

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

text = """
Team meeting on March 15th at 2pm with John, Mary and Bob.
Project review scheduled for March 20th at 10am with the engineering team.
"""

agent = Agent(
    name="Calendar extractor",
    instructions="Extract calendar events from text",
    output_type=list[CalendarEvent]  
)

async def main():
    events = await Runner.run(agent, input=text)
    for event in events.final_output:
        print(f"Event: {event.name}")
        print(f"Date: {event.date}")
        print(f"Participants: {', '.join(event.participants)}")
        print()

if __name__ == "__main__":
    asyncio.run(main())