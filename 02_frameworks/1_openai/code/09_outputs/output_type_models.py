from agents import Agent, Runner
from dotenv import load_dotenv
from models import EmailData, Person, Meeting, Task
from sample_data import sample_email


load_dotenv()

   # Create an email extraction agent with structured output
email_extractor = Agent(
   name="Email Extractor",
   instructions="""You are an assistant that extracts structured information from emails.
  
   When given an email, carefully identify:
   - Subject and main points
   - People mentioned (names, roles, contact info)
   - Meetings (dates, times, locations)
   - Tasks or action items (with assignees and deadlines)
   - Next steps or follow-ups
  
   Extract this information as structured data. If something is unclear or not mentioned,
   leave those fields empty rather than making assumptions.
   """,
   output_type=EmailData,  # This tells the agent to return data in EmailData format
)



async def process_email(email_text):
   runner = Runner()
   result = await runner.run(
       email_extractor,
       f"Please extract information from this email:\n\n{email_text}"
   )

   # The result is already a structured EmailData object
   return result


# Process the sample email
import asyncio
result = asyncio.run(process_email(sample_email))

# Display the extracted information
result = result.final_output

print(f"Subject: {result.subject}")
print(f"From: {result.sender.name} ({result.sender.role})")
print("\nMain points:")
for point in result.main_points:
   print(f"- {point}")

print("\nMeetings:")
for meeting in result.meetings:
   print(f"- {meeting.date} at {meeting.time}, Location: {meeting.location}")

print("\nTasks:")
for task in result.tasks:
   print(f"- {task.description}")
   print(
       f"  Assignee: {task.assignee}, Deadline: {task.deadline}, Priority: {task.priority}"
   )