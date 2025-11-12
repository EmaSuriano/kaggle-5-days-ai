from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

model = LiteLlm(model="ollama_chat/gpt-oss:120b-cloud")


def get_current_weather(city: str) -> dict:
    """Get the current weather for a specified city.

    Args:
        city: The name of the city to get the current weather for.

    Returns:
        A dictionary containing the status, city name, and current weather.
    """
    return {"status": "success", "city": city, "weather": "sunny"}


root_agent = Agent(
    name="weather_agent",
    model=model,
    description="Agent to retrieve the current weather in a specified city.",
    instruction="You are a helpful agent who can retrieve the current weather in a specified city.",
    tools=[get_current_weather],
)
