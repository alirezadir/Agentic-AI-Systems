# Weather Agent

A weather assistant that provides weather information and recommendations using OpenAI's Agents SDK, available through both CLI and web chat interfaces.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Running the Agent

##### Option 1: Command Line Interface (main.py)

Run the agent through the command line to process predefined weather queries:

```bash
python main.py
```

This will run through a set of example queries and display the responses in the terminal.

##### Option 2: Web Chat Interface (app.py)

To run the web-based chat interface, you must use the `chainlit` command:

```bash
# Install chainlit if you haven't already
pip install chainlit

# Run the app
chainlit run app.py
```

This will:
1. Start a local web server (typically at http://localhost:8000)
2. Automatically open your default web browser to the chat interface
3. Allow you to:
   - Chat with the weather assistant in real-time
   - Ask about weather in any city
   - Get immediate responses with weather information and recommendations

> **Note**: Running `python app.py` directly will not work - you must use the `chainlit run` command to start the web interface.

## Project Structure

```
weather_agent/
 weather_api/
    __init__.py
    weather_service.py
 weather_agent.py
 main.py
 app.py
 requirements.txt
```

- `weather_api/`: Contains weather service implementation
- `weather_agent.py`: Core agent implementation
- `main.py`: CLI interface
- `app.py`: Web chat interface
- `requirements.txt`: Project dependencies

## Example Queries

- "What's the weather like in San Francisco?"
- "Should I bring an umbrella in New York today?"
- "How's the weather in Tokyo right now?"
