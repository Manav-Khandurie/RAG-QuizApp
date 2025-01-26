from fastapi import FastAPI, UploadFile, File, HTTPException
from .models import Base, Document, QuizQuestion
from .database import engine, SessionLocal
from .schemas import DocumentUpload, QuizQuestionResponse
from .utils import process_document, generate_quiz_questions
import tempfile
import os
from fastapi.middleware.cors import CORSMiddleware
from langchain.vectorstores import PGVector
from .embeddings import HuggingFaceAPIEmbeddings  # New import
from .logger import logger

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, use specific domains in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)
@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(file.file.read())
            tmp_path = tmp.name

        # Process the document
        db = process_document(tmp_path)

        # Save the document to the database
        db_session = SessionLocal()
        try:
            document = Document(content="Sample content")  # Replace with actual content
            db_session.add(document)
            db_session.commit()
            db_session.refresh(document)
            document_id = document.id
        except Exception as e:
            db_session.rollback()
            logger.error(f"Failed to save document to the database: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {e}")
        finally:
            db_session.close()

        # Clean up the temporary file
        os.unlink(tmp_path)

        return {"message": "Document uploaded and processed successfully", "document_id": document_id}
    except Exception as e:
        logger.error(f"Error in upload_document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-quiz")
async def generate_quiz(document_id: int):
    try:
        logger.info(f"Generating quiz for document_id: {document_id}")

        # Check if the document exists
        db_session = SessionLocal()
        document = db_session.query(Document).filter(Document.id == document_id).first()
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        # Initialize embeddings and PGVector
        embeddings = HuggingFaceAPIEmbeddings()
        db = PGVector(
            connection_string=os.getenv("DATABASE_URL"),
            embedding_function=embeddings,
            use_jsonb=True
        )

        # Generate quiz questions
        questions = generate_quiz_questions(db)

        logger.info(f"Generated {len(questions)} questions.")
        logger.info(f"Sample question: {questions[0]}")

        # Save questions to the database
        try:
            for question in questions:
                db_question = QuizQuestion(
                    document_id=document_id,
                    question=question["question"],
                    options=question["options"],
                    answer=question["answer"]
                )
                db_session.add(db_question)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            logger.error(f"Failed to save questions to the database: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {e}")
        finally:
            db_session.close()

        return {"questions": questions}
    except Exception as e:
        logger.error(f"Error in generate_quiz: {e}")
        raise HTTPException(status_code=500, detail=str(e))