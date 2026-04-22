"""Admin dashboard UI component for Streamlit."""
import os, streamlit as st
from modules.config import settings
from modules.ingest import ingest_pdf, reindex_all, get_collection_stats
from modules.hitl import get_pending_tickets, get_resolved_tickets, admin_respond
from modules import db


def render_admin_dashboard():
    """Render the admin dashboard."""
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0 0.5rem;">
        <h1 style="margin:0; font-size:1.8rem;">🛡️ Admin Dashboard</h1>
        <p style="color:#888; font-size:0.9rem; margin:0.3rem 0 0;">Manage knowledge base, settings, and support tickets</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📄 Documents", "⚙️ Settings", "🎫 Tickets", "📊 Stats"])

    with tab1:
        _render_documents_tab()
    with tab2:
        _render_settings_tab()
    with tab3:
        _render_tickets_tab()
    with tab4:
        _render_stats_tab()


def _render_documents_tab():
    st.subheader("Upload PDFs")
    uploaded_files = st.file_uploader("Choose PDF files", type=["pdf"], accept_multiple_files=True, key="pdf_upload")

    if uploaded_files:
        if st.button("📥 Ingest Uploaded PDFs", key="ingest_btn"):
            settings.ensure_directories()
            results = []
            progress = st.progress(0)
            for i, file in enumerate(uploaded_files):
                filepath = os.path.join(settings.UPLOAD_DIR, file.name)
                with open(filepath, "wb") as f:
                    f.write(file.getbuffer())
                with st.spinner(f"Processing {file.name}..."):
                    result = ingest_pdf(filepath)
                    results.append(result)
                progress.progress((i + 1) / len(uploaded_files))
            for r in results:
                if r["status"] == "success":
                    st.success(f"✅ {r['filename']}: {r['num_pages']} pages, {r['num_chunks']} chunks")
                else:
                    st.error(f"❌ {r.get('filename','?')}: {r.get('message','Unknown error')}")

    st.markdown("---")
    st.subheader("Indexed Documents")
    docs = db.get_all_documents()
    if docs:
        for doc in docs:
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.markdown(f"**{doc['filename']}**")
            with col2:
                st.caption(f"{doc['num_pages']} pages · {doc['num_chunks']} chunks · {doc['file_size']//1024}KB")
            with col3:
                st.caption(doc['uploaded_at'][:10])
    else:
        st.info("No documents uploaded yet.")

    st.markdown("---")
    if st.button("🔄 Reindex All Documents", key="reindex_btn"):
        with st.spinner("Reindexing..."):
            result = reindex_all()
        st.success(result["message"])


def _render_settings_tab():
    st.subheader("RAG Settings")
    current = db.get_all_settings()

    col1, col2 = st.columns(2)
    with col1:
        threshold = st.slider("Confidence Threshold", 0.0, 1.0,
                              float(current.get("confidence_threshold", "0.72")), 0.01, key="threshold_slider")
    with col2:
        top_k = st.number_input("Top K Results", 1, 20,
                                int(current.get("top_k", "4")), key="topk_input")

    st.subheader("Escalation Triggers")
    esc_enabled = st.toggle("Enable Escalation System", current.get("escalation_enabled","true")=="true", key="esc_toggle")
    esc_low = st.toggle("Escalate on Low Confidence", current.get("escalation_on_low_confidence","true")=="true", key="esc_low")
    esc_no_ctx = st.toggle("Escalate on No Context", current.get("escalation_on_no_context","true")=="true", key="esc_noctx")
    esc_approval = st.toggle("Escalate on Approval Required", current.get("escalation_on_approval_required","true")=="true", key="esc_approval")
    esc_user = st.toggle("Escalate on User Request", current.get("escalation_on_user_request","true")=="true", key="esc_user")

    if st.button("💾 Save Settings", key="save_settings"):
        db.update_setting("confidence_threshold", str(threshold))
        db.update_setting("top_k", str(top_k))
        db.update_setting("escalation_enabled", str(esc_enabled).lower())
        db.update_setting("escalation_on_low_confidence", str(esc_low).lower())
        db.update_setting("escalation_on_no_context", str(esc_no_ctx).lower())
        db.update_setting("escalation_on_approval_required", str(esc_approval).lower())
        db.update_setting("escalation_on_user_request", str(esc_user).lower())
        st.success("Settings saved!")


def _render_tickets_tab():
    st.subheader("Open Tickets")
    open_tickets = get_pending_tickets()
    if open_tickets:
        for ticket in open_tickets:
            with st.expander(f"🔴 {ticket['id']} — {ticket['query'][:60]}...", expanded=False):
                st.markdown(f"**Query:** {ticket['query']}")
                st.markdown(f"**AI Response:** {ticket['ai_response'][:200]}..." if len(ticket.get('ai_response',''))>200 else f"**AI Response:** {ticket.get('ai_response','N/A')}")
                st.markdown(f"**Priority:** {ticket['priority']} | **Created:** {ticket['created_at'][:16]}")
                st.markdown(f"**Session:** `{ticket['session_id']}`")
                if ticket.get("transcript"):
                    with st.expander("📜 Transcript"):
                        for msg in ticket["transcript"]:
                            st.markdown(f"**{msg['role']}:** {msg['content']}")
                response = st.text_area("Admin Response", key=f"resp_{ticket['id']}")
                if st.button("✅ Send Response", key=f"send_{ticket['id']}"):
                    if response.strip():
                        admin_respond(ticket['id'], response.strip())
                        st.success(f"Response sent for {ticket['id']}!")
                        st.rerun()
                    else:
                        st.warning("Please enter a response.")
    else:
        st.success("No open tickets! 🎉")

    st.markdown("---")
    st.subheader("Resolved Tickets")
    resolved = get_resolved_tickets()
    if resolved:
        for ticket in resolved:
            with st.expander(f"🟢 {ticket['id']} — {ticket['query'][:60]}"):
                st.markdown(f"**Query:** {ticket['query']}")
                st.markdown(f"**Admin Response:** {ticket['admin_response']}")
                st.caption(f"Resolved: {ticket.get('resolved_at','N/A')}")
    else:
        st.info("No resolved tickets yet.")


def _render_stats_tab():
    st.subheader("System Statistics")
    stats = get_collection_stats()
    docs = db.get_all_documents()
    tickets = db.get_all_tickets()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📄 Documents", len(docs))
    with col2:
        st.metric("🧩 Chunks", stats.get("total_chunks", 0))
    with col3:
        st.metric("🎫 Open Tickets", len([t for t in tickets if t["status"]=="open"]))
    with col4:
        st.metric("✅ Resolved", len([t for t in tickets if t["status"]=="resolved"]))

    st.markdown(f"**Vector Store Status:** {stats.get('status','unknown')}")
