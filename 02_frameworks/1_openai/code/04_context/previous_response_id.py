import asyncio

from agents import Agent, Runner



async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant. be VERY concise.",
    )

    result = await Runner.run(agent, "What is the largest country in South America?")
    print(result.final_output)
    # Brazil

    result = await Runner.run(
        agent,
        "What is the capital of that country?",
        previous_response_id=result.last_response_id,
    )
    print(result.final_output)
    # Brasilia


async def main_stream():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant. be VERY concise.",
    )

    result = Runner.run_streamed(agent, "What is the largest country in South America?")

    async for event in result.stream_events():
        if event.type == "raw_response_event" and event.data.type == "response.output_text.delta":
            print(event.data.delta, end="", flush=True)

    print()

    result = Runner.run_streamed(
        agent,
        "What is the capital of that country?",
        previous_response_id=result.last_response_id,
    )

    async for event in result.stream_events():
        if event.type == "raw_response_event" and event.data.type == "response.output_text.delta":
            print(event.data.delta, end="", flush=True)


if __name__ == "__main__":
    is_stream = input("Run in stream mode? (y/n): ")
    if is_stream == "y":
        asyncio.run(main_stream())
    else:
        asyncio.run(main())
