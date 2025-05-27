from models import EmailData, Person, Meeting, Task
from sample_data import sample_email
from agents import Agent, Runner
import asyncio

# Create an email processing agent
email_processor = Agent(
    name="Email Processor",
    instructions="""You are an email processing assistant that extracts structured information from emails.
    Parse the email content and extract:
    - Sender and recipient information
    - Main discussion points
    - Meeting details
    - Action items and tasks
    - Next steps
    
    Format the output according to the EmailData model structure.
    """,
)

async def process_email(email_content: str) -> EmailData:
    """Process email content and return structured data."""
    result = await Runner.run(
        email_processor,
        f"Please parse this email and extract structured information:\n\n{email_content}"
    )
    return result.final_output

async def main():
    try:
        print("\nProcessing sample email...")
        print("=" * 50)
        email_data = await process_email(sample_email)
        print("\nExtracted Email Data:")
        print("-" * 30)
        print(f"Subject: {email_data.subject}")
        print(f"From: {email_data.sender.name} ({email_data.sender.role})")
        print("\nRecipients:")
        for recipient in email_data.recipients:
            print(f"- {recipient.name}")
        print("\nMain Points:")
        for point in email_data.main_points:
            print(f"- {point}")
        print("\nMeetings:")
        for meeting in email_data.meetings:
            print(f"- {meeting.date} at {meeting.time} ({meeting.duration})")
        print("\nTasks:")
        for task in email_data.tasks:
            print(f"- {task.description} (Priority: {task.priority})")
        print("\nNext Steps:")
        print(email_data.next_steps)
        print("=" * 50)
    except Exception as e:
        print(f"Error processing email: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 