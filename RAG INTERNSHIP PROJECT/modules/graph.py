"""
LangGraph workflow orchestration for the RAG customer support pipeline.
Nodes: input, retrieve, generate, decision, output, escalate, human_response
Routes: confident->output, low_confidence/no_context/approval/human_request->escalate
"""
import json, os
from typing import Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from modules.config import settings
from modules.retriever import retrieve_documents, format_context, format_sources, has_documents
from modules.prompts import RAG_PROMPT
from modules.hitl import should_escalate, create_escalation_ticket, detect_human_request, get_admin_response_for_session
from modules import db

class GraphState(TypedDict):
    query: str
    session_id: str
    retrieved_docs: list
    context: str
    answer: str
    confidence: float
    route: str
    sources: list
    ticket_id: str
    escalation_reason: str
    error: str
    intent: str
    admin_response: str

def get_llm(temperature=0):
    return ChatGroq(model=settings.MODEL_NAME, temperature=temperature, api_key=settings.GROQ_API_KEY, max_retries=2)

def get_fallback_llm(temperature=0):
    return ChatGroq(model=settings.FALLBACK_MODEL, temperature=temperature, api_key=settings.GROQ_API_KEY, max_retries=2)

def input_node(state: GraphState) -> dict:
    query = state.get("query", "").strip()
    if not query:
        return {"route": "error", "error": "Empty query", "answer": "Please enter a question so I can help you."}
    if detect_human_request(query):
        return {"query": query, "route": "user_requested_human"}
    return {"query": query, "route": "retrieve"}

def retrieve_node(state: GraphState) -> dict:
    query = state.get("query", "")
    if not has_documents():
        return {"retrieved_docs": [], "context": "", "sources": [], "route": "no_context"}
    app_settings = db.get_all_settings()
    top_k = int(app_settings.get("top_k", settings.TOP_K))
    docs = retrieve_documents(query, top_k=top_k)
    if not docs:
        return {"retrieved_docs": [], "context": "", "sources": [], "route": "no_context"}
    return {"retrieved_docs": docs, "context": format_context(docs), "sources": format_sources(docs)}

def generate_node(state: GraphState) -> dict:
    query, context = state.get("query", ""), state.get("context", "")
    try:
        answer = (RAG_PROMPT | get_llm() | StrOutputParser()).invoke({"query": query, "context": context})
    except Exception:
        try:
            answer = (RAG_PROMPT | get_fallback_llm() | StrOutputParser()).invoke({"query": query, "context": context})
        except Exception as e2:
            return {"answer": "I'm having trouble generating a response. Please try again or request a human agent.",
                    "confidence": 0.0, "error": str(e2), "route": "escalate", "escalation_reason": "LLM failure"}
    return {"answer": answer}

def _calc_confidence(query, context, answer, retrieved_docs):
    if not retrieved_docs:
        return 0.0
    scores = [d.get("score", 0) for d in retrieved_docs]
    avg = sum(scores) / len(scores) if scores else 0.0
    uncertainty = ["i don't have enough information", "i'm not sure", "i cannot find", "not in our knowledge base"]
    penalty = 0.3 if any(p in answer.lower() for p in uncertainty) else 0.0
    bonus = min(0.1, len(retrieved_docs) * 0.025)
    return round(min(1.0, max(0.0, avg - penalty + bonus)), 3)

def decision_node(state: GraphState) -> dict:
    query, context, answer = state.get("query",""), state.get("context",""), state.get("answer","")
    retrieved_docs = state.get("retrieved_docs", [])
    app_settings = db.get_all_settings()
    threshold = float(app_settings.get("confidence_threshold", settings.CONFIDENCE_THRESHOLD))
    confidence = _calc_confidence(query, context, answer, retrieved_docs)
    esc, reason = should_escalate(query, confidence, threshold, retrieved_docs, app_settings)
    if esc:
        return {"confidence": confidence, "route": "escalate", "escalation_reason": reason}
    return {"confidence": confidence, "route": "output"}

def output_node(state: GraphState) -> dict:
    return {"route": "complete"}

def escalate_node(state: GraphState) -> dict:
    session_id = state.get("session_id", "unknown")
    query, answer = state.get("query",""), state.get("answer","")
    reason = state.get("escalation_reason", "Escalation triggered")
    transcript = [{"role":"customer","content":query}, {"role":"ai","content":answer}, {"role":"system","content":f"Escalated: {reason}"}]
    ticket_id = create_escalation_ticket(session_id=session_id, query=query, ai_response=answer, transcript=transcript, category="escalation", reason=reason)
    msg = f"I've escalated your query to our support team. Your ticket ID is **{ticket_id}**. A human agent will review your case shortly.\n\n_Reason: {reason}_"
    full = f"{answer}\n\n---\n\n🎫 **Escalated to Human Support**\n\n{msg}" if answer else f"🎫 **Escalated to Human Support**\n\n{msg}"
    return {"ticket_id": ticket_id, "answer": full, "route": "escalated"}

def human_response_node(state: GraphState) -> dict:
    session_id = state.get("session_id", "unknown")
    resp = get_admin_response_for_session(session_id)
    if resp:
        return {"admin_response": resp, "answer": f"💬 **Response from our support team:**\n\n{resp}", "route": "complete"}
    return {"route": "waiting"}

def route_after_input(state: GraphState) -> Literal["retrieve_node", "escalate_node", "__end__"]:
    r = state.get("route", "retrieve")
    if r == "user_requested_human": return "escalate_node"
    if r == "error": return END
    return "retrieve_node"

def route_after_retrieve(state: GraphState) -> Literal["generate_node", "escalate_node"]:
    return "escalate_node" if state.get("route") == "no_context" else "generate_node"

def route_after_decision(state: GraphState) -> Literal["output_node", "escalate_node"]:
    return "escalate_node" if state.get("route") == "escalate" else "output_node"

def build_graph():
    wf = StateGraph(GraphState)
    wf.add_node("input_node", input_node)
    wf.add_node("retrieve_node", retrieve_node)
    wf.add_node("generate_node", generate_node)
    wf.add_node("decision_node", decision_node)
    wf.add_node("output_node", output_node)
    wf.add_node("escalate_node", escalate_node)
    wf.add_node("human_response_node", human_response_node)
    wf.add_edge(START, "input_node")
    wf.add_conditional_edges("input_node", route_after_input, ["retrieve_node", "escalate_node", END])
    wf.add_conditional_edges("retrieve_node", route_after_retrieve, ["generate_node", "escalate_node"])
    wf.add_edge("generate_node", "decision_node")
    wf.add_conditional_edges("decision_node", route_after_decision, ["output_node", "escalate_node"])
    wf.add_edge("output_node", END)
    wf.add_edge("escalate_node", END)
    wf.add_edge("human_response_node", END)
    return wf.compile()

def run_query(query: str, session_id: str = "default") -> dict:
    graph = build_graph()
    initial = {"query": query, "session_id": session_id, "retrieved_docs": [], "context": "", "answer": "",
               "confidence": 0.0, "route": "", "sources": [], "ticket_id": "", "escalation_reason": "",
               "error": "", "intent": "", "admin_response": ""}
    return graph.invoke(initial)

def check_for_admin_response(session_id: str) -> dict:
    return human_response_node({"query":"","session_id":session_id,"retrieved_docs":[],"context":"","answer":"",
                                 "confidence":0.0,"route":"","sources":[],"ticket_id":"","escalation_reason":"",
                                 "error":"","intent":"","admin_response":""})
