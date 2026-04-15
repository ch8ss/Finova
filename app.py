import streamlit as st

st.set_page_config(
    page_title="Finova",
    page_icon=None,
    layout="centered"
)

if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"

# Auto-login if uid is in URL params
if "owner_name" not in st.session_state:
    uid = st.query_params.get("uid")
    if uid:
        from core.session import restore_session
        if restore_session(uid):
            st.switch_page("pages/2_Dashboard.py")

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
    min-height: 100vh;
}
body { background: #0a1a0e !important; }
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: -20%;
    left: -20%;
    width: 60%;
    height: 60%;
    background: radial-gradient(ellipse, rgba(82,183,136,0.12) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}
[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    bottom: -20%;
    right: -20%;
    width: 60%;
    height: 60%;
    background: radial-gradient(ellipse, rgba(45,106,79,0.1) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}
[data-testid="stMain"] { background: transparent !important; }
#MainMenu, footer, header, [data-testid="stToolbar"] { display: none !important; }

.main .block-container {
    padding: 5rem 2rem 4rem !important;
    max-width: 420px !important;
    margin: 0 auto !important;
    position: relative;
    z-index: 1;
}

.brand {
    margin-bottom: 3rem;
    text-align: center;
}
.brand-name {
    font-size: 4.5rem;
    font-weight: 800;
    letter-spacing: -0.05em;
    color: #e8f4f0;
    margin: 0 auto 0.4rem;
    white-space: nowrap;
    overflow: hidden;
    width: 0;
    border-right: 3px solid rgba(82,183,136,0.8);
    animation:
        finova-type 0.9s steps(6, end) 0.2s forwards,
        finova-blink 0.7s step-end 6;
}
@keyframes finova-type {
    to { width: 7ch }
}
@keyframes finova-blink {
    from, to { border-color: transparent }
    50% { border-color: rgba(82,183,136,0.8) }
}
.brand-sub {
    font-size: 0.9rem;
    color: rgba(232,244,240,0.45);
    font-weight: 400;
    opacity: 0;
    animation: finova-sub-fade 0.5s ease 1.2s forwards;
}
@keyframes finova-sub-fade {
    to { opacity: 1 }
}

.glass-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.06);
    margin-bottom: 1.5rem;
}

.section-title {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(82,183,136,0.7);
    margin-bottom: 1.5rem;
}

.stTextInput > div > div > input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e8f4f0 !important;
    font-family: inherit !important;
    font-size: 0.93rem !important;
    padding: 0.75rem 1rem !important;
    transition: all 0.2s !important;
    box-shadow: none !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(82,183,136,0.5) !important;
    box-shadow: 0 0 0 3px rgba(82,183,136,0.1) !important;
    background: rgba(82,183,136,0.05) !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(232,244,240,0.25) !important; }
.stTextInput label {
    color: rgba(232,244,240,0.6) !important;
    font-size: 0.83rem !important;
    font-weight: 500 !important;
}

[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e8f4f0 !important;
    font-family: inherit !important;
}
[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: rgba(82,183,136,0.5) !important;
    box-shadow: 0 0 0 3px rgba(82,183,136,0.1) !important;
}
.stSelectbox label {
    color: rgba(232,244,240,0.6) !important;
    font-size: 0.83rem !important;
    font-weight: 500 !important;
}

.stButton > button {
    background: rgba(82,183,136,0.15) !important;
    color: #52b788 !important;
    font-family: inherit !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    border: 1px solid rgba(82,183,136,0.35) !important;
    border-radius: 10px !important;
    padding: 0.75rem 2rem !important;
    width: 100% !important;
    margin-top: 0.5rem !important;
    transition: all 0.2s !important;
    backdrop-filter: blur(10px) !important;
    box-shadow: 0 4px 15px rgba(82,183,136,0.1) !important;
}
.stButton > button:hover {
    background: rgba(82,183,136,0.25) !important;
    border-color: rgba(82,183,136,0.6) !important;
    box-shadow: 0 4px 20px rgba(82,183,136,0.25) !important;
    transform: translateY(-1px) !important;
}

.stAlert { border-radius: 10px !important; }

.footer {
    margin-top: 3rem;
    font-size: 0.72rem;
    color: rgba(232,244,240,0.2);
    text-align: center;
    letter-spacing: 0.05em;
}
</style>
""", unsafe_allow_html=True)

from core.auth import sign_in, sign_up
from core.database import load_messages

st.markdown("""
<div class="brand">
    <div class="brand-name">Finova</div>
    <div class="brand-sub">Your AI financial advisor</div>
</div>
""", unsafe_allow_html=True)

tab_in, tab_up = st.tabs(["Sign in", "Create account"])

with tab_in:
    st.markdown('<div class="section-title">Welcome back</div>', unsafe_allow_html=True)
    with st.form("signin_form"):
        si_email    = st.text_input("Email", placeholder="you@example.com", key="si_email")
        si_password = st.text_input("Password", type="password", placeholder="••••••••", key="si_pass")
        si_submitted = st.form_submit_button("Sign in")
    if si_submitted:
        if si_email.strip() and si_password.strip():
            with st.spinner("Signing in..."):
                user_id, profile, err = sign_in(si_email.strip(), si_password.strip())
            if err:
                st.error(err)
            else:
                st.session_state["user_id"]       = user_id
                st.session_state["owner_name"]    = profile["owner_name"]
                st.session_state["business_name"] = profile["business_name"]
                st.session_state["business_type"] = profile["business_type"]
                st.session_state["messages"]      = load_messages(user_id)
                st.session_state["total_queries"] = len([m for m in st.session_state["messages"] if m["role"] == "user"])
                st.query_params["uid"] = user_id
                st.switch_page("pages/2_Dashboard.py")
        else:
            st.error("Please enter your email and password.")

with tab_up:
    st.markdown('<div class="section-title">Create your account</div>', unsafe_allow_html=True)
    with st.form("signup_form"):
        su_email    = st.text_input("Email", placeholder="you@example.com", key="su_email")
        su_password = st.text_input("Password", type="password", placeholder="Min. 6 characters", key="su_pass")
        su_name     = st.text_input("Your name", placeholder="e.g. Priya Sharma", key="su_name")
        su_biz      = st.text_input("Business name", placeholder="e.g. Sharma Traders", key="su_biz")
        su_type     = st.selectbox("Type of business", [
            "Retail", "Restaurant / Cafe", "Manufacturing",
            "Tech", "Healthcare", "E-commerce",
            "Construction", "Education", "Freelance",
            "Finance / Consulting", "Services", "Other"
        ], key="su_type")
        su_submitted = st.form_submit_button("Create account")
    if su_submitted:
        if su_email.strip() and su_password.strip() and su_name.strip() and su_biz.strip():
            with st.spinner("Creating account..."):
                user_id, profile, err = sign_up(su_email.strip(), su_password.strip(), su_name.strip(), su_biz.strip(), su_type)
            if err:
                st.error(err)
            else:
                st.session_state["user_id"]       = user_id
                st.session_state["owner_name"]    = profile["owner_name"]
                st.session_state["business_name"] = profile["business_name"]
                st.session_state["business_type"] = profile["business_type"]
                st.session_state["messages"]      = []
                st.session_state["total_queries"] = 0
                st.query_params["uid"] = user_id
                st.switch_page("pages/2_Dashboard.py")
        else:
            st.error("Please fill in all fields.")

st.markdown('<div class="footer">Your data stays private.</div>', unsafe_allow_html=True)
