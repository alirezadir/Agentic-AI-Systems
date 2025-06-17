# LangChain Examples

This directory contains example implementations using LangChain, a framework for building applications with LLMs.

## MultiModal RAG Example

The `multimodal_rag.py` example demonstrates how to build a Retrieval-Augmented Generation (RAG) system that can handle both text and images. It uses:
- GPT-4 Vision for image understanding
- ChromaDB for vector storage
- LangChain's document loaders for text and images
- Recursive text splitting for efficient chunking

### Prerequisites

- Python 3.9+
- OpenAI API key
- Tesseract OCR (for image text extraction)
- Required packages (install using `pip install -r requirements.txt`)

### Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Tesseract OCR:
- On macOS: `brew install tesseract`
- On Ubuntu: `sudo apt-get install tesseract-ocr`
- On Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

4. Set your OpenAI API key:
```bash
export OPENAI_API_KEY=your_api_key_here
```

### Usage

1. Create a `data` directory and add your documents:
```bash
mkdir data
# Add .txt files for text documents
# Add .png, .jpg, or .jpeg files for images
```

2. Run the example:
```bash
python multimodal_rag.py
```

### Features

- **Multi-modal Document Loading**: Handles both text and image files
- **Vector Storage**: Uses ChromaDB for efficient document storage and retrieval
- **Text Splitting**: Implements recursive text splitting for optimal chunking
- **Vision Capabilities**: Uses GPT-4 Vision for image understanding
- **Persistence**: Saves the vector store for future use

### Example Queries

The example includes sample queries:
- "What is shown in the images?"
- "Can you describe the main topics in the text documents?"
- "What are the key points from both text and images?"

### Customization

You can customize the implementation by:
1. Modifying the prompt template in `_create_rag_chain()`
2. Adjusting chunk size and overlap in the text splitter
3. Adding more document loaders for different file types
4. Implementing custom retrieval strategies

### Notes

- The system uses GPT-4 Vision for image understanding, which requires an OpenAI API key
- Image processing may be slow depending on the size and number of images
- Text extraction from images depends on Tesseract OCR quality

## Resources

- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Tesseract OCR Documentation](https://github.com/tesseract-ocr/tesseract) 