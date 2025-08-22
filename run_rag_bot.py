import faiss
import pickle
from sentence_transformers import SentenceTransformer
import subprocess
import yaml
import os
import sys
import threading
import time

# ✅ Suppress HuggingFace tokenizer parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Load config
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

BOT_NAME = config.get("bot_name", "SustainaBot 🤖")
CREATOR_NAME = config.get("creator_name", "Unknown")
INTRO_MESSAGE = config.get(
    "intro_message",
    f"Hi, I’m {BOT_NAME}, a chatbot built by {CREATOR_NAME} to answer sustainability and circular bioeconomy questions."
)

print(INTRO_MESSAGE)

# Minimal loading
print("Loading model...")

# Load FAISS index & chunks
FAISS_PATH = "data/faiss_index/index.faiss"
CHUNKS_PATH = "data/faiss_index/chunks.pkl"
index = faiss.read_index(FAISS_PATH)
with open(CHUNKS_PATH, "rb") as f:
    chunks = pickle.load(f)

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Function to retrieve top chunks
def retrieve_chunks(query, top_k=3):
    query_vec = embedder.encode([query])
    scores, indices = index.search(query_vec, top_k)
    return [chunks[i] for i in indices[0] if i < len(chunks)]

# Simple spinner while model is thinking
class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1:
            for cursor in "|/-\\":
                yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def __enter__(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)

# Ready message
print("\n✅ SustainaBot is ready!")
print("Type your question here:\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye 👋")
        break

    # Retrieve context
    top_chunks = retrieve_chunks(user_input, top_k=3)
    context_text = "\n\n".join(top_chunks)

    # Prompt for sustainabot model
    final_prompt = f"""
You are SustainaBot, a chatbot for sustainability and circular bioeconomy.
Answer the following question directly and clearly using the context provided.
If the context is not sufficient, say you don't know.

Context:
{context_text}

Question:
{user_input}
Answer:
"""

    # Call sustainabot model with spinner
    with Spinner():
        try:
            result = subprocess.run(
                ["ollama", "run", "sustainabot:latest"],
                input=final_prompt,
                capture_output=True,
                text=True,
                check=True
            )
            answer = result.stdout.strip()
        except subprocess.CalledProcessError as e:
            answer = f"Error calling sustainabot model: {e}"

    # Print clean answer only
    print(f"\n🤖 SustainaBot: {answer}\n")
