import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA

# Load environment variables
load_dotenv()

def load_documents():
    """Load documents from the data directory"""
    documents = []
    data_dir = "data"
    
    # Load sample.txt
    sample_loader = TextLoader(os.path.join(data_dir, "sample.txt"))
    documents.extend(sample_loader.load())
    
    # Load neural_networks.txt
    neural_loader = TextLoader(os.path.join(data_dir, "neural_networks.txt"))
    documents.extend(neural_loader.load())
    
    return documents

def create_vector_store(documents):
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
        persist_directory="./chroma_db"
    )
    
    return vectorstore

def create_qa_chain(vectorstore):
    """Create a QA chain using the vector store"""
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True
    )
    
    return qa_chain

def main():
    # Load documents
    print("Loading documents...")
    documents = load_documents()
    
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
        "What are some applications of AI?"
    ]
    
    print("\nTesting RAG system with sample queries:")
    print("-" * 50)
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = qa_chain({"query": query})
        print(f"Answer: {result['result']}")
        print("\nSource documents:")
        for doc in result['source_documents']:
            print(f"- {doc.page_content[:200]}...")

if __name__ == "__main__":
    main() 