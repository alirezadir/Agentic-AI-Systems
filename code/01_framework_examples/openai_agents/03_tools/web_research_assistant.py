from agents import Agent, Runner, WebSearchTool, function_tool
from dotenv import load_dotenv
import asyncio

load_dotenv()

@function_tool
def location_aware_search(query: str) -> str:
    """Search the web with location context."""
    search_tool = WebSearchTool(
        user_location="San Francisco, CA",
        search_context_size=3
    )
    return search_tool.search(query)

# Create a research assistant with web search capability
research_assistant = Agent(
   name="Research Assistant",
   instructions="""You are a research assistant that helps users find and summarize information.
   When asked about a topic:
   1. Search the web for relevant, up-to-date information
   2. Synthesize the information into a clear, concise summary
   3. Structure your response with headings and bullet points when appropriate
   4. Always cite your sources at the end of your response
  
   If the information might be time-sensitive or rapidly changing, mention when the search was performed.
   """,
   tools=[WebSearchTool()] # location_aware_search
)

async def research_topic(topic):
   result = await Runner.run(research_assistant, f"Please research and summarize: {topic}. Only return the found links with very minimal text.")
   return result.final_output

async def main():
    # Example topic to research
    topic = "Latest developments in AI agents and their applications in 2025"
    
    try:
        print(f"\nResearching topic: {topic}\n")
        result = await research_topic(topic)
        print("\nResearch Results:")
        print("=" * 50)
        print(result)
        print("=" * 50)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())