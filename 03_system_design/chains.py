# RAG chain 
docs = load_documents(path)
splits = split_documents(docs, chunk_size=1000, chunk_overlap=200)
embedding_model = Embeddings()
vector_db = Chroma.from_documents(texts, embeddings) # index and store in FAISS
llm = OpenAI(temperature=0.0) # most deterministic
retriever = vector_db.as_retriever()
rag_chain = 


chat_history = []
while True:
    respose = rag_chain({"question": user_query, "chat_history": chat_history})
