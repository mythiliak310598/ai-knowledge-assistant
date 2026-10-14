# Master Blueprint: AI Knowledge & Document Assistant

## 1. Tech Stack & Architecture
- Backend: Python, FastAPI, SQLAlchemy, Pydantic, pypdf
- Database: PostgreSQL with pgvector extension
- Infrastructure: Docker, Docker Compose
- AI Pipeline: OpenAI API (Embeddings & LLM)
- Isolation Rule: Pure Python RAG implementation. Do NOT install LangChain or LlamaIndex.

## 2. Business Requirements & Enterprise Guardrails
- Core Problem: Users waste hours searching for facts across dense multi-page PDFs regarding corporate compliance, leave, or financial statistics.
- Source Attribution SLA: Every single AI response must explicitly output the source filename and page number. Never return an answer without a chunk reference.
- No-Hallucination Directive: If information is not found in the top retrieved context blocks, output exactly: *"I couldn't find this information in the uploaded documents."* Never allow the LLM to make up or deduce a policy.
- Corporate Data Privacy: All internal text vectors and uploaded document text data must remain private within our local system.

## 3. Current Project Roadmap & Progress
- [x] STEP 1 — Project Setup
- [x] STEP 2 — FastAPI Foundation (Health Check)
- [x] STEP 3 — PostgreSQL + SQLAlchemy Connection
- [x] STEP 4 — PDF Upload
- [x] STEP 5 — PDF Text Extraction
- [x] STEP 6 — Chunking Strategy
- [/] STEP 7 — Embeddings (Logic complete, verification pending in `test_embedding.py`)
- [ ] STEP 8 — pgvector Integration (Next Target)
- [ ] STEP 9 — Vector Similarity Search
- [ ] STEP 10 — Build RAG Manually
- [ ] STEP 11 — Source Citations API
- [ ] STEP 12 — Minimal Next.js UI
- [ ] STEP 13 — Conversation History
- [ ] STEP 14 — Streaming (SSE)
- [ ] STEP 15 — Basic RAG Evaluation
- [ ] STEP 16 — Production Docker Setup
- [ ] STEP 17 — Integration Testing Suite
- [ ] STEP 18 — README + Portfolio Architecture Diagram

## 4. Crucial Rules for Codex Agent (Strict Teaching Mode)
1. Provide precise architectural blueprints, database schema maps, execution algorithms, and step-by-step implementation checklists.
2. Teach me the foundational computer science concepts behind every step (e.g., memory management, connection pooling, vector space math) because I am front end developer transtition to be a AI Engineer
3. Keep outputs minimal. Provide conceptual frameworks directly without conversational greetings or lengthy introductions to minimize token usage.

