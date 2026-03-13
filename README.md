# FAQ Assistant (GenAI)
A FastAPI-based FAQ assistant with fuzzy matching, fallback logic, unanswered query logging, and a simple front-end chatbot UI.  
This project demonstrates how to build a robust, transparent, and demo-ready conversational assistant.

## Overview
This chatbot answers frequently asked questions using a SQLite knowledge base.  
It uses **fuzzy matching** to handle varied phrasing, **fallback logic** to avoid hallucinations, and **logging** to track unanswered queries for continuous improvement.  
A lightweight front-end provides a chat-style interface for interactive demos.
 
This is Weekend 1 of my GenAI hackathon-style learning series.

## Tech Stack
- **Backend**: FastAPI (Python)
- **Database**: SQLite
- **Matching**: RapidFuzz (fuzzy string matching)
- **Frontend**: HTML + JavaScript (served via FastAPI static files)
- **Logging**: Python `logging` module
- **Deployment**: Uvicorn (ASGI server)

## Setup

1. Clone repo:
```bash
git clone https://github.com/abhishek-bot/faq-assistant-genai.git
cd faq-assistant-genai

2. Create virtual environment:
python -m venv venv
.\venv\Scripts\activate   # Windows

3. Install dependencies:
pip install -r requirements.txt

4. Run app:
uvicorn app.main:app --reload

5. Open browser:
http://localhost:8000/

Demo Flow
- Ask a direct FAQ: “What is your refund policy?”
- Ask a fuzzy query: “Tell me about refunds”
- Ask something outside FAQ: “Do you sell gift cards?” → fallback + logged
- Check unanswered queries:

1. Health Check
Verify the backend is running:
http://localhost:8000/health
response: {"status": "healthy"}

2. Direct FAQ Match
http://localhost:8000/ask?query=What is your refund policy?
response: {"query": "What is your refund policy?", "faq_answer": "We offer a 30-day refund policy for unused services.", "response": "We offer a 30-day refund policy for unused services."}

3. Fuzzy Query
http://localhost:8000/ask?query=Tell me about refunds
response: {"query": "Tell me about refunds", "faq_answer": "We offer a 30-day refund policy for unused services.", "response": "We offer a 30-day refund policy for unused services."}

4. Fallback + Logging
http://localhost:8000/ask?query=toys?
response: {"query": "toys?", "faq_answer": "Sorry, I couldn't find an answer to your question.", "response": "Sorry, I couldn't find an answer to your question."}

5. View Unanswered Queries
http://localhost:8000/unanswered
response: {"unanswered_queries": [{"query": "Do you sell gift cards?", "timestamp": "2026-03-08 14:20:00"}]}

6. Frontend Chatbot UI
http://localhost:8000/


## Features
- Fuzzy Matching: Handles synonyms and varied phrasing. Uses RapidFuzz to match queries against FAQ entries.Example: “Tell me about refunds” → “What is your refund policy?”.

- Fallback Logic: Safe responses when no match is found. If no match is found, the assistant skips the model and returns a safe fallback. Prevents hallucinations and ensures transparency.

- Unanswered Query Logging: Stores missed queries for dataset expansion. Logs queries that trigger fallback into unanswered_queries table. Example: “Do you sell gift cards?” → logged for future FAQ expansion.

- Model-Agnostic Design: Ready for integration with BART, Flan-T5, Pegasus.

- Frontend Chatbot UI: Simple, interactive demo interface. Minimal HTML/JS interface served via FastAPI. Displays user queries and bot responses in chat style.

## Motivation & Goal
The goal of this project is to build a robust, transparent, and demo-ready FAQ assistant that:
- Impresses recruiters with clean design and reproducibility.
- Demonstrates practical GenAI concepts like fuzzy matching, fallback, and logging.
- Provides a foundation for future RAG (Retrieval-Augmented Generation) integration.

## How Others Can Benefit
- Developers: Learn how to structure a GenAI FAQ assistant with FastAPI + SQLite.
- Students: Use this as a starter project for NLP and chatbot demos.
- Recruiters/Interviewers: See a working demo that highlights problem-solving and system design.
- Teams: Extend this into a production-ready FAQ bot with semantic search and RAG.

