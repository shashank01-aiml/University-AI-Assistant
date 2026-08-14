from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.academic import router as academic_router
from app.api.documents import router as documents_router


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="University AI Assistant",
    description="AI-powered university document assistant using RAG and Gemini.",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

# Allows the frontend to communicate with the FastAPI backend.
# This is useful while running the project locally.
#
# Later, when the application is deployed,
# replace "*" with your actual frontend domain.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROUTERS
# ============================================================

# Academic APIs
#
# Examples:
# /academic/programs
# /academic/years
# /academic/semesters
# /academic/branches
# /academic/subjects
# /academic/documents
# /academic/rag/search
# /academic/rag/ask

app.include_router(
    academic_router
)


# Document upload APIs
#
# POST /documents/upload

app.include_router(
    documents_router
)


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "University AI Assistant API is running.",
        "status": "online",
        "version": "1.0.0",
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "University AI Assistant",
    }