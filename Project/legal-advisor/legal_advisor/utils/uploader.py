import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def check_file_type(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        return "text"
    elif ext == ".pdf":
        return "pdf"
    else:
        raise ValueError(f"Unsupported file format: {ext}")

class Loader:
    def __init__(self, path: str):
        self.path = path 
    
    def upload(self):
        check = check_file_type(self.path)
        if check == "text":
            return TextLoader(file_path=self.path, encoding="utf-8").load()
        elif check == "pdf":
            return PyPDFLoader(file_path=self.path).load()

class Chunker:
    def __init__(self, text: str):
        self.text = text

    def split(self, chunk_size: int, chunk_overlap: int = 0):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        return splitter.split_text(self.text)

    def for_embedding(self):
        return self.split(chunk_size=2000, chunk_overlap=100)

    def for_summary(self):
        return self.split(chunk_size=10000, chunk_overlap=0)
