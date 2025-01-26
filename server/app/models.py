from sqlalchemy import Column, Integer, Text
from sqlalchemy.dialects.postgresql import ARRAY
from .database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    embedding = Column(Text)  # Store embeddings as text or use a custom type for vectors

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, index=True)
    question = Column(Text)
    options = Column(ARRAY(Text))  # Array of strings for options
    answer = Column(Text)