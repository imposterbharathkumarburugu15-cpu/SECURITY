import sys
import os

# Allow running via `python app/main.py`
if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    __package__ = "app"

from fastapi import FastAPI, HTTPException, Security, Header
from pydantic import BaseModel
from .models import Interaction, HoneyPotResponse
from .agent import agent

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
    return {"status": "active", "service": "Agentic Honey-Pot"}

@app.post("/analyze", response_model=HoneyPotResponse)
def analyze_interaction(input_data: ScammerInput, api_key: str = Security(verify_api_key)):
    """
    Analyzes the incoming message, detects if it's a scam, extracting intelligence,
    and generates a persona-based response.
    """
    try:
        is_scam = agent.detect_scam(input_data.message)
        intelligence = agent.extract_intelligence(input_data.message)
        response_text = agent.generate_response(input_data.message, is_scam, input_data.session_id)
        
        return HoneyPotResponse(
            session_id=input_data.session_id,
            is_scam=is_scam,
            response_message=response_text,
            intelligence=intelligence,
            status="engaged" if is_scam else "ignored"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
