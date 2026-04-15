import streamlit as st
from core.chain import ask, process_uploaded_files
from core.auth import sign_out
from core.session import restore_session
from core.theme import inject_theme, get_theme

if "owner_name" not in st.session_state:
    uid = st.query_params.get("uid")
    if uid:
        restore_session(uid)

if st.session_state.get("user_id"):
    st.query_params["uid"] = st.session_state["user_id"]

st.set_page_config(page_title="Finova · Chat", layout="wide")

if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"

mode = st.session_state["theme"]
t = get_theme(mode)

if "owner_name" not in st.session_state:
    st.markdown(inject_theme(mode), unsafe_allow_html=True)
    st.markdown(f"""
    <div style="max-width:420px;margin:6rem auto;background:{t['card_bg']};border:1px solid {t['card_border']};border-radius:16px;padding:2.5rem 2rem;text-align:center;">
        <div style="font-size:1.1rem;font-weight:600;color:{t['text']};margin-bottom:0.5rem;">Sign in required</div>
        <div style="font-size:0.85rem;color:{t['text_muted']};margin-bottom:1.5rem;">Please sign in to access your CFO chat.</div>
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

if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "total_queries" not in st.session_state:
    st.session_state["total_queries"] = 0
if "pending_image_b64" not in st.session_state:
    st.session_state["pending_image_b64"] = None
if "pending_image_mime" not in st.session_state:
    st.session_state["pending_image_mime"] = "image/png"

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

    if st.button("Dashboard", key="nav_dash"):
        st.switch_page("pages/2_Dashboard.py")
    if st.button("New Chat", key="nav_new_chat"):
        st.session_state["messages"] = []
        st.session_state["total_queries"] = 0
        st.session_state["pending_image_b64"] = None
        st.rerun()
    if st.button("Clear chat", key="nav_clear"):
        st.session_state["messages"] = []
        st.session_state["total_queries"] = 0
        st.rerun()
    if st.button("Switch account", key="nav_switch"):
        sign_out()
        st.query_params.clear()
        for k in ["user_id", "owner_name", "business_name", "business_type", "messages", "total_queries", "uploaded_files", "pending_image_b64"]:
            st.session_state.pop(k, None)
        st.switch_page("app.py")

    st.markdown(f"""
    <div style="margin: 1.5rem 0; height: 1px; background: {t['divider']};"></div>
    <div style="font-size: 0.65rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: {t['accent_muted']}; margin-bottom: 0.75rem;">Upload Files</div>
    """, unsafe_allow_html=True)

    sidebar_upload = st.file_uploader(
        "Docs", type=["pdf", "csv", "xlsx"],
        accept_multiple_files=True,
        label_visibility="collapsed",
        key="sidebar_upload"
    )
    if sidebar_upload:
        user_id = st.session_state.get("user_id")
        uploaded_names = [f.name for f in sidebar_upload]
        if st.session_state.get("uploaded_file_names") != uploaded_names and user_id:
            st.session_state["uploaded_file_names"] = uploaded_names
            with st.spinner("Processing..."):
                process_uploaded_files(sidebar_upload, user_id=user_id)
        if st.session_state.get("uploaded_file_names") == uploaded_names and user_id:
            files_html = "".join(f'<div style="font-size:0.75rem;color:{t["accent"]};padding:0.3rem 0;border-bottom:1px solid {t["divider"]};">&#10003; {f.name} · ready</div>' for f in sidebar_upload)
        else:
            files_html = "".join(f'<div style="font-size:0.75rem;color:{t["text_muted"]};padding:0.3rem 0;border-bottom:1px solid {t["divider"]};">{f.name}</div>' for f in sidebar_upload)
        st.markdown(f'<div style="margin-top:0.5rem;">{files_html}</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="margin: 1.5rem 0; height: 1px; background: {t['divider']};"></div>
    <div style="font-size: 0.65rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: {t['accent_muted']}; margin-bottom: 0.5rem;">Status</div>
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

    queries = st.session_state.get("total_queries", 0)
    st.markdown(f'<div style="font-size:0.75rem;color:{t["text_faint"]};margin-bottom:1rem;">Queries this session: {queries}</div>', unsafe_allow_html=True)

    if st.button(t['toggle_label'], key="theme_toggle"):
        st.session_state["theme"] = "light" if mode == "dark" else "dark"
        st.rerun()


# Main
title_col, btn_col = st.columns([5, 1])
with title_col:
    st.markdown(f"""
    <div class="page-title">CFO Chat</div>
    <div class="page-sub">Ask anything about {business_name}'s finances in plain English.</div>
    """, unsafe_allow_html=True)
with btn_col:
    st.markdown("<div style='padding-top:1rem;'></div>", unsafe_allow_html=True)
    if st.button("+ New Chat", key="main_new_chat"):
        st.session_state["messages"] = []
        st.session_state["total_queries"] = 0
        st.session_state["pending_image_b64"] = None
        st.rerun()

st.markdown('<div class="section-label">Conversation</div>', unsafe_allow_html=True)

messages = st.session_state.get("messages", [])
chat_html = '<div class="chat-window">'

if not messages:
    chat_html += f"""
    <div class="empty-state">
        <div class="empty-title">Hello, {owner_name}.</div>
        <div class="empty-hint">Upload your financial documents from the sidebar, then ask me anything about {business_name}. You can also attach or paste images.</div>
    </div>"""
else:
    for msg in messages:
        if msg["role"] == "user":
            img_tag = ""
            if msg.get("image_b64"):
                img_tag = f'<img src="data:{msg.get("image_mime","image/png")};base64,{msg["image_b64"]}" style="max-width:260px;max-height:180px;border-radius:8px;margin-bottom:6px;display:block;" />'
            chat_html += f"""
            <div class="msg-row-user">
                <div class="msg-bubble-user">{img_tag}{msg['content']}</div>
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

# ── Message input ───────────────────────────────────────────────────────
st.markdown('<div class="section-label">Your message</div>', unsafe_allow_html=True)
with st.form(key="chat_form", clear_on_submit=True):
    c1, c2 = st.columns([5, 1])
    with c1:
        user_input = st.text_input("msg", placeholder=f"Ask about {business_name}...", label_visibility="collapsed")
    with c2:
        send = st.form_submit_button("Send")

if send and ((user_input and user_input.strip()) or st.session_state.get("pending_image_b64")):
    question = user_input.strip() if user_input else "What can you see in this image?"
    image_b64 = st.session_state.get("pending_image_b64")
    image_mime = st.session_state.get("pending_image_mime", "image/png")

    st.session_state["messages"].append({
        "role": "user",
        "content": question,
        "image_b64": image_b64,
        "image_mime": image_mime,
    })
    st.session_state["total_queries"] = st.session_state.get("total_queries", 0) + 1

    # Clear pending image before rerun
    st.session_state["pending_image_b64"] = None
    st.session_state["pending_image_mime"] = "image/png"

    session_id = business_name.lower().replace(" ", "_")
    user_id = st.session_state.get("user_id")
    with st.spinner("Thinking..."):
        reply = ask(
            question, session_id,
            user_id=user_id,
            business_type=business_type,
            image_b64=image_b64,
            image_mime=image_mime,
        )

    st.session_state["messages"].append({"role": "assistant", "content": reply})
    st.rerun()
