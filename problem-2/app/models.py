from pydantic import BaseModel
from typing import Optional, List, Dict

class Interaction(BaseModel):
    session_id: str
    message: str
    sender: str # "scammer" or "user" (though typically we just get the scammer message)

class Intelligence(BaseModel):
    bank_details: List[str] = []
    upi_ids: List[str] = []
    phishing_links: List[str] = []
    phone_numbers: List[str] = []
    crypto_addresses: List[str] = []

class HoneyPotResponse(BaseModel):
    session_id: str
    is_scam: bool
    response_message: str
    intelligence: Intelligence
    status: str # "engaged", "completed", "ignored"
