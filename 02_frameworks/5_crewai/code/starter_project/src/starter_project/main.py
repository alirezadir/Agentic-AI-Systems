#!/usr/bin/env python
import os
from dotenv import load_dotenv
from starter_project.crew import ResearchAndWritingCrew

def main():
    """Run the research and writing crew."""
    # Load environment variables
    load_dotenv()
    
    # Define the topic for research and writing
    topic = "Artificial Intelligence in Healthcare"
    
    # Create and run the crew
    crew = ResearchAndWritingCrew()
    result = crew.crew().kickoff(inputs={'topic': topic})
    
    print("\nFinal Result:")
    print(result)

if __name__ == "__main__":
    main() 