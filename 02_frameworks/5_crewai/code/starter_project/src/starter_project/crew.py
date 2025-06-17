from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from .tools.custom_tool import WebSearchTool
import os

@CrewBase
class ResearchAndWritingCrew:
    """A crew for conducting research and creating content."""
    
    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True,
            tools=[WebSearchTool(api_key=os.getenv('SERPER_API_KEY'))]
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['writer'],
            verbose=True
        )

    @agent
    def reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['reviewer'],
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task']
        )

    @task
    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['writing_task']
        )

    @task
    def review_task(self) -> Task:
        return Task(
            config=self.tasks_config['review_task']
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Research and Writing crew."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        ) 