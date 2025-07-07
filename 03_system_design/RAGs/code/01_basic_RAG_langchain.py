import os
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain

# Set your OpenAI API key (or environment variable)
os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"  # Replace with your actual key

# 1. Load your document
with open("your_document.txt", "r") as file:
    document = file.read()

# 2. Chunk the document
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_text(document)

# 3. Create embeddings and store them in a vector store (FAISS)
embeddings = OpenAIEmbeddings()
vector_db = FAISS.from_texts(texts, embeddings)  # Index and store in FAISS (use other options)

# 4. Create a retrieval chain
llm = OpenAI(temperature=0.0)  # You can adjust temperature for creativity
retriever = vector_db.as_retriever()  # LangChain's retriever handles the search
rag_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, return_source_documents=True)  # Create a chain

# 5. Get user input and generate a response
chat_history = []
while True:
    user_query = input("Enter your question (or 'exit'): ")
    if user_query.lower() == "exit":
        break

    response = rag_chain({"question": user_query, "chat_history": chat_history})
    print(f"Answer: {response['answer']}")
    chat_history.extend([(user_query, response['answer'])])