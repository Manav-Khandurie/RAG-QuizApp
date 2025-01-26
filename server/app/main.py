from fastapi import FastAPI, UploadFile, File, HTTPException
from .models import Base, Document, QuizQuestion
from .database import engine, SessionLocal
from .schemas import DocumentUpload, QuizQuestionResponse
from .utils import process_document, generate_quiz_questions
import tempfile
import os
from langchain.vectorstores import PGVector
from .embeddings import HuggingFaceAPIEmbeddings  # New import

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)



@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        print(file)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file.file.read())
            tmp_path = tmp.name

        # Process the document
        db = process_document(tmp_path)

        # Clean up the temporary file
        os.unlink(tmp_path)

        return {"message": "Document uploaded and processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# app/main.py
@app.post("/generate-quiz")
async def generate_quiz(document_id: int):
    try:
        embeddings = HuggingFaceAPIEmbeddings()
        db = PGVector(
            connection_string=os.getenv("DATABASE_URL"),
            embedding_function=embeddings
        )

        # Generate quiz questions
        questions = generate_quiz_questions(db)

        # Save questions to the database
        db_session = SessionLocal()
        for question in questions:
            db_question = QuizQuestion(
                document_id=document_id,
                question=question["question"],
                options=question["options"],
                answer=question["answer"]
            )
            db_session.add(db_question)
        db_session.commit()

        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
