
import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok", "agent": "summarizer_agent"}

@app.post("/summarize")
async def summarize(request: Request):
    try:
        body = await request.json()
        user_input = body.get("text", "")
        if not user_input:
            return JSONResponse({"error": "No text provided"}, status_code=400)
        import google.generativeai as genai
        api_key = os.environ.get("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Summarize in 2-3 sentences: " + user_input)
        return {"summary": response.text}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
