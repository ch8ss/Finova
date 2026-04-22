import streamlit as st
from streamlit_cookies_controller import CookieController
from core.auth import sign_out
from core.session import restore_session
from core.theme import inject_theme, get_theme

# Handle pending sign-out before anything else renders
if st.session_state.get("_signout_pending"):
    del st.session_state["_signout_pending"]
    from core.auth import sign_out as _sign_out
    from core.memory import clear_memory as _clear_memory
    _sign_out()
    _c = CookieController()
    _c.remove("finova_uid")
    _biz = st.session_state.get("business_name", "")
    _clear_memory(_biz.lower().replace(" ", "_"))
    for _k in ["user_id", "owner_name", "business_name", "business_type", "messages", "total_queries", "uploaded_file_names"]:
        st.session_state.pop(_k, None)
    st.switch_page("app.py")
    st.stop()

# Only instantiate CookieController when the user isn't already in session
if "owner_name" not in st.session_state:
    cookie = CookieController()
    uid = cookie.get("finova_uid")
    if uid:
        restore_session(uid)

st.set_page_config(page_title="Finova · Dashboard", layout="wide")

if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"

mode = st.session_state["theme"]
t = get_theme(mode)

if "owner_name" not in st.session_state:
    st.markdown(inject_theme(mode), unsafe_allow_html=True)
    st.markdown(f"""
    <div style="max-width:420px;margin:6rem auto;background:{t['card_bg']};border:1px solid {t['card_border']};border-radius:16px;padding:2.5rem 2rem;text-align:center;">
        <div style="font-size:1.1rem;font-weight:600;color:{t['text']};margin-bottom:0.5rem;">Sign in required</div>
        <div style="font-size:0.85rem;color:{t['text_muted']};margin-bottom:1.5rem;">Please sign in to access your dashboard.</div>
    </div>
    """, unsafe_allow_html=True)
    col = st.columns([1, 2, 1])[1]
    with col:
        if st.button("Go to sign in", key="gate_btn"):
            st.switch_page("app.py")
    st.stop()

owner_name = st.session_state.get("owner_name", "")
business_name = st.session_state.get("business_name", "")
business_type = st.session_state.get("business_type", "")

st.markdown(inject_theme(mode), unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown(f"""
    <div style="padding: 1.25rem 0 1.75rem;">
        <div style="font-size: 1.15rem; font-weight: 700; color: {t['text']}; letter-spacing: -0.02em;">Finova</div>
        <div style="font-size: 0.75rem; color: {t['text_muted']}; margin-top: 0.2rem;">{business_name}</div>
    </div>
    <div style="font-size: 0.65rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: {t['accent_muted']}; margin-bottom: 0.6rem;">Navigation</div>
    """, unsafe_allow_html=True)

    if st.button("AI CFO", key="nav_chat"):
        st.switch_page("pages/1_Chat.py")
    if st.button("Switch account", key="nav_switch"):
        st.session_state["_signout_pending"] = True
        st.rerun()

    st.markdown(f"""
    <div style="margin: 1.5rem 0; height: 1px; background: {t['divider']};"></div>
    <div style="font-size: 0.65rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: {t['accent_muted']}; margin-bottom: 0.6rem;">Status</div>
    <div style="font-size: 0.8rem; color: {t['text_muted']}; margin-bottom: 0.3rem; display:flex; align-items:center; gap:0.5rem;">
        <span style="width:6px;height:6px;border-radius:50%;background:#52b788;box-shadow:0 0 6px #52b788;display:inline-block;"></span>AI Engine Online
    </div>
    <div style="font-size: 0.8rem; color: {t['text_muted']}; margin-bottom: 0.3rem; display:flex; align-items:center; gap:0.5rem;">
        <span style="width:6px;height:6px;border-radius:50%;background:#52b788;display:inline-block;"></span>Memory Active
    </div>
    <div style="font-size: 0.8rem; color: {t['text_muted']}; display:flex; align-items:center; gap:0.5rem;">
        <span style="width:6px;height:6px;border-radius:50%;background:#74c69d;display:inline-block;"></span>RAG Ready
    </div>
    <div style="margin: 1.5rem 0; height: 1px; background: {t['divider']};"></div>
    """, unsafe_allow_html=True)

    if st.button(t['toggle_label'], key="theme_toggle"):
        st.session_state["theme"] = "light" if mode == "dark" else "dark"
        st.rerun()


# Main
st.markdown(f"""
<div class="page-title">{business_name}</div>
<div class="page-sub">Welcome back, {owner_name}. {business_type} dashboard.</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([1.4, 1], gap="large")

with col_left:
    messages = st.session_state.get("messages", [])
    # If session state is empty, try loading from Supabase
    if not messages:
        from core.database import load_messages
        user_id = st.session_state.get("user_id")
        if user_id:
            messages = load_messages(user_id)
            if messages:
                st.session_state["messages"] = messages
                st.session_state["total_queries"] = len([m for m in messages if m["role"] == "user"])

    st.markdown('<div class="section-label">Recent Conversations</div>', unsafe_allow_html=True)

    user_messages = [m for m in messages if m["role"] == "user"]

    if not user_messages:
        st.markdown(f"""
        <div style="background:{t['card_bg']};border:1px solid {t['card_border']};border-radius:14px;text-align:center;padding:2.5rem 1rem;">
            <div style="font-size:0.88rem;font-weight:600;color:{t['text_muted']};margin-bottom:0.4rem;">No conversations yet</div>
            <div style="font-size:0.78rem;color:{t['text_faint']};">Head to CFO Chat to get started.</div>
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
        st.markdown(f"""
        <div class="insight-body" style="margin-bottom:0.6rem;">Upload financial documents and ask questions like:</div>
        <div class="insight-body" style="color:{t['accent']};font-style:italic;margin-bottom:0.4rem;">"What was my highest revenue month?"</div>
        <div class="insight-body">→ Your best month was December at $289,000, driven by strong holiday demand.</div>
        """, unsafe_allow_html=True)

    with st.expander("Track patterns"):
        st.markdown(f"""
        <div class="insight-body" style="margin-bottom:0.6rem;">Finova spots trends and flags anomalies across your history:</div>
        <div class="insight-body" style="color:{t['accent']};font-style:italic;margin-bottom:0.4rem;">"Are my expenses trending up?"</div>
        <div class="insight-body">→ Operating expenses rose 63% from Jan to Dec, outpacing revenue growth of 103%. Worth reviewing.</div>
        """, unsafe_allow_html=True)

    with st.expander("Ask about cash flow"):
        st.markdown(f"""
        <div class="insight-body" style="margin-bottom:0.6rem;">Get plain-English cash flow summaries:</div>
        <div class="insight-body" style="color:{t['accent']};font-style:italic;margin-bottom:0.4rem;">"Do I have enough cash to hire someone?"</div>
        <div class="insight-body">→ Your average monthly cash flow is $41,700. A new hire at $3,000/month is well within range.</div>
        """, unsafe_allow_html=True)

    with st.expander("Persistent memory"):
        st.markdown(f"""
        <div class="insight-body" style="margin-bottom:0.6rem;">Your CFO remembers previous conversations:</div>
        <div class="insight-body" style="color:{t['accent']};font-style:italic;margin-bottom:0.4rem;">"Last time you said my margins were low — is that still true?"</div>
        <div class="insight-body">→ Yes, your gross margin is 52%. Industry average for e-commerce is 40–60%, so you're in range but there's room to improve.</div>
        """, unsafe_allow_html=True)
