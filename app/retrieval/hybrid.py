from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.retrievers import BM25Retriever

from app.ingestion.loader import load_documents, split_documents

CHROMA_PATH = "db"


def get_hybrid_retriever():
    print("Loading documents...")

    documents = load_documents()
    chunks = split_documents(documents)

    print("Creating BM25 retriever...")

    bm25_retriever = BM25Retriever.from_documents(chunks)
    bm25_retriever.k = 4

    print("Connecting ChromaDB...")

    embedding_function = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_function
    )

    vector_retriever = db.as_retriever(search_kwargs={"k": 4})

    return bm25_retriever, vector_retriever