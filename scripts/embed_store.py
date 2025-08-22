from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
embedder = SentenceTransformer(MODEL_NAME)

PROCESSED = "data/processed"
DB_PATH = "data/faiss_index/index.faiss"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

texts = []

# Load & chunk
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
for file in os.listdir(PROCESSED):
    with open(os.path.join(PROCESSED, file), "r", encoding="utf-8") as f:
        raw_text = f.read()
        hunks = splitter.split_text(raw_text)
        texts.extend(hunks)

# Embeddings
embeddings = embedder.encode(texts)

# Store in FAISS
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))
faiss.write_index(index, DB_PATH)

print(f"Stored {len(texts)} chunks in FAISS index.")

# Save texts for retrieval
with open("data/faiss_index/texts.pkl", "wb") as f:
    pickle.dump(texts, f)
