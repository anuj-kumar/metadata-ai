from fastapi import FastAPI, Body, Request
from fastapi.responses import JSONResponse
import uvicorn

from config import Config
from core.llm_client import GeminiClient
from core.query_engine import QueryResolver
from feedback.tracking import track_interaction, FeedbackSignal
from dotenv import load_dotenv
from mcp_client import MCPClient, ClientSession

load_dotenv()
app = FastAPI()
llm_client = GeminiClient(Config.GEMINI_API_KEY)
query_resolver = QueryResolver(llm_client)


@app.post("/api/v1/query")
async def query_endpoint(request: Request):
    data = await request.json()
    client = MCPClient()
    await client.connect_to_server("mcp_server.py")
    query = data.get("query")

    if not query:
        return JSONResponse(status_code=400, content={"error": "Missing 'query' in request body"})
    session: ClientSession = await client.get_session()
    reply = await query_resolver.answer_with_context(query, session, data.get("context", {}))
    return {"reply": reply}


@app.post("/api/v1/feedback")
async def feedback_endpoint(feedback: FeedbackSignal = Body(...)):
    track_interaction(feedback)
    return {"status": "ok", "message": "success"}


if __name__ == "__main__":
    uvicorn.run("api_main:app", host="0.0.0.0", port=8000, reload=True)
