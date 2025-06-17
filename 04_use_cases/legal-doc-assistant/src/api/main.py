from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
from ..data.document_processor import DocumentProcessor
from ..data.vector_store import VectorStore
from ..models.rag_chain import RAGChain
from ..config.settings import settings

app = FastAPI(title="Legal Document Assistant")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
document_processor = DocumentProcessor()
vector_store = VectorStore()
rag_chain = RAGChain()

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a legal document."""
    # Save the uploaded file temporarily
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    try:
        # Process the document
        documents = document_processor.load_pdf(file_path)
        vector_store.add_documents(documents)
        return {"message": "Document processed successfully", "chunks": len(documents)}
    finally:
        # Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)

@app.post("/query")
async def query_documents(query: str):
    """Query the legal documents."""
    # Retrieve relevant documents
    documents = vector_store.similarity_search(query)
    
    # Generate response
    response = rag_chain.generate_response(query, documents)
    
    return {
        "query": query,
        "response": response,
        "sources": [doc.metadata for doc in documents]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT) 