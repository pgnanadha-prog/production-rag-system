from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

DATA_PATH = "data/raw_docs"

def load_documents():
    documents = []

    for file in os.listdir(DATA_PATH):
        if file.endswith(".pdf"):
            file_path = os.path.join(DATA_PATH, file)

            loader = PyPDFLoader(file_path)
            docs = loader.load()

            documents.extend(docs)

    return documents

def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = text_splitter.split_documents(documents)

    return chunks

if __name__ == "__main__":
    docs = load_documents()
    chunks = split_documents(docs)

    print(f"Total documents loaded: {len(docs)}")
    print(f"Total chunks created: {len(chunks)}")