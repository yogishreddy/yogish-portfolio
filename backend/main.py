import os
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

from retriever import retrieve
from query_rewriter import rewrite_query


load_dotenv()


# --------------------------------------------------
# Gemini configuration
# --------------------------------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured")

client = genai.Client(api_key=GEMINI_API_KEY)

GEMINI_MODEL = "gemini-3.5-flash-lite"


# --------------------------------------------------
# FastAPI
# --------------------------------------------------

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


# --------------------------------------------------
# Request models
# --------------------------------------------------

class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = []


# --------------------------------------------------
# Health endpoints
# --------------------------------------------------

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


# --------------------------------------------------
# Gemini streaming
# --------------------------------------------------

def generate_from_gemini(prompt, sources):

    try:

        # Send sources first so the frontend knows
        # which documents were retrieved.
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


        # Stream Gemini response
        response_stream = client.models.generate_content_stream(
            model=GEMINI_MODEL,
            contents=prompt,
        )


        for chunk in response_stream:

            if chunk.text:

                yield json.dumps({
                    "type": "token",
                    "content": chunk.text,
                }) + "\n"


        # Tell frontend generation is complete
        yield json.dumps({
            "type": "done",
        }) + "\n"


    except Exception as error:

        yield json.dumps({
            "type": "error",
            "content": str(error),
        }) + "\n"


# --------------------------------------------------
# Chat endpoint
# --------------------------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    # --------------------------------------------------
    # Keep only the most recent conversation
    # --------------------------------------------------

    recent_history = request.history[-10:]


    history_text = "\n".join(
        [
            f"{message.role}: {message.content}"
            for message in recent_history
        ]
    )


    # --------------------------------------------------
    # Rewrite the user's query using conversation history
    # --------------------------------------------------

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


    # --------------------------------------------------
    # Retrieve relevant portfolio knowledge
    # --------------------------------------------------

    results = retrieve(
        search_query,
        top_k=3,
    )


    # --------------------------------------------------
    # Remove weak retrieval results
    # --------------------------------------------------

    results = [
        result
        for result in results
        if result["similarity"] >= 0.70
    ]


    # --------------------------------------------------
    # Build knowledge context
    # --------------------------------------------------

    context = "\n\n".join(
        [
            f"Source: {result['title']}\n{result['content']}"
            for result in results
        ]
    )


    # --------------------------------------------------
    # Prompt
    # --------------------------------------------------

    prompt = f"""
You are Yogish's personal portfolio AI assistant.

Your job is to answer questions about Yogish using the
provided portfolio knowledge and conversation history.

Use conversation history to understand references,
follow-up questions, and conversational context.

Use the Knowledge context as the source of truth for
facts about Yogish.

If the Knowledge context contains no document that is
clearly relevant to the question, do not answer using
general knowledge.

Say:

"I don't have enough information about that."


Do not treat statements from conversation history as
new facts about Yogish unless they are supported by
the Knowledge context.

Do not invent experience, skills, projects, technologies,
companies, responsibilities, achievements, benefits,
results, or production experience.


IMPORTANT RULES:

- The Knowledge context is the ONLY source of factual
  information about Yogish.

- Use only information explicitly stated in the
  Knowledge context.

- Do NOT use general knowledge to fill gaps.

- A planned or ongoing project is NOT proof of completed
  experience.

- A technology mentioned in a project is NOT proof of
  production experience with that technology.

- Never convert planned work into completed work.


For questions asking WHY something is useful, its benefits,
advantages, impact, or results:

- Only state benefits explicitly supported by the
  Knowledge context.

- Do not infer benefits from technologies or project
  descriptions.

- If the Knowledge context does not explicitly state
  the benefits, say that the available portfolio
  information does not specify them.


Do not convert capabilities into claimed outcomes.

For example:

"analyze failures" does NOT mean
"improves reliability".

"assist with safe remediation" does NOT mean
"reduces incidents".

"gather evidence" does NOT mean
"improves decision-making".


Repeat the supported capability instead of inferring
its benefit.


Before answering, check every factual claim against
the Knowledge context.

If a claim cannot be directly supported by the
Knowledge context, do not include it.


Recent conversation history:

{history_text}


Knowledge context:

{context}


Search query used to retrieve the knowledge:

{search_query}


Current user question:

{request.message}
"""


    # --------------------------------------------------
    # Stream response
    # --------------------------------------------------

    return StreamingResponse(
        generate_from_gemini(prompt, results),
        media_type="application/x-ndjson",
    )