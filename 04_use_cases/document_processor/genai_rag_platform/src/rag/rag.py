import faiss
import numpy as np
import openai
from typing import List
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from src.config.settings import OPENAI_API_KEY
import logging

openai.api_key = OPENAI_API_KEY

class RAGPipeline:
    def __init__(self, dimension: int = 1536):
        self.index = faiss.IndexFlatL2(dimension)
        self.texts: List[str] = []

    def chunk_documents(self, documents: List[str], chunk_size: int = 300, chunk_overlap: int = 50) -> List[str]:
        splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        langchain_docs = [Document(page_content=d) for d in documents]
        chunks = splitter.split_documents(langchain_docs)
        return [chunk.page_content for chunk in chunks]

    def embed_text(self, text: str) -> List[float]:
        try:
            response = openai.Embedding.create(
                input=[text],
                model="text-embedding-ada-002"
            )
            return response['data'][0]['embedding']
        except Exception as e:
            logging.error(f"Embedding failed: {e}")
            raise

    def build_index(self, texts: List[str]) -> None:
        logging.info("Building FAISS vector index...")
        embeddings = [self.embed_text(text) for text in texts]
        self.index.add(np.array(embeddings).astype("float32"))
        self.texts.extend(texts)
        logging.info("Index built successfully.")

    def retrieve(self, query: str, top_k: int = 5) -> str:
        try:
            query_vec = np.array([self.embed_text(query)]).astype("float32")
            scores, indices = self.index.search(query_vec, top_k)
            return "\n---\n".join([self.texts[i] for i in indices[0] if i < len(self.texts)])
        except Exception as e:
            logging.error(f"Retrieval failed: {e}")
            return "[Error] Retrieval failed."
