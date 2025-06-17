"""
Basic RAG (Retrieval Augmented Generation) Implementation using LangGraph

This script implements a basic RAG system using LangGraph for better flow control and error handling.
The system processes text documents, creates embeddings, and uses them to answer questions
based on the document content.

Main Components:
1. Document Processing: Loads and splits text documents
2. Vector Store: Creates and manages document embeddings
3. Retrieval: Finds relevant document chunks for queries
4. Generation: Uses LLM to generate answers based on retrieved context
5. Workflow: LangGraph-based orchestration of the RAG pipeline
"""

import os
from pathlib import Path
from typing import List, Dict, Any, TypedDict, Annotated, Sequence
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage

# ============================================================================
# Configuration & Setup
# ============================================================================

# Load environment variables (OpenAI API key, etc.)
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
# Type Definitions
# ============================================================================

class RAGState(TypedDict):
    """
    Type definition for the RAG state.
    This defines the structure of the state that flows through the LangGraph workflow.
    
    Fields:
        query: The user's question
        documents: List of loaded documents
        vectorstore: The vector store instance
        answer: The generated answer
        error: Any error message
    """
    query: str
    documents: List[Document]
    vectorstore: Chroma
    answer: str
    error: str

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
    
    This function:
    1. Splits documents into chunks
    2. Creates embeddings for each chunk
    3. Stores the embeddings in a Chroma vector store
    
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

def create_retriever(vectorstore: Chroma):
    """
    Create a retriever from the vector store.
    
    The retriever uses similarity search to find the most relevant
    document chunks for a given query.
    
    Args:
        vectorstore: Chroma vector store instance
        
    Returns:
        Retriever instance
    """
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}  # Number of most similar chunks to retrieve
    )

# ============================================================================
# LLM & Prompting Functions
# ============================================================================

def create_qa_prompt() -> ChatPromptTemplate:
    """
    Create the QA prompt template.
    
    This template instructs the LLM to:
    1. Use only the provided context
    2. Be concise and accurate
    3. Admit when it can't answer based on the context
    
    Returns:
        ChatPromptTemplate instance
    """
    template = """You are a helpful AI assistant. Answer the question based on the following context. 
    If you cannot answer the question based on the context, say so.
    Be concise and accurate in your response.

    Context: {context}
    Question: {question}
    
    Answer:"""
    
    return ChatPromptTemplate.from_template(template)

def create_llm():
    """
    Create the language model instance.
    
    Returns:
        ChatOpenAI instance configured for QA
    """
    return ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,      # No randomness in responses
        max_tokens=500      # Limit response length
    )

# ============================================================================
# LangGraph Node Functions
# ============================================================================

def load_docs_node(state: RAGState) -> RAGState:
    """
    Node for loading documents.
    
    Args:
        state: Current RAG state
        
    Returns:
        Updated RAG state with loaded documents
    """
    try:
        state["documents"] = load_documents(DATA_DIR)
        return state
    except Exception as e:
        state["error"] = f"Error loading documents: {str(e)}"
        return state

def create_vector_store_node(state: RAGState) -> RAGState:
    """
    Node for creating vector store.
    
    Args:
        state: Current RAG state
        
    Returns:
        Updated RAG state with vector store
    """
    try:
        state["vectorstore"] = create_vector_store(state["documents"], VECTOR_STORE_DIR)
        return state
    except Exception as e:
        state["error"] = f"Error creating vector store: {str(e)}"
        return state

def answer_query_node(state: RAGState) -> RAGState:
    """
    Node for answering queries.
    
    This node:
    1. Creates a retriever
    2. Sets up the QA chain
    3. Generates the answer
    
    Args:
        state: Current RAG state
        
    Returns:
        Updated RAG state with answer
    """
    try:
        retriever = create_retriever(state["vectorstore"])
        prompt = create_qa_prompt()
        llm = create_llm()
        
        # Create the QA chain
        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        
        state["answer"] = chain.invoke(state["query"])
        return state
    except Exception as e:
        state["error"] = f"Error answering query: {str(e)}"
        return state

def should_end(state: RAGState) -> bool:
    """
    Determine if the graph should end.
    
    The graph ends if either:
    1. An error occurred
    2. An answer was generated
    
    Args:
        state: Current RAG state
        
    Returns:
        True if should end, False otherwise
    """
    return bool(state.get("error")) or bool(state.get("answer"))

# ============================================================================
# Graph Construction
# ============================================================================

def create_rag_graph() -> StateGraph:
    """
    Create the RAG workflow graph.
    
    The graph consists of three main nodes:
    1. load_docs: Loads documents
    2. create_vector_store: Creates embeddings
    3. answer_query: Generates answers
    
    Returns:
        StateGraph instance
    """
    # Create the graph
    workflow = StateGraph(RAGState)
    
    # Add nodes
    workflow.add_node("load_docs", load_docs_node)
    workflow.add_node("create_vector_store", create_vector_store_node)
    workflow.add_node("answer_query", answer_query_node)
    
    # Add edges
    workflow.add_edge("load_docs", "create_vector_store")
    workflow.add_edge("create_vector_store", "answer_query")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "answer_query",
        should_end,
        {
            True: END,
            False: "answer_query"
        }
    )
    
    # Set entry point
    workflow.set_entry_point("load_docs")
    
    return workflow

# ============================================================================
# Main Execution
# ============================================================================

def main():
    """
    Main function to run the RAG system.
    
    This function:
    1. Sets up the RAG graph
    2. Processes test queries
    3. Writes results to output file
    """
    print(f"Project root directory: {SCRIPT_DIR}")
    print(f"Data directory: {DATA_DIR}")
    print(f"Vector store directory: {VECTOR_STORE_DIR}")
    print(f"Output directory: {OUT_DIR}")
    
    # Create the graph
    rag_graph = create_rag_graph()
    app = rag_graph.compile()
    
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
    
    output_lines = ["# RAG Demo Output\n"]
    for query in test_queries:
        print(f"\nQuery: {query}")
        output_lines.append(f"## Query: {query}\n")
        try:
            # Initialize state
            state = {
                "query": query,
                "documents": [],
                "vectorstore": None,
                "answer": "",
                "error": ""
            }
            
            # Run the graph
            result = app.invoke(state)
            
            # Handle results
            if result.get("error"):
                print(f"Error: {result['error']}")
                output_lines.append(f"**Error:** {result['error']}\n")
            else:
                print(f"Answer: {result['answer']}")
                output_lines.append(f"**Answer:** {result['answer']}\n")
                
        except Exception as e:
            print(f"Error processing query: {str(e)}")
            output_lines.append(f"**Exception:** {str(e)}\n")
        output_lines.append("\n---\n")
    
    # Write output to file
    output_path = OUT_DIR / "rag_output.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    print(f"\nResults written to {output_path}")

if __name__ == "__main__":
    main() 