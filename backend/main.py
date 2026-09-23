import os
import json
import requests
from fastapi.responses import StreamingResponse
from retriever import retrieve
from query_rewriter import rewrite_query

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3:8b"

load_dotenv()


app = FastAPI(
    title="Yogish AI Portfolio",
    description="AI-powered personal portfolio backend",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = []



@app.get("/")
def root():
    return {
        "name": "Yogish AI Portfolio",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }

def generate_from_ollama(prompt, sources):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "stream": True,
            "options": {
                "temperature": 0.1,
            },
        },
        stream=True,
    )

    response.raise_for_status()

    for line in response.iter_lines():
        if not line:
            continue

        data = json.loads(line.decode("utf-8"))

        # Only send actual answer content.
        # Ignore Ollama/Qwen thinking chunks.
        content = data.get("message", {}).get("content", "")

        if content:
            yield json.dumps({
                "type": "token",
                "content": content,
            }) + "\n"

    # Send retrieved sources after the answer finishes.
    yield json.dumps({
        "type": "sources",
        "sources": [
            {
                "title": source["title"],
                "similarity": source["similarity"],
            }
            for source in sources
        ],
    }) + "\n"

    yield json.dumps({
        "type": "done",
    }) + "\n"

@app.post("/chat")

def chat(request: ChatRequest):
    recent_history = request.history[-10:]
    history_text = "\n".join(
    [
        f"{message.role}: {message.content}"
        for message in recent_history
    ])
    
    search_query = rewrite_query(
    request.message,
    [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in recent_history
    ],
)

    results = retrieve(search_query, top_k=3)

# Only keep sufficiently relevant documents
    results = [
        result
        for result in results
        if result["similarity"] >= 0.70
]

    context = "\n\n".join(
        [
            f"Source: {result['title']}\n{result['content']}"
            for result in results
        ]
    )

    prompt = f"""
You are Yogish's personal portfolio AI assistant.

Your job is to answer questions about Yogish using the
provided portfolio knowledge and conversation history.

Use conversation history to understand references,
follow-up questions, and conversational context.

Use the knowledge context as the source of truth for
facts about Yogish.

If the Knowledge context contains no document that is
clearly relevant to the question, do not answer using
general knowledge. Say:
"I don't have enough information about that."

Do not treat statements from conversation history as
new facts about Yogish unless they are supported by
the knowledge context.

If the knowledge context does not contain enough
information to answer a question about Yogish,
say that you don't have enough information.

Do not invent experience, skills, projects, technologies,
companies, responsibilities, achievements, benefits, results,
or production experience.

Do not explain why a stated capability is beneficial unless
the benefit is explicitly stated in the Knowledge context.

Do not convert a capability into a claimed outcome.

For example:
"analyze failures" does NOT mean "improves reliability".
"assist with safe remediation" does NOT mean "reduces incidents".
"gather evidence" does NOT mean "improves decision-making".

Repeat the supported capability rather than inferring its benefit.

The Knowledge context is the ONLY source of factual information
about Yogish.

Use only information explicitly stated in the Knowledge context.

Do NOT use your general knowledge to fill gaps.

For questions asking WHY something is useful, its benefits,
advantages, impact, or results:
- Only state benefits explicitly supported by the Knowledge context.
- Do not infer benefits from the technologies or project description.
- If the Knowledge context does not explicitly state the benefits,
  say that the available portfolio information does not specify them.

For questions about experience:
- A planned or ongoing project is NOT proof of completed experience.
- A technology mentioned in a project is NOT proof of production
  experience with that technology.
- Never convert planned work into completed work.

If the requested information is not explicitly supported by the
Knowledge context, say:
"I don't have enough information about that."

Before answering, check every factual claim against the
Knowledge context. If a claim cannot be directly supported
by the Knowledge context, do not include it.

Recent conversation history:
{history_text}

Knowledge context:
{context}

Search query used to retrieve the knowledge:
{search_query}

Current user question:
{request.message}
"""

    return StreamingResponse(
    generate_from_ollama(prompt, results),
    media_type="application/x-ndjson",
)