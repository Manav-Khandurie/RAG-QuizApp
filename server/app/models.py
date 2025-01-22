from sqlalchemy import Column, Integer, String, Text, ARRAY
from .database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    embedding = Column(String)  # Store embeddings as text or use PGVector

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, index=True)
    question = Column(Text)
    options = Column(ARRAY(String))
    answer = Column(String)