"""
Centralized configuration loader.
Reads from .env and provides typed access to all settings.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
    FALLBACK_MODEL: str = os.getenv("FALLBACK_MODEL", "llama-3.1-8b-instant")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    CHROMA_DIR: str = os.getenv("CHROMA_DIR", "./chroma_db")
    SQLITE_PATH: str = os.getenv("SQLITE_PATH", "./support.db")
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.72"))
    TOP_K: int = int(os.getenv("TOP_K", "4"))
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./data/uploads")
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "support_docs")
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))

    @classmethod
    def validate(cls) -> list[str]:
        """Validate required settings. Returns list of error messages."""
        errors = []
        if not cls.GROQ_API_KEY:
            errors.append("GROQ_API_KEY is not set in .env")
        return errors

    @classmethod
    def ensure_directories(cls):
        """Create required directories if they don't exist."""
        os.makedirs(cls.UPLOAD_DIR, exist_ok=True)
        os.makedirs(os.path.dirname(cls.CHROMA_DIR) or ".", exist_ok=True)
        os.makedirs(cls.CHROMA_DIR, exist_ok=True)


settings = Settings()
