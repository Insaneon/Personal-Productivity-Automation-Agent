# tools.py
import json
from pydantic import BaseModel, Field
from datetime import datetime

# --- Tool Schemas (Defining input types for the LLM) ---

class LogActionSchema(BaseModel):
    """Schema for the log_agent_action tool."""
    agent_thought: str = Field(description="The internal reasoning or decision made by the agent.")
    tool_name: str = Field(description="The name of the tool called, or 'Decision' if no tool was used.")
    outcome_summary: str = Field(description="A brief summary of the action outcome (e.g., 'Success', 'Failure', 'ClarificationNeeded').")

class ScheduleEventSchema(BaseModel):
    """Schema for scheduling a calendar event."""
    title: str = Field(description="The title of the calendar event.")
    start_time: str = Field(description="The start time of the event (e.g., 'YYYY-MM-DDTHH:MM:SS').")
    end_time: str = Field(description="The end time of the event (e.g., 'YYYY-MM-DDTHH:MM:SS').")

class AddTaskSchema(BaseModel):
    """Schema for adding a to-do task."""
    task_name: str = Field(description="The name or description of the task.")
    due_date: str = Field(description="The due date for the task (optional, use ISO format if provided).")
    priority: str = Field(description="The task priority (e.g., 'High', 'Medium', 'Low').")

class DraftEmailSchema(BaseModel):
    """Schema for drafting an email."""
    recipient: str = Field(description="The email address of the recipient.")
    subject: str = Field(description="The subject line of the email.")
    body: str = Field(description="The main body content of the email.")


# --- Tool Functions (The actual logic) ---

def log_agent_action(agent_thought: str, tool_name: str, outcome_summary: str) -> str:
    """
    MANDATORY TOOL: Logs agent decisions and actions to a central audit database (simulated here).
    Returns a confirmation string for internal use.
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "agent_thought": agent_thought,
        "tool_name": tool_name,
        "outcome": outcome_summary
    }
    # Writes log to console for demonstration. Replace with DB/File write in production.
    print("\n--- PPAA AUDIT LOG ---")
    print(json.dumps(log_entry, indent=2))
    print("----------------------\n")
    return f"Action logged successfully: {outcome_summary}"

def schedule_calendar_event(title: str, start_time: str, end_time: str) -> str:
    """Creates a calendar event and returns a success confirmation."""
    return f"SUCCESS: Event '{title}' simulated scheduled from {start_time} to {end_time}."

def add_todo_task(task_name: str, due_date: str = None, priority: str = "Medium") -> str:
    """Adds a new task to the user's to-do list."""
    due_info = f" Due: {due_date}" if due_date else ""
    return f"SUCCESS: Task '{task_name}' simulated added with {priority} priority.{due_info}"

def draft_email(recipient: str, subject: str, body: str) -> str:
    """Composes and saves an email draft."""
    return f"SUCCESS: Email draft simulated saved. To: {recipient}, Subject: {subject}. Body snippet: {body[:50]}..."

# List of all available tools
AVAILABLE_TOOLS = [
    (log_agent_action, LogActionSchema),
    (schedule_calendar_event, ScheduleEventSchema),
    (add_todo_task, AddTaskSchema),
    (draft_email, DraftEmailSchema)
]