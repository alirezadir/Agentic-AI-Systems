# CrewAI Code Examples

This directory contains example implementations using the CrewAI framework.

## Setup

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

## Examples

### Starter Template (`starter_template.py`)
A basic example demonstrating:
- Creating agents with specific roles
- Defining tasks for each agent
- Setting up a crew to manage the workflow
- Running the crew with sequential task execution

## Usage

Run any example using:
```bash
python starter_template.py
```

## Additional Resources

- [CrewAI Documentation](https://github.com/crewAIInc/crewAI)
- [CrewAI Examples Repository](https://github.com/crewAIInc/crewAI-examples) 