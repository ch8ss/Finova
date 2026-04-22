import hashlib
import html
import json
import re
import uuid
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from streamlit_cookies_controller import CookieController
from core.chain import ask, process_uploaded_files
from core.auth import sign_out
from core.session import restore_session
from core.theme import inject_theme, get_theme
from core.memory import clear_memory

PLOT_COLORS = ['#52b788','#74c69d','#40916c','#b7e4c7','#2d6a4f','#95d5b2']
PLOT_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(255,255,255,0.02)',
    font=dict(family='-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif', color='rgba(232,244,240,0.75)', size=12),
    xaxis=dict(gridcolor='rgba(82,183,136,0.08)', linecolor='rgba(82,183,136,0.12)', tickfont=dict(size=11)),
    yaxis=dict(gridcolor='rgba(82,183,136,0.08)', linecolor='rgba(82,183,136,0.12)', tickfont=dict(size=11)),
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='rgba(232,244,240,0.6)')),
)

def parse_response(content):
    """Split LLM reply into (text, chart_data). chart_data is None if no chart block."""
    match = re.search(r'```chart\s*\n(.*?)\n```', content, re.DOTALL)
    if match:
        try:
            chart_data = json.loads(match.group(1))
            text = (content[:match.start()] + content[match.end():]).strip()
            return text, chart_data
        except Exception:
            pass
    return content, None

def render_chart(chart_data):
    """Render a Plotly chart from the LLM's chart JSON block."""
    try:
        ctype  = chart_data.get("type", "bar")
        title  = chart_data.get("title", "")
        x      = chart_data.get("x", [])
        y      = chart_data.get("y", [])
        series = chart_data.get("series", [])
        x_lbl  = chart_data.get("x_label", "")
        y_lbl  = chart_data.get("y_label", "")

        if ctype == "pie":
            labels = chart_data.get("labels", x)
            values = chart_data.get("values", y)
            fig = go.Figure(go.Pie(
                labels=labels, values=values,
                marker=dict(colors=PLOT_COLORS),
                hole=0.4, textposition='inside', textinfo='percent+label'
            ))
        elif series:
            fig = go.Figure()
            for i, s in enumerate(series):
                c = PLOT_COLORS[i % len(PLOT_COLORS)]
                if ctype == "bar":
                    fig.add_trace(go.Bar(name=s["name"], x=x, y=s["values"], marker_color=c, opacity=0.85))
                else:
                    fig.add_trace(go.Scatter(name=s["name"], x=x, y=s["values"],
                                             mode='lines+markers', line=dict(color=c, width=2.5)))
            if ctype == "bar":
                fig.update_layout(barmode='group')
        else:
            df_c = pd.DataFrame({"x": x, "y": y})
            labels = {"x": x_lbl, "y": y_lbl}
            if ctype == "line":
                fig = px.line(df_c, x="x", y="y", color_discrete_sequence=PLOT_COLORS, labels=labels, markers=True)
                fig.update_traces(line=dict(width=2.5))
            elif ctype == "area":
                fig = px.area(df_c, x="x", y="y", color_discrete_sequence=PLOT_COLORS, labels=labels)
                fig.update_traces(line=dict(width=2.5), fillcolor='rgba(82,183,136,0.08)')
            else:
                fig = px.bar(df_c, x="x", y="y", color_discrete_sequence=PLOT_COLORS, labels=labels)

        fig.update_layout(title=title, **PLOT_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    except Exception:
        pass

# Handle pending sign-out before anything else renders
if st.session_state.get("_signout_pending"):
    del st.session_state["_signout_pending"]
    sign_out()
    try:
        _c = CookieController()
        _c.remove("finova_uid")
    except Exception:
        pass
    _biz = st.session_state.get("business_name", "")
    clear_memory(_biz.lower().replace(" ", "_"))
    for _k in ["user_id", "owner_name", "business_name", "business_type", "messages", "total_queries", "uploaded_file_names"]:
        st.session_state.pop(_k, None)
    st.session_state["_skip_autologin"] = True
    st.switch_page("app.py")
    st.stop()

# Only instantiate CookieController when the user isn't already in session
if "owner_name" not in st.session_state:
    cookie = CookieController()
    uid = cookie.get("finova_uid")
    if uid:
        restore_session(uid)

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
if "conversation_id" not in st.session_state:
    st.session_state["conversation_id"] = str(uuid.uuid4())

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
    if st.button("Clear chat", key="nav_clear"):
        from core.database import delete_conversation
        user_id = st.session_state.get("user_id")
        cid = st.session_state.get("conversation_id")
        if user_id and cid:
            delete_conversation(user_id, cid)
        session_id = business_name.lower().replace(" ", "_")
        clear_memory(session_id)
        st.session_state["conversation_id"] = str(uuid.uuid4())
        st.session_state["messages"] = []
        st.session_state["total_queries"] = 0
        st.rerun()
    if st.button("Switch account", key="nav_switch"):
        st.session_state["_signout_pending"] = True
        st.rerun()

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
        oversized = [f.name for f in sidebar_upload if f.size > 15 * 1024 * 1024]
        if oversized:
            st.warning(f"File(s) too large (max 15MB): {', '.join(oversized)}")
            sidebar_upload = [f for f in sidebar_upload if f.size <= 15 * 1024 * 1024]
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
        session_id = business_name.lower().replace(" ", "_")
        clear_memory(session_id)
        st.session_state["conversation_id"] = str(uuid.uuid4())
        st.session_state["messages"] = []
        st.session_state["total_queries"] = 0
        st.rerun()

st.markdown('<div class="section-label">Conversation</div>', unsafe_allow_html=True)

messages = st.session_state.get("messages", [])

with st.container(border=True):
    if not messages:
        st.markdown(f"""
        <div class="empty-state" style="padding:3rem 1rem;">
            <div class="empty-title">Hello, {owner_name}.</div>
            <div class="empty-hint">Upload your financial documents from the sidebar, then ask me anything about {business_name}.</div>
        </div>""", unsafe_allow_html=True)
    else:
        for msg in messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="msg-row-user">
                    <div class="msg-bubble-user">{html.escape(msg['content'])}</div>
                </div>""", unsafe_allow_html=True)
            else:
                text, chart_data = parse_response(msg["content"])
                st.markdown(f"""
                <div class="msg-row-ai">
                    <div class="msg-avatar">CFO</div>
                    <div class="msg-ai-inner">
                        <div class="msg-ai-name">Finova · {business_name}</div>
                        <div class="msg-bubble-ai">{html.escape(text)}</div>
                    </div>
                </div>""", unsafe_allow_html=True)
                if chart_data:
                    render_chart(chart_data)

# ── Read aloud for last AI response ─────────────────────────────────────
last_ai = next((m for m in reversed(messages) if m["role"] == "assistant"), None)
if last_ai:
    last_text, _ = parse_response(last_ai["content"])
    safe_text = last_text.replace("'", " ").replace('"', " ").replace("\n", " ").replace("`", " ")
    components.html(f"""
    <button onclick="(function(){{
        window.speechSynthesis.cancel();
        var u=new SpeechSynthesisUtterance('{safe_text}');
        u.rate=0.93; u.pitch=1.05;
        function go(){{
            var voices=window.speechSynthesis.getVoices();
            var want=['Google UK English Female','Samantha','Karen','Moira','Tessa','Fiona'];
            for(var i=0;i<want.length;i++){{var v=voices.find(function(x){{return x.name===want[i];}});if(v){{u.voice=v;break;}}}}
            window.speechSynthesis.speak(u);
        }}
        if(window.speechSynthesis.getVoices().length){{go();}}else{{window.speechSynthesis.onvoiceschanged=go;}}
    }})()"
        style="background:rgba(82,183,136,0.1);border:1px solid rgba(82,183,136,0.3);color:#52b788;
               padding:0.35rem 0.9rem;border-radius:8px;cursor:pointer;font-size:0.78rem;
               font-family:-apple-system,sans-serif;margin:0.25rem 0 0.5rem;">
        &#128266; Read aloud
    </button>
    """, height=45)

# ── Message input ───────────────────────────────────────────────────────
st.markdown('<div class="section-label">Your message</div>', unsafe_allow_html=True)
form_col, mic_col = st.columns([14, 1])
with form_col:
    with st.form(key="chat_form", clear_on_submit=True):
        c1, c2 = st.columns([6, 1])
        with c1:
            user_input = st.text_input("msg", placeholder=f"Ask about {business_name}...", label_visibility="collapsed")
        with c2:
            send = st.form_submit_button("Send")

audio = None
with mic_col:
    try:
        audio = st.audio_input("", label_visibility="collapsed", key="mic_input")
    except AttributeError:
        pass

# ── Handle mic transcription ─────────────────────────────────────────────
if audio is not None:
    audio_bytes = audio.read()
    audio_hash = hashlib.md5(audio_bytes).hexdigest()
    if st.session_state.get("_last_audio_hash") != audio_hash:
        st.session_state["_last_audio_hash"] = audio_hash
        from core.audio import transcribe_audio
        with st.spinner("Transcribing..."):
            question = transcribe_audio(audio_bytes)
        if question and question.strip():
            st.session_state["messages"].append({"role": "user", "content": question})
            st.session_state["total_queries"] = st.session_state.get("total_queries", 0) + 1
            session_id = business_name.lower().replace(" ", "_")
            user_id = st.session_state.get("user_id")
            with st.spinner("Thinking..."):
                reply = ask(question, session_id, user_id=user_id, business_type=business_type,
                            has_uploaded=bool(st.session_state.get("uploaded_file_names")),
                            conversation_id=st.session_state.get("conversation_id"))
            st.session_state["messages"].append({"role": "assistant", "content": reply})
            st.rerun()
        else:
            st.toast("Couldn't pick up audio — try again or type your question.", icon="🎙️")

if send and user_input and user_input.strip():
    question = user_input.strip()

    st.session_state["messages"].append({
        "role": "user",
        "content": question,
    })
    st.session_state["total_queries"] = st.session_state.get("total_queries", 0) + 1

    session_id = business_name.lower().replace(" ", "_")
    user_id = st.session_state.get("user_id")
    has_uploaded = bool(st.session_state.get("uploaded_file_names"))
    conversation_id = st.session_state.get("conversation_id")
    with st.spinner("Thinking..."):
        reply = ask(
            question, session_id,
            user_id=user_id,
            business_type=business_type,
            has_uploaded=has_uploaded,
            conversation_id=conversation_id,
        )

    st.session_state["messages"].append({"role": "assistant", "content": reply})
    st.rerun()
