# SustainaBot 🌱

<img width="1280" height="800" alt="Screenshot 2025-08-23 at 10 24 07 AM" src="https://github.com/user-attachments/assets/26025388-9b4a-4638-bae8-8fbd7acc1eba" />



**SustainaBot** is a Retrieval-Augmented Generation (RAG) chatbot for sustainability and circular bioeconomy queries. It answers questions based on uploaded documents using a local LLM.

## Features
- Role-based answers (user/admin)
- FastAPI backend with Streamlit frontend
- Uses FAISS for vector search
- Local/offline-friendly: no paid APIs required
- trained on UN and IWMI publically available reports and data.

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

