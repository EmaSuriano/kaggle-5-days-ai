from google.adk.agents.llm_agent import Agent, LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import (
    StreamableHTTPServerParams,
)
import os

ollama_model = LiteLlm(model="ollama_chat/gpt-oss:120b-cloud")


mcp_github_server = McpToolset(
    connection_params=StreamableHTTPServerParams(
        url="https://api.githubcopilot.com/mcp/",
        headers={
            "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
            "X-MCP-Toolsets": "all",
            "X-MCP-Readonly": "true",
        },
    ),
)

# Create image agent with MCP integration
root_agent = LlmAgent(
    model=ollama_model,
    name="github_mcp_agent",
    instruction="You are a helpful assistant that can answer questions about GitHub.",
    tools=[mcp_github_server],
)
