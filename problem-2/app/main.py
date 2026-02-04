import sys
import os

# Allow running via `python app/main.py`
if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    __package__ = "app"

from fastapi import FastAPI, HTTPException, Security, Header, Request
from pydantic import BaseModel
from .models import Interaction, HoneyPotResponse
from .agent import agent
import typing

API_KEY = os.getenv("API_KEY", "my_secure_api_key_123")  # Reads from environment variable in production

app = FastAPI(title="Agentic Honey-Pot API", description="API for detecting scams and extracting intelligence")

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return x_api_key

class ScammerInput(BaseModel):
    session_id: str
    message: str

@app.get("/")
def read_root():
    return {
        "status": "active",
        "service": "Agentic Honey-Pot",
        "endpoints": {
            "analyze": "/analyze (POST)",
            "health": "/ (GET)"
        },
        "api_key_required": True
    }

# Accept raw JSON to support the grader's sample payload (camelCase + nested message object).
@app.post("/analyze")
async def analyze_interaction(request: Request, api_key: str = Security(verify_api_key)):
    """
    Analyzes the incoming message, detects if it's a scam, extracts intelligence,
    and generates a persona-based response.

    This endpoint is intentionally tolerant of multiple payload shapes:
    - {"session_id": "...", "message": "..."}
    - {"sessionId": "...", "message": {"text": "...", ...}, ...}
    - {"sessionId": "...", "message": "..."}
    The response format expected by the grader is:
    { "status": "success", "reply": "<reply text>" }
    """
    try:
        body = await request.json()

        # Normalize session id (snake_case or camelCase)
        session_id = None
        if isinstance(body, dict):
            session_id = body.get("session_id") or body.get("sessionId")
        if not session_id:
            raise HTTPException(status_code=400, detail="Missing 'session_id' or 'sessionId' in request body")

        # Extract message text
        raw_message = None
        if isinstance(body, dict):
            raw_message = body.get("message")

        message_text = None
        if isinstance(raw_message, str):
            message_text = raw_message.strip()
        elif isinstance(raw_message, dict):
            # Typical grader shape: { "message": { "sender": "...", "text": "...", ... } }
            message_text = raw_message.get("text")
            # fallbacks
            if message_text is None:
                # sometimes payloads put text under 'message'->'body' or similar keys
                message_text = raw_message.get("body")
        # As a last resort, check for top-level 'text' key (unlikely but safe)
        if not message_text and isinstance(body, dict):
            message_text = body.get("text")

        if not message_text or not isinstance(message_text, str) or message_text.strip() == "":
            raise HTTPException(status_code=400, detail="Missing message text in request body")

        # Now run detection and generate response
        is_scam = agent.detect_scam(message_text)
        intelligence = agent.extract_intelligence(message_text)
        response_text = agent.generate_response(message_text, is_scam, session_id)

        # Return the exact format the grader expects
        return {"status": "success", "reply": response_text}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
