from google.adk.agents.llm_agent import Agent, LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

ollama_model = LiteLlm(model="ollama_chat/gpt-oss:120b-cloud")
gemini_model = Gemini(model="gemini-2.5-flash-lite")

mcp_image_server = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="npx",  # Run MCP server via npx
            args=[
                "-y",  # Argument for npx to auto-confirm install
                "@modelcontextprotocol/server-everything",
            ],
        ),
        timeout=30,
    )
)

# Create image agent with MCP integration
root_agent = LlmAgent(
    model=gemini_model,
    name="image_agent",
    instruction="Use the MCP Tool to generate images for user queries",
    tools=[mcp_image_server],
)
