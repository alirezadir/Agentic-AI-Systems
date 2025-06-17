import pytest
from src.data.document_processor import DocumentProcessor
from langchain.schema import Document

def test_document_processor_initialization():
    processor = DocumentProcessor()
    assert processor is not None

def test_split_documents():
    processor = DocumentProcessor()
    test_docs = [
        Document(page_content="This is a test document." * 10, metadata={"source": "test.pdf"}),
        Document(page_content="Another test document." * 10, metadata={"source": "test2.pdf"})
    ]
    
    split_docs = processor.split_documents(test_docs)
    assert len(split_docs) > len(test_docs)  # Should create more chunks
    assert all(isinstance(doc, Document) for doc in split_docs)
    assert all("source" in doc.metadata for doc in split_docs) 