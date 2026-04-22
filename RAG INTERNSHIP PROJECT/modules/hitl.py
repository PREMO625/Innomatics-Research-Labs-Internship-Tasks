"""
Human-in-the-Loop (HITL) escalation management.
Handles ticket creation, admin responses, and conversation resumption.
"""

import json
from typing import Optional
from modules import db


# ── Escalation Detection ─────────────────────────────────────────────

ESCALATION_KEYWORDS = [
    "speak to a human",
    "talk to a person",
    "human agent",
    "real person",
    "manager",
    "supervisor",
    "escalate",
    "talk to someone",
    "live agent",
    "representative",
]

APPROVAL_KEYWORDS = [
    "refund",
    "cancel",
    "exception",
    "override",
    "approve",
    "authorization",
    "waive",
    "dispute",
]

FRUSTRATION_KEYWORDS = [
    "frustrated",
    "angry",
    "unacceptable",
    "terrible",
    "worst",
    "ridiculous",
    "incompetent",
    "useless",
    "furious",
    "charged twice",
    "double charged",
]


def detect_human_request(query: str) -> bool:
    """Check if the user explicitly requests a human agent."""
    query_lower = query.lower()
    return any(kw in query_lower for kw in ESCALATION_KEYWORDS)


def detect_approval_needed(query: str) -> bool:
    """Check if the query requires approval-level actions."""
    query_lower = query.lower()
    return any(kw in query_lower for kw in APPROVAL_KEYWORDS)


def detect_frustration(query: str) -> bool:
    """Check if the customer is expressing frustration."""
    query_lower = query.lower()
    return any(kw in query_lower for kw in FRUSTRATION_KEYWORDS)


def should_escalate(
    query: str,
    confidence: float,
    threshold: float,
    retrieved_docs: list,
    settings_dict: Optional[dict] = None,
) -> tuple[bool, str]:
    """
    Determine if a query should be escalated to a human agent.
    Returns (should_escalate: bool, reason: str).
    """
    if settings_dict is None:
        settings_dict = db.get_all_settings()

    escalation_enabled = settings_dict.get("escalation_enabled", "true") == "true"
    if not escalation_enabled:
        return False, ""

    # Check each escalation trigger
    if (
        settings_dict.get("escalation_on_user_request", "true") == "true"
        and detect_human_request(query)
    ):
        return True, "Customer requested a human agent"

    if (
        settings_dict.get("escalation_on_no_context", "true") == "true"
        and len(retrieved_docs) == 0
    ):
        return True, "No relevant documents found in knowledge base"

    if (
        settings_dict.get("escalation_on_low_confidence", "true") == "true"
        and confidence < threshold
    ):
        return True, f"Low confidence score ({confidence:.2f} < {threshold:.2f})"

    if (
        settings_dict.get("escalation_on_approval_required", "true") == "true"
        and detect_approval_needed(query)
    ):
        return True, "Query requires approval or involves sensitive actions"

    if detect_frustration(query):
        return True, "Customer frustration detected"

    return False, ""


# ── Ticket Management ────────────────────────────────────────────────

def create_escalation_ticket(
    session_id: str,
    query: str,
    ai_response: str = "",
    transcript: list = None,
    category: str = "general",
    reason: str = "",
) -> str:
    """Create an escalation ticket and return the ticket ID."""
    # Determine priority based on reason
    priority = "normal"
    if "frustration" in reason.lower():
        priority = "high"
    elif "approval" in reason.lower() or "refund" in reason.lower():
        priority = "high"
    elif "human agent" in reason.lower():
        priority = "normal"

    ticket_id = db.create_ticket(
        session_id=session_id,
        query=query,
        ai_response=ai_response,
        transcript=transcript or [],
        category=category,
        priority=priority,
    )
    return ticket_id


def admin_respond(ticket_id: str, response: str) -> bool:
    """Admin responds to an escalated ticket."""
    ticket = db.get_ticket(ticket_id)
    if not ticket:
        return False
    db.respond_to_ticket(ticket_id, response)
    return True


def get_pending_tickets() -> list[dict]:
    """Get all open/pending escalation tickets."""
    return db.get_all_tickets(status="open")


def get_resolved_tickets() -> list[dict]:
    """Get all resolved tickets."""
    return db.get_all_tickets(status="resolved")


def get_ticket_for_session(session_id: str) -> Optional[dict]:
    """Get the latest ticket for a session (if any)."""
    all_tickets = db.get_all_tickets()
    for ticket in all_tickets:
        if ticket["session_id"] == session_id:
            return ticket
    return None


def get_admin_response_for_session(session_id: str) -> Optional[str]:
    """Check if there's an admin response for this session's latest ticket."""
    ticket = get_ticket_for_session(session_id)
    if ticket and ticket["status"] == "resolved" and ticket["admin_response"]:
        return ticket["admin_response"]
    return None
