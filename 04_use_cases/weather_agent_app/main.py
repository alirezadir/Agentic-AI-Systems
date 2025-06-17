import asyncio
import os
from dotenv import load_dotenv
from weather_agent import weather_agent

# Load environment variables
load_dotenv()

# Environment validation
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set")

async def main():
    # Example queries
    queries = [
        "What's the weather like in San Francisco?",
        "Should I bring an umbrella in New York today?",
        "How's the weather in Tokyo right now?",
    ]

    # Process queries
    for query in queries:
        print(f"\nQuery: {query}")
        try:
            response = await weather_agent.run_query(query)
            print(f"Response: {response}")
            print("-" * 50)
        except Exception as e:
            print(f"Error processing query: {str(e)}")
            print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main())
