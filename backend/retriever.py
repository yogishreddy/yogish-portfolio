import json
import math
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


# --------------------------------------------------
# Gemini configuration
# --------------------------------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured")


client = genai.Client(api_key=GEMINI_API_KEY)


# --------------------------------------------------
# Load knowledge index
# --------------------------------------------------

with open("knowledge/index.json", "r", encoding="utf-8") as file:
    index = json.load(file)


# --------------------------------------------------
# Cosine similarity
# --------------------------------------------------

def cosine_similarity(vector_a, vector_b):

    dot_product = sum(
        a * b for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = math.sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


# --------------------------------------------------
# Embed query
# --------------------------------------------------

def embed_query(query):

    result = client.models.embed_content(
        model="gemini-embedding-2",
        contents=query,
        config=types.EmbedContentConfig(
            output_dimensionality=768
        ),
    )

    return result.embeddings[0].values


# --------------------------------------------------
# Retrieve relevant documents
# --------------------------------------------------

def retrieve(query, top_k=3):

    query_embedding = embed_query(query)

    results = []

    for document in index:

        similarity = cosine_similarity(
            query_embedding,
            document["embedding"],
        )

        results.append(
            {
                "id": document["id"],
                "title": document["title"],
                "content": document["content"],
                "similarity": similarity,
            }
        )

    results.sort(
        key=lambda item: item["similarity"],
        reverse=True,
    )

    return results[:top_k]


# --------------------------------------------------
# Local testing
# --------------------------------------------------

if __name__ == "__main__":

    query = "Yogish college projects completed"

    results = retrieve(query)

    print("\nQuery:")
    print(query)

    print("\nRetrieved documents:")

    for result in results:

        print(
            f"\n{result['title']}"
            f" — similarity: {result['similarity']:.4f}"
        )

        print(result["content"])