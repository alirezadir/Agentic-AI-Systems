"""
Anthropic Agent over RAG Pipeline

This script demonstrates how to build a Retrieval-Augmented Generation (RAG) pipeline using LlamaIndex,
leveraging OpenAI embeddings and Anthropic's Claude-3-Haiku model. The pipeline loads Uber's 2021 10-K filing,
indexes it, and exposes a query tool for an Anthropic agent to answer questions about Uber's financials.
"""

# ----------------------------------------------------------------------
# Data download (run these shell commands manually if needed):
# !mkdir -p 'data/10k/'
# !wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/10k/uber_2021.pdf' -O 'data/10k/uber_2021.pdf'

from llama_index.core.tools import QueryEngineTool
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.anthropic import Anthropic
from llama_index.core.agent.workflow import FunctionAgent
import asyncio

# ----------------------------------------------------------------------
# Set up embedding model and LLM
embed_model = OpenAIEmbedding(
    model_name="text-embedding-3-large",
    api_key="sk-proj-..."
)
llm = Anthropic(
    model="claude-3-haiku-20240307",
    api_key="sk-..."
)

# ----------------------------------------------------------------------
# Load and index the Uber 10-K document
uber_docs = SimpleDirectoryReader(
    input_files=["./data/10k/uber_2021.pdf"]
).load_data()

uber_index = VectorStoreIndex.from_documents(
    uber_docs,
    embed_model=embed_model
)

# ----------------------------------------------------------------------
# Create a query engine and wrap it as a tool for the agent
uber_engine = uber_index.as_query_engine(
    similarity_top_k=3,
    llm=llm
)

query_engine_tool = QueryEngineTool.from_defaults(
    query_engine=uber_engine,
    name="uber_10k",
    description=(
        "Provides information about Uber's financials for the year 2021. "
        "Use a detailed plain text question as input to the tool."
    ),
)

# ----------------------------------------------------------------------
# Create the Anthropic agent with the RAG tool
agent = FunctionAgent(
    tools=[query_engine_tool],
    llm=llm,
    verbose=True
)

# ----------------------------------------------------------------------
# Run a sample query
async def main():
    response = await agent.run(
        "Tell me both the risk factors and tailwinds for Uber?"
    )
    print(str(response))

if __name__ == "__main__":
    asyncio.run(main())