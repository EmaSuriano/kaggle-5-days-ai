from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.memory import InMemoryMemoryService
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools import load_memory
from google.genai import types

import asyncio

ollama_model = LiteLlm(model="ollama_chat/gpt-oss:120b-cloud")

# Define constants used throughout the notebook
APP_NAME = "MemoryDemoApp"
USER_ID = "demo_user"

# ADK's built-in Memory Service for development and testing
memory_service = InMemoryMemoryService()

# Create Session Service
session_service = InMemorySessionService()  # Handles conversations

# Create agent
user_agent = Agent(
    model=ollama_model,
    name="MemoryDemoAgent",
    instruction="Answer user questions in simple words. Use load_memory tool if you need to recall past conversations.",
    tools=[
        load_memory
    ],  # Agent now has access to Memory and can search it whenever it decides to!
)

# Create runner with BOTH services
runner = Runner(
    agent=user_agent,
    app_name="MemoryDemoApp",
    session_service=session_service,
    memory_service=memory_service,  # Memory service is now available!
)


async def run_session(
    runner_instance: Runner, user_queries: list[str] | str, session_id: str = "default"
):
    """Helper function to run queries in a session and display responses."""
    print(f"\n### Session: {session_id}")

    # Create or retrieve session
    try:
        session = await session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_id
        )
    except:
        session = await session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_id
        )

    # Convert single query to list
    if isinstance(user_queries, str):
        user_queries = [user_queries]

    # Process each query
    for query in user_queries:
        print(f"\nUser > {query}")
        query_content = types.Content(role="user", parts=[types.Part(text=query)])

        # Stream agent response
        async for event in runner_instance.run_async(
            user_id=USER_ID, session_id=session.id, new_message=query_content
        ):
            if event.is_final_response() and event.content and event.content.parts:
                text = event.content.parts[0].text
                if text and text != "None":
                    print(f"Model: > {text}")


# uv run python -m memory_agent.agent
if __name__ == "__main__":
    asyncio.run(
        run_session(
            runner,
            "My favorite color is blue-green. Can you write a Haiku about it?",
            "conversation-01",
        )
    )

    session = asyncio.run(
        session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id="conversation-01"
        )
    )

    if session:
        asyncio.run(memory_service.add_session_to_memory(session))

    asyncio.run(run_session(runner, "What is my favorite color?", "color-test"))
