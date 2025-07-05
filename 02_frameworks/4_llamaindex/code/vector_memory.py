"""
LlamaIndex Vector Memory Example

This script demonstrates how to use the VectorMemory module from LlamaIndex for conversational memory.
It covers initializing vector memory, storing and retrieving chat messages, and resetting memory.

Reference: https://docs.llamaindex.ai/en/stable/examples/agent/memory/vector_memory/
"""

from llama_index.core.memory import VectorMemory
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.llms import ChatMessage

# ----------------------------------------------------------------------
# Initialize vector memory with OpenAI embeddings
vector_memory = VectorMemory.from_defaults(
    vector_store=None,  # Use default in-memory vector store
    embed_model=OpenAIEmbedding(),
    retriever_kwargs={"similarity_top_k": 1},
)

# ----------------------------------------------------------------------
# Example 1: Store and retrieve simple user messages

# Create a list of user messages
messages = [
    ChatMessage.from_str("Jerry likes juice.", role="user"),
    ChatMessage.from_str("Bob likes burgers.", role="user"),
    ChatMessage.from_str("Alice likes apples.", role="user"),
]

# Store messages in vector memory
for msg in messages:
    vector_memory.put(msg)

# Retrieve the most relevant message for a query
query_1 = "What does Jerry like?"
result_1 = vector_memory.get(query_1)
print(f"Retrieved for '{query_1}': {result_1}")

# ----------------------------------------------------------------------
# Example 2: Reset memory and use both user and assistant messages

vector_memory.reset()

messages = [
    ChatMessage.from_str("Jerry likes burgers.", role="user"),
    ChatMessage.from_str("Bob likes apples.", role="user"),
    ChatMessage.from_str("Indeed, Bob likes apples.", role="assistant"),
    ChatMessage.from_str("Alice likes juice.", role="user"),
]
vector_memory.set(messages)

query_2 = "What does Bob like?"
result_2 = vector_memory.get(query_2)
print(f"\nRetrieved for '{query_2}': {result_2}")

# Output will show both the user and assistant messages related to Bob and apples.