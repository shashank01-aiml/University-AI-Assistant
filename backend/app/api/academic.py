from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.academic import (
    Program,
    Year,
    Semester,
    Branch,
    Subject,
    Document,
)

from app.rag.vector_store import search
from app.services.rag_service import generate_answer


# ============================================================
# ACADEMIC API ROUTER
# ============================================================

router = APIRouter(
    prefix="/academic",
    tags=["Academic"],
)


# ============================================================
# PROGRAMS
# ============================================================

@router.get("/programs")
def get_programs(
    db: Session = Depends(get_db),
):
    """
    Get all academic programs.
    """

    programs = db.query(Program).all()

    return [
        {
            "id": program.id,
            "name": program.name,
        }
        for program in programs
    ]


# ============================================================
# YEARS
# ============================================================

@router.get("/programs/{program_id}/years")
def get_years(
    program_id: int,
    db: Session = Depends(get_db),
):
    """
    Get all years belonging to a program.
    """

    years = (
        db.query(Year)
        .filter(Year.program_id == program_id)
        .all()
    )

    return [
        {
            "id": year.id,
            "name": year.name,
            "program_id": year.program_id,
        }
        for year in years
    ]


# ============================================================
# SEMESTERS
# ============================================================

@router.get("/years/{year_id}/semesters")
def get_semesters(
    year_id: int,
    db: Session = Depends(get_db),
):
    """
    Get all semesters belonging to a year.
    """

    semesters = (
        db.query(Semester)
        .filter(Semester.year_id == year_id)
        .all()
    )

    return [
        {
            "id": semester.id,
            "name": semester.name,
            "year_id": semester.year_id,
        }
        for semester in semesters
    ]


# ============================================================
# BRANCHES
# ============================================================

@router.get("/semesters/{semester_id}/branches")
def get_branches(
    semester_id: int,
    db: Session = Depends(get_db),
):
    """
    Get all branches belonging to a semester.
    """

    branches = (
        db.query(Branch)
        .filter(Branch.semester_id == semester_id)
        .all()
    )

    return [
        {
            "id": branch.id,
            "name": branch.name,
            "semester_id": branch.semester_id,
        }
        for branch in branches
    ]


# ============================================================
# SUBJECTS
# ============================================================

@router.get("/branches/{branch_id}/subjects")
def get_subjects(
    branch_id: int,
    db: Session = Depends(get_db),
):
    """
    Get all subjects belonging to a branch.
    """

    subjects = (
        db.query(Subject)
        .filter(Subject.branch_id == branch_id)
        .all()
    )

    return [
        {
            "id": subject.id,
            "name": subject.name,
            "branch_id": subject.branch_id,
        }
        for subject in subjects
    ]


# ============================================================
# DOCUMENTS
# ============================================================

@router.get("/subjects/{subject_id}/documents")
def get_documents(
    subject_id: int,
    db: Session = Depends(get_db),
):
    """
    Get all documents belonging to a subject.
    """

    documents = (
        db.query(Document)
        .filter(Document.subject_id == subject_id)
        .all()
    )

    return [
        {
            "id": document.id,
            "title": document.title,
            "file_path": document.file_path,
            "subject_id": document.subject_id,
        }
        for document in documents
    ]


# ============================================================
# RAG SEMANTIC SEARCH
# ============================================================

@router.get("/rag/search")
def rag_search(
    query: str,
    top_k: int = 3
):
    result = generate_answer(
        query=query,
        top_k=top_k
    )

    return {
        "query": query,
        "answer": result["answer"],
        "sources": result["sources"]
    }

# ============================================================
# RAG AI ANSWER
# ============================================================

@router.get("/rag/ask")
def rag_ask(
    query: str,
    top_k: int = 3,
):
    """
    Generate an AI answer using university documents.

    Flow:

    User Question
          ↓
    Semantic Search
          ↓
    Relevant Chunks
          ↓
        Gemini
          ↓
    Grounded Answer
    """

    result = generate_answer(
        query=query,
        top_k=top_k,
    )

    return {
        "query": query,
        "answer": result["answer"],
        "sources": result["sources"],
    }