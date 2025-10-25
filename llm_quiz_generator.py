import os
import json
from models import QuizOutput, QuizQuestion
from typing import List
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

def simple_local_quiz_generator(title: str, text: str, url: str):
    # A very basic heuristic quiz generator for offline testing.
    # It extracts sentences and makes fill-in style questions.
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text)
    questions = []
    idx = 0
    for s in sentences:
        s = s.strip()
        if len(s) < 40 or len(questions) >= 6:
            continue
        # find a proper noun-ish word to ask about (capitalized word not at start)
        words = s.split()
        candidate = None
        for w in words[1:]:
            if w.istitle() and len(w) > 3:
                candidate = w.strip(",.()")
                break
        if not candidate:
            continue
        # build options (dumb)
        options = [candidate, "Unknown", "Other", "None"]
        questions.append({
            "question": f"In the article: '{s[:80]}...', which of the following is correct (pick the named entity)?",
            "options": options,
            "answer": candidate,
            "explanation": f"Taken from the sentence: {s}",
            "difficulty": "medium"
        })
    # if still empty, create generic questions
    if not questions:
        questions = [{
            "question": f"What is the main topic of the article titled '{title}'?",
            "options": [title, "History", "Science", "Other"],
            "answer": title,
            "explanation": "Title-based question",
            "difficulty": "easy"
        }]
    out = {
        "url": url,
        "title": title,
        "summary": (text[:800] + "...") if text else "",
        "key_entities": {},
        "sections": [],
        "quiz": questions,
        "related_topics": []
    }
    return out

def generate_quiz_with_llm(title: str, text: str, url: str):
    # Placeholder for real LangChain + Gemini integration.
    # If GEMINI_API_KEY is present, user can implement using langchain-google-genai wrappers.
    # For now we'll try to fall back to simple generator.
    if GEMINI_API_KEY:
        # User can implement this block with LangChain following the reference docs.
        # It's intentionally left as an exercise to paste their Gemini key and enable the chain.
        raise NotImplementedError("Gemini integration placeholder. Add LangChain code here.")
    else:
        return simple_local_quiz_generator(title, text, url)
