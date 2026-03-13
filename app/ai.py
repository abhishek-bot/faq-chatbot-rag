import os
import logging
from dotenv import load_dotenv   # Load environment variables from a .env file
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, BartForConditionalGeneration  # Import tokenizer + model classes

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME", "google/flan-t5-small")  # Default to 'google/flan-t5-small' if not set

if "bart" in MODEL_NAME.lower():
    model_class = BartForConditionalGeneration
else:
    model_class = AutoModelForSeq2SeqLM
# Log which model is being loaded
logger.info(f"Loading Hugging Face model: {MODEL_NAME}")

# Load tokenizer and model for Flan-T5 (seq2seq model)
# Tokenizer: converts text → tokens
# Model: generates new text from tokens
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = model_class.from_pretrained(MODEL_NAME)

def generate_response(query: str, context: str) -> str:
    """
    Generate a helpful response using Flan-T5 directly.
    Steps:
    1. Build a prompt combining user query + FAQ answer.
    2. Tokenize the prompt into model input format.
    3. Run the model to generate output tokens.
    4. Decode tokens back into human-readable text.
    """
    # Step 1: Build prompt
    if "bart" in MODEL_NAME.lower():
        prompt = context
        logger.info(f"Using BART model, User Prompt: {query} , is ignored and only FAQ answer is used as prompt.")

    else:
        prompt = f"""
            The user asked: "{query}"
            The FAQ answer is: "{context}"
            Rewrite the FAQ answer into a complete, helpful, and user-friendly response.
            """

    logger.info(f"Prompt:\n{prompt.strip()}")

    # Step 2: Tokenize input
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)

    # Step 3: Generate output tokens
    outputs = model.generate(
        **inputs,
        max_length=60,         # Limit length of response
        min_length=10,         # Ensure response is at least 10 tokens
        num_beams=4,           # Use beam search for better quality
        repetition_penalty=2.0, # Penalize repetition to avoid generic responses
        early_stopping=True     # Stop when end token is generated
    )

    # Step 4: Decode tokens into text
    response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    logger.info(f"Model response:\n{response}")

    # Fallback: if response is too short, repetitive, or contains suspicious words
    suspicious_words = ["year", "website", "fee", "varies", "requirement", "charged", "money back", "customer service"]
    if len(response) < 20 or any(word in response.lower() for word in suspicious_words):
        logger.warning("Model response invalid or repetitive, using FAQ answer as fallback.")
        return context

    return response
