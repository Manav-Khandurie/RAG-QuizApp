from pydantic import BaseModel
from typing import List

class DocumentUpload(BaseModel):
    file: bytes

class QuizQuestionCreate(BaseModel):
    document_id: int
    question: str
    options: List[str]
    answer: str

class QuizQuestionResponse(BaseModel):
    id: int
    document_id: int
    question: str
    options: List[str]
    answer: str