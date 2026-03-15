from fastapi import FastAPI
from pydantic import BaseModel
import json

# import our helper modules
from app.faiss_utils import build_index, search_index
from app.ai import generate_answer

# initialize the FastAPI app
app = FastAPI(tittle="FAQ Chatbot with RAG", description="Semantic FAQ chatbot with FAISS + Flan-T5")

# Load FAQ dataset
with open("data/faqs.json", "r") as f:
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
    # Step 1: Semantic search
    results = search_index(query.question, index, model, faqs, k=1)
    best_match = results[0]

    # Step 2: FAQ answer
    faq_answer = best_match["answer"]

    # Step 3: Enriched answer via Flan-T5
    enriched = generate_answer(query.question, faq_answer)

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
