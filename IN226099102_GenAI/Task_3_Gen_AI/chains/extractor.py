"""
Extraction chains for resume and job description structured data.

Uses LCEL (LangChain Expression Language) with ChatPromptTemplate,
ChatGroq, and StrOutputParser as documented in doc.md.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

from utils.config import GROQ_API_KEY, MODEL_NAME, TEMPERATURE, MAX_TOKENS
from utils.schemas import ResumeProfile, JobRequirements

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Prompt directory
# ---------------------------------------------------------------------------
_PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts"

# ---------------------------------------------------------------------------
# Shared LLM instance
# ---------------------------------------------------------------------------

def _build_llm() -> ChatGroq:
    """Build the ChatGroq LLM instance with project settings."""
    return ChatGroq(
        model=MODEL_NAME,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        max_retries=3,
        api_key=GROQ_API_KEY,
    )


# ---------------------------------------------------------------------------
# Helper — robust JSON extraction from LLM text output
# ---------------------------------------------------------------------------

def _parse_json_from_text(raw: str) -> dict:
    """
    Extract the first valid JSON object from raw LLM output.

    The LLM sometimes wraps JSON in ```json ... ``` blocks
    or adds trailing commentary — this helper handles that.
    """
    text = raw.strip()

    # Strip markdown code fences if present
    if text.startswith("```"):
        # Remove opening fence (```json or ```)
        first_newline = text.index("\n")
        text = text[first_newline + 1 :]
        # Remove closing fence
        if text.rstrip().endswith("```"):
            text = text.rstrip()[:-3]

    # Find the first { and last } to isolate the JSON object
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"No JSON object found in LLM output:\n{raw[:200]}")

    return json.loads(text[start : end + 1])


# ---------------------------------------------------------------------------
# Resume extraction chain  (Feature C)
# ---------------------------------------------------------------------------

def extract_resume(resume_text: str) -> ResumeProfile:
    """
    Run the resume extraction LCEL chain.

    Pipeline: ChatPromptTemplate -> ChatGroq -> StrOutputParser -> JSON parse -> ResumeProfile

    Args:
        resume_text: Raw text extracted from a PDF resume.

    Returns:
        A validated ResumeProfile Pydantic object.
    """
    prompt_template = (_PROMPT_DIR / "resume_extract.txt").read_text(encoding="utf-8")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a precise data extraction assistant. Return only valid JSON."),
        ("user", prompt_template),
    ])

    llm = _build_llm()
    parser = StrOutputParser()

    # LCEL chain — creates a RunnableSequence
    chain = prompt | llm | parser

    # Execute with .invoke() and LangSmith tags
    raw_output: str = chain.invoke(
        {"resume_text": resume_text},
        config={"tags": ["extraction", "resume"]},
    )

    try:
        data = _parse_json_from_text(raw_output)
        return ResumeProfile(**data)
    except Exception as exc:
        logger.error("Resume extraction parse error: %s", exc)
        return ResumeProfile()


# ---------------------------------------------------------------------------
# Job description extraction chain  (Feature D)
# ---------------------------------------------------------------------------

def extract_jd(jd_text: str) -> JobRequirements:
    """
    Run the JD extraction LCEL chain.

    Pipeline: ChatPromptTemplate -> ChatGroq -> StrOutputParser -> JSON parse -> JobRequirements

    Args:
        jd_text: Raw job description text.

    Returns:
        A validated JobRequirements Pydantic object.
    """
    prompt_template = (_PROMPT_DIR / "jd_extract.txt").read_text(encoding="utf-8")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a precise data extraction assistant. Return only valid JSON."),
        ("user", prompt_template),
    ])

    llm = _build_llm()
    parser = StrOutputParser()

    chain = prompt | llm | parser

    raw_output: str = chain.invoke(
        {"jd_text": jd_text},
        config={"tags": ["extraction", "jd"]},
    )

    try:
        data = _parse_json_from_text(raw_output)
        return JobRequirements(**data)
    except Exception as exc:
        logger.error("JD extraction parse error: %s", exc)
        return JobRequirements()
