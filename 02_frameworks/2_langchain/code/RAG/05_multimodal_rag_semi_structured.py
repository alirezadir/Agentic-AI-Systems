import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    TextLoader,
    DirectoryLoader,
    UnstructuredImageLoader,
    JSONLoader
)
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.schema import Document
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
import json

# Load environment variables
load_dotenv()

def load_multimodal_documents(data_dir: str) -> List[Document]:
    """Load both text and structured data documents"""
    documents = []
    
    # Load text documents
    text_loader = DirectoryLoader(
        data_dir,
        glob="**/*.txt",
        loader_cls=TextLoader
    )
    documents.extend(text_loader.load())
    
    # Load JSON documents (structured data)
    json_loader = DirectoryLoader(
        data_dir,
        glob="**/*.json",
        loader_cls=JSONLoader,
        loader_kwargs={
            "jq_schema": ".",
            "content_key": "content"
        }
    )
    documents.extend(json_loader.load())
    
    return documents

def create_vector_store(documents: List[Document]) -> Chroma:
    """Create a vector store from documents"""
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(documents)
    
    # Create vector store
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=OpenAIEmbeddings(),
        persist_directory="./chroma_db_semi_structured"
    )
    
    return vectorstore

def create_qa_chain(vectorstore: Chroma) -> Any:
    """Create a QA chain for semi-structured data"""
    # Create the retriever
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    
    # Create the prompt template
    template = """You are an AI assistant that can handle both text and structured data.
    Answer the question based on the following context. If the context contains structured data (like JSON),
    make sure to reference specific fields and values in your answer.
    If you cannot answer the question based on the context, say so.

    Context: {context}
    Question: {question}
    
    Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    
    # Create the LLM
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    # Create the chain
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain

def main():
    # Load documents
    print("Loading documents...")
    documents = load_multimodal_documents("data")
    
    # Create vector store
    print("Creating vector store...")
    vectorstore = create_vector_store(documents)
    
    # Create QA chain
    print("Creating QA chain...")
    qa_chain = create_qa_chain(vectorstore)
    
    # Test queries
    test_queries = [
        "What are the key components of neural networks?",
        "What are the main types of machine learning?",
        "How do neural networks learn?",
        "What are some applications of AI?",
        "Can you describe the neural network architecture shown in the diagram?"
    ]
    
    print("\nTesting Semi-Structured RAG system with sample queries:")
    print("-" * 50)
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        try:
            result = qa_chain.invoke(query)
            print(f"Answer: {result}")
        except Exception as e:
            print(f"Error processing query: {str(e)}")

if __name__ == "__main__":
    main() 