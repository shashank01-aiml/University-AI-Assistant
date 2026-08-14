from pathlib import Path

import fitz  # PyMuPDF
import pytesseract
from PIL import Image


# ============================================================
# TESSERACT CONFIGURATION
# ============================================================

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


# ============================================================
# PROJECT PATHS
# ============================================================

# Project root:
# university-ai-assistant/
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# PDF folder:
DOCUMENTS_DIR = PROJECT_ROOT / "documents"


# ============================================================
# LOAD PDF DOCUMENTS
# ============================================================

def load_documents():
    """
    Load all PDF files from the project's documents folder.

    First attempts normal PDF text extraction using PyMuPDF.
    If no text is found, uses Tesseract OCR on each page.
    """

    documents = []

    pdf_files = list(DOCUMENTS_DIR.glob("*.pdf"))

    print(f"Found {len(pdf_files)} PDF file(s).")

    if not pdf_files:
        print(
            "Please put PDF files inside the project's "
            "documents folder."
        )
        return documents

    for pdf_path in pdf_files:

        print("\n" + "=" * 60)
        print(f"Processing: {pdf_path.name}")
        print("=" * 60)

        try:
            pdf = fitz.open(pdf_path)

            text_parts = []

            # ------------------------------------------------
            # STEP 1: NORMAL PDF TEXT EXTRACTION
            # ------------------------------------------------

            print("Trying normal PDF text extraction...")

            for page_number, page in enumerate(pdf):

                text = page.get_text("text").strip()

                if text:
                    text_parts.append(text)

            full_text = "\n".join(text_parts).strip()

            # ------------------------------------------------
            # STEP 2: OCR FALLBACK
            # ------------------------------------------------

            if not full_text:

                print("No text layer found.")
                print("Starting Tesseract OCR...")

                ocr_parts = []

                total_pages = len(pdf)

                for page_number, page in enumerate(pdf):

                    print(
                        f"OCR processing page "
                        f"{page_number + 1}/{total_pages}..."
                    )

                    # Render PDF page as image
                    pix = page.get_pixmap(
                        dpi=200,
                        alpha=False
                    )

                    # Convert image to PIL format
                    image = Image.frombytes(
                        "RGB",
                        [pix.width, pix.height],
                        pix.samples
                    )

                    # Run Tesseract OCR
                    ocr_text = pytesseract.image_to_string(
                        image,
                        lang="eng"
                    ).strip()

                    if ocr_text:
                        ocr_parts.append(ocr_text)

                full_text = "\n".join(ocr_parts).strip()

            pdf.close()

            # ------------------------------------------------
            # STEP 3: CHECK EXTRACTION RESULT
            # ------------------------------------------------

            if not full_text:

                print(
                    f"ERROR: Could not extract text from "
                    f"{pdf_path.name}"
                )

                continue

            print(
                f"Successfully extracted "
                f"{len(full_text)} characters."
            )

            # ------------------------------------------------
            # STORE DOCUMENT
            # ------------------------------------------------

            documents.append(
                {
                    "text": full_text,
                    "source": pdf_path.name,
                    "path": str(pdf_path),
                }
            )

        except Exception as e:

            print(
                f"ERROR processing {pdf_path.name}: {e}"
            )

    print("\n" + "=" * 60)
    print(f"Loaded {len(documents)} document(s).")
    print("=" * 60)

    return documents


# ============================================================
# TEXT CHUNKING
# ============================================================

def chunk_text(text, chunk_size=1000, overlap=200):
    """
    Split text into overlapping chunks.

    chunk_size:
        Maximum number of characters in each chunk.

    overlap:
        Number of characters shared between consecutive chunks.
    """

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        # Prevent invalid/infinite chunking
        if end >= len(text):
            break

        start += chunk_size - overlap

    return chunks


# ============================================================
# LOAD AND CHUNK DOCUMENTS
# ============================================================

def load_and_chunk_documents():
    """
    Load PDFs and split their extracted text into chunks.
    """

    documents = load_documents()

    chunks = []

    for document in documents:

        document_chunks = chunk_text(
            document["text"]
        )

        for index, chunk in enumerate(document_chunks):

            chunks.append(
                {
                    "text": chunk,
                    "source": document["source"],
                    "path": document["path"],
                    "chunk_id": index,
                }
            )

    print(
        f"Created {len(chunks)} document chunks."
    )

    return chunks


# ============================================================
# TEST THE LOADER
# ============================================================

if __name__ == "__main__":

    chunks = load_and_chunk_documents()

    print(
        f"TOTAL CHUNKS: {len(chunks)}"
    )