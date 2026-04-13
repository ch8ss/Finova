import streamlit as st
from core.chain import ask, process_uploaded_files

st.set_page_config(page_title="Finova · Chat", layout="wide")

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
        <div class="gate-sub">Please sign in to access your CFO chat.</div>
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

if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "total_queries" not in st.session_state:
    st.session_state["total_queries"] = 0
if "input_key" not in st.session_state:
    st.session_state["input_key"] = 0

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
    bottom: -10%;
    right: -10%;
    width: 50%;
    height: 50%;
    background: radial-gradient(ellipse, rgba(82,183,136,0.08) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}
[data-testid="stMain"] { background: transparent !important; }
#MainMenu, footer, header, [data-testid="stToolbar"] { display: none !important; }
.main .block-container { padding: 2rem 2.5rem 2rem !important; max-width: 1300px !important; position: relative; z-index: 1; }

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
    font-size: 1.6rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: #e8f4f0;
    margin-bottom: 0.3rem;
}
.page-sub {
    font-size: 0.86rem;
    color: rgba(232,244,240,0.4);
    margin-bottom: 1.75rem;
}

.section-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(82,183,136,0.6);
    margin-bottom: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

.chat-window {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.75rem;
    height: 460px;
    overflow-y: auto;
    margin-bottom: 1.25rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.04);
}
.chat-window::-webkit-scrollbar { width: 3px; }
.chat-window::-webkit-scrollbar-thumb { background: rgba(82,183,136,0.2); border-radius: 2px; }

.msg-row-user {
    display: flex;
    justify-content: flex-end;
    margin: 0.75rem 0;
}
.msg-bubble-user {
    background: rgba(82,183,136,0.2);
    border: 1px solid rgba(82,183,136,0.3);
    color: #e8f4f0;
    font-size: 0.9rem;
    padding: 0.75rem 1.1rem;
    border-radius: 14px 14px 3px 14px;
    max-width: 65%;
    line-height: 1.55;
    backdrop-filter: blur(10px);
}
.msg-row-ai {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    margin: 0.75rem 0;
}
.msg-avatar {
    width: 30px;
    height: 30px;
    min-width: 30px;
    background: rgba(82,183,136,0.2);
    border: 1px solid rgba(82,183,136,0.3);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #52b788;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.02em;
    backdrop-filter: blur(10px);
}
.msg-ai-inner { max-width: 70%; }
.msg-ai-name {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: rgba(82,183,136,0.6);
    margin-bottom: 0.3rem;
}
.msg-bubble-ai {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.08);
    color: #e8f4f0;
    font-size: 0.9rem;
    line-height: 1.65;
    padding: 0.75rem 1.1rem;
    border-radius: 3px 14px 14px 14px;
}

.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    text-align: center;
    gap: 0.75rem;
}
.empty-title { font-size: 1rem; font-weight: 600; color: rgba(232,244,240,0.4); }
.empty-hint { font-size: 0.8rem; color: rgba(232,244,240,0.22); line-height: 1.6; max-width: 300px; }

.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e8f4f0 !important;
    font-family: inherit !important;
    font-size: 0.93rem !important;
    padding: 0.78rem 1rem !important;
    box-shadow: none !important;
    transition: all 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(82,183,136,0.45) !important;
    box-shadow: 0 0 0 3px rgba(82,183,136,0.08) !important;
    background: rgba(82,183,136,0.04) !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(232,244,240,0.2) !important; }
.stTextInput label { display: none !important; }

.stButton > button {
    background: rgba(82,183,136,0.12) !important;
    color: #52b788 !important;
    font-family: inherit !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    border: 1px solid rgba(82,183,136,0.3) !important;
    border-radius: 10px !important;
    padding: 0.75rem 1.2rem !important;
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
    border-radius: 10px !important;
    padding: 0.9rem 1rem !important;
    display: flex !important;
    align-items: center !important;
    gap: 0.75rem !important;
    flex-wrap: wrap !important;
}
[data-testid="stFileUploaderDropzone"] > div {
    flex: 1 !important;
    min-width: 0 !important;
}
[data-testid="stFileUploaderDropzone"] p {
    color: rgba(232,244,240,0.5) !important;
    font-size: 0.8rem !important;
    font-family: inherit !important;
    margin: 0 !important;
}
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] span {
    color: rgba(232,244,240,0.28) !important;
    font-size: 0.7rem !important;
    font-family: inherit !important;
}
[data-testid="stFileUploaderDropzone"] button {
    background: rgba(82,183,136,0.15) !important;
    color: #52b788 !important;
    border: 1px solid rgba(82,183,136,0.35) !important;
    border-radius: 8px !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    font-family: inherit !important;
    padding: 0.42rem 1rem !important;
    white-space: nowrap !important;
    flex-shrink: 0 !important;
}
[data-testid="stFileUploaderDropzone"] svg {
    color: rgba(232,244,240,0.25) !important;
    width: 15px !important;
    height: 15px !important;
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
    if st.button("CFO Chat", key="nav_chat"):
        st.switch_page("pages/1_Chat.py")

    st.markdown("""
    <div style="margin: 1.5rem 0; height: 1px; background: rgba(255,255,255,0.05);"></div>
    <div style="font-size: 0.65rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: rgba(82,183,136,0.5); margin-bottom: 0.75rem;">Upload Files</div>
    """, unsafe_allow_html=True)

    sidebar_upload = st.file_uploader(
        "Docs",
        type=["pdf", "csv", "xlsx"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        key="sidebar_upload"
    )
    if sidebar_upload:
        if st.session_state.get("uploaded_files") != sidebar_upload:
            st.session_state["uploaded_files"] = sidebar_upload
            with st.spinner("Processing..."):
                process_uploaded_files(sidebar_upload)
        files_html = "".join(f'<div style="font-size:0.75rem;color:#52b788;padding:0.3rem 0;border-bottom:1px solid rgba(255,255,255,0.05);">&#10003; {f.name}</div>' for f in sidebar_upload)
        st.markdown(f'<div style="margin-top:0.5rem;">{files_html}</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="margin: 1.5rem 0; height: 1px; background: rgba(255,255,255,0.05);"></div>
    <div style="font-size: 0.65rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: rgba(82,183,136,0.5); margin-bottom: 0.5rem;">Status</div>
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

    queries = st.session_state.get("total_queries", 0)
    st.markdown(f'<div style="font-size:0.75rem;color:rgba(232,244,240,0.25);margin-bottom:1rem;">Queries this session: {queries}</div>', unsafe_allow_html=True)

    if st.button("Clear chat", key="clear"):
        st.session_state["messages"] = []
        st.session_state["total_queries"] = 0
        st.rerun()

    if st.button("Log out", key="logout"):
        for k in ["owner_name", "business_name", "business_type", "messages", "total_queries", "uploaded_files"]:
            st.session_state.pop(k, None)
        st.switch_page("app.py")

# Main
st.markdown(f"""
<div class="page-title">CFO Chat</div>
<div class="page-sub">Ask anything about {business_name}'s finances in plain English.</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Conversation</div>', unsafe_allow_html=True)

messages = st.session_state.get("messages", [])
chat_html = '<div class="chat-window">'

if not messages:
    chat_html += f"""
    <div class="empty-state">
        <div class="empty-title">Hello, {owner_name}.</div>
        <div class="empty-hint">Upload your financial documents from the sidebar, then ask me anything about {business_name}.</div>
    </div>"""
else:
    for msg in messages:
        if msg["role"] == "user":
            chat_html += f"""
            <div class="msg-row-user">
                <div class="msg-bubble-user">{msg['content']}</div>
            </div>"""
        else:
            chat_html += f"""
            <div class="msg-row-ai">
                <div class="msg-avatar">CFO</div>
                <div class="msg-ai-inner">
                    <div class="msg-ai-name">Finova · {business_name}</div>
                    <div class="msg-bubble-ai">{msg['content']}</div>
                </div>
            </div>"""

chat_html += '</div>'
st.markdown(chat_html, unsafe_allow_html=True)

st.markdown('<div class="section-label">Your message</div>', unsafe_allow_html=True)
c1, c2 = st.columns([5, 1])
with c1:
    user_input = st.text_input("msg", placeholder=f"Ask about {business_name}...", label_visibility="collapsed", key=f"chat_input_{st.session_state['input_key']}")
with c2:
    send = st.button("Send", key="send_btn")

if send and user_input and user_input.strip():
    st.session_state["messages"].append({"role": "user", "content": user_input.strip()})
    st.session_state["total_queries"] = st.session_state.get("total_queries", 0) + 1
    st.session_state["input_key"] += 1

    session_id = business_name.lower().replace(" ", "_")
    with st.spinner("Thinking..."):
        reply = ask(user_input.strip(), session_id)

    st.session_state["messages"].append({"role": "assistant", "content": reply})
    st.rerun()
