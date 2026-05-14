from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from app.ingestion.loader import load_documents, split_documents

CHROMA_PATH = "db"

def create_vector_store():
    print("Loading documents...")

    documents = load_documents()
    chunks = split_documents(documents)

    print(f"Documents loaded: {len(documents)}")
    print(f"Chunks created: {len(chunks)}")

    print("Creating embeddings...")

    embedding_function = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    print("Saving to ChromaDB...")

    db = Chroma.from_documents(
        chunks,
        embedding_function,
        persist_directory=CHROMA_PATH
    )

    db.persist()

    print("Vector database created successfully!")

if __name__ == "__main__":
    create_vector_store()