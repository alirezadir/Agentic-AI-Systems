from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
from langchain.schema.runnable import RunnablePassthrough
from ..config.settings import settings

class RAGChain:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            temperature=0,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a legal document assistant. Use the following context to answer the question.
            If you don't know the answer, just say that you don't know. Don't try to make up an answer.
            Always cite your sources using the document metadata.
            
            Context: {context}
            """),
            ("human", "{question}")
        ])
        
        self.chain = (
            {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
        )
    
    def format_documents(self, docs: List[Document]) -> str:
        """Format documents for the prompt."""
        return "\n\n".join(
            f"Document {i+1}:\n{doc.page_content}\nSource: {doc.metadata.get('source', 'Unknown')}"
            for i, doc in enumerate(docs)
        )
    
    def generate_response(self, query: str, documents: List[Document]) -> str:
        """Generate a response using the RAG chain."""
        formatted_docs = self.format_documents(documents)
        return self.chain.invoke({"context": formatted_docs, "question": query}) 