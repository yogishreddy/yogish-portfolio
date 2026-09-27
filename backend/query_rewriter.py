import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured")


client = genai.Client(api_key=GEMINI_API_KEY)

GEMINI_MODEL = "gemini-3.5-flash-lite"


def rewrite_query(question, history):

    if not history:
        return question

    history_text = "\n".join(
        [
            f"{message['role']}: {message['content']}"
            for message in history
        ]
    )

    prompt = f"""
You are a query rewriting component for a portfolio AI assistant.

Your job is to rewrite the user's current question into a
standalone search query that can be used for semantic retrieval.

Use the conversation history only to resolve references such as:

- it
- they
- this
- that
- what about
- why
- how
- those
- the project
- the technology

Do not answer the question.

Do not add information that is not present in the conversation.

If the current question is already standalone, return it unchanged.

Conversation history:

{history_text}

Current question:

{question}

Return ONLY the rewritten standalone search query.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )

    return response.text.strip()


if __name__ == "__main__":

    history = [
        {
            "role": "user",
            "content": "What is the AI SRE Platform?",
        },
        {
            "role": "assistant",
            "content": (
                "The AI SRE Platform is an agentic AI system "
                "designed to investigate CI/CD incidents, "
                "analyze failures, gather evidence, and assist "
                "with safe remediation."
            ),
        },
    ]

    question = "Why is it useful?"

    print("Calling Gemini...")

    rewritten = rewrite_query(question, history)

    print("\nOriginal question:")
    print(question)

    print("\nRewritten query:")
    print(rewritten)