"""
Module 6 — Hallucination control: relevance threshold & answer validation.
"""

import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

RELEVANCE_THRESHOLD = 0.25  # Minimum hybrid score to consider results relevant

FALLBACK_RESPONSE = (
    "I don't have enough information to answer that question. "
    "Please try rephrasing your query or contact our support team."
)


def check_relevance(results: list[dict], threshold: float = RELEVANCE_THRESHOLD) -> bool:
    """Return True if retrieved results are relevant enough."""
    if not results:
        return False
    avg_score = sum(r["score"] for r in results) / len(results)
    return avg_score >= threshold


def validate_answer(query: str, answer: str, context: str) -> dict:
    """
    Use Groq to verify the answer is supported by context.
    Returns {"valid": bool, "reason": str}
    """
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key or api_key == "your_groq_api_key_here":
        # Skip validation if no API key — assume valid in dev
        return {"valid": True, "reason": "Validation skipped (no API key)"}

    client = Groq(api_key=api_key)

    verification_prompt = f"""You are a strict fact-checker. Given the following:

CONTEXT:
{context}

QUESTION: {query}

ANSWER: {answer}

Is the answer fully supported by the context? Reply with ONLY a JSON object:
{{"valid": true/false, "reason": "brief explanation"}}"""

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": verification_prompt}],
            temperature=0.0,
            max_tokens=150,
        )
        text = response.choices[0].message.content.strip()

        # Try to parse JSON response
        import json
        # Handle cases where model wraps JSON in markdown
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()

        result = json.loads(text)
        return {"valid": bool(result.get("valid", True)), "reason": result.get("reason", "")}
    except Exception:
        # If validation fails, assume valid to not block the user
        return {"valid": True, "reason": "Validation inconclusive"}
