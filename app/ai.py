from transformers import pipeline

# Load the Hugging Face text-to-text generation pipeline with a suitable model (e.g., T5 or GPT-3)
# Flan-T5-Large is a strong general-purpose model for Q&A and instruction following tasks
generator = pipeline("text2text-generation", model="google/flan-t5-Large")

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

    prompt = f"Question: {query}\nContext: {context}\nAnswer:"

    # Generate the answer using the model
    response = generator(
        prompt,
        max_length=150, # Limit the length of the generated answer
        num_return_sequences=1, # We only want one answer
        temperature=0.7, # Control the creativity of the output(lower is more focused)
        )[0]["generated_text"]
    
    return response
