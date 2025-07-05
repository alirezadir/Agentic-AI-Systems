"""
LlamaIndex Composable Memory Example

Demonstrates how to combine a primary chat buffer (short-term memory) with a secondary vector memory (long-term memory)
using `SimpleComposableMemory` from LlamaIndex. This setup enables an agent to retrieve context from both recent and
semantic memory sources.

Reference:
    https://docs.llamaindex.ai/en/stable/examples/agent/memory/composable_memory/
"""

from llama_index.core.memory import (
    VectorMemory,
    SimpleComposableMemory,
    ChatMemoryBuffer,
)
from llama_index.core.llms import ChatMessage
from llama_index.embeddings.openai import OpenAIEmbedding

# ----------------------------------------------------------------------
# Initialize secondary (long-term) vector memory
vector_memory = VectorMemory.from_defaults(
    vector_store=None,  # Use default in-memory vector store
    embed_model=OpenAIEmbedding(),
    retriever_kwargs={"similarity_top_k": 1},
)

# Populate vector memory with initial messages
initial_messages = [
    ChatMessage.from_str("You are a SOMEWHAT helpful assistant.", role="system"),
    ChatMessage.from_str("Bob likes burgers.", role="user"),
    ChatMessage.from_str("Indeed, Bob likes apples.", role="assistant"),
    ChatMessage.from_str("Alice likes apples.", role="user"),
]
vector_memory.set(initial_messages)

# Initialize primary (short-term) chat memory buffer
chat_memory_buffer = ChatMemoryBuffer.from_defaults()

# Compose the memory: primary = chat buffer, secondary = vector memory
composable_memory = SimpleComposableMemory.from_defaults(
    primary_memory=chat_memory_buffer,
    secondary_memory_sources=[vector_memory],
)

# ----------------------------------------------------------------------
# Example: Retrieve from composable memory (simulating agent usage)

# Add a new user message to the primary memory
chat_memory_buffer.put(ChatMessage.from_str("What does Bob like?", role="user"))

# Retrieve relevant messages from composable memory (uses both memory sources)
retrieved_messages = composable_memory.get("What does Bob like?")

print("\nRetrieved messages for 'What does Bob like?':")
for msg in retrieved_messages:
    print(f"- {msg.role}: {msg.content}")

# Display the contents of primary and secondary memory for inspection
print("\nPrimary memory (chat buffer):", composable_memory.primary_memory)
print("Secondary memory sources:", composable_memory.secondary_memory_sources)