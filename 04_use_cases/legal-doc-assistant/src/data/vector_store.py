from typing import List, Dict, Any
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from ..config.settings import settings

class VectorStore:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.vector_store = Chroma(
            persist_directory=settings.CHROMA_PERSIST_DIRECTORY,
            embedding_function=self.embeddings
        )
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the vector store."""
        self.vector_store.add_documents(documents)
        self.vector_store.persist()
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Perform similarity search."""
        return self.vector_store.similarity_search(query, k=k)
    
    def similarity_search_with_score(self, query: str, k: int = 4) -> List[tuple[Document, float]]:
        """Perform similarity search with scores."""
        return self.vector_store.similarity_search_with_score(query, k=k) 