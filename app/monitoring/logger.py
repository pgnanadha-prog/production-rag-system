import time


def log_query(query):
    print("\n==============================")
    print("USER QUESTION:")
    print(query)
    print("==============================\n")


def log_retrieved_docs(docs):
    print("\nRETRIEVED DOCUMENTS:\n")

    for i, doc in enumerate(docs, 1):
        print(f"Document {i}:")
        print(doc.page_content[:300])
        print("\n----------------------\n")


def log_response(response):
    print("\nFINAL ANSWER:\n")
    print(response)
    print("\n==============================\n")


def start_timer():
    return time.time()


def end_timer(start_time):
    end_time = time.time()
    total_time = end_time - start_time

    print(f"\nResponse Time: {total_time:.2f} seconds\n")