import pytest
from src.data.document_processor import DocumentProcessor

def test_document_processor_initialization():
    """Test DocumentProcessor initialization."""
    processor = DocumentProcessor()
    assert processor is not None
    assert processor.text_splitter is not None

def test_document_processor_custom_params():
    """Test DocumentProcessor with custom parameters."""
    chunk_size = 500
    chunk_overlap = 100
    processor = DocumentProcessor(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    assert processor.text_splitter._chunk_size == chunk_size
    assert processor.text_splitter._chunk_overlap == chunk_overlap

def test_split_text():
    """Test text splitting functionality."""
    processor = DocumentProcessor()
    text = "This is a test document. It has multiple sentences. We want to test the splitting functionality."
    metadata = {"source": "test"}
    
    chunks = processor.split_text(text, metadata)
    assert len(chunks) > 0
    assert all(chunk.metadata == metadata for chunk in chunks)
    assert all(len(chunk.page_content) > 0 for chunk in chunks)

def test_invalid_pdf_file():
    """Test handling of invalid PDF file."""
    processor = DocumentProcessor()
    with pytest.raises(Exception):
        processor.load_pdf("nonexistent.pdf") 