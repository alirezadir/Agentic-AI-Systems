# Airline Customer Support Bot

This project is an agentic customer support assistant for airlines. It can answer FAQs, handle seat changes, and triage requests between specialized agents.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. (Optional) Set up your Python version using `.python-version` or your preferred tool.

## Running the Bot

### Command Line Interface (CLI)

Run the bot in the terminal:
```bash
python main.py
```

### Web Chat Interface (Chainlit UI)

Run the bot with a web-based chat interface:
```bash
chainlit run app.py
```

This will start a local web server (usually at http://localhost:8000) where you can chat with the airline support bot in your browser.

## Features
- Ask about baggage, seats, wifi, or request seat changes
- Multi-agent handoff between FAQ and seat booking agents
- Works in both CLI and web UI modes
