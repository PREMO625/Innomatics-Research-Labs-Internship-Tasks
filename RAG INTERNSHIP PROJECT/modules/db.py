"""
SQLite database utilities for tickets, settings, uploaded docs, and chat sessions.
Uses parameterized queries throughout to prevent SQL injection.
"""

import sqlite3
import json
import uuid
from datetime import datetime
from typing import Optional
from modules.config import settings


def get_connection() -> sqlite3.Connection:
    """Get a SQLite connection with row factory for dict-like access."""
    conn = sqlite3.connect(settings.SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """Initialize all database tables."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS tickets (
            id TEXT PRIMARY KEY,
            session_id TEXT NOT NULL,
            query TEXT NOT NULL,
            ai_response TEXT DEFAULT '',
            transcript TEXT DEFAULT '[]',
            status TEXT DEFAULT 'open',
            category TEXT DEFAULT 'general',
            priority TEXT DEFAULT 'normal',
            admin_response TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            resolved_at TEXT DEFAULT NULL
        );

        CREATE TABLE IF NOT EXISTS uploaded_docs (
            id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL,
            file_size INTEGER DEFAULT 0,
            num_pages INTEGER DEFAULT 0,
            num_chunks INTEGER DEFAULT 0,
            uploaded_at TEXT NOT NULL,
            status TEXT DEFAULT 'indexed'
        );

        CREATE TABLE IF NOT EXISTS app_settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS chat_sessions (
            id TEXT PRIMARY KEY,
            created_at TEXT NOT NULL,
            last_activity TEXT NOT NULL,
            messages TEXT DEFAULT '[]'
        );
    """)

    # Initialize default settings if not present
    defaults = {
        "confidence_threshold": str(settings.CONFIDENCE_THRESHOLD),
        "top_k": str(settings.TOP_K),
        "escalation_enabled": "true",
        "escalation_on_low_confidence": "true",
        "escalation_on_no_context": "true",
        "escalation_on_approval_required": "true",
        "escalation_on_user_request": "true",
    }
    now = datetime.utcnow().isoformat()
    for key, value in defaults.items():
        cursor.execute(
            "INSERT OR IGNORE INTO app_settings (key, value, updated_at) VALUES (?, ?, ?)",
            (key, value, now),
        )

    conn.commit()
    conn.close()


# ── Settings ─────────────────────────────────────────────────────────

def get_setting(key: str, default: str = "") -> str:
    """Get a setting value by key."""
    conn = get_connection()
    row = conn.execute("SELECT value FROM app_settings WHERE key=?", (key,)).fetchone()
    conn.close()
    return row["value"] if row else default


def update_setting(key: str, value: str):
    """Update or insert a setting."""
    conn = get_connection()
    now = datetime.utcnow().isoformat()
    conn.execute(
        "INSERT OR REPLACE INTO app_settings (key, value, updated_at) VALUES (?, ?, ?)",
        (key, value, now),
    )
    conn.commit()
    conn.close()


def get_all_settings() -> dict:
    """Get all settings as a dictionary."""
    conn = get_connection()
    rows = conn.execute("SELECT key, value FROM app_settings").fetchall()
    conn.close()
    return {row["key"]: row["value"] for row in rows}


# ── Tickets ──────────────────────────────────────────────────────────

def create_ticket(
    session_id: str,
    query: str,
    ai_response: str = "",
    transcript: list = None,
    category: str = "general",
    priority: str = "normal",
) -> str:
    """Create a new support ticket. Returns ticket ID."""
    ticket_id = f"TKT-{uuid.uuid4().hex[:8].upper()}"
    now = datetime.utcnow().isoformat()
    conn = get_connection()
    conn.execute(
        """INSERT INTO tickets (id, session_id, query, ai_response, transcript,
           status, category, priority, created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, 'open', ?, ?, ?, ?)""",
        (
            ticket_id,
            session_id,
            query,
            ai_response,
            json.dumps(transcript or []),
            category,
            priority,
            now,
            now,
        ),
    )
    conn.commit()
    conn.close()
    return ticket_id


def get_ticket(ticket_id: str) -> Optional[dict]:
    """Get a ticket by ID."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM tickets WHERE id=?", (ticket_id,)).fetchone()
    conn.close()
    if row:
        d = dict(row)
        d["transcript"] = json.loads(d["transcript"])
        return d
    return None


def get_all_tickets(status: Optional[str] = None) -> list[dict]:
    """Get all tickets, optionally filtered by status."""
    conn = get_connection()
    if status:
        rows = conn.execute(
            "SELECT * FROM tickets WHERE status=? ORDER BY created_at DESC", (status,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM tickets ORDER BY created_at DESC"
        ).fetchall()
    conn.close()
    result = []
    for row in rows:
        d = dict(row)
        d["transcript"] = json.loads(d["transcript"])
        result.append(d)
    return result


def respond_to_ticket(ticket_id: str, admin_response: str):
    """Admin responds to a ticket and marks it resolved."""
    now = datetime.utcnow().isoformat()
    conn = get_connection()
    conn.execute(
        """UPDATE tickets SET admin_response=?, status='resolved',
           updated_at=?, resolved_at=? WHERE id=?""",
        (admin_response, now, now, ticket_id),
    )
    conn.commit()
    conn.close()


def update_ticket_status(ticket_id: str, status: str):
    """Update ticket status."""
    now = datetime.utcnow().isoformat()
    conn = get_connection()
    conn.execute(
        "UPDATE tickets SET status=?, updated_at=? WHERE id=?",
        (status, now, ticket_id),
    )
    conn.commit()
    conn.close()


# ── Uploaded Docs ────────────────────────────────────────────────────

def register_document(
    filename: str, filepath: str, file_size: int = 0,
    num_pages: int = 0, num_chunks: int = 0,
) -> str:
    """Register an uploaded document. Returns doc ID."""
    doc_id = f"DOC-{uuid.uuid4().hex[:8].upper()}"
    now = datetime.utcnow().isoformat()
    conn = get_connection()
    conn.execute(
        """INSERT INTO uploaded_docs (id, filename, filepath, file_size,
           num_pages, num_chunks, uploaded_at, status)
           VALUES (?, ?, ?, ?, ?, ?, ?, 'indexed')""",
        (doc_id, filename, filepath, file_size, num_pages, num_chunks, now),
    )
    conn.commit()
    conn.close()
    return doc_id


def get_all_documents() -> list[dict]:
    """Get all registered documents."""
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM uploaded_docs ORDER BY uploaded_at DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def delete_document(doc_id: str):
    """Delete a document record."""
    conn = get_connection()
    conn.execute("DELETE FROM uploaded_docs WHERE id=?", (doc_id,))
    conn.commit()
    conn.close()


def clear_all_documents():
    """Clear all document records."""
    conn = get_connection()
    conn.execute("DELETE FROM uploaded_docs")
    conn.commit()
    conn.close()


# ── Chat Sessions ────────────────────────────────────────────────────

def create_session() -> str:
    """Create a new chat session. Returns session ID."""
    session_id = uuid.uuid4().hex[:12]
    now = datetime.utcnow().isoformat()
    conn = get_connection()
    conn.execute(
        "INSERT INTO chat_sessions (id, created_at, last_activity, messages) VALUES (?, ?, ?, '[]')",
        (session_id, now, now),
    )
    conn.commit()
    conn.close()
    return session_id


def save_session_messages(session_id: str, messages: list):
    """Save messages for a session."""
    now = datetime.utcnow().isoformat()
    conn = get_connection()
    conn.execute(
        "UPDATE chat_sessions SET messages=?, last_activity=? WHERE id=?",
        (json.dumps(messages), now, session_id),
    )
    conn.commit()
    conn.close()


def get_session_messages(session_id: str) -> list:
    """Get messages for a session."""
    conn = get_connection()
    row = conn.execute(
        "SELECT messages FROM chat_sessions WHERE id=?", (session_id,)
    ).fetchone()
    conn.close()
    if row:
        return json.loads(row["messages"])
    return []
