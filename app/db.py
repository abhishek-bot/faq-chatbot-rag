import logging   # Built-in library for logging
import sqlite3   # Built-in library for SQLite
import re   # Built-in library for regular expressions (optional, can be used for more advanced query processing)
from rapidfuzz import process   # Third-party library for fast fuzzy string matching (optional, can be used instead of difflib for better performance)

DB_PATH = "data/faq.db"   # Path to the SQLite database file

logging.basicConfig(level=logging.INFO)   # Set up logging configuration
logger = logging.getLogger(__name__)   # Create a logger for this module

def get_connection():
    """Establish a connection to the SQLite database."""
    logger.info("Establishing database connection.")
    conn = sqlite3.connect(DB_PATH)
    return conn

def normalize(text: str) -> str:
    """
    Normalize text by lowercasing and stripping punctuation.
    """
    logger.info(f"Normalizing text: {text}")
    return re.sub(r'[^a-z0-9\s]', '', text.lower().strip())


def get_faq_answer(query:str, threshold:int = 70, return_info:bool = False):
    """
    Search the FAQ table for a question that matches the user query.
    Currently uses a simple fuzzy matching.
    Returns the answer if found, otherwise a default message.
    """
    logger.info(f"Getting FAQ answer for query: {query}")
    conn = get_connection()   # Get a connection to the database
    cursor = conn.cursor()   # Create a cursor object to execute SQL queries

    cursor.execute("SELECT question, answer FROM faq")   # Fetch all questions and answers from the FAQ table
    faqs = cursor.fetchall()   # Get all rows from the executed query
    conn.close()   # Close the database connection

    if not faqs:
        logger.info("No FAQs found.")
        fallback = "Sorry, I couldn't find an answer to your question."   # Return a default message if no FAQs are found
        return (fallback, None) if return_info else fallback
    
    #Extract questions
    questions = [normalize(q) for (q,a) in faqs]   # Create a list of questions from the fetched FAQs
    normalized_query = normalize(query)

    # Use rapidfuzz to find the closest matching question
    match, score, idx = process.extractOne(normalized_query, questions)  # Get the closest match for the query from the list of questions
    logger.info(f"Best match: '{match}' with score {score} at index {idx}")  # Debug print to show the best match and its score
    if match and score >= threshold:   # Check if the match is above the specified threshold
        matched_answer = faqs[idx][1]   # Return the corresponding answer if a good match is found
        return (matched_answer, (match, score)) if return_info else matched_answer
    else:
        logger.info("No good match found for the query.")
        log_unanswered_query(query)  # Log the unanswered query for future analysis
        fallback = "Sorry, I couldn't find an answer to your question."
        return (fallback, None) if return_info else fallback

def log_unanswered_query(query: str):
    """
    Log unanswered queries into the database for future analysis.
    """
    logger.info(f"Logging unanswered query: {query}")
    conn = get_connection()   # Get a connection to the database
    cursor = conn.cursor()   # Create a cursor object to execute SQL queries

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS unanswered_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')  # Create a table for unanswered queries to log any questions that the system couldn't answer, which can be useful for improving the FAQ database over time.


    cursor.execute("INSERT INTO unanswered_queries (query) VALUES (?)", (query,))   # Insert the unanswered query into the database
    conn.commit()   # Commit the transaction
    conn.close()   # Close the database connection
    logger.info(f"Logged unanswered query: '{query}'")

def get_unanswered_queries():
    """
    Retrieve all unanswered queries from the database.
    """
    logger.info("Retrieving unanswered queries from the database.")
    conn = get_connection()   # Get a connection to the database
    cursor = conn.cursor()   # Create a cursor object to execute SQL queries

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS unanswered_queries (id INTEGER PRIMARY KEY AUTOINCREMENT, query TEXT NOT NULL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)"
    )   # Ensure the unanswered_queries table exists before trying to fetch data from it

    cursor.execute("SELECT query, timestamp FROM unanswered_queries ORDER BY timestamp DESC")   # Fetch all unanswered queries ordered by timestamp
    queries = cursor.fetchall()   # Get all rows from the executed query
    conn.close()   # Close the database connection

    return [{"query": query, "timestamp": timestamp} for query, timestamp in queries]   # Return the list of unanswered queries with their timestamps