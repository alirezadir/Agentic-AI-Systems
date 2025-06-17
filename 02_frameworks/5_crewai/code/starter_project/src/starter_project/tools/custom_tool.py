from crewai_tools import SerperDevTool
from typing import Optional

class WebSearchTool(SerperDevTool):
    """Custom web search tool that extends SerperDevTool with additional functionality."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key=api_key)
        self.name = "Web Search Tool"
        self.description = """
        A tool for searching the web for information. Use this tool when you need to:
        1. Find up-to-date information about a topic
        2. Verify facts or claims
        3. Gather examples or case studies
        4. Research current trends or developments
        """ 