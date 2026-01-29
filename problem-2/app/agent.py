import re
import random
from typing import Dict, List
from .models import Intelligence

# Enum-like states
STATE_INITIAL = "INITIAL"
STATE_ENGAGED = "ENGAGED"
STATE_BAITING = "BAITING"
STATE_STALLING = "STALLING"

class SessionState:
    def __init__(self):
        self.state = STATE_INITIAL
        self.turns_count = 0
        self.scam_score = 0

class HoneyPotAgent:
    def __init__(self):
        self.sessions: Dict[str, SessionState] = {}
        self.persona_name = "Grandma Gertrude"
    
    def get_session(self, session_id: str) -> SessionState:
        if session_id not in self.sessions:
            self.sessions[session_id] = SessionState()
        return self.sessions[session_id]

    def detect_scam(self, message: str) -> bool:
        """
        Weighted scoring for scam detection.
        """
        message_lower = message.lower()
        score = 0
        
        keywords = {
            "urgency": ["urgent", "immediately", "now", "quick", "deadline"],
            "money": ["bank", "transfer", "wire", "money", "funds", "dollar", "usd", "rupees"],
            "auth": ["password", "pin", "otp", "code", "verify", "login"],
            "prize": ["winner", "lottery", "gift", "prize", "won"]
        }
        
        for category, words in keywords.items():
            for word in words:
                if word in message_lower:
                    score += 1
        
        # Heuristic: If we see patterns like URLs or Phone numbers early, it adds to score
        if re.search(r'http[s]?://', message_lower):
            score += 2
        
        return score >= 1  # Low threshold to engage broadly

    def extract_intelligence(self, message: str) -> Intelligence:
        intel = Intelligence()
        
        # 1. URLs
        intel.phishing_links = re.findall(r'http[s]?://[^\s]+', message)
        
        # 2. UPI IDs
        intel.upi_ids = re.findall(r'[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}', message)
        
        # 3. Bank Patterns (9-18 digits)
        intel.bank_details = re.findall(r'\b\d{9,18}\b', message)
        
        # 4. Phone Numbers (US & India variations)
        # Matches: +91-9876543210, 9876543210, +1-555-0199, (555) 019-0199
        phone_pattern = r'(\+?\d{1,4}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4})'
        matches = re.findall(phone_pattern, message)
        # Filter short matches that might be dates/years
        intel.phone_numbers = [m for m in matches if len(re.sub(r'\D', '', m)) >= 10]

        # 5. Crypto Addresses (Bitcoin, Ethereum simple checks)
        # BTC: 1 or 3 followed by 25-34 alphanumeric
        # ETH: 0x followed by 40 hex
        btc_pattern = r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b'
        eth_pattern = r'\b0x[a-fA-F0-9]{40}\b'
        
        intel.crypto_addresses.extend(re.findall(btc_pattern, message))
        intel.crypto_addresses.extend(re.findall(eth_pattern, message))
        
        return intel

    def _add_typos(self, text: str) -> str:
        """Simulate elderly typing with occasional caps and ellipses."""
        if random.random() < 0.3:
            text = text.replace(".", "...")
        if random.random() < 0.2:
            text = text.upper()
        return text

    def generate_response(self, message: str, is_scam: bool, session_id: str) -> str:
        session = self.get_session(session_id)
        session.turns_count += 1
        
        if not is_scam and session.state == STATE_INITIAL:
            return "Hello? Who is this?"

        # Update State Machine
        if session.turns_count == 1:
            session.state = STATE_ENGAGED
        elif session.turns_count > 2 and session.turns_count < 5:
            session.state = STATE_BAITING
        elif session.turns_count >= 5:
            session.state = STATE_STALLING

        # Logic based on state
        response = ""
        msg_lower = message.lower()

        if session.state == STATE_ENGAGED:
            if "bank" in msg_lower or "money" in msg_lower:
                response = "Oh my... I am not verified good with computers. Is this about my savings?"
            else:
                response = "I received your message dear. What do I need to do? I allow hope this is safe."
        
        elif session.state == STATE_BAITING:
            # Pretend to be interested/compliant but failing
            if "click" in msg_lower or "link" in msg_lower:
                response = "I am clicking the blue letters but nothing happens. Is my mouse broken?"
            elif "send" in msg_lower or "pay" in msg_lower:
                response = "I have my checkbook right here. Can I just mail you a check? I trust you."
            else:
                response = "Please be patient with me young man. I am finding my reading glasses."

        elif session.state == STATE_STALLING:
            # Intentionally frustrating
            responses = [
                "My grandson usually helps me with this. Let me call him... wait...",
                "The screen went black! Did I break the internet?",
                "I think the cat walked on my keyboard. ashdjkl...",
                "Wait, is this the same person from Microsoft who called yesterday?"
            ]
            response = random.choice(responses)

        else:
            response = "I am confused. Please explain again clearly."

        return self._add_typos(response)

agent = HoneyPotAgent()
