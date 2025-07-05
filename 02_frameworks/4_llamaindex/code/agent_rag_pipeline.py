"""
Anthropic Agent over RAG Pipeline

Build an Anthropic agent over a simple 10K document. Uses OpenAI embeddings and claude-3-haiku-20240307 to construct the RAG pipeline, and passes it to the Anthropic agent as a tool.
"""

# ---
# Data download (run these shell commands manually if needed):
# !mkdir -p 'data/10k/'
# !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/10k/uber_2021.pdf' -O 'data/10k/uber_2021.pdf'

from llama_index.core.tools import QueryEngineTool
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.anthropic import Anthropic
from llama_index.core.agent.workflow import FunctionAgent

# ---
# Set up embedding model and LLM
embed_model = OpenAIEmbedding(
    model_name="text-embedding-3-large", api_key="sk-proj-..."
)
llm = Anthropic(model="claude-3-haiku-20240307", api_key="sk-...")

# ---
# Load data
uber_docs = SimpleDirectoryReader(
    input_files=["./data/10k/uber_2021.pdf"]
).load_data()

# ---
# Build vector index
uber_index = VectorStoreIndex.from_documents(
    uber_docs, embed_model=embed_model
)

# ---
# Create query engine and tool
uber_engine = uber_index.as_query_engine(similarity_top_k=3, llm=llm)
query_engine_tool = QueryEngineTool.from_defaults(
    query_engine=uber_engine,
    name="uber_10k",
    description=(
        "Provides information about Uber financials for year 2021. "
        "Use a detailed plain text question as input to the tool."
    ),
)

# ---
# Create Anthropic agent with the RAG tool
agent = FunctionAgent(tools=[query_engine_tool], llm=llm, verbose=True)

# ---
# Run a sample query
import asyncio

async def main():
    response = await agent.run(
        "Tell me both the risk factors and tailwinds for Uber?"
    )
    print(str(response))

if __name__ == "__main__":
    asyncio.run(main()) 