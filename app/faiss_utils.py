import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import logging

logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def build_index(faqs,model_name="sentence-transformers/all-MiniLM-L6-v2"):
    """ Build a FAISS index from FAQ questions.
    Args:
        faqs (list of dict): List of FAQ items with 'question' and 'answer' keys.
        model_name (str): Hugging Face model name for generating embeddings.

    Returns:
        index (faiss.IndexFlatL2): A FAISS index containing the question embeddings.
        model (SentenceTransformer): Loaded embedding model for reuse.
    """

    # Load the embedding model (MiniLM is lightweight and effective for sentence embeddings)
    model = SentenceTransformer(model_name)

    # Extract all FAQ questions
    questions = [faq['question'] for faq in faqs]

    # Convert questions to dense vectors (embeddings)
    ebeddings = model.encode(questions)

    # Each embedding has a fixed dimension (e.g., 384 for MiniLM), so we can create a FAISS index with that dimension
    dimension = ebeddings.shape[1]

    # Create a FAISS index using L2 distance (you can also use other metrics like cosine similarity)
    # IndexFlatL2 is simple and efficient for small to medium datasets
    index = faiss.IndexFlatL2(dimension)

    # Add all question embeddings to the FAISS index
    index.add(np.array(ebeddings))
    logger.info(f"Built FAISS index with {len(faqs)} FAQ questions and embedding dimension {dimension}")
    return index, model

def search_index(query,index,model,faqs,k=1, threshold=0.6):
    """ Search the FAISS index for the most relevant FAQ question.
    Args:
        query (str): User query to search for.
        index (faiss.IndexFlatL2): The FAISS index containing FAQ question embeddings.
        model (SentenceTransformer): The embedding model used to encode the query.
        faqs (list of dict): List of FAQ dicts with 'question' and 'answer' keys.
        k (int): Number of top results to return.
        Returns:
            results (list of dict): Top k FAQ items that are most relevant to the query.\
    """

    # Convert the user query to a dense vector (embedding)
    query_embedding = model.encode([query])

    # Perform similarity search in FAISS
    # D = distances, I = indices of the closest matches
    D, I = index.search(np.array(query_embedding), k)

    similarity = 1 / (1 + D[0][0])  # Convert L2 distance to similarity score (simple transformation)

    if similarity < threshold:
        return None
    # Retrieve the corresponding FAQ items based on the best matches
    results = [faqs[i] for i in I[0]]
    logger.info(f"Search results for query: {query} - Similarity: {similarity:.4f} - Best match: {results[0]['question']}")
    return results