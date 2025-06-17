from src.data.loader import load_documents_from_folder
from src.rag.rag import RAGPipeline
from src.utils.guardrails import sanitize_input, validate_input, validate_output
from src.router.router import classify_intent, route_to_model
from src.interface.gateway import model_gateway
import logging

def run_cli():
    logging.info("Loading documents...")
    docs = load_documents_from_folder("sample_docs")

    rag = RAGPipeline()
    chunks = rag.chunk_documents(docs)
    rag.build_index(chunks)

    print("GenAI CLI — Type 'exit' to quit.")
    while True:
        try:
            query = input("You: ")
            if query.lower() in ["exit", "quit"]:
                break

            if not validate_input(query):
                print("⚠️  Blocked: Inappropriate or unsafe input.")
                continue

            clean_query = sanitize_input(query)
            context = rag.retrieve(clean_query)
            intent = classify_intent(clean_query)
            model_name = route_to_model(intent)

            answer = model_gateway(clean_query, context, provider="openai", model_name=model_name)
            final_answer = validate_output(answer)

            print("AI:", final_answer)

        except Exception as e:
            print("[System Error]", e)
