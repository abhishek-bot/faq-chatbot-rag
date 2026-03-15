from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import logging

logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load the Hugging Face text generation pipeline with a suitable model (e.g., T5 or GPT-3)
# Flan-T5-Large is a strong general-purpose model for Q&A and instruction following tasks
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-Large")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-Large")

def generate_answer(query: str, context: str) -> str:
    """
    Generate an enriched answer to using Flan-t5 with FAQ context
    Args:
        query (str): The user's question.
        context (str): The FAQ answer or retrieved context from FAISS.
        Returns:
            str: The generated answer that combines the query and context.
    """
    # Construct a prompt that guides the model
    # - provide the user question
    # - Supply the FAQ context
    # - Ask the model to generate a clear answer
    logger.info(f"Generating answer for query: {query} with context: {context}")
    prompt = (
        f"Paraphrase the context into a clear, user‑friendly answer. "
        f"Do not copy it word‑for‑word.\n\n"
        f"Question: {query}\n"
        f"Context: {context}\n"
        f"Paraphrased Answer:"
    )
    logger.info(f"Constructed prompt for generation: {prompt}") 
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_new_tokens=250,
        do_sample=True,
        temperature=0.9,
        top_p=0.9,
        repetition_penalty=2.0,
)
    
    generated_answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    logger.info(f"Generated answer: {generated_answer}")
    return generated_answer.strip()
