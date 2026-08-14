from sentence_transformers import SentenceTransformer
import numpy as np


# Embedding model
MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def generate_embeddings(texts):
    """
    Convert a list of text chunks into numerical embeddings.

    Args:
        texts: list of strings

    Returns:
        numpy array containing embeddings
    """

    if not texts:
        return np.array([])

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    return embeddings


def generate_embedding(text):
    """
    Convert a single text/query into an embedding.
    """

    if not text:
        return np.array([])

    embedding = model.encode(
        text,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embedding


def get_embedding_dimension():
    """
    Return the size of the embedding vector.
    """

    return model.get_sentence_embedding_dimension()