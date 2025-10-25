from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class Option(BaseModel):
    text: str

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    answer: str
    explanation: Optional[str] = None
    difficulty: Optional[str] = "medium"

class QuizOutput(BaseModel):
    id: Optional[int]
    url: str
    title: Optional[str]
    summary: Optional[str]
    key_entities: Optional[Dict[str, List[str]]] = {}
    sections: Optional[List[str]] = []
    quiz: List[QuizQuestion]
    related_topics: Optional[List[str]] = []
    date_generated: Optional[datetime]
