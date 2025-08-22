import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
embedder = SentenceTransformer(MODEL_NAME)

DB_PATH = "data/faiss_index/index.faiss"
CHUNKS_PATH = "data/faiss_index/chunks.pkl"

# Load FAISS
index = faiss.read_index(DB_PATH)

# Load chunks
with open(CHUNKS_PATH, "rb") as f:
    texts = pickle.load(f)

query = "How can wastewater be reused in agriculture?"
query_emb = embedder.encode([query])

D, I = index.search(np.array(query_emb), k=3)

print("\n🔎 Query:", query)
print("\n📌 Top Retrieved Chunks:\n")
for idx, score in zip(I[0], D[0]):
    print(f"Score: {score:.2f}")
    print(texts[idx][:500], "...")  # show first 500 chars
    print("-" * 80)
