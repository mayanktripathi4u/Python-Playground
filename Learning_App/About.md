This is Maths ELA App for my son.

Using
- Python
- Streamlit
- Ollama LLM (for RAG-guided generation)
  - Install from [ollama.com](ollama.com) and start it (defaults to http://localhost:11434). Ensure the Ollama server is running.
  - Pull a local model (pick one you already have or try):
  `ollama pull llama3.1:8b` # good balance for local laptops

# Project structure suggestion:
```sh
Learning_App/
├── app.py # Streamlit entry point
├── config.py # Config & constants
├── kb.py # Knowledge base & fallback bank
├── llm.py # Ollama client + LLM utilities
├── quiz.py # Question generation (LLM + fallback)
├── grading.py # Grading logic (MCQ + short answers)
├── ui.py # UI helpers & rendering pieces
└── requirements.txt
```

