from fastapi import FastAPI
from pydantic import BaseModel
from torch import embedding
import yaml
import faiss, pickle, subprocess
import numpy as np
import os

# Load config.yaml
# with open("config.yaml", "r") as f:
#     config = yaml.safe_load(f)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root
CONFIG_PATH = os.path.join(BASE_DIR, "config.yaml")

with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

model_name = config["model"]
faiss_index_path = config["faiss_index_path"]

# Load FAISS index + docstore
index = faiss.read_index(f"{faiss_index_path}/index.faiss")
with open(f"{faiss_index_path}/chunks.pkl", "rb") as f:
    docstore = pickle.load(f)

# Helper: call Ollama
def query_ollama(prompt: str) -> str:
    result = subprocess.run(
        ["ollama", "run", model_name],
        input=prompt.encode("utf-8"),
        capture_output=True
    )
    return result.stdout.decode("utf-8")

# RAG pipeline
def rag_pipeline(question: str) -> str:
    # (1) embed query — for now mock with FAISS ids
    # later we’ll add proper embeddings, for now assume embedding exists
    # embedding = <your embedding function>
    embedding = np.array([ [0.1] * index.d ], dtype="float32")  # shape (1, dim)
    D, I = index.search(embedding, config["top_k"]) 
    contexts = [docstore[i] for i in I[0] if i != -1]

    # build final prompt
    context_text = "\n".join(contexts)
    prompt = f"Context:\n{context_text}\n\nQuestion: {question}\nAnswer:"

    return query_ollama(prompt)

# FastAPI app
app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/chat")
async def chat(query: Query):
    answer = rag_pipeline(query.question)
    return {"answer": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


