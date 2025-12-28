import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from functools import lru_cache

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

CHUNKS_FILE = os.path.join(PROCESSED_DIR, "chunks.json")
EMBEDDINGS_FILE = os.path.join(PROCESSED_DIR, "embeddings.npy")
FAISS_INDEX_FILE = os.path.join(PROCESSED_DIR, "faiss.index")

# ------------------------------------------------------------------
# Retrieval config
# ------------------------------------------------------------------

TOP_K = 6
SIM_THRESHOLD = 0.4
POLICY_SOURCE = "doc3.md"

# ------------------------------------------------------------------
# Safety checks (run once)
# ------------------------------------------------------------------

for path in [CHUNKS_FILE, EMBEDDINGS_FILE, FAISS_INDEX_FILE]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing required file: {path}")

# ------------------------------------------------------------------
# Load EVERYTHING ONCE (FASTEST)
# ------------------------------------------------------------------

with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    ALL_CHUNKS = json.load(f)

EMBEDDINGS = np.load(EMBEDDINGS_FILE)
INDEX = faiss.read_index(FAISS_INDEX_FILE)

EMBED_CHUNKS = [
    c for c in ALL_CHUNKS
    if c["metadata"]["section"] not in ["Document Title", "Document Metadata"]
]

if len(EMBED_CHUNKS) != EMBEDDINGS.shape[0]:
    raise ValueError(
        f"Embedding count ({EMBEDDINGS.shape[0]}) "
        f"does not match chunks ({len(EMBED_CHUNKS)})"
    )

ID_TO_CHUNK = {i: c for i, c in enumerate(EMBED_CHUNKS)}

# ------------------------------------------------------------------
# Embedding model (cached)
# ------------------------------------------------------------------

@lru_cache(maxsize=1)
def get_embedder():
    return SentenceTransformer("all-MiniLM-L6-v2")

MODEL = get_embedder()

# ------------------------------------------------------------------
# Query utilities
# ------------------------------------------------------------------

def normalize_query(query: str) -> str:
    return query.lower().strip(" ?!.")

def is_underspecified(query: str) -> bool:
    return len(query.split()) <= 2

def detect_intent(query: str) -> str:
    q = query.lower()

    if any(w in q for w in [
        "delay", "delays",
        "deviation", "deviations",
        "timeline", "on-time",
        "penalty", "penalties",
        "accountable", "accountability",
        "enforce", "enforcement"
    ]):
        return "enforcement"

    if any(w in q for w in [
        "payment", "payments",
        "price", "pricing",
        "cost", "costs",
        "risk", "financial",
        "safety", "secure",
        "escrow"
    ]):
        return "payments"

    return "general"

INTENT_CANONICAL_QUERY = {
    "enforcement":
        "How does Indecimal handle delays, deviations, and accountability?",
    "payments":
        "What payment safety and escrow mechanisms does Indecimal use?"
}


# ------------------------------------------------------------------
# Main retrieval (FAST PATH)
# ------------------------------------------------------------------

def retrieve_chunks(query: str, k: int = TOP_K):
    intent = detect_intent(query)

    query = normalize_query(query)
    if is_underspecified(query):
        query = INTENT_CANONICAL_QUERY.get(intent, query)

    # Embed query
    q_emb = MODEL.encode([query], normalize_embeddings=True)

    scores, indices = INDEX.search(q_emb, k)

    results = []

    for score, idx in zip(scores[0], indices[0]):
        if idx == -1 or score < SIM_THRESHOLD:
            continue

        results.append({
            "score": float(score),
            "chunk": ID_TO_CHUNK[idx]
        })

    # Intent-aware hard prioritization
    if intent == "enforcement":
        policy_results = [
            r for r in results
            if r["chunk"]["metadata"]["source_file"] == POLICY_SOURCE
        ]
        if policy_results:
            return policy_results[:k]

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:k]
