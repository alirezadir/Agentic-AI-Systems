# Multi-Agent Workflow 

-  We use the `AgentWorkflow` class to create multi-agent systems. 
- Specifically, we will create a system that can generate a report on a given topic

- `AgentWorkflow`: A class in LlamaIndex designed to manage multi-agent systems, facilitating task delegation and state sharing among agents.

## Setup

* **LLM Initialization**:

  ```python
  from llama_index.llms.openai import OpenAI

  llm = OpenAI(model="gpt-4o", api_key="sk-...")
  ```

<!-- * **Installation**:

  ```bash
  %pip install llama-index
  %pip install tavily-python
  ``` -->

## System Design

* **Agents**:

  1. **ResearchAgent**: Searches the web for information on a given topic.
  2. **WriteAgent**: Writes a report using information gathered by the ResearchAgent.
  3. **ReviewAgent**: Reviews the report and provides feedback.

* **Tools**:

  * `web_search`: Searches the web for information.
  * `record_notes`: Records notes on a given topic.
  * `write_report`: Writes a report using gathered information.
  * `review_report`: Reviews the report and provides feedback.

* **State Management**: Utilizes the `Context` class to pass and manage state between agents.

## Implementation Details

* **Web Search Tool**:

  ```python
  from tavily import AsyncTavilyClient
  from llama_index.core.workflow import Context

  async def search_web(query: str) -> str:
      """Useful for using the web to answer questions."""
      client = AsyncTavilyClient(api_key="tvly-...")
      return str(await client.search(query))
  ```

* **Record Notes Tool**:

  ```python
  async def record_notes(ctx: Context, notes: str, notes_title: str) -> str:
      """Useful for recording notes on a given topic."""
      current_state = await ctx.get("state")
      if "research_notes" not in current_state:
          current_state["research_notes"] = {}
      current_state["research_notes"][notes_title] = notes
      await ctx.set("state", current_state)
      return "Notes recorded."
  ```

* **Write Report Tool**:

  ```python
  async def write_report(ctx: Context, report_content: str) -> str:
      """Useful for writing a report on a given topic."""
      current_state = await ctx.get("state")
      current_state["report_content"] = report_content
      await ctx.set("state", current_state)
      return "Report written."
  ```

* **Review Report Tool**:

  ```python
  async def review_report(ctx: Context, review: str) -> str:
      """Useful for reviewing a report and providing feedback."""
      current_state = await ctx.get("state")
      current_state["review"] = review
      await ctx.set("state", current_state)
      return "Report reviewed."
  ```

* **Agent Definitions**:

  ```python
  from llama_index.core.agent.workflow import FunctionAgent

  research_agent = FunctionAgent(
      name="ResearchAgent",
      description="Searches the web for information on a given topic.",
      system_prompt="You are a research assistant. Use the web_search tool to find information and record_notes to save it.",
      tools=[search_web, record_notes],
      llm=llm,
      can_handoff_to=["WriteAgent"]
  )

  write_agent = FunctionAgent(
      name="WriteAgent",
      description="Writes a report using the information found by the ResearchAgent.",
      system_prompt="You are a writer. Use the write_report tool to draft the report based on the research notes.",
      tools=[write_report],
      llm=llm,
      can_handoff_to=["ReviewAgent"]
  )

  review_agent = FunctionAgent(
      name="ReviewAgent",
      description="Reviews the report and provides feedback.",
      system_prompt="You are a reviewer. Use the review_report tool to critique the report.",
      tools=[review_report],
      llm=llm
  )
  ```

* **AgentWorkflow Initialization**:

  ```python
  from llama_index.core.agent.workflow import AgentWorkflow

  agent_workflow = AgentWorkflow(
      agents=[research_agent, write_agent, review_agent],
      root_agent=research_agent.name,
      initial_state={
          "research_notes": {},
          "report_content": "Not written yet.",
          "review": "Review required.",
      },
  )
  ```

## Running the Workflow

* **Execution**:

  ```python
  await agent_workflow.run()
  ```

This setup creates a sequential multi-agent system where each agent performs its designated task and passes control to the next, maintaining a shared state throughout the workflow.
