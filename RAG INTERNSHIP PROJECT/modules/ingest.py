"""
PDF ingestion pipeline:
  1. Load PDFs using PyPDFLoader
  2. Clean extracted text
  3. Chunk with RecursiveCharacterTextSplitter
  4. Add metadata (source file, page number)
  5. Generate embeddings via sentence-transformers
  6. Store in persistent ChromaDB
"""

import os
import re
import shutil
from typing import Optional

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

from modules.config import settings
from modules import db


def get_embeddings() -> HuggingFaceEmbeddings:
    """Get the embedding model (cached at module level for reuse)."""
    return HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)


def clean_text(text: str) -> str:
    """Clean extracted PDF text by normalizing whitespace and removing artifacts."""
    # Remove excessive newlines
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Normalize whitespace within lines
    text = re.sub(r"[ \t]+", " ", text)
    # Remove page break artifacts
    text = re.sub(r"\x0c", "", text)
    # Strip leading/trailing whitespace per line
    lines = [line.strip() for line in text.split("\n")]
    text = "\n".join(lines)
    return text.strip()


def load_pdf(filepath: str) -> list[Document]:
    """Load a PDF and return a list of Documents (one per page)."""
    loader = PyPDFLoader(filepath)
    docs = loader.load()
    # Clean text and enrich metadata
    filename = os.path.basename(filepath)
    for i, doc in enumerate(docs):
        doc.page_content = clean_text(doc.page_content)
        doc.metadata["source"] = filename
        doc.metadata["page"] = doc.metadata.get("page", i) + 1  # 1-indexed
        doc.metadata["filepath"] = filepath
    return docs


def chunk_documents(docs: list[Document]) -> list[Document]:
    """Split documents into chunks with metadata preserved."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    # Add chunk index metadata
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = f"{chunk.metadata.get('source', 'unknown')}_{i}"
    return chunks


def get_vectorstore(embeddings: Optional[HuggingFaceEmbeddings] = None) -> Chroma:
    """Get or create the persistent ChromaDB vector store."""
    if embeddings is None:
        embeddings = get_embeddings()
    return Chroma(
        persist_directory=settings.CHROMA_DIR,
        embedding_function=embeddings,
        collection_name=settings.COLLECTION_NAME,
    )


def ingest_pdf(filepath: str) -> dict:
    """
    Full ingestion pipeline for a single PDF.
    Returns summary dict with counts.
    """
    # Load
    docs = load_pdf(filepath)
    if not docs:
        return {"status": "error", "message": "No pages extracted from PDF"}

    # Chunk
    chunks = chunk_documents(docs)
    if not chunks:
        return {"status": "error", "message": "No chunks created from document"}

    # Embed and store
    embeddings = get_embeddings()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=settings.CHROMA_DIR,
        collection_name=settings.COLLECTION_NAME,
    )

    # Register in SQLite
    file_size = os.path.getsize(filepath) if os.path.exists(filepath) else 0
    db.register_document(
        filename=os.path.basename(filepath),
        filepath=filepath,
        file_size=file_size,
        num_pages=len(docs),
        num_chunks=len(chunks),
    )

    return {
        "status": "success",
        "filename": os.path.basename(filepath),
        "num_pages": len(docs),
        "num_chunks": len(chunks),
    }


def ingest_multiple_pdfs(filepaths: list[str]) -> list[dict]:
    """Ingest multiple PDFs. Returns list of result dicts."""
    results = []
    for fp in filepaths:
        try:
            result = ingest_pdf(fp)
            results.append(result)
        except Exception as e:
            results.append({
                "status": "error",
                "filename": os.path.basename(fp),
                "message": str(e),
            })
    return results


def reindex_all() -> dict:
    """
    Delete existing vector store and re-ingest all registered documents.
    Returns summary.
    """
    # Clear ChromaDB
    if os.path.exists(settings.CHROMA_DIR):
        shutil.rmtree(settings.CHROMA_DIR)
    os.makedirs(settings.CHROMA_DIR, exist_ok=True)

    # Get all registered docs
    docs = db.get_all_documents()
    if not docs:
        return {"status": "success", "message": "No documents to reindex", "count": 0}

    # Re-ingest each
    filepaths = [d["filepath"] for d in docs if os.path.exists(d["filepath"])]
    # Clear doc records and re-register during ingestion
    db.clear_all_documents()

    results = ingest_multiple_pdfs(filepaths)
    success_count = sum(1 for r in results if r["status"] == "success")

    return {
        "status": "success",
        "message": f"Reindexed {success_count}/{len(filepaths)} documents",
        "count": success_count,
        "details": results,
    }


def get_collection_stats() -> dict:
    """Get statistics about the current vector store collection."""
    try:
        vs = get_vectorstore()
        collection = vs._collection
        count = collection.count()
        return {"total_chunks": count, "status": "healthy"}
    except Exception as e:
        return {"total_chunks": 0, "status": "error", "message": str(e)}
