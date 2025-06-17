# --- Multimodal RAG with CLIP Embeddings and LangChain ---
# This script demonstrates a multimodal retrieval-augmented generation (RAG) pipeline
# using OpenCLIP embeddings for images and text, with LangChain and Chroma vectorstore.

# NOTE: The following pip commands are for notebook environments.
# In scripts, install dependencies via requirements.txt or pip before running.
# ! pip install -U langchain openai langchain-chroma langchain-experimental
# ! pip install "unstructured[all-docs]==0.10.19" pillow pydantic lxml matplotlib tiktoken open_clip_torch torch

import os
import uuid
import base64
import io
import numpy as np
import chromadb
from PIL import Image as _PILImage
from PIL import Image
from io import BytesIO

# Path to folder containing the PDF and extracted images
path = "/Users/rlm/Desktop/photos/"

# --- 1. Extract images, tables, and chunked text from PDF ---
from unstructured.partition.pdf import partition_pdf

# Partition the PDF into elements (text, tables, images)
raw_pdf_elements = partition_pdf(
    filename=os.path.join(path, "photos.pdf"),
    extract_images_in_pdf=True,
    infer_table_structure=True,
    chunking_strategy="by_title",
    max_characters=4000,
    new_after_n_chars=3800,
    combine_text_under_n_chars=2000,
    image_output_dir_path=path,
)

# --- 2. Categorize extracted elements into tables and texts ---
tables = []
texts = []
for element in raw_pdf_elements:
    # Identify tables and composite text elements by type string
    if "unstructured.documents.elements.Table" in str(type(element)):
        tables.append(str(element))
    elif "unstructured.documents.elements.CompositeElement" in str(type(element)):
        texts.append(str(element))

# --- 3. Set up Chroma vectorstore with OpenCLIP embeddings ---
from langchain_chroma import Chroma
from langchain_experimental.open_clip import OpenCLIPEmbeddings

# Initialize Chroma vectorstore for multimodal retrieval
vectorstore = Chroma(
    collection_name="mm_rag_clip_photos",
    embedding_function=OpenCLIPEmbeddings()
)

# --- 4. Add images to the vectorstore ---
# Gather all .jpg image file paths in the directory
image_uris = sorted([
    os.path.join(path, image_name)
    for image_name in os.listdir(path)
    if image_name.endswith(".jpg")
])
vectorstore.add_images(uris=image_uris)

# --- 5. Add text documents to the vectorstore ---
vectorstore.add_texts(texts=texts)

# --- 6. Create a retriever from the vectorstore ---
retriever = vectorstore.as_retriever()

# --- 7. Utilities for image handling ---

def resize_base64_image(base64_string, size=(128, 128)):
    """
    Resize a base64-encoded image to the given size and return as base64 string.
    """
    img_data = base64.b64decode(base64_string)
    img = Image.open(io.BytesIO(img_data))
    resized_img = img.resize(size, Image.LANCZOS)
    buffered = io.BytesIO()
    # Use original format if possible, else default to JPEG
    fmt = img.format if img.format else "JPEG"
    resized_img.save(buffered, format=fmt)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def is_base64(s):
    """
    Check if a string is valid base64-encoded data.
    """
    try:
        return base64.b64encode(base64.b64decode(s)) == s.encode()
    except Exception:
        return False

def split_image_text_types(docs):
    """
    Split retrieved docs into base64 images and text.
    Images are resized for display/processing.
    Returns a dict with 'images' and 'texts' lists.
    """
    images, text = [], []
    for doc in docs:
        content = doc.page_content
        if is_base64(content):
            images.append(resize_base64_image(content, size=(250, 250)))
        else:
            text.append(content)
    return {"images": images, "texts": text}

# --- 8. RAG chain setup with LangChain and OpenAI Vision model ---
from operator import itemgetter
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI

def prompt_func(data_dict):
    """
    Construct a prompt for the vision model, including images and related text.
    """
    formatted_texts = "\n".join(data_dict["context"]["texts"])
    messages = []

    # If images are present, add the first image as an image_url message
    if data_dict["context"]["images"]:
        image_message = {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{data_dict['context']['images'][0]}"
            },
        }
        messages.append(image_message)

    # Add the main text message with instructions and context
    text_message = {
        "type": "text",
        "text": (
            "As an expert art critic and historian, your task is to analyze and interpret images, "
            "considering their historical and cultural significance. Alongside the images, you will be "
            "provided with related text to offer context. Both will be retrieved from a vectorstore based "
            "on user-input keywords. Please use your extensive knowledge and analytical skills to provide a "
            "comprehensive summary that includes:\n"
            "- A detailed description of the visual elements in the image.\n"
            "- The historical and cultural context of the image.\n"
            "- An interpretation of the image's symbolism and meaning.\n"
            "- Connections between the image and the related text.\n\n"
            f"User-provided keywords: {data_dict['question']}\n\n"
            "Text and / or tables:\n"
            f"{formatted_texts}"
        ),
    }
    messages.append(text_message)
    return [HumanMessage(content=messages)]

# Initialize the OpenAI Vision model (GPT-4-vision-preview)
model = ChatOpenAI(
    temperature=0,
    model="gpt-4-vision-preview",
    max_tokens=1024
)

# Compose the RAG chain: retrieve, split, prompt, run model, parse output
chain = (
    {
        "context": retriever | RunnableLambda(split_image_text_types),
        "question": RunnablePassthrough(),
    }
    | RunnableLambda(prompt_func)
    | model
    | StrOutputParser()
)

# --- 9. Display utilities for images in Jupyter/IPython ---
from IPython.display import HTML, display

def plt_img_base64(img_base64):
    """
    Display a base64-encoded image inline in a Jupyter notebook.
    """
    image_html = f'<img src="data:image/jpeg;base64,{img_base64}" />'
    display(HTML(image_html))

# --- 10. Retrieve and display results for a sample query ---
# Retrieve top-10 relevant docs for the query
docs = retriever.invoke("Woman with children", k=10)
for doc in docs:
    if is_base64(doc.page_content):
        plt_img_base64(doc.page_content)
    else:
        print(doc.page_content)

# --- 11. Run the full RAG chain for the query ---
chain.invoke("Woman with children")