from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.rag.vector_store import build_vector_store, load_vector_store


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


# ============================================================
# PROJECT PATHS
# ============================================================

# Project structure:
#
# university-ai-assistant/
# ├── backend/
# │   └── app/
# │       └── api/
# │           └── documents.py   <-- this file
# │
# └── documents/                 <-- PDFs go here
#
# parents[3] brings us back to:
# university-ai-assistant/

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DOCUMENTS_DIR = PROJECT_ROOT / "documents"

# Make sure the documents folder exists
DOCUMENTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# UPLOAD PDF
# ============================================================

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):
    """
    Upload a university PDF document.

    The PDF is:
        1. Saved into the project's documents folder
        2. Text is extracted
        3. Text is split into chunks
        4. Embeddings are generated
        5. Vector store is rebuilt
        6. The new document becomes searchable
    """

    # ========================================================
    # STEP 1: CHECK FILE
    # ========================================================

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )

    # Only allow PDF files
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # ========================================================
    # STEP 2: CREATE SAFE FILENAME
    # ========================================================

    # Prevent directory traversal such as:
    # ../../something.pdf

    safe_filename = Path(file.filename).name

    file_path = DOCUMENTS_DIR / safe_filename

    # ========================================================
    # STEP 3: SAVE PDF
    # ========================================================

    try:

        contents = await file.read()

        if not contents:
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty."
            )

        with open(file_path, "wb") as output_file:
            output_file.write(contents)

        print("\n" + "=" * 60)
        print("FILE UPLOAD")
        print("=" * 60)
        print(f"File saved successfully: {safe_filename}")
        print(f"Location: {file_path}")

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Could not save file: {str(e)}"
        )

    # ========================================================
    # STEP 4: REBUILD VECTOR STORE
    # ========================================================

    try:

        print("\n" + "=" * 60)
        print("REBUILDING VECTOR STORE")
        print("=" * 60)

        success = build_vector_store()

        if not success:

            raise HTTPException(
                status_code=500,
                detail=(
                    f"{safe_filename} was uploaded successfully, "
                    "but could not be extracted/indexed. "
                    "Please check the PDF text extraction/OCR."
                )
            )

    except HTTPException:
        raise

    except Exception as e:

        print("\nVECTOR STORE ERROR")
        print(str(e))

        raise HTTPException(
            status_code=500,
            detail=(
                f"{safe_filename} was uploaded successfully, "
                f"but indexing failed: {str(e)}"
            )
        )

    # ========================================================
    # STEP 5: VERIFY THAT THE DOCUMENT WAS INDEXED
    # ========================================================

    try:

        embeddings, documents = load_vector_store()

        indexed_documents = {
            document.get("source")
            for document in documents
        }

        if safe_filename not in indexed_documents:

            print("\n" + "=" * 60)
            print("INDEX VERIFICATION FAILED")
            print("=" * 60)

            print(f"Uploaded file: {safe_filename}")
            print("Indexed documents:")

            for document_name in sorted(indexed_documents):
                print(f" - {document_name}")

            raise HTTPException(
                status_code=500,
                detail=(
                    f"{safe_filename} was uploaded successfully, "
                    "but was not found in the vector store."
                )
            )

        # Count chunks belonging to this document
        document_chunks = [
            document
            for document in documents
            if document.get("source") == safe_filename
        ]

        chunk_count = len(document_chunks)

        print("\n" + "=" * 60)
        print("INDEX VERIFICATION SUCCESSFUL")
        print("=" * 60)

        print(f"File: {safe_filename}")
        print(f"Chunks created: {chunk_count}")
        print(f"Total indexed chunks: {len(documents)}")

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                "Document was uploaded and indexed, "
                f"but verification failed: {str(e)}"
            )
        )

    # ========================================================
    # STEP 6: SUCCESS RESPONSE
    # ========================================================

    return {
        "success": True,
        "message": "Document uploaded and indexed successfully.",
        "filename": safe_filename,
        "chunks_created": chunk_count,
        "total_indexed_chunks": len(documents)
    }