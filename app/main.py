# import our helper modules
from app.faiss_utils import build_index, search_index
from app.ai import generate_answer
from object_classes.feedback import Feedback

from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# initialize the FastAPI app
app = FastAPI(tittle="FAQ Chatbot with RAG", description="Semantic FAQ chatbot with FAISS + Flan-T5")

# Load FAQ dataset
with open("data/faqs.json", "r", encoding="utf-8") as f:
    faqs = json.load(f)

# Build FAISS index once at startup
index, model = build_index(faqs)

# Define request schema
class Query(BaseModel):
    question: str

@app.post("/ask")
def ask(query: Query):
    """
    Endpoint to handle user queries.
    Steps:
    1. Search FAISS index for closest FAQ match.
    2. Retrieve FAQ answer.
    3. Pass query + FAQ answer to Flan-T5 for enriched response.
    4. Return both FAQ answer and generated answer for transparency.
    """
    logger.info(f"Received query: {query.question}")
    # Step 1: Semantic search
    results = search_index(query.question, index, model, faqs, k=1)
    if results is None:
        log_unmatched_query(query.question)
        logger.info(f"No relevant FAQ found for query: {query.question}")
        return {
            "query": query.question,
            "matched_question": None,
            "faq_answer": None,
            "generated_answer": "No relevant FAQ found. Please try rephrasing your question."
            }
    best_match = results[0]
    logger.info(f"Best match found: {best_match['question']}")
    # Step 2: FAQ answer
    faq_answer = best_match["answer"]

    # Step 3: Enriched answer via Flan-T5
    enriched = generate_answer(best_match["question"], faq_answer)
    logger.info(f"Generated enriched answer: {enriched}")
    # Step 4: Return structured response
    return {
        "query": query.question,
        "matched_question": best_match["question"],
        "faq_answer": faq_answer,
        "generated_answer": enriched
    }

@app.get("/health")
def health():
    """Simple health check endpoint."""
    return {"status": "ok"}

@app.post("/feedback")
def feedback(data: Feedback):
    """
    Handle human feedback for unanswered queries.
    action: accept, edit, reject
    """
    if data.action in ["accept", "edit"]:
        try:
            with open("data/faqs.json", "r", encoding="utf-8") as f:
                faqs = json.load(f)
        except FileNotFoundError:
            faqs = []
        faqs.append({"question": data.question, "answer": data.answer})
        with open("data/faqs.json", "w", encoding="utf-8") as f:
            json.dump(faqs, f, indent=2)

        # Remove from unmatched queries and reload index
        remove_unmatched_query(data.question)
        # Reload FAQs and FAISS index
        reload_faqs_and_index() 

        logger.info(f"Added new FAQ from feedback: {data.question} -> {data.answer}")
        return {"status": "added", "question": data.question, "answer": data.answer}
    elif data.action == "reject":
        remove_unmatched_query(data.question)
        logger.info(f"Rejected feedback for query: {data.question}")
        return {"status": "rejected", "question": data.question}
    else:
        logger.warning(f"Invalid feedback action: {data.action} for query: {data.question}")
        return {"status": "invalid action"}

def log_unmatched_query(query: str):
    """Log unmatched queries for future analysis and improvement."""
    entry = {"query": query}
    os.makedirs(os.path.dirname("data/unmatched_queries.json"), exist_ok=True)

    if os.path.exists("data/unmatched_queries.json"):
        with open("data/unmatched_queries.json", "r+", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
            if any(entry["query"].lower() == query.lower() for entry in data):
                logger.info(f"Query already logged: {query}")
                return
            data.append(entry)
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
    else:
        with open("data/unmatched_queries.json", "w", encoding="utf-8") as f:
            json.dump([entry], f, indent=2)\
            
def remove_unmatched_query(question: str):
    """Remove a query from unmatched list once reviewed."""
    if os.path.exists("data/unmatched_queries.json"):
        with open("data/unmatched_queries.json", "r+", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
            data = [q for q in data if q["query"].lower() != question.lower()]
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()

def reload_faqs_and_index():
    """Reload FAQs and rebuild FAISS index after updates."""
    global faqs, index, model
    with open("data/faqs.json", "r", encoding="utf-8") as f:
        faqs = json.load(f)
    index, model = build_index(faqs)
    logger.info("Reloaded FAQs and rebuilt FAISS index")


