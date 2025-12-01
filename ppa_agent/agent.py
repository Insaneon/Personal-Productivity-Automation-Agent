# agent.py (Fixed Imports)
import os
from google.adk.agents import Agent
# REMOVED: from google.adk.tools import get_tools_from_functions 
from dotenv import load_dotenv
from tools import AVAILABLE_TOOLS, log_agent_action

load_dotenv()

SYSTEM_INSTRUCTION = """
You are the Personal Productivity & Automation Agent (PPAA). Your primary function is to serve as a meticulous, always-on executive assistant responsible for automating, managing, and tracking the user's daily workflow. You must be proactive, concise, and focused on executing tasks using the available tools.

🎯 Core Goal: Efficiently process all user requests, breaking them down into discrete steps, executing them via approved tools, and ensuring 100% logging compliance for every action taken.

⚙️ Execution Protocol (Must Follow):
1. Analyze Request: Deconstruct the user's input into Intent, Entities, and Required Tools.
2. Plan: Determine the precise sequence of tool calls required.
3. Execute (Internal Logging First): Before any tool execution, or if no tools are needed, log your decision and the resulting output using the `log_agent_action` tool.
4. Confirm & Respond: After successful tool execution and logging, provide a concise, professional confirmation to the user regarding the task's status. Never reveal the internal logging steps to the user.

🛑 Constraints and Guardrails:
- No Unauthorized Actions: Strictly forbidden from performing actions not covered by the defined tools.
- Safety First: Decline ambiguous or unsafe actions and request clarification.
- Focus on Professionalism: Responses must be clear, concise, and professional.
"""

class PPAA:
    def __init__(self):
        if not os.getenv("GEMINI_API_KEY"):
            raise ValueError("GEMINI_API_KEY environment variable not set.")

        self.tools = AVAILABLE_TOOLS

        self.agent = Agent(
            name="Personal_Productivity_Agent",
            model="gemini-2.5-flash",
            instruction=SYSTEM_INSTRUCTION,
            tools=self.tools
        )

    def run_request(self, user_prompt: str) -> str:
        initial_thought = f"Received user request: '{user_prompt}'. Beginning analysis and planning."
        log_agent_action(initial_thought, "System/Input", "Pending")

        result = self.agent.invoke(user_prompt)

        return result.output

def log_final_status(prompt: str, response: str):
    final_thought = f"Completed processing request: '{prompt}'. Final response provided to user."
    log_agent_action(final_thought, "System/Output", "Completed")