from typing import Optional
from pydantic import BaseModel
from agents import Agent, Runner, function_tool
import asyncio

# Define the weather response model
class WeatherResponse(BaseModel):
    temperature: float
    conditions: str
    location: str
    recommendation: Optional[str] = None

@function_tool
async def get_weather(city: str) -> WeatherResponse:
    """Get the current weather for a city.
    
    Args:
        city: The name of the city to get weather for
    """
    # Simulated weather data (in real app, you'd call a weather API)
    return WeatherResponse(
        temperature=72.5,
        conditions="Sunny with light clouds",
        location=city,
        recommendation="Great day for outdoor activities!"
    )

async def main():
    # Create the weather agent
    weather_agent = Agent(
        name="Weather Assistant",
        instructions="""You are a helpful weather assistant.
        When asked about weather, use the get_weather tool and provide friendly recommendations.
        Always mention both the temperature and conditions in your response.""",
        tools=[get_weather],
    )

    # Example queries
    queries = [
        "What's the weather like in San Francisco?",
        "Should I bring an umbrella in New York today?",
    ]

    for query in queries:
        print(f"\nQuery: {query}")
        result = await Runner.run(weather_agent, query)
        print(f"Response: {result.final_output}")

if __name__ == "__main__":
    asyncio.run(main()) 