import faiss
import pickle
from sentence_transformers import SentenceTransformer

# Load FAISS index
index = faiss.read_index("faiss_index/index.faiss")  # your FAISS binary

# Load chunks
with open("faiss_index/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)  # list of text chunks

# Load embedding model (same used for creating index)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_chunks(query, top_k=3):
    """Return top_k chunks most relevant to the query."""
    query_vec = embedder.encode([query])
    scores, indices = index.search(query_vec, top_k)
    results = [chunks[i] for i in indices[0] if i < len(chunks)]
    return results
