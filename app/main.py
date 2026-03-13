from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles    # FastAPI framework
from app import db,ai    # Importing own database and AI modules from the app package
import logging   # Built-in library for logging

logging.basicConfig(level=logging.INFO)   # Set up logging configuration
logger = logging.getLogger(__name__)   # Create a logger for this module

app = FastAPI()    # Create an instance of the FastAPI application

app.mount("/static", StaticFiles(directory="static"), name="static")   # Mount the static files directory to serve CSS, JS, images, etc.

@app.get("/")
def root():
    # This is the root endpoint that can be used to serve a homepage or documentation.
    logger.info("Root endpoint called.")   # Log when the root endpoint is called
    return FileResponse("static/index.html")   # Serve the index.html file from the static directory when the root endpoint is accessed

@app.get("/health")   # Define a GET endpoint for health check
def health_check():
    # This endpoint can be used to check if the application is running and healthy.
    logger.info("Health check endpoint called.")   # Log when the health check endpoint is called
    return {"status": "healthy"}

@app.get("/ask")   # Define a GET endpoint for asking questions
def ask(query: str):

    logger.info(f"Ask endpoint called with query: {query}")   # Log the query received

    faq_answer,match_info = db.get_faq_answer(query, return_info=True)   # Get an answer from the FAQ database

    if not match_info:
        logger.info("No FAQ match found, returning fallback response.")
        return {
            "query": query,
            "faq_answer": faq_answer,
            "match_info": None,
            "response": faq_answer  # Return the fallback message as the response when no match is found
        }
    # If a match is found, generate a response using the AI module
    response = ai.generate_response(query, faq_answer)

    return {
        "query": query,   # Return the original query
        "faq_answer": faq_answer,   # Return the FAQ answer retrieved from the database
        "match_info": match_info,   # Return the match information such as the matched question and its score
        "response": response   # Return the AI-generated response
    }

@app.get("/unanswered")   # Define a GET endpoint to retrieve unanswered queries
def get_unanswered_queries():

    """Endpoint to retrieve unanswered queries for analysis and improvement of the FAQ database."""

    queries = db.get_unanswered_queries()   # Get the list of unanswered queries from the database
    logger.info(f"Retrieved {len(queries)} unanswered queries.")   # Log the number of unanswered queries retrieved
    return {"unanswered_queries": queries}   # Return the list of unanswered queries in the response