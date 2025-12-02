A lightweight, retrieval-augmented AI chatbot built for the SMARTeIS platform.
It combines FAISS-based FAQ retrieval, semantic embeddings, and LLM fallback (phi-mini via Ollama) to provide concise and reliable e-Invoicing support.
The system includes login authentication, chat history tracking, user feedback logging, and a floating chatbot UI.

Backend
Flask-based API

MySQL database for:
  Login authentication
  FAQ training data
  Chat history

Semantic similarity search using:
  SentenceTransformer (all-MiniLM-L6-v2)
  FAISS (IndexFlatIP)

LLM fallback using phi model served through Ollama on Azure Container Apps

Session-based login

Error handling for missing JSON, timeout, and bad LLM responses

Frontend
Clean floating chatbot design inspired by modern AI assistants

Includes:
  Chat bubbles
  Thinking indicator
  Predefined prompts
  Recommended questions
  Minimize & close buttons
  Feedback buttons 👍👎
  Intro greeting message
  Mobile-responsive layout
