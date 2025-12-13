from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.models import LlmRequest, LlmResponse
from google.genai import types
from google.adk.agents.callback_context import CallbackContext
from typing import Optional
from google.adk.tools import ToolContext


def check_access(callback_context: CallbackContext) -> Optional[types.Content]:
    """
    Checks if the user_id is in the allowed list.
    If yes -> allow agent/LLM execution (return None)
    If no -> skip LLM and return a message
    """
    session = callback_context._invocation_context.session
    user_id = session.user_id
    allowed_users = ["user_123", "user_abc", "user"]

    print(f"Checking access for user_id: {user_id}")

    if user_id in allowed_users:
        print(f"[Callback] Access granted for user_id: {user_id} - proceeding with agent execution.")
        return None
    else:
        print(f"[Callback] Access denied for user_id: {user_id} - skipping agent execution.")
        return types.Content(
            parts=[types.Part(text=f"\nAccess Denied: You do not have permission to use this agent.")],
            role="model"
        )

def log_completion(callback_context: CallbackContext) -> Optional[types.Content]:
    current_state = callback_context.state.to_dict()
    print(f"\n[Callback] Agent Execution Completed. Final State:\n{current_state}\n")
    print(f"======\n[Callback] Agent Execution Completed.======")
      

root_agent = Agent(
    model='gemini-2.0-flash',
    name='root_agent',
    description='A helpful assistant answering user queries.',
    instruction='Answer user queries to the best of your ability using available tools.',
    before_agent_callback=check_access,
    after_agent_callback=log_completion,
    output_key="result",
    tools=[google_search]
)