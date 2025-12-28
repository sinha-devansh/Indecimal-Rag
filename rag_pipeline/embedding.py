import os
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

CHUNKS_FILE = os.path.join(PROCESSED_DIR, "chunks.json")
EMBEDDINGS_FILE = os.path.join(PROCESSED_DIR, "embeddings.npy")
FAISS_INDEX_FILE = os.path.join(PROCESSED_DIR, "faiss.index")

os.makedirs(PROCESSED_DIR, exist_ok=True)

# ------------------------------------------------------------------
# Model
# ------------------------------------------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")

# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def is_embed_candidate(chunk):
    return chunk["metadata"]["section"] not in [
        "Document Title",
        "Document Metadata"
    ]

# ------------------------------------------------------------------
# Main embedding + indexing
# ------------------------------------------------------------------

def run_embedding():
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    embed_chunks = [c for c in chunks if is_embed_candidate(c)]
    texts = [c["text"] for c in embed_chunks]

    if not texts:
        raise ValueError("No valid chunks found for embedding.")

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    np.save(EMBEDDINGS_FILE, embeddings)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    faiss.write_index(index, FAISS_INDEX_FILE)

    print("✅ Embedding & indexing complete")
    print(f"Chunks embedded : {len(texts)}")
    print(f"Embedding shape : {embeddings.shape}")
    print(f"FAISS index size: {index.ntotal}")

# ------------------------------------------------------------------

if __name__ == "__main__":
    run_embedding()
