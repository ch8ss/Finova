import streamlit as st

st.set_page_config(
    page_title="Finova · AI CFO",
    page_icon="💎",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=Instrument+Serif:ital@0;1&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }

[data-testid="stAppViewContainer"] {
    background: #020608 !important;
    font-family: 'Syne', sans-serif !important;
}
[data-testid="stAppViewContainer"] > div {
    background:
        radial-gradient(ellipse 80% 50% at 20% 10%, rgba(0,255,170,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(0,180,255,0.07) 0%, transparent 60%),
        #020608 !important;
}
[data-testid="stMain"] { background: transparent !important; }
#MainMenu, footer, header, [data-testid="stToolbar"] { display: none !important; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: #00ffaa44; border-radius: 2px; }

.main .block-container {
    padding: 3rem 2rem 4rem !important;
    max-width: 480px !important;
    margin: 0 auto !important;
}

.hero {
    text-align: center;
    margin-bottom: 2.5rem;
    animation: fadein 0.9s ease both;
}
.logo-wrap {
    display: inline-block;
    animation: float 4s ease-in-out infinite;
    font-size: 4rem;
    margin-bottom: 1rem;
}
.brand-name {
    font-size: 3.2rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1;
    background: linear-gradient(135deg, #ffffff 0%, #00ffaa 45%, #00c8ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
}
.brand-sub {
    font-family: 'Instrument Serif', serif;
    font-style: italic;
    font-size: 1.05rem;
    color: rgba(232,244,240,0.4);
}
.brand-badge {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #00ffaa;
    background: rgba(0,255,170,0.08);
    border: 1px solid rgba(0,255,170,0.2);
    padding: 0.3rem 0.9rem;
    border-radius: 100px;
    margin-top: 0.75rem;
}

.form-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(0,255,170,0.12);
    border-radius: 24px;
    padding: 2.2rem 2rem;
    animation: fadein 1s ease 0.15s both;
    position: relative;
    overflow: hidden;
}
.form-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,255,170,0.4), transparent);
}
.form-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: rgba(0,255,170,0.5);
    text-align: center;
    margin-bottom: 1.6rem;
}

.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(0,255,170,0.18) !important;
    border-radius: 12px !important;
    color: #e8f4f0 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.93rem !important;
    padding: 0.75rem 1rem !important;
    transition: all 0.25s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(0,255,170,0.5) !important;
    box-shadow: 0 0 0 3px rgba(0,255,170,0.07) !important;
    background: rgba(0,255,170,0.03) !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(232,244,240,0.2) !important; }
.stTextInput label {
    color: rgba(232,244,240,0.5) !important;
    font-size: 0.8rem !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
}

[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(0,255,170,0.18) !important;
    border-radius: 12px !important;
    color: #e8f4f0 !important;
    font-family: 'Syne', sans-serif !important;
}
.stSelectbox label {
    color: rgba(232,244,240,0.5) !important;
    font-size: 0.8rem !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #00ffaa 0%, #00d4aa 50%, #00c8ff 100%) !important;
    color: #020608 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 1rem !important;
    letter-spacing: 0.02em !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.85rem 2rem !important;
    width: 100% !important;
    margin-top: 0.75rem !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 20px rgba(0,255,170,0.2) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 35px rgba(0,255,170,0.35) !important;
}
.stButton > button:active { transform: translateY(0px) !important; }

.footer {
    text-align: center;
    font-family: 'DM Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.18em;
    color: rgba(232,244,240,0.1);
    margin-top: 3rem;
    animation: fadein 1.2s ease 0.3s both;
}

@keyframes fadein {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-12px); }
}
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero">
    <div class="logo-wrap">💎</div>
    <div class="brand-name">Finova</div>
    <div class="brand-sub">Your AI Chief Financial Officer</div>
    <div class="brand-badge">✦ Powered by LLaMA · RAG · Memory</div>
</div>
""", unsafe_allow_html=True)

# Form
st.markdown('<div class="form-card"><div class="form-label">✦ Tell us about your business</div>', unsafe_allow_html=True)

owner_name = st.text_input("Your Name", placeholder="e.g. Priya Sharma", key="login_name")
business_name = st.text_input("Business Name", placeholder="e.g. Sharma Traders", key="login_biz")
business_type = st.selectbox("Type of Business", [
    "🛒 Retail Shop", "🍽️ Restaurant / Cafe", "🏭 Manufacturing",
    "💻 Tech Startup", "🏥 Healthcare / Clinic", "📦 E-commerce",
    "🏗️ Construction", "📚 Education", "🎨 Creative / Freelance",
    "🏦 Finance / Consulting", "🛠️ Services", "Other"
], key="login_type")

st.markdown("</div>", unsafe_allow_html=True)

if st.button("Enter Finova →", key="enter_btn"):
    if owner_name.strip() and business_name.strip():
        st.session_state["owner_name"] = owner_name.strip()
        st.session_state["business_name"] = business_name.strip()
        st.session_state["business_type"] = business_type
        st.session_state["messages"] = []
        st.session_state["total_queries"] = 0
        st.switch_page("pages/2_Dashboard.py")
    else:
        st.error("Please fill in your name and business name to continue!")

st.markdown("""
<div class="footer">
    FINOVA · AI CFO · YOUR DATA STAYS PRIVATE · BUILT WITH ♥️ BY THE TEAM
</div>
""", unsafe_allow_html=True)
