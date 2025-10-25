from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
from scraper import scrape_wikipedia
from llm_quiz_generator import generate_quiz_with_llm
from database import SessionLocal, engine
import models_db, json
from sqlalchemy.orm import Session
from models_db import Quiz
from models import QuizOutput
import models_db as mdb
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

load_dotenv()

# create DB tables
mdb.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Wiki Quiz Generator - Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLItem(BaseModel):
    url: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/generate_quiz")
def generate_quiz(item: URLItem, db: Session = Depends(get_db)):
    url = item.url
    try:
        title, cleaned = scrape_wikipedia(url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error scraping URL: {e}")
    try:
        quiz_json = generate_quiz_with_llm(title, cleaned, url)
    except Exception as e:
        # fallback
        quiz_json = {"url": url, "title": title, "summary": cleaned[:500], "quiz": [], "related_topics": []}
    # store to DB
    try:
        q = Quiz(url=url, title=title, scraped_content=cleaned, full_quiz_data=json.dumps(quiz_json))
        db.add(q)
        db.commit()
        db.refresh(q)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    # attach id and date
    quiz_json["id"] = q.id
    return quiz_json

@app.get("/history")
def history(db: Session = Depends(get_db)):
    rows = db.query(Quiz).order_by(Quiz.date_generated.desc()).all()
    out = []
    for r in rows:
        out.append({
            "id": r.id,
            "url": r.url,
            "title": r.title,
            "date_generated": r.date_generated.isoformat()
        })
    return out

@app.get("/quiz/{quiz_id}")
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    r = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Quiz not found")
    try:
        data = json.loads(r.full_quiz_data)
    except Exception:
        data = {"error": "invalid stored JSON", "raw": r.full_quiz_data}
    data["id"] = r.id
    data["date_generated"] = r.date_generated.isoformat()
    return data
