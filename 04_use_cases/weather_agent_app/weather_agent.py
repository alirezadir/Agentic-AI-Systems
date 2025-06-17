from agents import Agent, Runner, function_tool
from weather_api import WeatherResponse, get_weather

@function_tool
async def get_weather_tool(city: str) -> WeatherResponse:
    """Get the current weather for a city.
    
    Args:
        city: The name of the city to get weather for
    Returns:
        WeatherResponse object containing temperature, conditions and recommendation
    """
    print(f"get_weather tool called with city: {city}")
    return get_weather(city)

class WeatherAgent:
    def __init__(self):
        self.agent = Agent(
            name="Weather Agent",
            instructions="""
            """You are a weather assistant that can provide current weather information.  
            When asked about weather, use the get_weather tool to fetch accurate data.
            If the user doesn't specify a country code and there might be ambiguity,
            ask for clarification (e.g., Paris, France vs. Paris, Texas).
            
            Provide friendly commentary along with the weather data, such as clothing suggestions
            or activity recommendations based on the conditions.
            """,
            model="gpt-3.5-turbo",
            tools=[get_weather_tool],
        )

    async def run_query(self, query: str) -> str:
        """Run a weather query through the agent.
        
        Args:
            query: The weather query to process
        Returns:
            The agent's response as a string
        """
        result = await Runner.run(self.agent, query)
        return result.final_output

# Create a singleton instance
weather_agent = WeatherAgent()

