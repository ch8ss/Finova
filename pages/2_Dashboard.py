import streamlit as st
from core.auth import sign_out
from core.session import restore_session

if "owner_name" not in st.session_state:
    uid = st.query_params.get("uid")
    if uid:
        restore_session(uid)

# Keep uid in URL so refresh works
if st.session_state.get("user_id"):
    st.query_params["uid"] = st.session_state["user_id"]

st.set_page_config(page_title="Finova · Dashboard", layout="wide")

if "owner_name" not in st.session_state:
    st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a1a0e 0%, #0d2410 50%, #071510 100%) !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif !important;
        color: #e8f4f0 !important;
    }
    [data-testid="stMain"] { background: transparent !important; }
    #MainMenu, footer, header, [data-testid="stToolbar"] { display: none !important; }
    .main .block-container { padding: 6rem 2rem !important; max-width: 420px !important; margin: 0 auto !important; }
    .gate-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    .gate-title { font-size: 1.1rem; font-weight: 600; color: #e8f4f0; margin-bottom: 0.5rem; }
    .gate-sub { font-size: 0.85rem; color: rgba(232,244,240,0.45); margin-bottom: 1.5rem; }
    .stButton > button {
        background: rgba(82,183,136,0.15) !important;
        color: #52b788 !important;
        border: 1px solid rgba(82,183,136,0.35) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        width: 100% !important;
        padding: 0.7rem !important;
        box-shadow: none !important;
    }
    </style>
    <div class="gate-card">
        <div class="gate-title">Sign in required</div>
        <div class="gate-sub">Please sign in to access your dashboard.</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    col = st.columns([1, 2, 1])[1]
    with col:
        if st.button("Go to sign in", key="gate_btn"):
            st.switch_page("app.py")
    st.stop()

owner_name = st.session_state.get("owner_name", "")
business_name = st.session_state.get("business_name", "")
business_type = st.session_state.get("business_type", "")

st.markdown("""<style>
[data-testid="collapsedControl"] { display: none !important; }
section[data-testid="stSidebar"] { transform: none !important; min-width: 240px !important; }
[data-testid="stSidebarNav"] { display: none !important; }
</style>""", unsafe_allow_html=True)

st.markdown("""
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif !important;
    color: #e8f4f0 !important;
}
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > section,
[data-testid="stAppViewContainer"] > section > div {
    background: linear-gradient(135deg, #0a1a0e 0%, #0d2410 50%, #071510 100%) !important;
}
body { background: #0a1a0e !important; }
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: -10%;
    left: -10%;
    width: 50%;
    height: 50%;
    background: radial-gradient(ellipse, rgba(82,183,136,0.1) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}
[data-testid="stMain"] { background: transparent !important; }
#MainMenu, footer, header, [data-testid="stToolbar"] { display: none !important; }
.main .block-container { padding: 2rem 2.5rem 4rem !important; max-width: 1300px !important; position: relative; z-index: 1; }

[data-testid="stSidebar"] {
    background: rgba(10,26,14,0.85) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.04) !important;
    color: rgba(232,244,240,0.7) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    width: 100% !important;
    margin-bottom: 0.4rem !important;
    padding: 0.55rem 1rem !important;
    font-size: 0.87rem !important;
    text-align: left !important;
    box-shadow: none !important;
    transition: all 0.2s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(82,183,136,0.12) !important;
    border-color: rgba(82,183,136,0.3) !important;
    color: #52b788 !important;
    box-shadow: none !important;
    transform: none !important;
}

.page-title {
    font-size: 1.9rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: #e8f4f0;
    margin-bottom: 0.3rem;
}
.page-sub {
    font-size: 0.88rem;
    color: rgba(232,244,240,0.4);
    margin-bottom: 2.5rem;
}

.section-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(82,183,136,0.6);
    margin-bottom: 0.9rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

.metric-card {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.5rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.04);
    transition: all 0.25s;
}
.metric-card:hover {
    border-color: rgba(82,183,136,0.2);
    box-shadow: 0 4px 24px rgba(82,183,136,0.08);
}
.metric-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: rgba(82,183,136,0.6);
    margin-bottom: 0.5rem;
}
.metric-value {
    font-size: 0.9rem;
    color: rgba(232,244,240,0.4);
    line-height: 1.4;
}

.insight-card {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.75rem;
    transition: all 0.2s;
    box-shadow: 0 2px 16px rgba(0,0,0,0.15);
}
.insight-card:hover {
    border-color: rgba(82,183,136,0.2);
    background: rgba(82,183,136,0.04);
}
.insight-title {
    font-size: 0.88rem;
    font-weight: 600;
    color: #e8f4f0;
    margin-bottom: 0.3rem;
}
.insight-body {
    font-size: 0.8rem;
    color: rgba(232,244,240,0.4);
    line-height: 1.6;
}

.stButton > button {
    background: rgba(82,183,136,0.12) !important;
    color: #52b788 !important;
    font-family: inherit !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    border: 1px solid rgba(82,183,136,0.3) !important;
    border-radius: 10px !important;
    padding: 0.65rem 1.2rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
    box-shadow: 0 2px 12px rgba(82,183,136,0.08) !important;
}
.stButton > button:hover {
    background: rgba(82,183,136,0.22) !important;
    border-color: rgba(82,183,136,0.55) !important;
    box-shadow: 0 4px 20px rgba(82,183,136,0.2) !important;
    transform: translateY(-1px) !important;
}

[data-testid="stFileUploaderDropzone"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px dashed rgba(82,183,136,0.2) !important;
    border-radius: 12px !important;
    padding: 1.1rem 1.2rem !important;
    display: flex !important;
    align-items: center !important;
    gap: 1rem !important;
    flex-wrap: wrap !important;
}
[data-testid="stFileUploaderDropzone"] > div {
    flex: 1 !important;
    min-width: 0 !important;
}
[data-testid="stFileUploaderDropzone"] p {
    color: rgba(232,244,240,0.55) !important;
    font-size: 0.82rem !important;
    font-family: inherit !important;
    margin: 0 !important;
}
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] span {
    color: rgba(232,244,240,0.3) !important;
    font-size: 0.72rem !important;
    font-family: inherit !important;
}
[data-testid="stFileUploaderDropzone"] button {
    background: rgba(82,183,136,0.15) !important;
    color: #52b788 !important;
    border: 1px solid rgba(82,183,136,0.35) !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    font-family: inherit !important;
    padding: 0.45rem 1.1rem !important;
    white-space: nowrap !important;
    flex-shrink: 0 !important;
}
[data-testid="stFileUploaderDropzone"] svg {
    color: rgba(232,244,240,0.3) !important;
    width: 16px !important;
    height: 16px !important;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 14px !important;
    padding: 0 !important;
    overflow: hidden !important;
}
[data-testid="stVerticalBlockBorderWrapper"] .stButton > button {
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid rgba(255,255,255,0.04) !important;
    border-radius: 0 !important;
    text-align: left !important;
    color: rgba(232,244,240,0.65) !important;
    font-size: 0.83rem !important;
    font-weight: 400 !important;
    padding: 0.65rem 1.1rem !important;
    width: 100% !important;
    box-shadow: none !important;
    justify-content: flex-start !important;
    margin: 0 !important;
}
[data-testid="stVerticalBlockBorderWrapper"] .stButton > button:hover {
    background: rgba(82,183,136,0.06) !important;
    color: rgba(232,244,240,0.9) !important;
    border-bottom-color: rgba(255,255,255,0.04) !important;
    transform: none !important;
    box-shadow: none !important;
}


[data-testid="stExpander"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
    margin-bottom: 0.5rem !important;
}
[data-testid="stExpander"] summary {
    font-size: 0.86rem !important;
    font-weight: 600 !important;
    color: #e8f4f0 !important;
    padding: 0.75rem 1rem !important;
}
[data-testid="stExpander"] summary:hover { color: #52b788 !important; }
[data-testid="stExpander"] svg { color: rgba(82,183,136,0.5) !important; }
[data-testid="stExpander"] > div:last-child {
    padding: 0.25rem 1rem 1rem !important;
    border-top: 1px solid rgba(255,255,255,0.05) !important;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown(f"""
    <div style="padding: 1.25rem 0 1.75rem;">
        <div style="font-size: 1.15rem; font-weight: 700; color: #e8f4f0; letter-spacing: -0.02em;">Finova</div>
        <div style="font-size: 0.75rem; color: rgba(232,244,240,0.35); margin-top: 0.2rem;">{business_name}</div>
    </div>
    <div style="font-size: 0.65rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: rgba(82,183,136,0.5); margin-bottom: 0.6rem;">Navigation</div>
    """, unsafe_allow_html=True)

    if st.button("Dashboard", key="nav_dash"):
        st.switch_page("pages/2_Dashboard.py")
    if st.button("New CFO Chat", key="nav_chat"):
        st.session_state["messages"] = []
        st.session_state["total_queries"] = 0
        st.switch_page("pages/1_Chat.py")

    st.markdown("""
    <div style="margin: 1.5rem 0; height: 1px; background: rgba(255,255,255,0.05);"></div>
    <div style="font-size: 0.65rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: rgba(82,183,136,0.5); margin-bottom: 0.6rem;">Status</div>
    <div style="font-size: 0.8rem; color: rgba(232,244,240,0.4); margin-bottom: 0.3rem; display:flex; align-items:center; gap:0.5rem;">
        <span style="width:6px;height:6px;border-radius:50%;background:#52b788;box-shadow:0 0 6px #52b788;display:inline-block;"></span>AI Engine Online
    </div>
    <div style="font-size: 0.8rem; color: rgba(232,244,240,0.4); margin-bottom: 0.3rem; display:flex; align-items:center; gap:0.5rem;">
        <span style="width:6px;height:6px;border-radius:50%;background:#52b788;display:inline-block;"></span>Memory Active
    </div>
    <div style="font-size: 0.8rem; color: rgba(232,244,240,0.4); display:flex; align-items:center; gap:0.5rem;">
        <span style="width:6px;height:6px;border-radius:50%;background:#74c69d;display:inline-block;"></span>RAG Ready
    </div>
    <div style="margin: 1.5rem 0; height: 1px; background: rgba(255,255,255,0.05);"></div>
    """, unsafe_allow_html=True)

    if st.button("Log out", key="logout"):
        sign_out()
        st.query_params.clear()
        for k in ["user_id", "owner_name", "business_name", "business_type", "messages", "total_queries", "uploaded_files"]:
            st.session_state.pop(k, None)
        st.switch_page("app.py")

# Main
st.markdown(f"""
<div class="page-title">{business_name}</div>
<div class="page-sub">Welcome back, {owner_name}. {business_type} dashboard.</div>
""", unsafe_allow_html=True)


col_left, col_right = st.columns([1.4, 1], gap="large")

with col_left:
    messages = st.session_state.get("messages", [])
    st.markdown('<div class="section-label">Recent Conversations</div>', unsafe_allow_html=True)

    user_messages = [m for m in messages if m["role"] == "user"]

    if not user_messages:
        st.markdown("""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:14px;text-align:center;padding:2.5rem 1rem;">
            <div style="font-size:0.88rem;font-weight:600;color:rgba(232,244,240,0.3);margin-bottom:0.4rem;">No conversations yet</div>
            <div style="font-size:0.78rem;color:rgba(232,244,240,0.18);">Head to CFO Chat to get started.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.container(border=True):
            for i, msg in enumerate(user_messages):
                text = msg["content"]
                truncated = text if len(text) <= 60 else text[:57] + "..."
                if st.button(f"{i + 1}   {truncated}", key=f"hist_{i}"):
                    st.switch_page("pages/1_Chat.py")

with col_right:
    st.markdown('<div class="section-label">What Finova Can Do</div>', unsafe_allow_html=True)

    with st.expander("Analyse your data"):
        st.markdown("""
        <div class="insight-body" style="margin-bottom:0.6rem;">Upload financial documents and ask questions like:</div>
        <div class="insight-body" style="color:rgba(82,183,136,0.7);font-style:italic;margin-bottom:0.4rem;">"What was my highest revenue month?"</div>
        <div class="insight-body" style="color:rgba(232,244,240,0.55);">→ Your best month was December at $289,000, driven by strong holiday demand.</div>
        """, unsafe_allow_html=True)

    with st.expander("Track patterns"):
        st.markdown("""
        <div class="insight-body" style="margin-bottom:0.6rem;">Finova spots trends and flags anomalies across your history:</div>
        <div class="insight-body" style="color:rgba(82,183,136,0.7);font-style:italic;margin-bottom:0.4rem;">"Are my expenses trending up?"</div>
        <div class="insight-body" style="color:rgba(232,244,240,0.55);">→ Operating expenses rose 63% from Jan to Dec, outpacing revenue growth of 103%. Worth reviewing.</div>
        """, unsafe_allow_html=True)

    with st.expander("Ask about cash flow"):
        st.markdown("""
        <div class="insight-body" style="margin-bottom:0.6rem;">Get plain-English cash flow summaries:</div>
        <div class="insight-body" style="color:rgba(82,183,136,0.7);font-style:italic;margin-bottom:0.4rem;">"Do I have enough cash to hire someone?"</div>
        <div class="insight-body" style="color:rgba(232,244,240,0.55);">→ Your average monthly cash flow is $41,700. A new hire at $3,000/month is well within range.</div>
        """, unsafe_allow_html=True)

    with st.expander("Persistent memory"):
        st.markdown("""
        <div class="insight-body" style="margin-bottom:0.6rem;">Your CFO remembers previous conversations:</div>
        <div class="insight-body" style="color:rgba(82,183,136,0.7);font-style:italic;margin-bottom:0.4rem;">"Last time you said my margins were low — is that still true?"</div>
        <div class="insight-body" style="color:rgba(232,244,240,0.55);">→ Yes, your gross margin is 52%. Industry average for e-commerce is 40–60%, so you're in range but there's room to improve.</div>
        """, unsafe_allow_html=True)
