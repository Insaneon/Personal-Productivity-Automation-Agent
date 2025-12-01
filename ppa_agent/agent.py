# agent.py
import os
from google.adk.agents import Agent
from google.adk.tools import get_tools_from_functions
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import the tools defined in tools.py
from ppa_agent.tools import AVAILABLE_TOOLS, log_agent_action

class PPAA:
    """
    The Personal Productivity & Automation Agent (PPAA) class.
    Handles initialization, configuration, and running the agent.
    """
    def __init__(self):
        # 1. API Key Check
        if not os.getenv("GEMINI_API_KEY"):
            raise ValueError("GEMINI_API_KEY environment variable not set. Please create a .env file.")

        # 2. Convert raw functions into ADK Tools
        self.tools = get_tools_from_functions(AVAILABLE_TOOLS)

        # 3. The Professional System Prompt
        self.system_instruction = """
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

        # 4. Initialize the ADK Agent
        self.agent = Agent(
            name="Personal_Productivity_Agent",
            model="gemini-2.5-flash",  # Recommended model for task execution
            instruction=self.system_instruction,
            tools=self.tools
        )

    def run_request(self, user_prompt: str) -> str:
        """Processes a single user prompt with the agent."""
        
        # 1. Log the incoming request and initial decision
        initial_thought = f"Received user request: '{user_prompt}'. Beginning analysis and planning."
        log_agent_action(initial_thought, "System/Input", "Pending")

        # 2. Execute the request through the ADK Agent
        result = self.agent.run(user_prompt)

        # 3. The agent's final output (the professional confirmation)
        return result.output

# Helper to log the final interaction completion
def log_final_status(prompt: str, response: str):
    """Logs the completion of the full interaction for audit."""
    final_thought = f"Completed processing request: '{prompt}'. Final response provided to user."
    log_agent_action(final_thought, "System/Output", "Completed")