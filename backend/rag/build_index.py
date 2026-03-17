"""
Module 3 — Build FAISS index from FAQ dataset.

Usage:
    cd backend
    python -m rag.build_index
"""

import json
import os
import sys
import numpy as np

# Add parent dir so Django settings can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "data")
DOCS_PATH = os.path.join(DATA_DIR, "docs.json")
INDEX_DIR = os.path.join(DATA_DIR, "faiss_index")


def build():
    import faiss
    from sentence_transformers import SentenceTransformer

    print("📦  Loading dataset...")
    with open(DOCS_PATH, "r", encoding="utf-8") as f:
        docs = json.load(f)

    # Build text chunks
    chunks = [f"Q: {d['question']}\nA: {d['answer']}" for d in docs]
    print(f"    → {len(chunks)} FAQ chunks loaded")

    # Generate embeddings
    print("🔢  Generating embeddings (all-MiniLM-L6-v2)...")
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    embeddings = model.encode(chunks, show_progress_bar=True, convert_to_numpy=True)
    embeddings = embeddings.astype("float32")

    # Build FAISS index
    print("🗂️  Building FAISS index...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)  # Inner-product (cosine after normalisation)
    faiss.normalize_L2(embeddings)
    index.add(embeddings)

    # Save
    os.makedirs(INDEX_DIR, exist_ok=True)
    faiss.write_index(index, os.path.join(INDEX_DIR, "index.faiss"))
    np.save(os.path.join(INDEX_DIR, "chunks.npy"), chunks)
    print(f"✅  Index saved to {INDEX_DIR}  ({index.ntotal} vectors, dim={dimension})")


if __name__ == "__main__":
    build()
