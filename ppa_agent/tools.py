import json
from pydantic import BaseModel, Field
from datetime import datetime

class LogActionSchema(BaseModel):
    agent_thought: str = Field(description="The internal reasoning or decision made by the agent.")
    tool_name: str = Field(description="The name of the tool called, or 'Decision' if no tool was used.")
    outcome_summary: str = Field(description="A brief summary of the action outcome.")

class ScheduleEventSchema(BaseModel):
    title: str = Field(description="The title of the calendar event.")
    start_time: str = Field(description="The start time of the event (e.g., 'YYYY-MM-DDTHH:MM:SS').")
    end_time: str = Field(description="The end time of the event (e.g., 'YYYY-MM-DDTHH:MM:SS').")

class AddTaskSchema(BaseModel):
    task_name: str = Field(description="The name or description of the task.")
    due_date: str = Field(description="The due date for the task (optional, use ISO format if provided).")
    priority: str = Field(description="The task priority (e.g., 'High', 'Medium', 'Low').")

class DraftEmailSchema(BaseModel):
    recipient: str = Field(description="The email address of the recipient.")
    subject: str = Field(description="The subject line of the email.")
    body: str = Field(description="The main body content of the email.")


def log_agent_action(agent_thought: str, tool_name: str, outcome_summary: str) -> str:
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "agent_thought": agent_thought,
        "tool_name": tool_name,
        "outcome": outcome_summary
    }
    print("\n--- PPAA AUDIT LOG ---")
    print(json.dumps(log_entry, indent=2))
    print("----------------------\n")
    return f"Action logged successfully: {outcome_summary}"

def schedule_calendar_event(title: str, start_time: str, end_time: str) -> str:
    return f"SUCCESS: Event '{title}' simulated scheduled from {start_time} to {end_time}."

def add_todo_task(task_name: str, due_date: str = None, priority: str = "Medium") -> str:
    due_info = f" Due: {due_date}" if due_date else ""
    return f"SUCCESS: Task '{task_name}' simulated added with {priority} priority.{due_info}"

def draft_email(recipient: str, subject: str, body: str) -> str:
    return f"SUCCESS: Email draft simulated saved. To: {recipient}, Subject: {subject}. Body snippet: {body[:50]}..."


AVAILABLE_TOOLS = [
    log_agent_action,
    schedule_calendar_event,
    add_todo_task,
    draft_email
]