# prd.md

# Product Requirements Document

## Project Title

RAG-Based Customer Support Assistant with LangGraph & Human-in-the-Loop (HITL)

## Executive Summary

Build a production-style customer support platform where admins upload PDF knowledge bases, configure support rules, and customers interact with an AI assistant that uses Retrieval-Augmented Generation (RAG). The system uses LangGraph for workflow orchestration and escalates to humans when confidence is low or approvals are required.

## Objectives

* Process PDF knowledge bases
* Chunk and embed content
* Store embeddings in ChromaDB
* Retrieve relevant context for user queries
* Generate grounded answers using Groq LLM
* Route decisions using LangGraph
* Support HITL escalation workflows
* Provide Admin + Customer interfaces
* Include tests and documentation

## Users

### Admin

* Upload PDFs
* Re-index knowledge base
* Configure thresholds
* Manage escalations
* View analytics/logs

### Customer

* Ask support questions
* Receive grounded answers
* Request human help
* Track escalation status

## Functional Requirements

### Admin Panel

* Secure login (simple local auth acceptable)
* Upload one or multiple PDFs
* View indexed documents
* Rebuild vector index
* Set confidence threshold
* Toggle escalation triggers
* View tickets
* Reply to escalations

### Customer Chat

* Chat UI
* Query submission
* Answer display
* Source citations (document/page)
* Escalation messages
* Session history (optional)

### RAG Pipeline

* PDF loading
* Text cleaning
* Recursive chunking
* Metadata extraction
* Embedding generation
* Chroma persistence
* Similarity retrieval
* Top-k configurable

### LangGraph Workflow

Nodes:

1. Input Node
2. Retrieve Node
3. Generate Node
4. Decision Node
5. Output Node
6. Escalation Node
7. Human Response Node

Conditional routes:

* confident_answer -> output
* low_confidence -> escalate
* no_context -> escalate
* approval_required -> escalate
* user_requests_human -> escalate

### HITL Module

* Create ticket ID
* Store transcript
* Assign category
* Admin response UI
* Resume conversation

## Non-Functional Requirements

* Modular codebase
* Clear separation of concerns
* Persistent storage
* Fast local retrieval
* Reasonable latency (<5 sec typical)
* Error handling
* Maintainable structure

## Recommended Tech Stack

* Python 3.11+
* Streamlit (UI)
* FastAPI (optional API layer)
* LangChain
* LangGraph
* ChromaDB
* sentence-transformers
* Groq API
* SQLite
* pytest
* python-dotenv
* pypdf

## Model Choice

Primary: llama-3.3-70b-versatile
Fallback Dev: llama-3.1-8b-instant
Embeddings: all-MiniLM-L6-v2

## Suggested Folder Structure

```text
project/
  .env
  .env.template
  app.py
  requirements.txt
  data/
  uploads/
  chroma_db/
  docs/
  tests/
  modules/
    config.py
    ingest.py
    retriever.py
    prompts.py
    graph.py
    hitl.py
    db.py
    ui_admin.py
    ui_customer.py
```

## APIs / Interfaces

### POST /upload

Upload PDFs and ingest.

### POST /query

Input: {message, session_id}
Output: {answer, confidence, sources, escalated}

### POST /ticket/respond

Admin responds to escalated ticket.

## Data Structures

### Chunk

```json
{ "id":"chunk_1", "text":"...", "source":"refund.pdf", "page":2, "section":"refund", "embedding":[] }
```

### Graph State

```json
{ "query":"...", "retrieved_docs":[], "answer":"", "confidence":0.0, "route":"output", "ticket_id":null }
```

## Routing Logic

Escalate if:

* confidence < threshold
* zero relevant docs
* refund/approval intent detected
* complaint sentiment high
* explicit human request

## Prompting Rules

* Use only retrieved context when possible
* If uncertain, state limitation
* Never invent policies
* Mention sources when available
* Keep support tone professional

## Scalability Considerations

* Batch ingestion
* Multi-document collections
* Metadata filters
* Cache embeddings
* Async processing
* Swap SQLite -> Postgres if needed

## Deliverables Required

* HLD PDF
* LLD PDF
* Technical Documentation PDF
* Working Project

## Acceptance Criteria

* PDF uploads successfully
* Questions answered from docs
* Hallucinations minimized
* Escalations work end-to-end
* Admin can reply
* Tests pass
* App runs locally with setup instructions

---

# test.md

# Testing & Evaluation Guide

## Setup Test Data

Use 3 PDFs:

1. refund_policy.pdf
2. shipping_faq.pdf
3. billing_support.pdf

## Functional Tests

### Ingestion

* Upload single PDF
* Upload multiple PDFs
* Re-upload updated PDF
* Corrupt PDF handling

### Retrieval Tests

Query: "What is refund timeline?"
Expected: Retrieves refund doc chunk.

Query: "How long is shipping?"
Expected: Retrieves shipping chunk.

### Generation Tests

* Answer concise and grounded
* Includes source references
* No fabricated policy

### Escalation Tests

Query: "I was charged twice and I need manager now"
Expected: Ticket created.

Query: "Approve refund outside 30-day window"
Expected: Approval escalation.

### Human Response Tests

* Admin replies to ticket
* Customer sees update

## Edge Cases

* Empty query
* Very long query
* No docs uploaded
* API key missing
* Groq timeout
* Chroma folder missing

## Quality Metrics

* Retrieval relevance@k
* Response latency
* Escalation precision
* Hallucination rate (manual)
* UI usability

## Manual Demo Flow

1. Upload PDFs
2. Ask normal question
3. Ask unknown question
4. Trigger escalation
5. Respond from admin panel
6. Show resumed conversation

---

# .env.template

```env
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama-3.3-70b-versatile
CHROMA_DIR=./chroma_db
SQLITE_PATH=./support.db
CONFIDENCE_THRESHOLD=0.72
TOP_K=4
```

---

