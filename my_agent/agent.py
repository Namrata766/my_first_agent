from google.adk.agents import Agent
from google.adk.tools import google_search

def morning_greet(name: str) -> str:
    return f"Good morning, {name}! How can I assist you with Google Cloud today?"

def evening_greet(name: str) -> str:
    return f"Good evening, {name}! Hope you had a great day. How can I help you with Google Cloud?"

root_agent = Agent(
    name="my_first_agent",    
    description="An agent that answers the user queries related to Google Cloud.",   
    model="gemini-2.0-flash",
    instruction="""
    Ask the user for their name and start conversation base don user's greet.
    If user says "good morning" use morning_greet tool.
    If user says "good evening" use evening_greet tool.
    """,
    tools = [morning_greet, evening_greet]
)