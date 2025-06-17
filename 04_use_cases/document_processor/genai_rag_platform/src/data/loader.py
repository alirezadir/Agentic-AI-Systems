import os
from typing import List

def load_documents_from_folder(folder_path: str) -> List[str]:
    """Loads all text documents from a folder."""
    docs = []
    for filename in os.listdir(folder_path):
        path = os.path.join(folder_path, filename)
        if os.path.isfile(path) and path.endswith(".md"):
            with open(path, "r", encoding="utf-8") as f:
                docs.append(f.read())
    return docs
