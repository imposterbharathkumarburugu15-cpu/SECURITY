# Agentic Honey-Pot API (Advanced Edition)

This is the **Advanced Hackathon Submission** for Problem 2: Agentic Honey-Pot.
It features a **Stateful AI Agent** that baits scammers, extracts intelligence, and wastes their time.

## Key Features
- **State Machine**: The agent moves through `ENGAGED` -> `BAITING` -> `STALLING` states to keep scammers hooked.
- **Advanced Intelligence Extraction**:
    - **Crypto Wallets** (Bitcoin, Ethereum)
    - **Phone Numbers** (International formats)
    - **Bank Accounts & UPI**
    - **Phishing Links**
- **Dynamic Persona**: "Grandma Gertrude" - simulates elderly typing quirks (ellipses, typos, confusion).
- **Security**: Protected via `x-api-key`.

## API Specification

**Endpoint**: `POST /analyze`

**Headers**:
- `Content-Type: application/json`
- `x-api-key: my_secure_api_key_123`

**Request Body**:
```json
{
  "session_id": "session_unique_id",
  "message": "URGENT: Transfer 500 USD to 1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2 immediately."
}
```

**Response**:
```json
{
  "session_id": "session_unique_id",
  "is_scam": true,
  "response_message": "I received your message dear. What do I need to do? I allow hope this is safe.",
  "intelligence": {
    "bank_details": [],
    "upi_ids": [],
    "phishing_links": [],
    "phone_numbers": [],
    "crypto_addresses": ["1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2"]
  },
  "status": "engaged"
}
```

## Setup & Run Locally

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Start the Server**:
    ```bash
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```

## Deployment
1.  **Push to GitHub**.
2.  **Deploy** (Render/Railway/Heroku).
    - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3.  **Submit** your live URL.
