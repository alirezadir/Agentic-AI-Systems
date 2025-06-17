from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document
from ..config.settings import settings

class DocumentProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
        )
    
    def load_pdf(self, file_path: str) -> List[Document]:
        """Load and process a PDF file."""
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        return self.split_documents(documents)
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks."""
        return self.text_splitter.split_documents(documents)
    
    def process_metadata(self, document: Document) -> Dict[str, Any]:
        """Extract and process metadata from a document."""
        metadata = document.metadata.copy()
        # Add any additional metadata processing here
        return metadata 