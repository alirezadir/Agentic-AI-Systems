"""
Multimodal RAG (Retrieval Augmented Generation) Implementation
This script implements a multimodal RAG system that can handle text, tables, and images.
It uses LangChain for the RAG pipeline and OpenAI's GPT-4 Vision for image understanding.
"""

# Standard library imports
import base64
import io
import os
import re
import uuid
from typing import List, Dict, Any

# Third-party imports
from dotenv import load_dotenv
from PIL import Image
from unstructured.partition.pdf import partition_pdf

# LangChain imports
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.storage import InMemoryStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain_chroma import Chroma

# Load environment variables
load_dotenv()

# ============================================================================
# Basic RAG Functions
# These functions implement the core RAG functionality for text-based documents
# ============================================================================

def load_documents(data_dir: str) -> List[Document]:
    """
    Load documents from the data directory.
    This function handles loading text documents from a specified directory.
    """
    documents = []
    
    # Load text documents
    text_loader = DirectoryLoader(
        data_dir,
        glob="**/*.txt",
        loader_cls=TextLoader
    )
    documents.extend(text_loader.load())
    
    return documents

def create_vector_store(documents: List[Document]) -> Chroma:
    """
    Create a vector store from documents.
    This function handles document chunking and vector store creation.
    """
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200       
    )
    splits = text_splitter.split_documents(documents)
    
    # Create vector store
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=OpenAIEmbeddings(),
        persist_directory="./chroma_db"
    )
    
    return vectorstore

def create_qa_chain(vectorstore: Chroma) -> Any:
    """
    Create a QA chain for text-based question answering.
    This function sets up the RAG pipeline for text queries.
    """
    # Create the retriever
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    
    # Create the prompt template
    template = """Answer the question based on the following context. 
    If you cannot answer the question based on the context, say so.

    Context: {context}
    Question: {question}
    
    Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    
    # Create the LLM
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    
    # Create the chain
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain

# ============================================================================
# PDF Processing Functions
# These functions handle PDF document processing and element extraction
# ============================================================================

def extract_pdf_elements(path: str, fname: str):
    """
    Extract images, tables, and chunk text from a PDF file.
    This function uses Unstructured to parse PDF documents.
    """
    return partition_pdf(
        filename=path + fname,
        extract_images_in_pdf=False,
        infer_table_structure=True,
        chunking_strategy="by_title",
        max_characters=4000,
        new_after_n_chars=3800,
        combine_text_under_n_chars=2000,
        image_output_dir_path=path,
    )

def categorize_elements(raw_pdf_elements):
    """
    Categorize extracted elements from a PDF into tables and texts.
    This function separates different types of content from the PDF.
    """
    tables = []
    texts = []
    for element in raw_pdf_elements:
        if "unstructured.documents.elements.Table" in str(type(element)):
            tables.append(str(element))
        elif "unstructured.documents.elements.CompositeElement" in str(type(element)):
            texts.append(str(element))
    return texts, tables

# ============================================================================
# Image Processing Functions
# These functions handle image processing, encoding, and summarization
# ============================================================================

def encode_image(image_path: str) -> str:
    """
    Convert image to base64 string.
    This function prepares images for the vision model.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def image_summarize(img_base64: str, prompt: str) -> str:
    """
    Generate summary for an image using GPT-4 Vision.
    This function uses the vision model to understand and summarize images.
    """
    chat = ChatOpenAI(model="gpt-4-vision-preview", max_tokens=1024)
    msg = chat.invoke([
        HumanMessage(content=[
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"},
            },
        ])
    ])
    return msg.content

def generate_img_summaries(path: str) -> tuple:
    """
    Generate summaries and base64 encoded strings for images.
    This function processes all images in a directory and creates summaries.
    """
    img_base64_list = []
    image_summaries = []
    prompt = """You are an assistant tasked with summarizing images for retrieval. \
    These summaries will be embedded and used to retrieve the raw image. \
    Give a concise summary of the image that is well optimized for retrieval."""

    for img_file in sorted(os.listdir(path)):
        if img_file.endswith(".jpg"):
            img_path = os.path.join(path, img_file)
            base64_image = encode_image(img_path)
            img_base64_list.append(base64_image)
            image_summaries.append(image_summarize(base64_image, prompt))

    return img_base64_list, image_summaries

# ============================================================================
# Text Processing Functions
# These functions handle text processing and summarization
# ============================================================================

def generate_text_summaries(texts: List[str], tables: List[str], summarize_texts: bool = False) -> tuple:
    """
    Summarize text elements using GPT-4.
    This function creates concise summaries of text and tables for retrieval.
    """
    prompt_text = """You are an assistant tasked with summarizing tables and text for retrieval. \
    These summaries will be embedded and used to retrieve the raw text or table elements. \
    Give a concise summary of the table or text that is well optimized for retrieval. Table or text: {element} """
    prompt = ChatPromptTemplate.from_template(prompt_text)

    model = ChatOpenAI(temperature=0, model="gpt-4")
    summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()

    text_summaries = []
    table_summaries = []

    if texts and summarize_texts:
        text_summaries = summarize_chain.batch(texts, {"max_concurrency": 5})
    elif texts:
        text_summaries = texts

    if tables:
        table_summaries = summarize_chain.batch(tables, {"max_concurrency": 5})

    return text_summaries, table_summaries

# ============================================================================
# Image Display Functions
# These functions handle image display and manipulation
# ============================================================================

def display_base64_image(img_base64: str, size: tuple = (400, 400)) -> None:
    """
    Display base64 encoded string as image using PIL.
    This function saves the image to a temporary file and displays it.
    
    Args:
        img_base64: Base64 encoded image string
        size: Tuple of (width, height) for resizing
    """
    # Decode base64 string
    image_data = base64.b64decode(img_base64)
    image = Image.open(io.BytesIO(image_data))
    
    # Resize image
    image = image.resize(size)
    
    # Save to temporary file
    temp_path = f"_out/temp_{uuid.uuid4()}.jpg"
    image.save(temp_path)
    print(f"Image saved to {temp_path}")

def looks_like_base64(sb: str) -> bool:
    """
    Check if the string looks like base64.
    This function validates base64 encoded strings.
    """
    return bool(re.match(r"^[A-Za-z0-9+/=]+$", sb))

def is_image_data(b64data: str) -> bool:
    """
    Check if the base64 string represents an image.
    This function validates image data in base64 format.
    """
    try:
        image_data = base64.b64decode(b64data)
        image = Image.open(io.BytesIO(image_data))
        return True
    except Exception:
        return False

def resize_base64_image(base64_string: str, size: tuple = (128, 128)) -> str:
    """
    Resize a base64 encoded image.
    This function resizes images while maintaining aspect ratio.
    """
    # Decode base64 string
    image_data = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))
    
    # Resize image
    image = image.resize(size)
    
    # Convert back to base64
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

# ============================================================================
# RAG Chain Functions
# These functions implement the multimodal RAG pipeline
# ============================================================================

def create_multi_vector_retriever(
    vectorstore: Chroma,
    text_summaries: List[str],
    texts: List[str],
    table_summaries: List[str],
    tables: List[str],
    image_summaries: List[str],
    images: List[str]
) -> MultiVectorRetriever:
    """
    Create a multi-vector retriever that can handle different types of content.
    This function sets up the retrieval system for multimodal content.
    """
    # Initialize the retriever
    retriever = MultiVectorRetriever(
        vectorstore=vectorstore,
        docstore=InMemoryStore(),
        id_key="doc_id",
    )

    # Helper function to add documents
    def add_documents(retriever, doc_summaries, doc_contents):
        doc_ids = [str(uuid.uuid4()) for _ in doc_contents]
        summary_docs = [
            Document(page_content=s, metadata={"doc_id": doc_ids[i]})
            for i, s in enumerate(doc_summaries)
        ]
        retriever.vectorstore.add_documents(summary_docs)
        retriever.docstore.mset(list(zip(doc_ids, doc_contents)))

    # Add different types of content
    if text_summaries:
        add_documents(retriever, text_summaries, texts)
    if table_summaries:
        add_documents(retriever, table_summaries, tables)
    if image_summaries:
        add_documents(retriever, image_summaries, images)

    return retriever

def split_image_text_types(docs: List[Document]) -> Dict[str, List]:
    """
    Split documents into image and text types.
    This function categorizes documents based on their content type.
    """
    images = []
    texts = []
    for doc in docs:
        if looks_like_base64(doc.page_content) and is_image_data(doc.page_content):
            images.append(doc.page_content)
        else:
            texts.append(doc.page_content)
    return {"images": images, "texts": texts}

def img_prompt_func(data_dict: Dict) -> List[HumanMessage]:
    """
    Create a prompt for image-based queries.
    This function formats the prompt for the vision model.
    """
    messages = []
    if data_dict.get("images"):
        for image in data_dict["images"]:
            image_message = {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image}"},
            }
            messages.append(image_message)
    if data_dict.get("texts"):
        text_message = {
            "type": "text",
            "text": data_dict["texts"][0],
        }
        messages.append(text_message)
    return [HumanMessage(content=messages)]

def multi_modal_rag_chain(retriever: MultiVectorRetriever):
    """
    Create a multimodal RAG chain.
    This function sets up the complete RAG pipeline for multimodal content.
    """
    # Create the LLM
    model = ChatOpenAI(temperature=0, model="gpt-4-vision-preview", max_tokens=1024)

    # Create the chain
    chain = (
        {
            "context": retriever,
            "question": RunnablePassthrough(),
        }
        | RunnableLambda(split_image_text_types)
        | RunnableLambda(img_prompt_func)
        | model
        | StrOutputParser()
    )

    return chain

# ============================================================================
# Main Execution
# ============================================================================

def main():
    """
    Main function to run the multimodal RAG system.
    This function demonstrates the complete multimodal RAG pipeline.
    """
    # Create output directory
    os.makedirs("_out", exist_ok=True)
    
    # Load and process text documents
    print("Loading text documents...")
    documents = load_documents("data")
    
    # Process the specific PDF file
    print("Processing cj.pdf...")
    pdf_path = "data/cj/"
    pdf_file = "cj.pdf"
    print(f"Processing {pdf_file}...")
    elements = extract_pdf_elements(pdf_path, pdf_file)
    
    # Categorize PDF elements
    texts, tables = categorize_elements(elements)
    
    # Generate summaries for texts and tables
    print("Generating summaries for texts and tables...")
    text_summaries, table_summaries = generate_text_summaries(texts, tables, summarize_texts=True)
    
    # Process images
    print("Processing images...")
    img_base64_list, image_summaries = generate_img_summaries(pdf_path)
    
    # Create vector store
    print("Creating vector store...")
    vectorstore = create_vector_store(documents)
    
    # Create multi-vector retriever
    print("Creating multi-vector retriever...")
    retriever = create_multi_vector_retriever(
        vectorstore=vectorstore,
        text_summaries=[doc.page_content for doc in documents] + text_summaries,
        texts=[doc.page_content for doc in documents] + texts,
        table_summaries=table_summaries,
        tables=tables,
        image_summaries=image_summaries,
        images=img_base64_list
    )
    
    # Create RAG chain
    print("Creating RAG chain...")
    chain = multi_modal_rag_chain(retriever)
    
    # Test queries
    test_queries = [
        "What are the EV / NTM and NTM rev growth for MongoDB, Cloudflare, and Datadog?",
        "Give me company names that are interesting investments based on EV / NTM and NTM rev growth. Consider EV / NTM multiples vs historical?",
        "Which companies show the best growth metrics in the data?",
        "What are the key financial ratios and metrics shown in the tables?",
        "Can you analyze the valuation multiples shown in the document?",
        "What are the main trends in revenue growth across different companies?",
        "Which companies have the most attractive EV/Revenue multiples?",
        "What insights can you draw from the financial charts and graphs?",
        "How do the current valuations compare to historical averages?"
    ]
    
    print("\nTesting RAG system with sample queries:")
    print("-" * 50)
    
    output_lines = ["# Multimodal RAG Demo Output\n"]
    for query in test_queries:
        print(f"\nQuery: {query}")
        output_lines.append(f"## Query: {query}\n")
        try:
            result = chain.invoke(query)
            print(f"Answer: {result}")
            output_lines.append(f"**Answer:** {result}\n")
        except Exception as e:
            error_msg = f"Error processing query: {str(e)}"
            print(error_msg)
            output_lines.append(f"**Error:** {error_msg}\n")
        output_lines.append("\n---\n")
    
    # Write output to file
    output_path = "_out/multimodal_rag_output.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    print(f"\nResults written to {output_path}")

if __name__ == "__main__":
    main() 