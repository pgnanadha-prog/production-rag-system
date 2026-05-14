def evaluate_answer(query, response, docs):
    print("\n==============================")
    print("EVALUATION REPORT")
    print("==============================\n")

    score = 0

    if len(response) > 50:
        score += 1
        print("✅ Answer length looks good")
    else:
        print("⚠ Answer may be too short")

    if len(docs) >= 2:
        score += 1
        print("✅ Multiple relevant documents retrieved")
    else:
        print("⚠ Very few documents retrieved")

    if query.lower() in response.lower():
        score += 1
        print("✅ Query terms found in answer")
    else:
        print("⚠ Query terms missing in answer")

    print(f"\nFinal Score: {score}/3")

    if score == 3:
        print("Excellent Answer Quality 🔥")
    elif score == 2:
        print("Good Answer Quality ✅")
    else:
        print("Needs Improvement ⚠")

    print("\n==============================\n")