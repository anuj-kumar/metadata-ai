import json

from google import genai
from google.genai import types
from typing import Any, Dict
from mcp import ClientSession


class GeminiClient:
    """
    Object-oriented client for calling a free LLM API (uses OpenAI's free GPT-3.5-turbo endpoint via openrouter.ai as an example).
    """

    def __init__(self, api_key: str = None):
        self.client = genai.Client(api_key=api_key)

    async def call(self, query: str, session: ClientSession, context=None) -> str:
        parts = [types.Part(text=query)]
        if context is not None:
            parts.append(types.Part(text=json.dumps(context)))
        contents = [
            types.Content(
                role="user", parts=parts
            )
        ]

        response = await self.client.aio.models.generate_content(
            model='gemini-2.0-flash',
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0,
                tools=[session],
            )
        )
        return response.text
