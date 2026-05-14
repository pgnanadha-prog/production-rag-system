from langchain_community.llms import Ollama
from app.retrieval.hybrid import get_hybrid_retriever
from app.monitoring.logger import (
    log_query,
    log_retrieved_docs,
    log_response,
    start_timer,
    end_timer
)
from app.evaluation.evaluator import evaluate_answer


def ask_question():
    print("Starting Production RAG System...")

    start_time = start_timer()

    bm25_retriever, vector_retriever = get_hybrid_retriever()

    query = input("Ask your question: ")

    log_query(query)

    docs_bm25 = bm25_retriever.invoke(query)
    docs_vector = vector_retriever.invoke(query)

    docs = docs_bm25 + docs_vector

    seen = set()
    unique_docs = []

    for doc in docs:
        if doc.page_content not in seen:
            seen.add(doc.page_content)
            unique_docs.append(doc)

    log_retrieved_docs(unique_docs)

    context = "\n\n".join([doc.page_content for doc in unique_docs])

    llm = Ollama(model="llama3")

    prompt = f"""
Use the following context to answer the question.

Context:
{context}

Question:
{query}
"""

    response = llm.invoke(prompt)

    log_response(response)

    evaluate_answer(query, response, unique_docs)

    end_timer(start_time)


if __name__ == "__main__":
    ask_question()