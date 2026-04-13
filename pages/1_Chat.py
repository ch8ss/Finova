import streamlit as st
import time
from core.chain import ask, process_uploaded_files

st.set_page_config(page_title="Finova · CFO Chat", page_icon="💎", layout="wide")

owner_name = st.session_state.get("owner_name", "User")
business_name = st.session_state.get("business_name", "My Business")
business_type = st.session_state.get("business_type", "Business")

if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "total_queries" not in st.session_state:
    st.session_state["total_queries"] = 0

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=Instrument+Serif:ital@0;1&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }

[data-testid="stAppViewContainer"] { background: #020608 !important; font-family: 'Syne', sans-serif !important; }
[data-testid="stAppViewContainer"] > div {
    background:
        radial-gradient(ellipse 80% 50% at 10% 10%, rgba(0,255,170,0.07) 0%, transparent 55%),
        radial-gradient(ellipse 60% 50% at 90% 90%, rgba(0,180,255,0.06) 0%, transparent 55%),
        #020608 !important;
}
[data-testid="stMain"] { background: transparent !important; }
#MainMenu, footer, header, [data-testid="stToolbar"] { display: none !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: #00ffaa44; border-radius: 2px; }
.main .block-container { padding: 2rem 2.5rem 2rem !important; max-width: 1400px !important; }

[data-testid="stSidebar"] {
    background: rgba(1,8,7,0.98) !important;
    border-right: 1px solid rgba(0,255,170,0.1) !important;
}
[data-testid="stSidebar"] * { color: #e8f4f0 !important; font-family: 'Syne', sans-serif !important; }
[data-testid="stSidebar"] .stButton > button {
    background: rgba(0,255,170,0.07) !important; color: #00ffaa !important;
    border: 1px solid rgba(0,255,170,0.18) !important; border-radius: 10px !important;
    font-weight: 600 !important; width: 100% !important; margin-bottom: 0.4rem !important;
    padding: 0.55rem 1rem !important; font-size: 0.85rem !important;
    transition: all 0.2s ease !important; text-align: left !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(0,255,170,0.14) !important;
    transform: translateX(5px) !important; box-shadow: none !important;
}

.chat-header { padding: 1.2rem 0 1.2rem; animation: fadein 0.7s ease both; }
.chat-title {
    font-size: 1.9rem; font-weight: 800; letter-spacing: -0.03em;
    background: linear-gradient(135deg, #fff 0%, #00ffaa 55%, #00c8ff 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.chat-sub {
    font-family: 'Instrument Serif', serif; font-style: italic;
    font-size: 0.9rem; color: rgba(232,244,240,0.32); margin-top: 0.2rem;
}

.section-label {
    font-family: 'DM Mono', monospace; font-size: 0.58rem;
    letter-spacing: 0.22em; text-transform: uppercase;
    color: rgba(0,255,170,0.45); margin-bottom: 0.75rem;
    display: flex; align-items: center; gap: 0.6rem;
}
.section-label::after { content: ''; flex: 1; height: 1px; background: rgba(0,255,170,0.07); }

.chat-window {
    background: rgba(255,255,255,0.015);
    border: 1px solid rgba(0,255,170,0.09);
    border-radius: 22px; padding: 1.5rem;
    height: 460px; overflow-y: auto; margin-bottom: 1rem;
    scroll-behavior: smooth;
}
.chat-window::-webkit-scrollbar { width: 3px; }
.chat-window::-webkit-scrollbar-thumb { background: rgba(0,255,170,0.2); border-radius: 2px; }

.msg-user {
    display: flex; justify-content: flex-end;
    margin: 0.65rem 0; animation: slideinright 0.3s ease both;
}
.msg-user-bubble {
    background: linear-gradient(135deg, #00b862, #008f4e);
    color: #001a0e; font-size: 0.9rem; font-weight: 600;
    padding: 0.85rem 1.15rem; border-radius: 18px 18px 4px 18px;
    max-width: 68%; line-height: 1.55;
    box-shadow: 0 4px 18px rgba(0,180,100,0.22);
}
.msg-ai {
    display: flex; align-items: flex-start; gap: 0.65rem;
    margin: 0.65rem 0; animation: slideinleft 0.3s ease both;
}
.msg-avatar {
    width: 36px; height: 36px; min-width: 36px;
    background: linear-gradient(135deg, #00ffaa, #00c8ff);
    border-radius: 11px; display: flex; align-items: center;
    justify-content: center; font-size: 0.95rem;
    box-shadow: 0 0 18px rgba(0,255,170,0.22);
}
.msg-ai-content { max-width: 74%; }
.msg-ai-name {
    font-family: 'DM Mono', monospace; font-size: 0.55rem;
    letter-spacing: 0.14em; text-transform: uppercase;
    color: #00ffaa; margin-bottom: 0.28rem;
}
.msg-ai-bubble {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(0,255,170,0.11);
    color: #e8f4f0; font-size: 0.89rem; line-height: 1.7;
    padding: 0.85rem 1.15rem; border-radius: 4px 18px 18px 18px;
}

.empty-chat {
    display: flex; flex-direction: column; align-items: center;
    justify-content: center; height: 100%; gap: 1.2rem; text-align: center;
}
.empty-icon { font-size: 3.2rem; animation: float 3.5s ease-in-out infinite; display: block; }
.empty-title { font-size: 1.05rem; font-weight: 700; color: rgba(232,244,240,0.4); }
.empty-hint {
    font-family: 'DM Mono', monospace; font-size: 0.68rem;
    color: rgba(232,244,240,0.18); line-height: 1.7; letter-spacing: 0.04em;
}
.empty-example {
    font-family: 'DM Mono', monospace; font-size: 0.7rem;
    color: rgba(0,255,170,0.35); background: rgba(0,255,170,0.05);
    border: 1px solid rgba(0,255,170,0.12); border-radius: 8px;
    padding: 0.5rem 1rem; margin-top: 0.25rem;
}

.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(0,255,170,0.18) !important;
    border-radius: 14px !important; color: #e8f4f0 !important;
    font-family: 'Syne', sans-serif !important; font-size: 0.93rem !important;
    padding: 0.82rem 1.2rem !important; transition: all 0.25s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(0,255,170,0.45) !important;
    box-shadow: 0 0 0 3px rgba(0,255,170,0.07) !important;
    background: rgba(0,255,170,0.025) !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(232,244,240,0.18) !important; }

.stButton > button {
    background: linear-gradient(135deg, #00ffaa, #00c8ff) !important;
    color: #020608 !important; font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important; border: none !important;
    border-radius: 12px !important; padding: 0.72rem 1.2rem !important;
    width: 100% !important; transition: all 0.25s ease !important;
    box-shadow: 0 4px 15px rgba(0,255,170,0.15) !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 28px rgba(0,255,170,0.3) !important; }

[data-testid="stFileUploader"] * { color: #e8f4f0 !important; }
[data-testid="stFileUploader"] section {
    background: rgba(255,255,255,0.02) !important;
    border: 1px dashed rgba(0,255,170,0.18) !important; border-radius: 12px !important;
}

@keyframes fadein { from { opacity:0; transform:translateY(12px); } to { opacity:1; transform:translateY(0); } }
@keyframes slideinright { from { opacity:0; transform:translateX(18px); } to { opacity:1; transform:translateX(0); } }
@keyframes slideinleft { from { opacity:0; transform:translateX(-18px); } to { opacity:1; transform:translateX(0); } }
@keyframes float { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-9px); } }
@keyframes blink { 0%,100% { opacity:1; } 50% { opacity:0.2; } }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    queries = st.session_state.get("total_queries", 0)
    st.markdown(f"""
    <div style="padding:0.75rem 0 1.5rem;">
        <div style="font-size:1.6rem;font-weight:800;
            background:linear-gradient(135deg,#00ffaa,#00c8ff);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
            letter-spacing:-0.02em;">💎 Finova</div>
        <div style="font-family:'DM Mono',monospace;font-size:0.55rem;letter-spacing:0.18em;
            color:rgba(232,244,240,0.25);text-transform:uppercase;margin-top:0.25rem;">
            AI Chief Financial Officer</div>
    </div>
    <div style="background:rgba(0,255,170,0.05);border:1px solid rgba(0,255,170,0.12);
        border-radius:14px;padding:1rem;margin-bottom:1.2rem;">
        <div style="font-family:'DM Mono',monospace;font-size:0.55rem;letter-spacing:0.15em;
            text-transform:uppercase;color:rgba(0,255,170,0.4);margin-bottom:0.5rem;">Active Session</div>
        <div style="font-size:0.95rem;font-weight:700;color:#e8f4f0;margin-bottom:0.1rem;">{owner_name}</div>
        <div style="font-family:'DM Mono',monospace;font-size:0.68rem;color:rgba(232,244,240,0.3);">
            {business_name}</div>
        <div style="font-family:'DM Mono',monospace;font-size:0.62rem;color:rgba(0,255,170,0.4);margin-top:0.5rem;">
            Queries: {queries}</div>
    </div>
    <div style="font-family:'DM Mono',monospace;font-size:0.55rem;letter-spacing:0.18em;
        text-transform:uppercase;color:rgba(0,255,170,0.35);margin-bottom:0.6rem;">Navigation</div>
    """, unsafe_allow_html=True)

    if st.button("📊  Dashboard", key="nav_dash"):
        st.switch_page("pages/2_Dashboard.py")
    if st.button("💬  CFO Chat", key="nav_chat"):
        st.switch_page("pages/1_Chat.py")

    st.markdown("""
    <div style="margin:1.2rem 0;height:1px;background:rgba(0,255,170,0.07);"></div>
    <div style="font-family:'DM Mono',monospace;font-size:0.55rem;letter-spacing:0.18em;
        text-transform:uppercase;color:rgba(0,255,170,0.35);margin-bottom:0.75rem;">Upload Files</div>
    """, unsafe_allow_html=True)

    sidebar_upload = st.file_uploader(
        "Docs",
        type=["pdf","csv","xlsx"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        key="sidebar_upload"
    )
    if sidebar_upload:
        if st.session_state.get("uploaded_files") != sidebar_upload:
            st.session_state["uploaded_files"] = sidebar_upload
            with st.spinner("Processing files..."):
                process_uploaded_files(sidebar_upload)
        for f in sidebar_upload:
            st.success(f"✓ {f.name}")

    st.markdown("""
    <div style="margin:1.2rem 0;height:1px;background:rgba(0,255,170,0.07);"></div>
    <div style="font-family:'DM Mono',monospace;font-size:0.55rem;letter-spacing:0.18em;
        text-transform:uppercase;color:rgba(0,255,170,0.35);margin-bottom:0.75rem;">System</div>
    <div style="font-size:0.8rem;color:rgba(232,244,240,0.4);margin-bottom:0.35rem;display:flex;align-items:center;gap:0.5rem;">
        <span style="width:7px;height:7px;border-radius:50%;background:#00ffaa;box-shadow:0 0 8px #00ffaa;display:inline-block;animation:blink 2s infinite;"></span>AI Engine Online
    </div>
    <div style="font-size:0.8rem;color:rgba(232,244,240,0.4);margin-bottom:0.35rem;display:flex;align-items:center;gap:0.5rem;">
        <span style="width:7px;height:7px;border-radius:50%;background:#00ffaa;box-shadow:0 0 8px #00ffaa;display:inline-block;"></span>Memory Active
    </div>
    <div style="font-size:0.8rem;color:rgba(232,244,240,0.4);display:flex;align-items:center;gap:0.5rem;">
        <span style="width:7px;height:7px;border-radius:50%;background:#00c8ff;box-shadow:0 0 8px #00c8ff;display:inline-block;"></span>RAG Ready
    </div>
    <div style="margin:1.2rem 0;height:1px;background:rgba(0,255,170,0.07);"></div>
    """, unsafe_allow_html=True)

    if st.button("🗑️  Clear Chat", key="clear"):
        st.session_state["messages"] = []
        st.session_state["total_queries"] = 0
        st.rerun()

    if st.button("🚪  Logout", key="logout"):
        for k in ["owner_name","business_name","business_type","messages","total_queries","uploaded_files"]:
            st.session_state.pop(k, None)
        st.switch_page("app.py")

# ── Main Chat ──
st.markdown(f"""
<div class="chat-header">
    <div class="chat-title">💬 CFO Chat</div>
    <div class="chat-sub">Ask {business_name}'s AI CFO anything about your finances — in plain English</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Conversation</div>', unsafe_allow_html=True)

# Build chat window
messages = st.session_state.get("messages", [])
chat_html = '<div class="chat-window">'

if not messages:
    chat_html += f"""
    <div class="empty-chat">
        <span class="empty-icon">💎</span>
        <div class="empty-title">Hello, {owner_name}! I am your AI CFO.</div>
        <div class="empty-hint">
            Upload your financial documents from the sidebar,<br>
            then ask me anything about {business_name}.
        </div>
        <div class="empty-example">Try: "What are my biggest expense risks?"</div>
        <div class="empty-example">Try: "How can I improve my cash flow?"</div>
        <div class="empty-example">Try: "Analyse my revenue trends"</div>
    </div>"""
else:
    for msg in messages:
        if msg["role"] == "user":
            chat_html += f"""
            <div class="msg-user">
                <div class="msg-user-bubble">{msg['content']}</div>
            </div>"""
        else:
            chat_html += f"""
            <div class="msg-ai">
                <div class="msg-avatar">💎</div>
                <div class="msg-ai-content">
                    <div class="msg-ai-name">Finova CFO · {business_name}</div>
                    <div class="msg-ai-bubble">{msg['content']}</div>
                </div>
            </div>"""

chat_html += '</div>'
st.markdown(chat_html, unsafe_allow_html=True)

# Suggestions
st.markdown('<div class="section-label">Suggested Questions</div>', unsafe_allow_html=True)
suggestions = [
    "📊 Analyse my revenue",
    "💸 Where am I losing money?",
    "🎯 Top cost-cutting ideas",
    "📈 Forecast next quarter",
    "⚠️ Flag financial risks",
    "🕵️ Hidden insights",
]
sug_cols = st.columns(6)
selected = None
for i, (col, sug) in enumerate(zip(sug_cols, suggestions)):
    with col:
        if st.button(sug, key=f"sug_{i}"):
            selected = sug

# Input
st.markdown('<div class="section-label" style="margin-top:0.85rem;">Your Message</div>', unsafe_allow_html=True)
c1, c2 = st.columns([5, 1])
with c1:
    user_input = st.text_input(
        "msg",
        placeholder=f"Ask your CFO about {business_name}...",
        label_visibility="collapsed",
        key="chat_input"
    )
with c2:
    send = st.button("Send →", key="send_btn")

if selected:
    user_input = selected
    send = True

if send and user_input and user_input.strip():
    st.session_state["messages"].append({"role": "user", "content": user_input.strip()})
    st.session_state["total_queries"] = st.session_state.get("total_queries", 0) + 1

    with st.spinner("Your CFO is analysing..."):
        session_id = business_name.lower().replace(" ", "_")
        reply = ask(user_input.strip(), session_id)

    st.session_state["messages"].append({"role": "assistant", "content": reply})
    st.rerun()

st.markdown("""
<div style="margin-top:2rem;text-align:center;font-family:'DM Mono',monospace;
    font-size:0.52rem;letter-spacing:0.2em;color:rgba(232,244,240,0.07);">
    FINOVA · AI CFO · TYPE "finova" FOR A SURPRISE · BUILT WITH ♥️
</div>
""", unsafe_allow_html=True)
