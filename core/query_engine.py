from mcp.types import CreateMessageResult, CreateMessageRequestParams, TextContent
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp import ClientSession

from core.llm_client import GeminiClient
from mcp_client import MCPClient


class QueryResolver:
    def __init__(self, llm_client: GeminiClient):
        self.llm_client = llm_client

    async def answer_with_context(self, user_query: str, session: ClientSession, context) -> str:
        """
        High-level function to answer a user query using MCP.
        """
        return await self.llm_client.call(user_query, session, context)
