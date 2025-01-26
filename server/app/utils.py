# app/utils.py
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import PGVector
from langchain.chains import RetrievalQA
from langchain_openai.chat_models.base import BaseChatOpenAI
from .embeddings import HuggingFaceAPIEmbeddings  # Updated import
import os

def process_document(file_path: str):
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()

    # Use the reusable embedding model
    embeddings = HuggingFaceAPIEmbeddings()
    
    db = PGVector.from_documents(
        documents=pages,
        embedding=embeddings,
        connection_string=os.getenv("DATABASE_URL"),
        collection_name="documents"
    )
    return db

# app/utils.py
def generate_quiz_questions(db, num_questions: int = 10):
    retriever = db.as_retriever()
    
    llm = BaseChatOpenAI(
        model='deepseek-chat',
        openai_api_key=os.getenv('DEEPSEEK_API_KEY'),
        openai_api_base='https://api.deepseek.com/',
        max_tokens=1024
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever
    )

    questions = []
    for _ in range(num_questions):
        query = "Generate a multiple-choice question based on the document.Use the contents properly"
        result = qa.run(query)
        
        # Parse the result into a structured format
        # Example: Assume the result is a string like "What is 2+2? A) 1 B) 2 C) 3 D) 4 | Answer: D"
        if "|" in result:
            question_part, answer_part = result.split("|")
            question = question_part.strip()
            answer = answer_part.replace("Answer:", "").strip()
            options = ["A) 1", "B) 2", "C) 3", "D) 4"]  # Replace with actual options parsing logic
        else:
            question = result.strip()
            answer = "Unknown"
            options = ["Option 1", "Option 2", "Option 3", "Option 4"]  # Default options
        
        questions.append({
            "question": question,
            "options": options,
            "answer": answer
        })

    return questions
