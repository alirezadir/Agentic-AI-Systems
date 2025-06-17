# CrewAI Starter Template
# This file demonstrates a basic setup for a CrewAI project.

from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Define Agents
researcher = Agent(
    role="Research Analyst",
    goal="Conduct thorough research on given topics",
    backstory="""You are an expert research analyst with a keen eye for detail 
    and a talent for finding relevant information quickly.""",
    verbose=True,
    allow_delegation=False
)

writer = Agent(
    role="Content Writer",
    goal="Create engaging and informative content based on research",
    backstory="""You are a skilled content writer with experience in creating 
    clear, concise, and engaging content across various topics.""",
    verbose=True,
    allow_delegation=False
)

reviewer = Agent(
    role="Content Reviewer",
    goal="Review and improve content quality",
    backstory="""You are a meticulous content reviewer with a strong attention 
    to detail and a talent for improving content quality.""",
    verbose=True,
    allow_delegation=False
)

# Define Tasks
research_task = Task(
    description="""Research the topic 'The Impact of Artificial Intelligence on Healthcare' 
    and gather key information about recent developments, benefits, and challenges.""",
    agent=researcher
)

write_task = Task(
    description="""Write a comprehensive article about 'The Impact of Artificial Intelligence 
    on Healthcare' based on the research provided. Focus on making it engaging and informative.""",
    agent=writer
)

review_task = Task(
    description="""Review the article about AI in healthcare. Check for accuracy, clarity, 
    and engagement. Provide suggestions for improvement.""",
    agent=reviewer
)

# Create Crew
crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[research_task, write_task, review_task],
    verbose=2,
    process=Process.sequential
)

# Run the Crew
if __name__ == "__main__":
    result = crew.kickoff()
    print("\nFinal Result:")
    print(result) 