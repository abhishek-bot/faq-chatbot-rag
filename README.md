
# FAQ Chatbot with RAG (Weekend 2)

A FastAPI-based FAQ assistant powered by semantic search, generative augmentation, and a feedback loop for continuous improvement.  
This project builds on last weekend’s fuzzy-matching assistant and introduces a full RAG pipeline with FAISS + Flan‑T5.

## Overview

This chatbot answers frequently asked questions using **semantic search** and **Retrieval-Augmented Generation (RAG)**.  
It embeds queries, retrieves the closest FAQ using FAISS, and enriches the response with Flan‑T5.  
Unanswered queries are logged and reviewed via a Streamlit feedback page — making the bot smarter with every interaction.

This is Weekend 2 of my GenAI hackathon-style learning series.

## Tech Stack

- **Backend**: FastAPI (Python)  
- **Retrieval**: FAISS + SentenceTransformers (`all-MiniLM-L6-v2`)  
- **Generation**: Hugging Face Flan‑T5‑Large  
- **Frontend**: Streamlit (chatbot + feedback UI)  
- **Data**: JSON files (`faqs.json`, `unmatched_queries.json`)  
- **Logging**: Python `logging` module  
- **Deployment**: Uvicorn (ASGI server)

## Setup

1. Clone repo:
```bash
git clone https://github.com/abhishek-bot/faq-chatbot-rag.git
cd faq-chatbot-rag
```

2. Create virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate   # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run FastAPI backend:
```bash
uvicorn main:app --reload
```

5. Run Streamlit chatbot UI:
```bash
streamlit run pages/chatbot.py
```

6. Run Streamlit feedback page:
```bash
streamlit run pages/feedback.py
```

## Demo Flow

- Ask a direct FAQ: “What is your refund policy?”  
- Ask a semantic query: “Tell me about refunds”  
- Ask something outside FAQ: “Do you sell toys?” → fallback + logged  
- Review unanswered queries in feedback page  
- Accept/Edit/Reject → updates `faqs.json` and rebuilds FAISS index

### Endpoints

- `GET /health` → check server status  
- `POST /ask` → query the chatbot  
- `POST /feedback` → submit feedback for unmatched queries

## Features

- **Semantic Search**: Uses FAISS and MiniLM to find closest FAQ match.  
- **Generative Augmentation**: Flan‑T5 paraphrases FAQ answers into natural responses.  
- **Fallback Logic**: Safe response when no match is found.  
- **Unmatched Query Logging**: Stores missed queries in `unmatched_queries.json`.  
- **Feedback Loop**: Streamlit UI for reviewing and updating FAQs.  
- **Real-Time Index Rebuild**: New FAQs are searchable immediately.  
- **Chatbot UI**: Interactive Streamlit interface for demo-ready conversations.

## Motivation & Goal

The goal of this sprint was to evolve last weekend’s assistant into a smarter, self-improving system.  
By integrating semantic search, generative models, and feedback loops, the bot now learns from every missed query.  
It’s robust, transparent, and ready for deeper RAG experimentation.

## How Others Can Benefit

- **Developers**: Learn how to build a RAG chatbot with FAISS + FastAPI.  
- **Students**: Use this as a hands-on NLP project.  
- **Recruiters/Interviewers**: See a working demo that highlights problem-solving and system design.  
- **Teams**: Extend this into a production-ready assistant with analytics and dashboards.

---
