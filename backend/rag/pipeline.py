"""
Module 7 — RAG Pipeline: orchestrates retrieval → generation → validation.
"""

from .retriever import hybrid_search
from .llm import generate_answer
from .validator import check_relevance, validate_answer, FALLBACK_RESPONSE


def run_pipeline(query: str, top_k: int = 5) -> dict:
    """
    Full RAG pipeline:
      1. Hybrid retrieval
      2. Relevance check
      3. LLM generation
      4. Answer validation
      5. Return structured response
    """
    # 1 — Retrieve
    results = hybrid_search(query, top_k=top_k)

    # 2 — Relevance check
    if not check_relevance(results):
        return {
            "answer": FALLBACK_RESPONSE,
            "sources": results,
            "confidence": 0.0,
            "validated": False,
        }

    # 3 — Build context & generate
    context = "\n\n---\n\n".join(r["text"] for r in results)
    answer = generate_answer(query, context)

    # 4 — Validate
    validation = validate_answer(query, answer, context)

    if not validation["valid"]:
        return {
            "answer": FALLBACK_RESPONSE,
            "sources": results,
            "confidence": 0.0,
            "validated": False,
            "validation_reason": validation["reason"],
        }

    # 5 — Compute confidence (average of top scores)
    confidence = round(sum(r["score"] for r in results) / len(results), 4) if results else 0.0

    return {
        "answer": answer,
        "sources": results,
        "confidence": confidence,
        "validated": True,
    }
