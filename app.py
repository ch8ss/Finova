import streamlit as st

st.set_page_config(
    page_title="Finova · AI CFO",
    page_icon="💎",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=Instrument+Serif:ital@0;1&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #020608 !important;
    color: #e8f4f0 !important;
    font-family: 'Syne', sans-serif !important;
}
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% 10%, rgba(0,255,170,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(0,180,255,0.06) 0%, transparent 60%),
        #020608 !important;
}
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: #00ffaa44; border-radius: 2px; }
.main .block-container {
    padding: 4rem 2rem !important;
    max-width: 500px !important;
    margin: 0 auto !important;
}
.hero { text-align: center; margin-bottom: 2.5rem; animation: fadein 0.8s ease both; }
.logo { font-size: 3.5rem; display: block; margin-bottom: 0.75rem; animation: float 3s ease-in-out infinite; }
.title {
    font-size: 3rem; font-weight: 800; letter-spacing: -0.03em;
    background: linear-gradient(135deg, #ffffff 0%, #00ffaa 50%, #00c8ff 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.subtitle {
    font-family: 'Instrument Serif', serif; font-style: italic;
    font-size: 1rem; color: rgba(232,244,240,0.4); margin-top: 0.4rem;
}
.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(0,255,170,0.15);
    border-radius: 24px; padding: 2rem;
    animation: fadein 0.9s ease 0.15s both;
}
.card-label {
    font-family: 'DM Mono', monospace; font-size: 0.6rem;
    letter-spacing: 0.2em; text-transform: uppercase;
    color: rgba(0,255,170,0.5); text-align: center; margin-bottom: 1.5rem;
}
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(0,255,170,0.2) !important;
    border-radius: 12px !important; color: #e8f4f0 !important;
    font-family: 'Syne', sans-serif !important; font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(0,255,170,0.5) !important;
    box-shadow: 0 0 0 3px rgba(0,255,170,0.08) !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(232,244,240,0.2) !important; }
.stTextInput label { color: rgba(232,244,240,0.55) !important; font-size: 0.82rem !important; }
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(0,255,170,0.2) !important;
    border-radius: 12px !important; color: #e8f4f0 !important;
}
.stSelectbox label { color: rgba(232,244,240,0.55) !important; font-size: 0.82rem !important; }
.stButton > button {
    background: linear-gradient(135deg, #00ffaa, #00c8ff) !important;
    color: #020608 !important; font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important; font-size: 1rem !important;
    border: none !important; border-radius: 14px !important;
    padding: 0.8rem 2rem !important; width: 100% !important; margin-top: 0.5rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 30px rgba(0,255,170,0.3) !important;
}
.footer {
    text-align: center; font-family: 'DM Mono', monospace;
    font-size: 0.55rem; letter-spacing: 0.15em;
    color: rgba(232,244,240,0.1); margin-top: 2.5rem;
}
@keyframes fadein { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: translateY(0); } }
@keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
</style>
""", unsafe_allow_html=True)

# Hero
st.markdown("""
<div class="hero">
    <span class="logo">💎</span>
    <div class="title">Finova</div>
    <div class="subtitle">Your AI Chief Financial Officer</div>
</div>
""", unsafe_allow_html=True)

# Form
st.markdown('<div class="card"><div class="card-label">✦ Tell us about your business</div>', unsafe_allow_html=True)

owner_name = st.text_input("Your Name", placeholder="e.g. Priya Sharma")
business_name = st.text_input("Business Name", placeholder="e.g. Sharma Traders")
business_type = st.selectbox("Type of Business", [
    "🛒 Retail Shop", "🍽️ Restaurant / Cafe", "🏭 Manufacturing",
    "💻 Tech Startup", "🏥 Healthcare / Clinic", "📦 E-commerce",
    "🏗️ Construction", "📚 Education", "🎨 Creative / Freelance",
    "🏦 Finance / Consulting", "🛠️ Services", "Other"
])

st.markdown("</div>", unsafe_allow_html=True)

if st.button("Enter Finova →"):
    if owner_name.strip() and business_name.strip():
        st.session_state["owner_name"] = owner_name.strip()
        st.session_state["business_name"] = business_name.strip()
        st.session_state["business_type"] = business_type
        st.session_state["messages"] = []
        st.session_state["total_queries"] = 0
        st.switch_page("pages/2_Dashboard.py")
    else:
        st.error("Please fill in your name and business name!")

st.markdown('<div class="footer">FINOVA · AI CFO · YOUR DATA STAYS PRIVATE · BUILT WITH ♥</div>', unsafe_allow_html=True)