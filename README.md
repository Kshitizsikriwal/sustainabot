# SustainaBot 🌱
<img width="1280" height="800" alt="Screenshot 2025-08-22 at 6 57 46 AM" src="https://github.com/user-attachments/assets/6da9b129-2440-4038-a589-f29579b29fe7" />


**SustainaBot** is a Retrieval-Augmented Generation (RAG) chatbot for sustainability and circular bioeconomy queries. It answers questions based on uploaded documents using a local LLM.

## Features
- Role-based answers (user/admin)
- FastAPI backend with Streamlit frontend
- Uses FAISS for vector search
- Local/offline-friendly: no paid APIs required

## Project Structure
```
sustainabot/
├── backend/ # FastAPI API
├── frontend/ # Streamlit UI
├── scripts/ # Data processing / embedding
├── notebooks/ # Experiments & demos
├── config.yaml # Configuration
└── README.md
```

## Setup
```bash
# Create conda environment
conda create -n sb python=3.11 -y
conda activate sb

# Install requirements
pip install -r requirements.txt

# Run backend
cd backend
uvicorn main:app --reload

# Run frontend
cd ../frontend
streamlit run app.py 
```
Usage
Ask sustainability-related questions
Get role-based, context-aware answers
Notes
Large model files and FAISS indexes are not included in this repo
Requires Ollama / Mistral 7B model for LLM inference

