"""
Module 4 — Hybrid Retrieval: FAISS (semantic) + BM25 (keyword).
"""

import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "data")
INDEX_DIR = os.path.join(DATA_DIR, "faiss_index")

# ── Lazy-loaded singletons ──────────────────────────────
_model = None
_index = None
_chunks = None
_bm25 = None


def _load():
    """Load model, FAISS index, and BM25 corpus once."""
    global _model, _index, _chunks, _bm25

    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    if _index is None:
        _index = faiss.read_index(os.path.join(INDEX_DIR, "index.faiss"))
        _chunks = np.load(os.path.join(INDEX_DIR, "chunks.npy"), allow_pickle=True).tolist()

    if _bm25 is None:
        tokenised = [chunk.lower().split() for chunk in _chunks]
        _bm25 = BM25Okapi(tokenised)


# ── Search functions ────────────────────────────────────

def semantic_search(query: str, top_k: int = 5) -> list[dict]:
    """FAISS cosine-similarity search."""
    _load()
    vec = _model.encode([query], convert_to_numpy=True).astype("float32")
    faiss.normalize_L2(vec)
    scores, indices = _index.search(vec, top_k)
    return [
        {"text": _chunks[i], "score": round(float(scores[0][rank]), 4)}
        for rank, i in enumerate(indices[0])
        if i != -1
    ]


def keyword_search(query: str, top_k: int = 5) -> list[dict]:
    """BM25 keyword search."""
    _load()
    tokens = query.lower().split()
    scores = _bm25.get_scores(tokens)
    top_indices = np.argsort(scores)[::-1][:top_k]
    return [
        {"text": _chunks[i], "score": round(float(scores[i]), 4)}
        for i in top_indices
        if scores[i] > 0
    ]


def hybrid_search(query: str, top_k: int = 5) -> list[dict]:
    """
    Merge semantic + keyword results.
    Normalise scores to [0,1] within each method, average, re-rank.
    """
    sem = semantic_search(query, top_k)
    kw = keyword_search(query, top_k)

    combined: dict[str, dict] = {}

    # Normalise semantic scores
    sem_max = max((r["score"] for r in sem), default=1) or 1
    for r in sem:
        key = r["text"]
        combined[key] = {"text": key, "sem": r["score"] / sem_max, "kw": 0.0}

    # Normalise keyword scores
    kw_max = max((r["score"] for r in kw), default=1) or 1
    for r in kw:
        key = r["text"]
        if key in combined:
            combined[key]["kw"] = r["score"] / kw_max
        else:
            combined[key] = {"text": key, "sem": 0.0, "kw": r["score"] / kw_max}

    # Weighted average (60% semantic, 40% keyword)
    results = []
    for v in combined.values():
        score = 0.6 * v["sem"] + 0.4 * v["kw"]
        results.append({"text": v["text"], "score": round(score, 4)})

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]
