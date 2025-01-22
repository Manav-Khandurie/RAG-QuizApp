from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import PGVector
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import tempfile
import os

def process_document(file_path: str):
    # Load and split the document
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()

    # Generate embeddings and store in PGVector
    embeddings = OpenAIEmbeddings()
    db = PGVector.from_documents(
        documents=pages,
        embedding=embeddings,
        connection_string=os.getenv("DATABASE_URL")
    )

    return db

def generate_quiz_questions(db, num_questions: int = 10):
    retriever = db.as_retriever()
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(temperature=0.7),
        chain_type="stuff",
        retriever=retriever
    )

    questions = []
    for _ in range(num_questions):
        query = "Generate a multiple-choice question based on the document."
        result = qa.run(query)
        questions.append(result)

    return questions