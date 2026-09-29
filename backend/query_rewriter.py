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

    if history:
        history_text = "\n".join(
        [
            f"{message['role']}: {message['content']}"
            for message in history
        ])
    
    else:
        history_text = "No previous conversation."
    

    prompt = f"""
You are a query rewriting component for a portfolio AI assistant.

Rewrite the user's current question into a concise, standalone,
retrieval-friendly search query.

Use conversation history to resolve references when previous
conversation exists.

When no conversation history exists, optimize the current question
for semantic retrieval without changing its meaning.
such as:
- they
- this
- that
- what about
- why
- how
- those
- the project
- the technology

Preserve important:
- entities
- topics
- technologies
- project names
- organizations
- time periods
- relationships

Do not answer the question.

Do not invent information.

If the current question is already a good retrieval query,
you may return it unchanged.

Conversation history:

{history_text}

Current question:

{question}

Return ONLY the rewritten search query.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )

    return response.text.strip()


if __name__ == "__main__":

    test_questions = [
        "What projects did Yogish complete during college?",
        "What are Yogish's completed college projects?",
        "Yogish college projects completed",
        "What did Yogish build with PHP?",
    ]

    for question in test_questions:

        print("\n" + "=" * 60)
        print("Original question:")
        print(question)

        rewritten = rewrite_query(question, [])

        print("\nRewritten query:")
        print(rewritten)