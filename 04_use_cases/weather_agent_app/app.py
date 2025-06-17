import os
import chainlit as cl
from dotenv import load_dotenv
from weather_agent import weather_agent

# Load environment variables
load_dotenv()

# Environment validation
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set")

@cl.on_chat_start
async def start():
    """Send a welcome message when the chat starts."""
    await cl.Message(
        content="👋 Welcome to the Weather Assistant! Ask me about the weather in any city.",
        author="Weather Bot"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    """Process incoming chat messages."""
    try:
        # Get response from weather agent
        response = await weather_agent.run_query(message.content)
        
        # Send response back to user
        await cl.Message(
            content=response,
            author="Weather Bot"
        ).send()
    
    except Exception as e:
        # Handle errors gracefully
        error_message = f"Sorry, I encountered an error: {str(e)}"
        await cl.Message(
            content=error_message,
            author="Weather Bot"
        ).send() 