from google.adk.agents.llm_agent import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search

gemini_model = Gemini(model="gemini-2.5-flash-lite")

root_agent = Agent(
    model=gemini_model,
    name="root_agent",
    description="A simple agent that can answer general questions.",
    instruction="You are a helpful assistant. Use Google Search for current info or if unsure.",
    tools=[google_search],
)
