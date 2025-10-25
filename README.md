# AI Wiki Quiz Generator - Full Project

This project is a deliverable for the DeepKlarity assignment. It contains:

- backend/ - FastAPI backend (Python)
- frontend/ - React frontend scaffold (Vite)
- README files for each part and a sample .env

Important: The LLM (Gemini) integration is scaffolded but not activated by default. Add your GEMINI_API_KEY to backend/.env and implement the LangChain chain in `llm_quiz_generator.generate_quiz_with_llm` if you want real LLM-based quizzes.

## Quickstart (recommended)
1. Backend:
   - cd backend
   - python -m venv venv
   - source venv/bin/activate  # Windows: venv\Scripts\activate
   - pip install -r requirements.txt
   - copy .env.sample to .env and adjust DATABASE_URL if using MySQL/Postgres
   - uvicorn main:app --reload --port 8000

2. Frontend:
   - cd frontend
   - npm install
   - npm run dev
   - open http://localhost:3000


