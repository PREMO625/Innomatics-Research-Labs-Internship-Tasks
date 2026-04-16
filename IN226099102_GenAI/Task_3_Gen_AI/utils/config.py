"""
Configuration loader for the AI Resume Screening System.

Loads environment variables from .env, validates required keys,
and exposes a typed Settings object for the rest of the application.
"""

import os
import sys
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Load .env BEFORE any other import that might need env vars
# ---------------------------------------------------------------------------
load_dotenv(override=True)

# ---------------------------------------------------------------------------
# Required environment variable keys
# ---------------------------------------------------------------------------
_REQUIRED_KEYS = [
    "GROQ_API_KEY",
    "LANGCHAIN_API_KEY",
]

# ---------------------------------------------------------------------------
# Validation helper
# ---------------------------------------------------------------------------

def _validate_env() -> None:
    """Raise a readable error when mandatory env vars are missing."""
    missing = [k for k in _REQUIRED_KEYS if not os.environ.get(k)]
    if missing:
        print(
            "\n❌  Missing required environment variables:\n   "
            + "\n   ".join(missing)
            + "\n\n   Please set them in your .env file and restart.\n"
        )
        sys.exit(1)


_validate_env()

# ---------------------------------------------------------------------------
# Public settings -- importable from anywhere via `from utils.config import *`
# ---------------------------------------------------------------------------

GROQ_API_KEY: str = os.environ["GROQ_API_KEY"]
LANGCHAIN_API_KEY: str = os.environ["LANGCHAIN_API_KEY"]

# LangSmith tracing — always enabled
LANGCHAIN_TRACING_V2: str = os.environ.get("LANGCHAIN_TRACING_V2", "true")
LANGCHAIN_ENDPOINT: str = os.environ.get(
    "LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com"
)
LANGCHAIN_PROJECT: str = os.environ.get(
    "LANGCHAIN_PROJECT", "resume-screening-system"
)

# Model configuration
MODEL_NAME: str = os.environ.get(
    "MODEL_NAME", "meta-llama/llama-4-scout-17b-16e-instruct"
)
TEMPERATURE: float = float(os.environ.get("TEMPERATURE", "0"))
MAX_TOKENS: int = int(os.environ.get("MAX_TOKENS", "2048"))

# Ensure LangSmith environment vars are actually set for the SDK to pick up
os.environ["LANGCHAIN_TRACING_V2"] = LANGCHAIN_TRACING_V2
os.environ["LANGCHAIN_ENDPOINT"] = LANGCHAIN_ENDPOINT
os.environ["LANGCHAIN_PROJECT"] = LANGCHAIN_PROJECT
