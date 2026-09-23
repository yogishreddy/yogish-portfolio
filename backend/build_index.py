import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not configured")

client = genai.Client(api_key=api_key)


with open("knowledge/documents.json", "r", encoding="utf-8") as file:
    documents = json.load(file)


index = []


for document in documents:
    print(f"Embedding: {document['title']}")

    result = client.models.embed_content(
        model="gemini-embedding-2",
        contents=document["content"],
        config=types.EmbedContentConfig(
            output_dimensionality=768
        ),
    )

    embedding = result.embeddings[0].values

    index.append(
        {
            "id": document["id"],
            "title": document["title"],
            "content": document["content"],
            "embedding": embedding,
        }
    )


with open("knowledge/index.json", "w", encoding="utf-8") as file:
    json.dump(index, file)


print(f"\nIndexed {len(index)} documents.")