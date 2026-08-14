# University AI Assistant

An AI-powered academic assistant for the School of Technology that enables students to ask questions about their academic and technical curriculum and receive grounded answers from institution-provided documents.

The system uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from uploaded academic PDFs before generating an answer. Each response can be traced back to the source document and relevant document section.

---

## 🚀 Overview

The University AI Assistant is designed to provide a centralized question-answering platform for students and instructors.

Instructors can upload academic and technical documents such as:

* Course handouts
* Lecture notes
* Subject materials
* Academic regulations
* Technical documentation
* Course outlines
* Reference PDFs

Students can select their:

* Program
* Year
* Semester
* Branch
* Subject

and ask questions related to their curriculum.

The assistant retrieves relevant information from the uploaded documents and generates an answer using an LLM while maintaining grounding in the retrieved academic content.

---

## 🎯 Objectives

The primary objectives of the project are:

1. Provide students with an AI-powered academic assistant.
2. Enable instructors to upload and manage academic documents.
3. Use RAG to reduce hallucination and improve answer grounding.
4. Provide references to the source documents used to generate answers.
5. Support multiple programs and branches across the School of Technology.
6. Create a scalable architecture that can initially run locally and later be deployed.
7. Maintain academic metadata so that responses are relevant to the selected program, semester, branch and subject.

---

## ✨ Key Features

### Student Features

* Select academic program
* Select year
* Select semester
* Select branch
* Select subject
* Ask natural-language questions
* Receive AI-generated answers
* View supporting source references
* Ask follow-up questions
* Maintain conversational context

### Instructor Features

* Upload academic PDFs
* Associate documents with academic metadata
* Organize documents by program, year, semester, branch and subject
* Process documents into searchable knowledge
* Update the academic knowledge base

### AI Features

* Retrieval-Augmented Generation
* Semantic document search
* Context-aware question answering
* Metadata-filtered retrieval
* Source-grounded responses
* Conversational follow-up questions

---

## 🧠 System Architecture

```text
                    ┌─────────────────────┐
                    │      Student       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ React + TypeScript │
                    │       Frontend     │
                    └──────────┬──────────┘
                               │
                         REST API
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI       │
                    │       Backend      │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
          ┌─────────────────┐    ┌─────────────────┐
          │ Academic SQLite │    │   RAG Pipeline  │
          │    Database     │    └────────┬────────┘
          └─────────────────┘             │
                                          ▼
                                  ┌─────────────────┐
                                  │    ChromaDB     │
                                  │ Vector Database │
                                  └────────┬────────┘
                                           │
                                      Retrieved
                                       Context
                                           │
                                           ▼
                                  ┌─────────────────┐
                                  │   Gemini LLM    │
                                  └────────┬────────┘
                                           │
                                           ▼
                                  Grounded Answer
                                           │
                                           ▼
                                  ┌─────────────────┐
                                  │     Student     │
                                  └─────────────────┘
```

---

## 🔄 RAG Pipeline

The application follows the following pipeline:

```text
PDF Upload
    ↓
PDF Text Extraction
    ↓
Document Cleaning
    ↓
Text Chunking
    ↓
Metadata Association
    ↓
Embedding Generation
    ↓
ChromaDB Storage
    ↓
Student Question
    ↓
Query Embedding
    ↓
Metadata Filtering
    ↓
Semantic Retrieval
    ↓
Relevant Context
    ↓
Gemini LLM
    ↓
Grounded Answer
    ↓
Source References
```

---

## 📚 Document Processing

When an instructor uploads a PDF, the system processes it through multiple stages.

### 1. Text Extraction

The text is extracted from the uploaded academic document.

### 2. Cleaning

Unnecessary formatting and irrelevant content are removed.

### 3. Chunking

The document is divided into smaller meaningful sections.

### 4. Metadata Association

Each chunk is associated with metadata such as:

```text
program
year
semester
branch
subject
document_name
page_number
```

### 5. Embedding

The chunks are converted into vector representations.

### 6. Vector Storage

The embeddings and associated metadata are stored in ChromaDB.

---

## 🔎 Retrieval

When a student asks a question, the system:

1. Converts the question into an embedding.
2. Identifies the selected academic context.
3. Searches the vector database.
4. Applies academic metadata filters.
5. Retrieves the most relevant chunks.
6. Passes the retrieved context to the LLM.
7. Generates a grounded answer.
8. Returns source information to the student.

This approach ensures that a question about one subject does not unnecessarily retrieve information from unrelated academic content.

---

## 🤖 Large Language Model

The project uses **Google Gemini** as the language model.

Gemini is responsible for generating the final response after the relevant academic information has been retrieved.

The LLM is not treated as the primary knowledge source. Instead, the retrieved academic documents provide the context used for answer generation.

---

## 🗄️ Databases

### SQLite

SQLite is used for structured academic and application metadata.

Example entities include:

```text
Program
Year
Semester
Branch
Subject
Document
Document Metadata
```

### ChromaDB

ChromaDB is used as the vector database for semantic retrieval.

It stores:

* Document chunks
* Embeddings
* Metadata
* Document identifiers
* Source information

---

## 🛠️ Technology Stack

| Layer               | Technology    |
| ------------------- | ------------- |
| Frontend            | React         |
| Language            | TypeScript    |
| Build Tool          | Vite          |
| Backend             | Python        |
| API Framework       | FastAPI       |
| Structured Database | SQLite        |
| Vector Database     | ChromaDB      |
| LLM                 | Google Gemini |
| Architecture        | REST API      |
| AI Architecture     | RAG           |
| Version Control     | Git / GitHub  |

---

## 📁 Project Structure

```text
university-ai-assistant/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── utils/
│   ├── data/
│   ├── chroma_db/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── types/
│   └── package.json
│
├── docs/
├── tests/
├── screenshots/
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### Prerequisites

Install the following:

* Python 3.10+
* Node.js 18+
* npm
* Git

---

## 🔧 Backend Setup

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>

cd university-ai-assistant
```

Create and activate a virtual environment:

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

Install backend dependencies:

```bash
cd backend

pip install -r requirements.txt
```

Create your environment file:

```bash
cp .env.example .env
```

Add the required API configuration to `.env`.

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://localhost:8000
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

---

## 🎨 Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will be available at the URL displayed by Vite.

---

## 🔐 Environment Variables

Create a `.env` file in the backend directory.

Example:

```env
GEMINI_API_KEY=your_api_key_here

DATABASE_URL=sqlite:///./data/academic.db

CHROMA_PERSIST_DIRECTORY=./chroma_db

FRONTEND_URL=http://localhost:5173
```

Never commit real API keys or secrets to GitHub.

Only commit `.env.example`.

---

## 🔒 Security

The project follows basic security practices including:

* Environment variables for secrets
* `.gitignore` protection
* Input validation
* File-type validation
* API validation
* Controlled document uploads
* Separation of frontend and backend responsibilities

Production deployment should additionally introduce authentication, authorization, rate limiting, secure file storage and HTTPS.

---

## 🧪 Testing

Backend tests can be executed using:

```bash
pytest
```

Frontend tests should be added for important UI components and API interactions.

Recommended testing areas include:

* Document upload
* PDF processing
* Metadata filtering
* Vector retrieval
* Chat API
* Invalid requests
* Empty queries
* Missing academic metadata
* Source reference generation

---

## 📊 Example Use Case

### Scenario

A student selects:

```text
Program: B.Tech
Year: 3
Semester: 5
Branch: AIML
Subject: Machine Learning
```

The student asks:

> What is the difference between bagging and boosting?

The system:

```text
Question
   ↓
Academic Context
   ↓
Vector Search
   ↓
Relevant Machine Learning PDF Chunks
   ↓
Gemini
   ↓
Generated Explanation
   ↓
Source Reference
```

The student receives an answer based on the relevant uploaded academic material rather than a generic response alone.

---

## 🌐 Future Scope

The architecture is designed so that additional functionality can be introduced later.

Potential improvements include:

* Student authentication
* Instructor authentication
* Role-based access control
* Multi-document management
* Conversation history
* Advanced citation handling
* Voice-based interaction
* Multilingual support
* Analytics dashboard
* Feedback-based answer evaluation
* Cloud deployment
* Automated document ingestion
* Improved retrieval and reranking
* Administrative dashboard

---

## 💰 Cost Consideration

The initial MVP is designed to run locally with a target demonstration cost of approximately **₹0**.

Local development avoids the need for paid infrastructure during the initial development and demonstration phase.

External API usage, hosting and production infrastructure may introduce costs during later deployment.

---

## 🚧 Current Project Status

**Status:** MVP Development

### Completed / Planned Core Components

* [x] Project architecture
* [x] Frontend technology selection
* [x] Backend technology selection
* [x] Academic metadata design
* [x] RAG architecture
* [x] Vector database selection
* [x] LLM selection
* [ ] Frontend implementation
* [ ] Backend API implementation
* [ ] PDF ingestion pipeline
* [ ] Vector indexing
* [ ] Chat interface
* [ ] Source citation interface
* [ ] Testing
* [ ] Deployment

---

## 👨‍💻 Development Philosophy

The project follows a modular architecture so that individual components can be improved without rewriting the entire application.

The separation between:

```text
Frontend
    ↓
API Layer
    ↓
Business Logic
    ↓
RAG Pipeline
    ↓
Databases
```

allows the system to evolve from a local MVP into a production-ready academic AI platform.

---

## 📜 License

This project is intended for academic and internship development purposes.

Add the appropriate license before public production use.

---

## ⭐ Acknowledgements

This project was developed as an academic/internship-oriented AI application focused on applying Retrieval-Augmented Generation, vector search, APIs and modern web technologies to university academic assistance.
