from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.models import LlmRequest, LlmResponse
from google.genai import types
from google.adk.agents.callback_context import CallbackContext
from typing import Optional
from google.adk.tools import ToolContext


def before_model(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    # Appends instructions to the last user message before sending to the LLM.
    agent_name = callback_context.agent_name

    #Find last user message
    last_user_message = ""
    if llm_request.contents and len(llm_request.contents) > 0:
        for content in reversed(llm_request.contents):
            if content.role == "user" and content.parts and len(content.parts) > 0:
                if hasattr(content.parts[0], 'text') and content.parts[0].text:
                    last_user_message = content.parts[0].text
                    break

    print("=== Model Request Started ===")
    print(f"Agent: {agent_name}")
          
    if last_user_message:
        print(f"User Message: {last_user_message[:100]}")  # Print first 100 characters
        
        # Append instructions to the last user message
        content_part = content.parts[0]
        content_part.text += "\nPlease respond politely and keep the anser under 50 words."  

        # Log modified message
        print(f"Modified User Message: {content_part.text[:150]}")  # Print first 150 characters 
        print("=== Model Request Completed ===")


def after_model(callback_context: CallbackContext, llm_response: LlmResponse) -> Optional[LlmResponse]:
    """Converts the model response text to uppercase."""
    if not llm_response or not llm_response.content or not llm_response.content.parts:
        return None
    for part in llm_response.content.parts:
        if hasattr(part, 'text') and part.text:
            part.text = part.text.upper()

    return llm_response
        

root_agent = Agent(
    model='gemini-2.0-flash',
    name='root_agent',
    description='A helpful assistant answering user queries.',
    instruction='Answer user queries to the best of your ability using available tools.',
    before_model_callback=before_model,
    after_model_callback=after_model,
    output_key="result",
    tools=[google_search]
)