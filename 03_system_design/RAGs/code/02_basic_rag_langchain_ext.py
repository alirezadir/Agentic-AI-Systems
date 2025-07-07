"""
Basic RAG (Retrieval Augmented Generation) Implementation using LangChain

This script implements a basic RAG system using LangChain for document processing,
vector storage, and question answering. It demonstrates a simpler approach compared
to the LangGraph version, using direct LangChain components.

Main Components:
1. Document Processing: Loads and splits text documents
2. Vector Store: Creates and manages document embeddings
3. Retrieval: Finds relevant document chunks for queries
4. Generation: Uses LLM to generate answers based on retrieved context
"""

import os
from pathlib import Path
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

# ============================================================================
# Configuration & Setup
# ============================================================================

# Load environment variables
load_dotenv()

# Directory Configuration
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"          # Directory containing input documents
VECTOR_STORE_DIR = SCRIPT_DIR / "vector_store"  # Directory for storing embeddings
OUT_DIR = SCRIPT_DIR / "_out"           # Directory for output files

# Create necessary directories if they don't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# Document Processing Functions
# ============================================================================

def validate_data_directory(data_dir: Path) -> None:
    """
    Validate the data directory structure.
    
    Args:
        data_dir: Path to the data directory
        
    Raises:
        FileNotFoundError: If the data directory doesn't exist
        ValueError: If the data directory is empty or has no text files
    """
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory '{data_dir}' not found")
    
    # Check for text files
    text_files = list(data_dir.glob("**/*.txt"))
    if not text_files:
        raise ValueError(f"No text files found in {data_dir}")
    
    print(f"Found {len(text_files)} text files in {data_dir}")

def load_documents(data_dir: Path) -> List[Document]:
    """
    Load documents from the data directory.
    
    Args:
        data_dir: Directory containing the documents to load
        
    Returns:
        List of loaded documents
        
    Raises:
        FileNotFoundError: If the data directory doesn't exist
        ValueError: If no documents are found
    """
    validate_data_directory(data_dir)
    
    documents = []
    text_loader = DirectoryLoader(
        str(data_dir),
        glob="**/*.txt",
        loader_cls=TextLoader
    )
    documents.extend(text_loader.load())
    
    if not documents:
        raise ValueError(f"No documents found in {data_dir}")
    
    print(f"Successfully loaded {len(documents)} documents")
    for i, doc in enumerate(documents):
        print(f"Document {i+1} length: {len(doc.page_content)} chars, preview: {doc.page_content[:100]!r}")
    return documents

# ============================================================================
# Vector Store & Retrieval Functions
# ============================================================================

def create_vector_store(documents: List[Document], persist_dir: Path) -> Chroma:
    """
    Create a vector store from documents.
    
    Args:
        documents: List of documents to process
        persist_dir: Directory to persist the vector store
        
    Returns:
        Chroma vector store instance
    """
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,    # Size of each text chunk
        chunk_overlap=200   # Overlap between chunks for context preservation
    )
    splits = text_splitter.split_documents(documents)
    print(f"Split documents into {len(splits)} chunks")
    if not splits:
        print("ERROR: No chunks were produced by the text splitter. Check document content and splitter settings.")
        raise ValueError("No chunks produced from documents. Check document content and splitter settings.")
    
    # Create vector store
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=OpenAIEmbeddings(),
        persist_directory=str(persist_dir)
    )
    
    return vectorstore

# ============================================================================
# LLM & Prompting Functions
# ============================================================================

def create_qa_chain(vectorstore: Chroma) -> Any:
    """
    Create a QA chain using LangChain components.
    
    This function:
    1. Creates a retriever from the vector store
    2. Sets up the prompt template
    3. Configures the LLM
    4. Combines everything into a chain
    
    Args:
        vectorstore: Chroma vector store instance
        
    Returns:
        LangChain chain for question answering
    """
    # Create the retriever
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}  # Number of most similar chunks to retrieve
    )
    
    # Create the prompt template
    template = """You are a helpful AI assistant. Answer the question based on the following context. 
    If you cannot answer the question based on the context, say so.
    Be concise and accurate in your response.

    Context: {context}
    Question: {question}
    
    Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    
    # Create the LLM
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,      # No randomness in responses
        max_tokens=500      # Limit response length
    )
    
    # Create the chain
    chain = (
        {"context": retriever, "question": RunnablePassthrough()} # this runnable map is equivalent to 
        # retriever.invoke(query) → context
	    # RunnablePassthrough().invoke(query) → question
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain

# ============================================================================
# Main Execution
# ============================================================================

def main():
    """
    Main function to run the RAG system.
    
    This function:
    1. Loads documents
    2. Creates vector store
    3. Sets up QA chain
    4. Processes test queries
    5. Writes results to output file
    """
    print(f"Project root directory: {SCRIPT_DIR}")
    print(f"Data directory: {DATA_DIR}")
    print(f"Vector store directory: {VECTOR_STORE_DIR}")
    print(f"Output directory: {OUT_DIR}")
    
    try:
        # Load documents
        print("\nLoading documents...")
        documents = load_documents(DATA_DIR)
        
        # Create vector store
        print("\nCreating vector store...")
        vectorstore = create_vector_store(documents, VECTOR_STORE_DIR)
        
        # Create QA chain
        print("\nCreating QA chain...")
        qa_chain = create_qa_chain(vectorstore)
        
        # Test queries
        test_queries = [
            "What are the key components of neural networks?",
            "What are the main types of machine learning?",
            "How do neural networks learn?",
            "What are some applications of AI?",
            "Can you describe the neural network architecture shown in the diagram?"
        ]
        
        print("\nTesting RAG system with sample queries:")
        print("-" * 50)
        
        output_lines = ["# RAG Demo Output (LangChain Version)\n"]
        for query in test_queries:
            print(f"\nQuery: {query}")
            output_lines.append(f"## Query: {query}\n")
            try:
                # invoke the chain with the query
                result = qa_chain.invoke(query)
                print(f"Answer: {result}")
                output_lines.append(f"**Answer:** {result}\n")
            except Exception as e:
                error_msg = f"Error processing query: {str(e)}"
                print(error_msg)
                output_lines.append(f"**Error:** {error_msg}\n")
            output_lines.append("\n---\n")
        
        # Write output to file
        output_path = OUT_DIR / "rag_output_langchain.md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(output_lines))
        print(f"\nResults written to {output_path}")
        
    except Exception as e:
        print(f"\nError in main execution: {str(e)}")

if __name__ == "__main__":
    main() 