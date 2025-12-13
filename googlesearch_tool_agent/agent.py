from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="googlesearch_agent",    
    description="An agent that answers the user queries related to Animes using google search results.",   
    model="gemini-2.0-flash",
    instruction="""
    You are a helpful assistant specialized in finding information about Animes using Google Search.
    You also provide references for the information you provide.
    """,
    tools = [google_search]
)