from agents import Agent, function_tool

import asyncio

from pydantic import BaseModel

from agents import Agent, Runner, function_tool


class Weather(BaseModel):
    city: str
    temperature_range: str
    conditions: str

@function_tool
async def get_weather(city: str) -> str:
    """
    Fetch the weather for a given location.

    Args:
        city: The city to fetch the weather for.
    """
    print(f"[debug] get_weather tool called with city: {city}")
    return Weather(city=city, temperature_range="14-20C", conditions="Sunny with wind.")

agent = Agent(
    name="Hello world",
    instructions="You are a helpful agent.",
    tools=[get_weather],
)


async def main():
    result = await Runner.run(agent, input="What's the weather in Tokyo?")
    print(result.final_output)
    # The weather in Tokyo is sunny.


if __name__ == "__main__":
    asyncio.run(main())





agent = Agent(
    name="Hello world",
    instructions="You are a helpful agent.",
    tools=[get_weather],
)