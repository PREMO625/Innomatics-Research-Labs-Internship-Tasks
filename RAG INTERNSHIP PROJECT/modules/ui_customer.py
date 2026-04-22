"""Customer chat UI component for Streamlit."""
import streamlit as st
from modules.graph import run_query, check_for_admin_response
from modules.hitl import get_ticket_for_session
from modules import db


def render_customer_chat():
    """Render the customer chat interface."""
    # Session state initialization
    if "session_id" not in st.session_state:
        st.session_state.session_id = db.create_session()
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "escalated" not in st.session_state:
        st.session_state.escalated = False

    # Header
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 0.5rem;">
        <h1 style="margin:0; font-size:1.8rem;">💬 Customer Support</h1>
        <p style="color:#888; font-size:0.9rem; margin:0.3rem 0 0;">Ask anything about our products and services</p>
    </div>
    """, unsafe_allow_html=True)

    # Check for admin response
    ticket = get_ticket_for_session(st.session_state.session_id)
    if ticket and ticket["status"] == "resolved" and ticket.get("admin_response"):
        if not any(m.get("is_admin_response") for m in st.session_state.messages):
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"💬 **Response from our support team:**\n\n{ticket['admin_response']}",
                "is_admin_response": True,
            })
            st.session_state.escalated = False

    # Display ticket status if escalated
    if ticket and ticket["status"] == "open":
        st.info(f"🎫 Your ticket **{ticket['id']}** is being reviewed by our support team. You'll see a response here once an agent replies.")

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources"):
                with st.expander("📚 Sources"):
                    for src in msg["sources"]:
                        st.markdown(f"- {src}")
            if msg.get("confidence") is not None and msg["role"] == "assistant" and not msg.get("is_admin_response"):
                conf = msg["confidence"]
                color = "#22c55e" if conf >= 0.7 else "#eab308" if conf >= 0.5 else "#ef4444"
                st.markdown(f'<span style="color:{color}; font-size:0.75rem;">Confidence: {conf:.0%}</span>', unsafe_allow_html=True)

    # Chat input
    if prompt := st.chat_input("Type your question here...", key="customer_input"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Process query
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = run_query(prompt, st.session_state.session_id)

            answer = result.get("answer", "Sorry, I couldn't process your request.")
            sources = result.get("sources", [])
            confidence = result.get("confidence", 0.0)
            ticket_id = result.get("ticket_id", "")

            st.markdown(answer)
            if sources:
                with st.expander("📚 Sources"):
                    for src in sources:
                        st.markdown(f"- {src}")
            if confidence > 0:
                color = "#22c55e" if confidence >= 0.7 else "#eab308" if confidence >= 0.5 else "#ef4444"
                st.markdown(f'<span style="color:{color}; font-size:0.75rem;">Confidence: {confidence:.0%}</span>', unsafe_allow_html=True)

            if ticket_id:
                st.session_state.escalated = True

        # Save assistant message
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": sources,
            "confidence": confidence,
        })

    # Sidebar session info
    with st.sidebar:
        st.markdown("---")
        st.caption(f"Session: `{st.session_state.session_id}`")
        if st.button("🔄 New Conversation", key="new_conv"):
            st.session_state.session_id = db.create_session()
            st.session_state.messages = []
            st.session_state.escalated = False
            st.rerun()
