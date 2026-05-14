import streamlit as st
from langchain_community.llms import Ollama
from app.retrieval.hybrid import get_hybrid_retriever

st.set_page_config(page_title="Production RAG Chatbot")

st.title("📘 AI-Powered RAG Chatbot")
st.write("Ask questions from your PDF documents")

query = st.text_input("Enter your question:")

if st.button("Get Answer"):
    if query:
        with st.spinner("Thinking..."):

            bm25_retriever, vector_retriever = get_hybrid_retriever()

            docs_bm25 = bm25_retriever.invoke(query)
            docs_vector = vector_retriever.invoke(query)

            docs = docs_bm25 + docs_vector

            seen = set()
            unique_docs = []

            for doc in docs:
                if doc.page_content not in seen:
                    seen.add(doc.page_content)
                    unique_docs.append(doc)

            context = "\n\n".join(
                [doc.page_content for doc in unique_docs]
            )

            llm = Ollama(model="llama3")

            prompt = f"""
Use the following context to answer the question.

Context:
{context}

Question:
{query}
"""

            response = llm.invoke(prompt)

            st.subheader("Answer:")
            st.write(response)