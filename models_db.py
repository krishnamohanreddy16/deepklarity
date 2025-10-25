from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(1000), index=True)
    title = Column(String(500))
    date_generated = Column(DateTime(timezone=True), server_default=func.now())
    scraped_content = Column(Text)
    full_quiz_data = Column(Text)  # store JSON string
