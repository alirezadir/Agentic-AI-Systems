import openai
from src.config.settings import OPENAI_API_KEY
import logging

openai.api_key = OPENAI_API_KEY

def openai_chat(query: str, context: str, model: str = "gpt-3.5-turbo") -> str:
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{query}"
            }],
            temperature=0.7,
            max_tokens=500,
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"OpenAI chat failed: {e}")
        return f"[Error] Model failed: {str(e)}"

def model_gateway(query: str, context: str, provider: str, model_name: str) -> str:
    if provider == "openai":
        return openai_chat(query, context, model=model_name)
    raise NotImplementedError(f"Model provider '{provider}' is not supported.")
