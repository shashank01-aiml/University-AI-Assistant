from pathlib import Path
import json
import numpy as np

from app.rag.loader import load_and_chunk_documents
from app.rag.embeddings import generate_embeddings, generate_embedding


VECTOR_STORE_DIR = Path(__file__).resolve().parent
EMBEDDINGS_FILE = VECTOR_STORE_DIR / "embeddings.npy"
DOCUMENTS_FILE = VECTOR_STORE_DIR / "chunks.json"


def build_vector_store():
    """
    Load document chunks, generate embeddings,
    and save them locally.
    """

    chunks = load_and_chunk_documents()

    if not chunks:
        print("No document chunks found.")
        print("Please put PDF files inside the project's documents folder.")
        return False

    texts = [chunk["text"] for chunk in chunks]

    print(f"Generating embeddings for {len(texts)} chunks...")

    embeddings = generate_embeddings(texts)

    np.save(EMBEDDINGS_FILE, embeddings)

    with open(DOCUMENTS_FILE, "w", encoding="utf-8") as file:
        json.dump(chunks, file, ensure_ascii=False, indent=2)

    print("Vector store created successfully.")
    print(f"Embeddings saved to: {EMBEDDINGS_FILE}")
    print(f"Chunks saved to: {DOCUMENTS_FILE}")

    return True


def load_vector_store():
    """
    Load the saved embeddings and document chunks.
    """

    if not EMBEDDINGS_FILE.exists() or not DOCUMENTS_FILE.exists():
        return None, []

    embeddings = np.load(EMBEDDINGS_FILE)

    with open(DOCUMENTS_FILE, "r", encoding="utf-8") as file:
        documents = json.load(file)

    return embeddings, documents


def search(query, top_k=5):
    """
    Find the most relevant document chunks for a query.
    """

    embeddings, documents = load_vector_store()

    if embeddings is None or not documents:
        return []

    query_embedding = generate_embedding(query)

    scores = np.dot(embeddings, query_embedding)

    top_k = min(top_k, len(scores))

    indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for index in indices:
        results.append(
            {
                "score": float(scores[index]),
                "text": documents[index]["text"],
                "source": documents[index]["source"],
                "path": documents[index]["path"],
                "chunk_id": documents[index]["chunk_id"],
            }
        )

    return results


if __name__ == "__main__":
    build_vector_store()