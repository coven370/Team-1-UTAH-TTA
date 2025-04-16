# Technical Overview

The Utah Teacher Training Assistant (UTAH-TTA) platform is a modular and scalable system designed to simulate realistic student-teacher interactions using artificial intelligence. Below is an overview of the technical components that made this project possible, including the tools, frameworks, models, and APIs utilized throughout development.

## Tools & Frameworks

| Layer            | Key Technologies                          | Purpose                                                                 |
|------------------|--------------------------------------------|-------------------------------------------------------------------------|
| **Backend**      | Python 3.11, FastAPI                       | High-performance REST endpoints for chat, scenario management, and logging. |
| **AI / Retrieval** | Faiss for similarity search, SentenceTransformer embeddings | Converts 17k+ textbook fragments into 768D vectors; supports sub-150 ms semantic search. |
| **Database**     | SQLite & `vector_db.sqlite`               | Stores vectorized knowledge chunks, user sessions, and progress metrics. |
| **Testing**      | Pytest, Coverage.py                       | 120+ unit tests (87% coverage) over retriever logic, API routes, and DB adapters. |
| **Collaboration**| GitHub, Markdown, GitHub Actions          | Version control, doc generation, continuous lint-test.                  |
| **Deployment / Networking** | Tailscale with Funnel                | Exposes the FastAPI server running on a local dev box to the public internet over WireGuard-secured HTTPS, eliminating the need for cloud hosting or port-forwarding. |

## Models & Local Inference Stack

| Component            | Details                                                                 |
|----------------------|-------------------------------------------------------------------------|
| **Ollama Runtime**    | Lightweight containerized LLM runner installed on the same local machine as the backend. |
| **DeepSeek-R1 8B**    | General-purpose language model (~8 billion params) loaded via Ollama. Handles intent classification, response generation, and retrieval augmentation. |
| **Embedding Model**   | `all-MiniLM-L6-v2` (or equivalent) from SentenceTransformers for fast, 384-dimensional embeddings of KB chunks. |
| **Knowledge Retriever** | Custom Python class that embeds the user prompt, queries Faiss, feeds top-k context into DeepSeek-R1, and returns an age-appropriate reply plus rationale. |

## Knowledge Base Integration

- **Vector Database (`vector_db.sqlite`)** — Stores over 17,000 segmented knowledge chunks extracted from textbooks and academic sources, categorized by:
  - General Education
  - Classroom Management
  - Teaching Strategies
  - Student Development

- **Knowledge DB (`knowledge.db`)** — Structured database containing behavioral rules, interaction metadata, and categorization tags for better scenario alignment.

## APIs and Integration

- **Custom RESTful API** — Built with FastAPI to handle:
  - Chatbot messaging routes
  - Scenario management
  - Data logging and analysis

- **Local File System Integration** — Direct access to local vector databases and configuration files using Python’s standard file and YAML libraries.

- **Testing Frameworks** — Unit tests developed using `pytest` to verify system integrity, including automated tests for the AI and data pipelines.

## Development and Testing

- **Git & GitHub** — Version control and collaborative development platform used for branching, pull requests, and code reviews.
- **Pytest** — Framework for unit testing key modules, especially the AI backend and data retrieval components.
- **Markdown** — Used for extensive internal documentation and external-facing guides.

## System Architecture

The system follows a modular architecture:

- **Frontend Interface (UI layer):** Chat interaction window and input/output displays.
- **Backend API:** FastAPI endpoints connecting UI to AI logic and databases.
- **AI Engine:** KnowledgeRetriever and embedded models performing search, reasoning, and response generation.
- **Database Layer:** Manages vectorized knowledge, user interactions, and progress tracking.
