import streamlit as st

st.set_page_config(page_title="Finova · Dashboard", page_icon="💎", layout="wide")

owner_name = st.session_state.get("owner_name", "User")
business_name = st.session_state.get("business_name", "My Business")
business_type = st.session_state.get("business_type", "Business")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=Instrument+Serif:ital@0;1&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }

[data-testid="stAppViewContainer"] { background: #020608 !important; font-family: 'Syne', sans-serif !important; }
[data-testid="stAppViewContainer"] > div {
    background:
        radial-gradient(ellipse 80% 50% at 10% 10%, rgba(0,255,170,0.08) 0%, transparent 55%),
        radial-gradient(ellipse 60% 50% at 90% 90%, rgba(0,180,255,0.07) 0%, transparent 55%),
        #020608 !important;
}
[data-testid="stMain"] { background: transparent !important; }
#MainMenu, footer, header, [data-testid="stToolbar"] { display: none !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: #00ffaa44; border-radius: 2px; }
.main .block-container { padding: 2rem 2.5rem 4rem !important; max-width: 1400px !important; }

[data-testid="stSidebar"] {
    background: rgba(1, 8, 7, 0.98) !important;
    border-right: 1px solid rgba(0,255,170,0.1) !important;
}
[data-testid="stSidebar"] * { color: #e8f4f0 !important; font-family: 'Syne', sans-serif !important; }
[data-testid="stSidebar"] .stButton > button {
    background: rgba(0,255,170,0.07) !important;
    color: #00ffaa !important;
    border: 1px solid rgba(0,255,170,0.18) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    width: 100% !important;
    margin-bottom: 0.4rem !important;
    padding: 0.55rem 1rem !important;
    font-size: 0.85rem !important;
    transition: all 0.2s ease !important;
    text-align: left !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(0,255,170,0.14) !important;
    transform: translateX(5px) !important;
    box-shadow: none !important;
}

.page-header { padding: 1.5rem 0 2rem; animation: fadein 0.7s ease both; }
.page-greeting {
    font-family: 'DM Mono', monospace; font-size: 0.65rem;
    letter-spacing: 0.18em; text-transform: uppercase;
    color: rgba(0,255,170,0.5); margin-bottom: 0.4rem;
}
.page-title {
    font-size: 2.4rem; font-weight: 800; letter-spacing: -0.03em; line-height: 1.05;
    background: linear-gradient(135deg, #fff 0%, #00ffaa 55%, #00c8ff 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.page-sub {
    font-family: 'Instrument Serif', serif; font-style: italic;
    font-size: 0.95rem; color: rgba(232,244,240,0.35); margin-top: 0.3rem;
}
.live-pill {
    display: inline-flex; align-items: center; gap: 0.4rem;
    font-family: 'DM Mono', monospace; font-size: 0.6rem; letter-spacing: 0.1em;
    color: #00ffaa; background: rgba(0,255,170,0.08);
    border: 1px solid rgba(0,255,170,0.2); padding: 0.28rem 0.8rem;
    border-radius: 100px; margin-top: 0.75rem;
}
.live-dot { width: 6px; height: 6px; border-radius: 50%; background: #00ffaa; animation: blink 2s infinite; }

.section-label {
    font-family: 'DM Mono', monospace; font-size: 0.58rem;
    letter-spacing: 0.22em; text-transform: uppercase;
    color: rgba(0,255,170,0.45); margin-bottom: 0.9rem;
    display: flex; align-items: center; gap: 0.6rem;
}
.section-label::after { content: ''; flex: 1; height: 1px; background: rgba(0,255,170,0.07); }

.metrics-grid {
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;
    margin-bottom: 2rem; animation: fadein 0.85s ease 0.1s both;
}
.metric-card {
    background: rgba(255,255,255,0.025); border: 1px solid rgba(0,255,170,0.09);
    border-radius: 20px; padding: 1.5rem 1.4rem; position: relative;
    overflow: hidden; transition: all 0.3s ease; cursor: default;
}
.metric-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, #00ffaa, #00c8ff); opacity: 0; transition: opacity 0.3s;
}
.metric-card:hover { border-color: rgba(0,255,170,0.25); transform: translateY(-4px); background: rgba(0,255,170,0.025); }
.metric-card:hover::before { opacity: 1; }
.metric-icon { font-size: 1.5rem; margin-bottom: 0.85rem; display: block; }
.metric-label { font-family: 'DM Mono', monospace; font-size: 0.58rem; letter-spacing: 0.16em; text-transform: uppercase; color: rgba(232,244,240,0.28); margin-bottom: 0.45rem; }
.metric-value { font-size: 0.88rem; font-weight: 500; color: rgba(232,244,240,0.35); font-family: 'DM Mono', monospace; line-height: 1.3; }
.metric-hint { font-family: 'DM Mono', monospace; font-size: 0.6rem; color: rgba(0,255,170,0.3); margin-top: 0.4rem; }

.insight-card {
    background: rgba(255,255,255,0.02); border: 1px solid rgba(0,255,170,0.09);
    border-radius: 16px; padding: 1.2rem 1.4rem; margin-bottom: 0.8rem;
    display: flex; align-items: flex-start; gap: 1rem;
    transition: all 0.25s ease; animation: fadein 0.9s ease 0.2s both;
}
.insight-card:hover { border-color: rgba(0,255,170,0.2); transform: translateX(5px); background: rgba(0,255,170,0.02); }
.insight-icon { font-size: 1.3rem; flex-shrink: 0; margin-top: 0.05rem; }
.insight-title { font-size: 0.88rem; font-weight: 700; color: #e8f4f0; margin-bottom: 0.3rem; }
.insight-body { font-family: 'DM Mono', monospace; font-size: 0.75rem; color: rgba(232,244,240,0.38); line-height: 1.6; }

.upload-area {
    background: rgba(255,255,255,0.02); border: 1.5px dashed rgba(0,255,170,0.18);
    border-radius: 20px; padding: 2.5rem 2rem; text-align: center;
    transition: all 0.3s ease; margin-bottom: 1rem; animation: fadein 0.9s ease 0.15s both;
}
.upload-area:hover { border-color: rgba(0,255,170,0.4); background: rgba(0,255,170,0.025); }
.upload-icon { font-size: 2.8rem; display: block; margin-bottom: 0.85rem; animation: float 3s ease-in-out infinite; }
.upload-title { font-size: 1.05rem; font-weight: 700; color: #e8f4f0; margin-bottom: 0.35rem; }
.upload-sub { font-family: 'DM Mono', monospace; font-size: 0.68rem; color: rgba(232,244,240,0.25); letter-spacing: 0.08em; }

.stButton > button {
    background: linear-gradient(135deg, #00ffaa, #00c8ff) !important;
    color: #020608 !important; font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important; border: none !important;
    border-radius: 12px !important; padding: 0.7rem 1.2rem !important;
    width: 100% !important; transition: all 0.25s ease !important;
    box-shadow: 0 4px 15px rgba(0,255,170,0.15) !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 28px rgba(0,255,170,0.3) !important; }

[data-testid="stFileUploader"] * { color: #e8f4f0 !important; font-family: 'Syne', sans-serif !important; }
[data-testid="stFileUploader"] section {
    background: rgba(255,255,255,0.02) !important;
    border: 1px dashed rgba(0,255,170,0.18) !important; border-radius: 12px !important;
}

.success-file {
    background: rgba(0,255,170,0.06); border: 1px solid rgba(0,255,170,0.2);
    border-radius: 10px; padding: 0.6rem 1rem; margin-bottom: 0.4rem;
    font-family: 'DM Mono', monospace; font-size: 0.75rem; color: #00ffaa;
    display: flex; align-items: center; gap: 0.5rem;
}

@keyframes fadein { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: translateY(0); } }
@keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
@keyframes blink { 0%,100% { opacity:1; } 50% { opacity:0.2; } }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
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
        <div style="font-size:0.95rem;font-weight:700;color:#e8f4f0;margin-bottom:0.1rem;">{business_name}</div>
        <div style="font-family:'DM Mono',monospace;font-size:0.68rem;color:rgba(232,244,240,0.3);">
            {owner_name} · {business_type}</div>
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
        text-transform:uppercase;color:rgba(0,255,170,0.35);margin-bottom:0.75rem;">System Status</div>
    <div style="font-size:0.8rem;color:rgba(232,244,240,0.45);margin-bottom:0.35rem;display:flex;align-items:center;gap:0.5rem;">
        <span style="width:7px;height:7px;border-radius:50%;background:#00ffaa;box-shadow:0 0 8px #00ffaa;display:inline-block;animation:blink 2s infinite;"></span>AI Engine Online
    </div>
    <div style="font-size:0.8rem;color:rgba(232,244,240,0.45);margin-bottom:0.35rem;display:flex;align-items:center;gap:0.5rem;">
        <span style="width:7px;height:7px;border-radius:50%;background:#00ffaa;box-shadow:0 0 8px #00ffaa;display:inline-block;"></span>Memory Active
    </div>
    <div style="font-size:0.8rem;color:rgba(232,244,240,0.45);display:flex;align-items:center;gap:0.5rem;">
        <span style="width:7px;height:7px;border-radius:50%;background:#00c8ff;box-shadow:0 0 8px #00c8ff;display:inline-block;"></span>RAG Ready
    </div>
    <div style="margin:1.2rem 0;height:1px;background:rgba(0,255,170,0.07);"></div>
    """, unsafe_allow_html=True)

    if st.button("🚪  Logout", key="logout"):
        for k in ["owner_name","business_name","business_type","messages","total_queries","uploaded_files"]:
            st.session_state.pop(k, None)
        st.switch_page("app.py")

# ── Main Content ──
st.markdown(f"""
<div class="page-header">
    <div class="page-greeting">Good day, {owner_name} 👋</div>
    <div class="page-title">{business_name}</div>
    <div class="page-sub">Financial Intelligence Dashboard · {business_type}</div>
    <div class="live-pill"><div class="live-dot"></div>Live · Awaiting Your Data</div>
</div>
""", unsafe_allow_html=True)

# Metrics
st.markdown('<div class="section-label">Key Financial Metrics</div>', unsafe_allow_html=True)
st.markdown("""
<div class="metrics-grid">
    <div class="metric-card">
        <span class="metric-icon">💰</span>
        <div class="metric-label">Total Revenue</div>
        <div class="metric-value">Upload your<br>financial data</div>
        <div class="metric-hint">↑ Awaiting files</div>
    </div>
    <div class="metric-card">
        <span class="metric-icon">📉</span>
        <div class="metric-label">Total Expenses</div>
        <div class="metric-value">Upload your<br>financial data</div>
        <div class="metric-hint">↑ Awaiting files</div>
    </div>
    <div class="metric-card">
        <span class="metric-icon">📈</span>
        <div class="metric-label">Net Profit</div>
        <div class="metric-value">Upload your<br>financial data</div>
        <div class="metric-hint">↑ Awaiting files</div>
    </div>
    <div class="metric-card">
        <span class="metric-icon">🏦</span>
        <div class="metric-label">Cash Position</div>
        <div class="metric-value">Upload your<br>financial data</div>
        <div class="metric-hint">↑ Awaiting files</div>
    </div>
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([1.5, 1], gap="large")

with col_left:
    st.markdown('<div class="section-label">Upload Financial Documents</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="upload-area">
        <span class="upload-icon">📂</span>
        <div class="upload-title">Drop your financial files here</div>
        <div class="upload-sub">PDF invoices · CSV sales data · XLSX reports · All data stays private & secure</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload",
        type=["pdf","csv","xlsx"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        key="dash_upload"
    )

    if uploaded:
        st.session_state["uploaded_files"] = uploaded
        for f in uploaded:
            st.markdown(f'<div class="success-file">✓ &nbsp;{f.name}</div>', unsafe_allow_html=True)
        st.success(f"✓ {len(uploaded)} file(s) ready! Ask your CFO to analyse them.")
        if st.button("💬  Analyse with CFO →", key="goto_chat"):
            st.switch_page("pages/1_Chat.py")
    else:
        st.markdown("""
        <div style="text-align:center;padding:1.5rem 0;font-family:'DM Mono',monospace;
            font-size:0.7rem;color:rgba(232,244,240,0.18);letter-spacing:0.08em;">
            Upload sales CSV, invoice PDF or expense sheet<br>to unlock your full financial dashboard
        </div>
        """, unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="section-label">CFO Insights</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-card">
        <div class="insight-icon">💡</div>
        <div>
            <div class="insight-title">Upload to Unlock Insights</div>
            <div class="insight-body">Once you upload financial data, your AI CFO automatically surfaces patterns, risks and opportunities specific to your business.</div>
        </div>
    </div>
    <div class="insight-card">
        <div class="insight-icon">🎯</div>
        <div>
            <div class="insight-title">What Your CFO Analyses</div>
            <div class="insight-body">Revenue trends · Expense breakdown · Cash flow health · Profit margins · Cost leakages · Growth forecasts · Risk flags</div>
        </div>
    </div>
    <div class="insight-card">
        <div class="insight-icon">🧠</div>
        <div>
            <div class="insight-title">Remembers Everything</div>
            <div class="insight-body">Your CFO remembers past conversations and financial history to give you smarter, more personalised advice over time.</div>
        </div>
    </div>
    <div class="insight-card">
        <div class="insight-icon">🔒</div>
        <div>
            <div class="insight-title">Your Data is Private</div>
            <div class="insight-body">All documents processed locally. Nothing shared externally. Your financial data belongs to you.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("💬  Ask Your CFO Now", key="cfo_btn"):
        st.switch_page("pages/1_Chat.py")

st.markdown("""
<div style="margin-top:4rem;text-align:center;font-family:'DM Mono',monospace;
    font-size:0.52rem;letter-spacing:0.2em;color:rgba(232,244,240,0.07);">
    FINOVA · AI CFO · UPLOAD YOUR DATA TO BEGIN · BUILT WITH ♥️ BY THE TEAM
</div>
""", unsafe_allow_html=True)
