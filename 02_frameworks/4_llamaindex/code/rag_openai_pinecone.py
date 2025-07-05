"""
OpenAI Agent + Query Engine with Pinecone Vector Store (LlamaIndex Example)

This script demonstrates how to use LlamaIndex with OpenAI and Pinecone for auto-retrieval and joint semantic/structured search.

Reference:
    https://docs.llamaindex.ai/en/stable/examples/agent/openai_agent_query_cookbook/
"""

# ----------------------------------------------------------------------
# Environment setup (run these shell commands manually if needed):
# %pip install llama-index llama-index-llms-openai llama-index-readers-wikipedia llama-index-vector-stores-pinecone
# export PINECONE_API_KEY=...  # Set your Pinecone API key
# export OPENAI_API_KEY=...    # Set your OpenAI API key

import os
import asyncio

from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from pinecone import Pinecone, ServerlessSpec
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.schema import TextNode
from llama_index.core.tools import QueryEngineTool
from llama_index.core.agent.openai import OpenAIAgent

# ----------------------------------------------------------------------
# LLM and Embedding Model Setup
Settings.llm = OpenAI(model="gpt-4o-mini")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

# ----------------------------------------------------------------------
# Pinecone Initialization and Index Creation
# NOTE: Only run index creation once; comment out after first run
# pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
# pc.create_index(
#     name="quickstart-index",
#     dimension=1536,
#     metric="euclidean",
#     spec=ServerlessSpec(cloud="aws", region="us-east-1"),
# )
# import time; time.sleep(10)  # Wait for index to be ready

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index("quickstart-index")

# ----------------------------------------------------------------------
# Sample Data Nodes with Metadata
nodes = [
    TextNode(
        text=(
            "Michael Jordan is a retired professional basketball player, widely regarded as one of the greatest basketball players of all time."
        ),
        metadata={
            "category": "Sports",
            "country": "United States",
            "gender": "male",
            "born": 1963,
        },
    ),
    TextNode(
        text=(
            "Angelina Jolie is an American actress, filmmaker, and humanitarian. She has received numerous awards for her acting and is known for her philanthropic work."
        ),
        metadata={
            "category": "Entertainment",
            "country": "United States",
            "gender": "female",
            "born": 1975,
        },
    ),
    TextNode(
        text=(
            "Elon Musk is a business magnate, industrial designer, and engineer. He is the founder, CEO, and lead designer of SpaceX, Tesla, Inc., Neuralink, and The Boring Company."
        ),
        metadata={
            "category": "Business",
            "country": "United States",
            "gender": "male",
            "born": 1971,
        },
    ),
    TextNode(
        text=(
            "Toronto is the capital city of the province of Ontario in Canada. It is the most populous city in Canada."
        ),
        metadata={
            "category": "Geography",
            "country": "Canada",
            "city": "Toronto",
        },
    ),
    TextNode(
        text=(
            "Tokyo is the capital city of Japan and one of the most populous cities in the world."
        ),
        metadata={
            "category": "Geography",
            "country": "Japan",
            "city": "Tokyo",
        },
    ),
    TextNode(
        text=(
            "Berlin is the capital and largest city of Germany by both area and population."
        ),
        metadata={
            "category": "Geography",
            "country": "Germany",
            "city": "Berlin",
        },
    ),
]

# ----------------------------------------------------------------------
# Pinecone Vector Store and LlamaIndex Setup
vector_store = PineconeVectorStore(pinecone_index=index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
vector_index = VectorStoreIndex(nodes, storage_context=storage_context)

# ----------------------------------------------------------------------
# Query Engine Tool Setup
vector_engine = vector_index.as_query_engine(similarity_top_k=2)
vector_tool = QueryEngineTool.from_defaults(
    query_engine=vector_engine,
    name="vector_tool",
    description=(
        "Performs semantic search over a set of people and cities. "
        "Use a detailed plain text question as input."
    ),
)

# ----------------------------------------------------------------------
# OpenAI Agent Instantiation with the Vector Tool
agent = OpenAIAgent.from_tools([vector_tool], llm=Settings.llm)

# ----------------------------------------------------------------------
# Example Queries and Streaming Output
async def main():
    # Example 1: Simple semantic search
    response = await agent.run("Tell me about the arts and culture of Tokyo.")
    print("\nResponse for 'arts and culture of Tokyo':\n", str(response))

    # Example 2: Streaming output for a history query
    handler = agent.run("Tell me about the history of Berlin")
    async for ev in handler.stream_events():
        if hasattr(ev, "tool_name") and hasattr(ev, "tool_output"):
            print(
                f"\nCalled tool {ev.tool_name} with args {ev.tool_kwargs}, got response: {ev.tool_output}"
            )
        elif hasattr(ev, "delta"):
            print(ev.delta, end="", flush=True)
    response = await handler
    print("\nFinal response for 'history of Berlin':\n", str(response))

    # Example 3: Country lookup
    response = await agent.run("Can you give me the country corresponding to each city?")
    print("\nResponse for 'country corresponding to each city':\n", str(response))


if __name__ == "__main__":
    asyncio.run(main())