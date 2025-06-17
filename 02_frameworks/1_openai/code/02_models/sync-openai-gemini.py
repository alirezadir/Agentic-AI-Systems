import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

# Load environment variables from .env file
load_dotenv()

# Get Gemini API key from environment
# you can get a key from https://makersuite.google.com/app
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please add it to your .env file.")

# Initialize Gemini client with OpenAI-compatible endpoint
# Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Configure the model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Set up run configuration
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Initialize the agent
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=model
)

# Run the agent synchronously
print("CALLING GOOGLE GEMINI AGENT:\n")
result = Runner.run_sync(agent, "Hello, how are you.", run_config=config)
print(result.final_output)