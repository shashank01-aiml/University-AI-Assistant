import os

from dotenv import load_dotenv
from google import genai

from app.rag.vector_store import search


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# GEMINI API KEY
# ============================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. Add it to your .env file."
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(api_key=GEMINI_API_KEY)


# ============================================================
# GEMINI MODEL
# ============================================================

MODEL = "gemini-3-flash-preview"


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(query: str, top_k: int = 3):
    """
    Retrieve relevant university document chunks
    and generate a grounded answer using Gemini.
    """

    # --------------------------------------------------------
    # STEP 1: SEMANTIC SEARCH
    # --------------------------------------------------------

    results = search(
        query=query,
        top_k=top_k
    )

    # --------------------------------------------------------
    # NO RELEVANT RESULTS
    # --------------------------------------------------------

    if not results:
        return {
            "answer": (
                "I could not find relevant information in the "
                "available university documents."
            ),
            "sources": []
        }

    # --------------------------------------------------------
    # STEP 2: BUILD CONTEXT
    # --------------------------------------------------------

    context_parts = []

    sources = []

    for i, result in enumerate(results, start=1):

        # Get text safely
        text = result.get("text", "")

        if not text:
            continue

        context_parts.append(
            f"--- Document Chunk {i} ---\n"
            f"{text}"
        )

        # ----------------------------------------------------
        # SOURCE INFORMATION
        # ----------------------------------------------------

        source = result.get("source", "")

        path = result.get("path", "")

        chunk_id = result.get("chunk_id")

        source_info = {
            "source": source,
            "path": path,
            "chunk_id": chunk_id
        }

        sources.append(source_info)

    # --------------------------------------------------------
    # IF NO TEXT WAS FOUND
    # --------------------------------------------------------

    if not context_parts:
        return {
            "answer": (
                "I could not find relevant information in the "
                "available university documents."
            ),
            "sources": []
        }

    # --------------------------------------------------------
    # COMBINE DOCUMENT CONTEXT
    # --------------------------------------------------------

    context = "\n\n".join(context_parts)

    # --------------------------------------------------------
    # STEP 3: CREATE GROUNDED PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are a university academic assistant.

Answer the user's question using ONLY the information
provided in the university document context below.

Do not invent information.

If the answer cannot be found in the provided context,
clearly say that the information is not available in
the university documents.

Give a clear, concise and student-friendly answer.

User Question:
{query}

University Document Context:
{context}

Instructions:
1. Answer directly.
2. Use only the provided context.
3. Do not make up facts.
4. Explain technical concepts simply when appropriate.
5. If the context does not contain the answer, say so.
"""

    # --------------------------------------------------------
    # STEP 4: CALL GEMINI
    # --------------------------------------------------------

    try:

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        answer = response.text

        if not answer:
            answer = (
                "Gemini did not return an answer. "
                "Please try again."
            )

    except Exception as e:

        # Print the real error in the terminal
        print("\n========== GEMINI ERROR ==========")
        print(str(e))
        print("==================================\n")

        raise

    # --------------------------------------------------------
    # STEP 5: RETURN ANSWER + SOURCES
    # --------------------------------------------------------

    return {
        "answer": answer,
        "sources": sources
    }