"""
Module 5 — Groq LLM integration for answer generation.
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

_client = None

SYSTEM_PROMPT = """You are a helpful SaaS support assistant for TaskFlow AI.
You MUST answer ONLY using the provided context below.
If the context does not contain enough information to answer the question, say:
"I don't have enough information to answer that question. Please try rephrasing or contact our support team."

Rules:
- Be concise and professional.
- Do NOT make up information.
- Do NOT reference information outside the provided context.
- Use bullet points for multi-step instructions.
"""


def _get_client() -> Groq:
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY", "")
        if not api_key or api_key == "your_groq_api_key_here":
            raise ValueError(
                "GROQ_API_KEY is not set. Add it to backend/.env"
            )
        _client = Groq(api_key=api_key)
    return _client


def generate_answer(query: str, context: str) -> str:
    """
    Generate an answer using Groq LLM grounded in retrieved context.
    """
    client = _get_client()

    user_message = f"""Context:
{context}

User Question: {query}

Answer the question using ONLY the context provided above."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.3,
        max_tokens=512,
        top_p=0.9,
    )
    return response.choices[0].message.content.strip()
