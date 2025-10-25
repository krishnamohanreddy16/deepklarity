# Backend (FastAPI) - AI Wiki Quiz Generator

## Overview
This backend provides:
- `/generate_quiz` POST endpoint that accepts JSON `{ "url": "<wikipedia-url>" }`
- `/history` GET endpoint for list of generated quizzes
- `/quiz/{quiz_id}` GET endpoint for fetching a stored quiz

## Run locally
1. Create venv and install:
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt

2. Create .env (see sample .env)
3. Start server:
    uvicorn main:app --reload --port 8000
