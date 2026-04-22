"""
RAG-Based Customer Support Assistant
Main Streamlit application entry point.
"""
import streamlit as st
from modules.config import settings
from modules.db import init_db

# ── Page Configuration ───────────────────────────────────────────────
st.set_page_config(
    page_title="Support Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS for Premium UI ────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-primary: #0f0f13;
    --bg-secondary: #1a1a24;
    --bg-card: #22222e;
    --accent: #6c5ce7;
    --accent-hover: #7f70f0;
    --text-primary: #e8e8ed;
    --text-secondary: #9494a8;
    --success: #00d4aa;
    --warning: #ffc107;
    --danger: #ff4757;
    --border: #2d2d3d;
}

.stApp { font-family: 'DM Sans', sans-serif; }

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #13131a 0%, #1a1a28 100%);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .stRadio label {
    font-size: 1rem;
    padding: 0.5rem 0;
}

/* Chat messages */
.stChatMessage { border-radius: 12px; margin-bottom: 0.5rem; }

/* Buttons */
.stButton > button {
    border-radius: 8px;
    font-weight: 500;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(108, 92, 231, 0.3);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0;
    font-weight: 500;
}

/* Metrics */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1e1e2e 0%, #2a2a3e 100%);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem;
}

/* Expanders */
.streamlit-expanderHeader { font-weight: 500; }

/* Progress bars */
.stProgress > div > div { border-radius: 4px; }

/* File uploader */
[data-testid="stFileUploader"] {
    border: 2px dashed var(--border);
    border-radius: 12px;
    padding: 1rem;
}

/* Hide Streamlit branding */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Initialize Database ──────────────────────────────────────────────
init_db()
settings.ensure_directories()

# ── Validate Configuration ───────────────────────────────────────────
errors = settings.validate()
if errors:
    for error in errors:
        st.error(f"⚠️ Configuration Error: {error}")
    st.info("Please check your `.env` file and ensure all required variables are set.")
    st.stop()

# ── Sidebar Navigation ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:1rem 0;">
        <h2 style="margin:0; font-size:1.5rem;">🤖 Support AI</h2>
        <p style="color:#888; font-size:0.8rem; margin:0.2rem 0 0;">RAG-Powered Assistant</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["💬 Customer Chat", "🛡️ Admin Dashboard"],
        label_visibility="collapsed",
        key="nav_radio",
    )

# ── Page Routing ─────────────────────────────────────────────────────
if page == "💬 Customer Chat":
    from modules.ui_customer import render_customer_chat
    render_customer_chat()
elif page == "🛡️ Admin Dashboard":
    from modules.ui_admin import render_admin_dashboard
    render_admin_dashboard()
