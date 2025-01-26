# app/models/embeddings.py
import os
import requests
from typing import List
from langchain.embeddings.base import Embeddings

class HuggingFaceAPIEmbeddings(Embeddings):
    """Custom Hugging Face embedding model using their inference API"""
    
    def __init__(self):
        self.token = os.getenv('HUGGINGFACE_TOKEN')
        self.api_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        response = requests.post(
            self.api_url,
            headers=self.headers,
            json={"inputs": texts}
        )
        return response.json()

    def embed_query(self, text: str) -> List[float]:
        response = requests.post(
            self.api_url,
            headers=self.headers,
            json={"inputs": [text]}
        )
        return response.json()[0]