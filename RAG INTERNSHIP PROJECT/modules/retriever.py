"""
Retriever module: handles similarity search against ChromaDB
and returns relevant documents with scores.
"""

from typing import Optional
from langchain_chroma import Chroma
from modules.config import settings
from modules.ingest import get_embeddings, get_vectorstore


def retrieve_documents(
    query: str,
    top_k: Optional[int] = None,
    score_threshold: Optional[float] = None,
) -> list[dict]:
    """
    Retrieve relevant document chunks for a query.
    Returns list of dicts with keys: content, metadata, score.
    """
    if top_k is None:
        top_k = settings.TOP_K

    try:
        vs = get_vectorstore()
        # Use similarity_search_with_relevance_scores for confidence signal
        results = vs.similarity_search_with_relevance_scores(query, k=top_k)
    except Exception:
        return []

    docs = []
    for doc, score in results:
        entry = {
            "content": doc.page_content,
            "metadata": doc.metadata,
            "score": round(score, 4),
            "source": doc.metadata.get("source", "Unknown"),
            "page": doc.metadata.get("page", "?"),
        }
        if score_threshold and score < score_threshold:
            continue
        docs.append(entry)

    return docs


def has_documents() -> bool:
    """Check if there are any documents in the vector store."""
    try:
        vs = get_vectorstore()
        return vs._collection.count() > 0
    except Exception:
        return False


def format_context(retrieved_docs: list[dict]) -> str:
    """Format retrieved documents into context string for the LLM."""
    if not retrieved_docs:
        return ""

    parts = []
    for i, doc in enumerate(retrieved_docs, 1):
        source = doc.get("source", "Unknown")
        page = doc.get("page", "?")
        content = doc.get("content", "")
        parts.append(f"[Source {i}: {source}, Page {page}]\n{content}")

    return "\n\n---\n\n".join(parts)


def format_sources(retrieved_docs: list[dict]) -> list[str]:
    """Format source citations from retrieved documents."""
    sources = []
    seen = set()
    for doc in retrieved_docs:
        source = doc.get("source", "Unknown")
        page = doc.get("page", "?")
        citation = f"📄 {source} (Page {page})"
        if citation not in seen:
            sources.append(citation)
            seen.add(citation)
    return sources
