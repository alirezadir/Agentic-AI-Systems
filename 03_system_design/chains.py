# ================
# RAG chain 
# ================
docs = load_documents(path)
splits = split_documents(docs, chunk_size=1000, chunk_overlap=200)
embedding_model = Embeddings()
vector_db = Chroma.from_documents(texts, embeddings) # index and store in FAISS
llm = OpenAI(temperature=0.0) # most deterministic
retriever = vector_db.as_retriever(search_type="similarity", search_kwargs={"k": 3})
template = """
You are a helpful AI assistant. ...

Context: {context}
Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
rag_chain = ({"context": retriever, "question": RunnablePassthrough()} 
             | prompt 
             | llm 
             | StrOutputParser())

retriever_tool = create_retriever_tool(
    retriever, "retrieve_blog_posts", "Search and return information about Lilian Weng blog posts.")

# chat_history = []
# while True:
#     respose = rag_chain({"question": user_query, "chat_history": chat_history})

# ================
# Agentic RAG chain 
# ================
# docs. splits, embedding, vector_db, gen_model, retriever same as above 
vector_db = Chroma.from_documents(...)
retriever = ...
retriever_tool = create_retriever_tool(
    retriever, tool_name, description)
# conditional to whether to use the retriever tool or respond
def generate_query_or_respond(state): 
    ...
# grade documents for relevance,  
# conditional to rewerite question or generate answer
def grade_documents(state):
  context = state["messages"][-1]
  question = state["messages"][0]
  grade_prompt = """
  You are a helpful AI assistant. ...
  Context: {context}
  Question: {question}
  """
  grade_model = ... 
  answer = grade_model.invoke(grade_prompt)
  return "generate_answer" if answer == "yes" else "rewrite_question"

def rewrite_question(state):
    ...
def generate_answer(state):
    ...

# assemble the graph 
graph = 