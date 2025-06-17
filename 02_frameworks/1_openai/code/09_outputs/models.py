from pydantic import BaseModel
from typing import List, Optional

# Define person data model
class Person(BaseModel):
    name: str
    role: Optional[str]
    contact: Optional[str]

# Define meeting data model
class Meeting(BaseModel):
    date: str
    time: str
    location: Optional[str]
    duration: Optional[str]

# Define task data model
class Task(BaseModel):
    description: str
    assignee: Optional[str]
    deadline: Optional[str]
    priority: Optional[str]

# Define the complete email data model
class EmailData(BaseModel):
    subject: str
    sender: Person
    recipients: List[Person]
    main_points: List[str]
    meetings: List[Meeting]
    tasks: List[Task]
    next_steps: Optional[str] 