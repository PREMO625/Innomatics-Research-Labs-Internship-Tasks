# Project Documentation & Architecture Guidelines

This document contains the latest official documentation links, modern best practices, recommended architecture, setup commands, and known deprecations for the core technologies in the RAG-Based Customer Support Assistant project. The goal is to accelerate development and prevent the use of outdated patterns.

## 1. Tech Stack & Recommended Versions

We recommend using the latest stable versions. Below is an example `requirements.txt` to lock in standard modern versions (as of 2024/2025 standards, adjust minor versions as needed):

```text
# requirements.txt
langchain>=1.2.0
langchain-core>=1.3.0
langchain-groq>=0.1.0
langchain-chroma>=0.1.0
langchain-community>=0.2.0
langgraph>=1.1.0
chromadb>=1.5.0
streamlit>=1.56.0
groq>=1.2.0
sentence-transformers>=3.0.0
pytest>=8.0.0
pypdf>=4.2.0
python-dotenv>=1.0.1
fastapi>=0.111.0
uvicorn>=0.30.0
```

## 2. Setup Commands

### Environment Setup
Use a virtual environment to avoid dependency conflicts.

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

**Mac/Linux:**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Common Pitfalls during Setup:
1. **ChromaDB C++ build errors on Windows**: If you face issues installing `chromadb`, install the [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
2. **Missing SQLite3**: ChromaDB requires SQLite > 3.35. Ensure your Python installation comes with an updated sqlite3.

---

## 3. Architecture & Folder Structure Guidance

A clean separation of concerns is critical. The UI should not contain core logic, and the graph should not directly interact with Streamlit.

```text
project/
├── .env                    # Environment variables (do not commit)
├── .env.template           # Template for environment variables
├── requirements.txt        # Python dependencies
├── app.py                  # Main Streamlit application entry point
├── tests/                  # Pytest directory
│   ├── test_ingest.py
│   ├── test_retrieval.py
│   └── test_graph.py
├── data/
│   ├── uploads/            # Raw PDF storage
│   └── chroma_db/          # Persistent Chroma vector store
├── db/                     # SQLite database files for HITL/Tickets
│   └── support.db
└── modules/                # Core backend logic
    ├── config.py           # Centralized environment & settings loader
    ├── ingest.py           # PDF parsing & text chunking logic
    ├── retriever.py        # Embedding and ChromaDB search functions
    ├── prompts.py          # System prompts and templates
    ├── graph.py            # LangGraph nodes, edges, and state definition
    ├── hitl.py             # Human-in-the-loop and ticket management logic
    ├── db_utils.py         # SQLite connection and queries
    ├── ui_admin.py         # Streamlit components for Admin Panel
    └── ui_customer.py      # Streamlit components for Customer Chat
```

---

## 4. Technology-Specific Best Practices & Deprecations

### 1. LangChain & LangChain Core
*   **Official Docs:** [python.langchain.com](https://python.langchain.com/v0.2/docs/introduction/)
*   **Best Practices:** 
    *   Use **LCEL (LangChain Expression Language)** using the `|` pipe operator instead of legacy `Chain` classes.
    *   Use `ChatPromptTemplate` for message formatting.
*   **Import Paths:**
    *   `from langchain_core.prompts import ChatPromptTemplate`
    *   `from langchain_core.output_parsers import StrOutputParser`
*   **Known Deprecations:** 
    *   `langchain.chat_models`, `langchain.llms`, and `langchain.vectorstores` are deprecated. Use `langchain_community`, `langchain_core`, or partner packages (e.g., `langchain_groq`, `langchain_chroma`).
    *   Legacy chains like `RetrievalQA` or `ConversationalRetrievalChain` are discouraged; use LCEL with LangGraph.

### 2. LangGraph
*   **Official Docs:** [langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph/)
*   **Best Practices:** 
    *   Define your `GraphState` strictly using `typing.TypedDict`.
    *   Use `StateGraph` for workflows. 
    *   Keep nodes simple: purely functional transformations of the `state`.
*   **Import Paths:**
    *   `from langgraph.graph import StateGraph, END`
*   **Common Pitfalls:** Forgetting to return the updated keys in your node functions (e.g., `return {"messages": [new_message]}` instead of mutating state directly).

### 3. Groq Python SDK / LangChain Integration
*   **Official Docs:** [console.groq.com/docs/quickstart](https://console.groq.com/docs/quickstart)
*   **Best Practices:**
    *   Use the LangChain integration rather than the raw Groq SDK to seamlessly fit into LCEL and LangGraph.
    *   Set `temperature=0` for grounded RAG answers to minimize hallucinations.
*   **Import Paths:**
    *   `from langchain_groq import ChatGroq`
*   **Usage:** `llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)`

### 4. ChromaDB
*   **Official Docs:** [docs.trychroma.com](https://docs.trychroma.com/)
*   **Best Practices:**
    *   Use `langchain-chroma` for integration instead of `langchain-community`.
    *   Specify a `persist_directory` to ensure vector indexes aren't lost on restart.
*   **Import Paths:**
    *   `from langchain_chroma import Chroma`
*   **Known Deprecations:** `from langchain_community.vectorstores import Chroma` is discouraged.

### 5. Streamlit
*   **Official Docs:** [docs.streamlit.io](https://docs.streamlit.io/)
*   **Best Practices:**
    *   Use `st.session_state` to store `session_id`, `messages`, and `admin_mode_toggle`.
    *   Use `st.chat_message` and `st.chat_input` for the UI.
    *   Use `st.cache_resource` for expensive initializations like the LLM client or VectorStore to prevent reloading on every UI interaction.
*   **Import Paths:**
    *   `import streamlit as st`
*   **Common Pitfalls:** Streamlit re-runs the entire script on every user interaction. Without `st.session_state` and `st.cache_resource`, the app will be extremely slow and lose context.

### 6. sentence-transformers & Embeddings
*   **Official Docs:** [sbert.net](https://sbert.net/)
*   **Best Practices:**
    *   `all-MiniLM-L6-v2` is perfect for fast, local CPU embeddings.
*   **Import Paths:**
    *   `from langchain_community.embeddings import HuggingFaceEmbeddings`
*   **Usage:** `embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")`

### 7. pypdf
*   **Official Docs:** [pypdf.readthedocs.io](https://pypdf.readthedocs.io/)
*   **Best Practices:** Use LangChain's built-in loader which wraps pypdf automatically.
*   **Import Paths:**
    *   `from langchain_community.document_loaders import PyPDFLoader`

### 8. SQLite
*   **Official Docs:** [docs.python.org/3/library/sqlite3.html](https://docs.python.org/3/library/sqlite3.html)
*   **Best Practices:** 
    *   Use standard library `sqlite3` for tracking tickets and HITL transcripts.
    *   Always use parameterized queries (`?`) to prevent SQL injection. Example: `cursor.execute("SELECT * FROM tickets WHERE id=?", (ticket_id,))`

### 9. FastAPI (Optional Layer)
*   **Official Docs:** [fastapi.tiangolo.com](https://fastapi.tiangolo.com/)
*   **Best Practices:**
    *   Use Pydantic models for request/response validation.
    *   If combining with Streamlit, run FastAPI on a separate port (e.g., 8000) and have Streamlit (port 8501) make HTTP requests via the `requests` library.

### 10. pytest
*   **Official Docs:** [docs.pytest.org](https://docs.pytest.org/)
*   **Best Practices:**
    *   Use `@pytest.fixture` to provide test PDFs or mock ChromaDB instances.
    *   Test LangGraph logic by bypassing the LLM (mocking `ChatGroq`) to avoid API costs and slow tests.
*   **Running tests:** `pytest tests/ -v`

---

## 5. Implementation Recommendations to Prevent Deprecated Code

1.  **Do not use `langchain.llms` or `langchain.chat_models`**. Always import from `langchain_{partner}`.
2.  **Avoid `ConversationalRetrievalChain`**. Instead, use a custom LCEL pipeline that generates a standalone query, retrieves documents, and then passes them to the final QA prompt. This pattern is naturally implemented inside LangGraph.
3.  **Graph State Management:** In LangGraph, dictionaries returned by nodes update the state. Ensure you only return the keys you want to update/append. 
4.  **Vector Store Filtering:** When retrieving, use Chroma's native metadata filtering if you need to restrict context by document. Example: `retriever = vectorstore.as_retriever(search_kwargs={"filter": {"source": "refund.pdf"}})`
