import asyncio
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
from core.llm_client import GeminiClient
from typing import Dict, Any

class QueryResolver:
    """
    Uses LLM to resolve user query to a Model Context Protocol (MCP) tool, then calls the tool via MCPClient and returns the result.
    """
    def __init__(self, llm_client: GeminiClient = None, mcp_url: str = "http://localhost:8000/api/v1/mcp"):
        self.llm_client = llm_client or GeminiClient()
        self.mcp_url = mcp_url


    async def resolve(self, query: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        # Discover available tools from MCP
        async with streamablehttp_client(self.mcp_url) as (read_stream, write_stream, _):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                tools = await session.list_tools()
                tool_names = [tool["name"] for tool in tools]
                prompt = (
                    f"You are an assistant that maps user queries to available tools. "
                    f"Given the query, respond with one of: {', '.join(tool_names)}. "
                    f"Respond ONLY with the tool name. Query: '" + query + "'"
                )
                tool_name = self.llm_client.call(prompt, {})
                tool_name = tool_name.strip().split()[0].replace('.', '').replace('_', '')
                if tool_name not in tool_names:
                    tool_name = tool_names[0]  # default fallback
                params = {k: v for k, v in request_data.items() if v is not None}
                tool_result = await session.call_tool(tool_name, params)
                return {"tool": tool_name, "result": tool_result}

    async def explain_result(self, tool_name: str, tool_result: Any, query: str) -> str:
        """
        Use the LLM to generate a user-friendly explanation of the tool result in the context of the user's query.
        """
        prompt = (
            f"Above is the result of calling one or more tools. The user cannot see the results, so you should explain them to the user if referencing them in your answer. "
            f"User query: '{query}'. Tool result: {tool_result}. "
            f"Explain the outcome in a clear, concise, and user-friendly way, summarizing what it means for the user."
        )
        return self.llm_client.call(prompt, {})

    async def resolve_and_explain(self, query: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        result = await self.resolve(query, request_data)
        explanation = await self.explain_result(result['tool'], result['result'], query)
        return {**result, "explanation": explanation}

def resolve_query(query, request_data):
    resolver = QueryResolver()
    return asyncio.run(resolver.resolve(query, request_data))

def resolve_query_with_explanation(query, request_data):
    resolver = QueryResolver()
    return asyncio.run(resolver.resolve_and_explain(query, request_data))
