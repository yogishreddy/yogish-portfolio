import json

from retriever import retrieve


QUESTIONS_FILE = "eval/questions.json"


def load_questions():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_question(question_data):
    question = question_data["question"]
    expected_documents = question_data["expected_documents"]

    results = retrieve(question, top_k=3)

    retrieved_ids = [result["id"] for result in results]

    hit_at_1 = any(
        document_id in expected_documents
        for document_id in retrieved_ids[:1]
    )

    hit_at_3 = any(
        document_id in expected_documents
        for document_id in retrieved_ids[:3]
    )

    return {
        "question": question,
        "expected_documents": expected_documents,
        "retrieved_documents": retrieved_ids,
        "hit_at_1": hit_at_1,
        "hit_at_3": hit_at_3,
    }


def main():
    questions = load_questions()

    results = []

    for question_data in questions:
        result = evaluate_question(question_data)
        results.append(result)

        print("\nQuestion:")
        print(result["question"])

        print("\nExpected:")
        print(result["expected_documents"])

        print("\nRetrieved:")
        print(result["retrieved_documents"])

        print(f"\nHit@1: {result['hit_at_1']}")
        print(f"Hit@3: {result['hit_at_3']}")
        print("-" * 60)


if __name__ == "__main__":
    main()