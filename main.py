import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from summarizer.agent import root_agent

app = FastAPI()
session_service = InMemorySessionService()
runner = Runner(agent=root_agent, app_name="summarizer", session_service=session_service)

@app.get("/")
def health():
    return {"status": "ok", "agent": "summarizer_agent"}

@app.post("/summarize")
async def summarize(request: Request):
    body = await request.json()
    user_input = body.get("text", "")
    if not user_input:
        return JSONResponse({"error": "No text provided"}, status_code=400)

    session = await session_service.create_session(app_name="summarizer", user_id="user1")
    content = types.Content(role="user", parts=[types.Part(text=user_input)])

    response_text = ""
    async for event in runner.run_async(
        user_id="user1",
        session_id=session.id,
        new_message=content
    ):
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if part.text:
                    response_text += part.text

    return {"summary": response_text}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
