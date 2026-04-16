DARK = {
    "bg": "linear-gradient(135deg, #0a1a0e 0%, #0d2410 50%, #071510 100%)",
    "bg_solid": "#0a1a0e",
    "text": "#e8f4f0",
    "text_muted": "rgba(232,244,240,0.4)",
    "text_faint": "rgba(232,244,240,0.2)",
    "accent": "#52b788",
    "accent_muted": "rgba(82,183,136,0.5)",
    "accent_bg": "rgba(82,183,136,0.12)",
    "accent_border": "rgba(82,183,136,0.3)",
    "card_bg": "rgba(255,255,255,0.04)",
    "card_border": "rgba(255,255,255,0.07)",
    "input_bg": "rgba(255,255,255,0.05)",
    "input_border": "rgba(255,255,255,0.1)",
    "sidebar_bg": "rgba(10,26,14,0.85)",
    "sidebar_border": "rgba(255,255,255,0.06)",
    "divider": "rgba(255,255,255,0.05)",
    "glow": "radial-gradient(ellipse, rgba(82,183,136,0.1) 0%, transparent 70%)",
    "toggle_icon": "",
    "toggle_label": "Light mode",
}

LIGHT = {
    "bg": "linear-gradient(135deg, #f0f7f4 0%, #e8f5ee 50%, #f5faf7 100%)",
    "bg_solid": "#f0f7f4",
    "text": "#1a2e22",
    "text_muted": "rgba(26,46,34,0.55)",
    "text_faint": "rgba(26,46,34,0.3)",
    "accent": "#2d6a4f",
    "accent_muted": "rgba(45,106,79,0.6)",
    "accent_bg": "rgba(45,106,79,0.1)",
    "accent_border": "rgba(45,106,79,0.3)",
    "card_bg": "rgba(255,255,255,0.85)",
    "card_border": "rgba(45,106,79,0.12)",
    "input_bg": "rgba(255,255,255,0.9)",
    "input_border": "rgba(45,106,79,0.2)",
    "sidebar_bg": "rgba(232,244,240,0.95)",
    "sidebar_border": "rgba(45,106,79,0.1)",
    "divider": "rgba(45,106,79,0.1)",
    "glow": "radial-gradient(ellipse, rgba(45,106,79,0.08) 0%, transparent 70%)",
    "toggle_icon": "",
    "toggle_label": "Dark mode",
}


def get_theme(mode: str) -> dict:
    return LIGHT if mode == "light" else DARK


def inject_theme(mode: str) -> str:
    t = get_theme(mode)
    return f"""
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body, [data-testid="stAppViewContainer"] {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif !important;
    color: {t['text']} !important;
}}
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > section,
[data-testid="stAppViewContainer"] > section > div {{
    background: {t['bg']} !important;
}}
body {{ background: {t['bg_solid']} !important; }}
[data-testid="stAppViewContainer"]::before {{
    content: '';
    position: fixed;
    top: -10%; left: -10%;
    width: 50%; height: 50%;
    background: {t['glow']};
    pointer-events: none;
    z-index: 0;
}}
[data-testid="stMain"] {{ background: transparent !important; }}
#MainMenu, footer, header, [data-testid="stToolbar"] {{ display: none !important; }}
[data-testid="collapsedControl"] {{ display: none !important; }}
section[data-testid="stSidebar"] {{ transform: none !important; min-width: 240px !important; }}
[data-testid="stSidebarNav"] {{ display: none !important; }}
.main .block-container {{ padding: 2rem 2.5rem 4rem !important; max-width: 1300px !important; position: relative; z-index: 1; }}

[data-testid="stSidebar"] {{
    background: {t['sidebar_bg']} !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-right: 1px solid {t['sidebar_border']} !important;
}}
[data-testid="stSidebar"] .stButton > button {{
    background: {t['card_bg']} !important;
    color: {t['text_muted']} !important;
    border: 1px solid {t['card_border']} !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    width: 100% !important;
    margin-bottom: 0.4rem !important;
    padding: 0.55rem 1rem !important;
    font-size: 0.87rem !important;
    text-align: left !important;
    box-shadow: none !important;
    transition: all 0.2s !important;
}}
[data-testid="stSidebar"] .stButton > button:hover {{
    background: {t['accent_bg']} !important;
    border-color: {t['accent_border']} !important;
    color: {t['accent']} !important;
    box-shadow: none !important;
    transform: none !important;
}}

.page-title {{
    font-size: 1.9rem; font-weight: 700;
    letter-spacing: -0.03em; color: {t['text']};
    margin-bottom: 0.3rem;
}}
.page-sub {{
    font-size: 0.88rem; color: {t['text_muted']};
    margin-bottom: 2.5rem;
}}
.section-label {{
    font-size: 0.68rem; font-weight: 600;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: {t['accent_muted']};
    margin-bottom: 0.9rem; padding-bottom: 0.5rem;
    border-bottom: 1px solid {t['divider']};
}}

.metric-card, .insight-card {{
    background: {t['card_bg']};
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid {t['card_border']};
    border-radius: 14px;
    padding: 1.5rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.06);
    transition: all 0.25s;
}}
.metric-card:hover, .insight-card:hover {{
    border-color: {t['accent_border']};
}}
.metric-label {{
    font-size: 0.68rem; font-weight: 600;
    letter-spacing: 0.1em; text-transform: uppercase;
    color: {t['accent_muted']}; margin-bottom: 0.5rem;
}}
.metric-value {{ font-size: 0.9rem; color: {t['text_muted']}; line-height: 1.4; }}
.insight-title {{ font-size: 0.88rem; font-weight: 600; color: {t['text']}; margin-bottom: 0.3rem; }}
.insight-body {{ font-size: 0.8rem; color: {t['text_muted']}; line-height: 1.6; }}

.stButton > button {{
    background: {t['accent_bg']} !important;
    color: {t['accent']} !important;
    font-family: inherit !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    border: 1px solid {t['accent_border']} !important;
    border-radius: 10px !important;
    padding: 0.65rem 1.2rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
    box-shadow: none !important;
}}
.stButton > button:hover {{
    background: {t['accent_border']} !important;
    border-color: {t['accent']} !important;
    transform: translateY(-1px) !important;
}}

.stTextInput > div > div > input {{
    background: {t['input_bg']} !important;
    border: 1px solid {t['input_border']} !important;
    border-radius: 10px !important;
    color: {t['text']} !important;
    font-family: inherit !important;
    font-size: 0.93rem !important;
    padding: 0.75rem 1rem !important;
    box-shadow: none !important;
    transition: all 0.2s !important;
}}
.stTextInput > div > div > input:focus {{
    border-color: {t['accent']} !important;
    box-shadow: 0 0 0 3px {t['accent_bg']} !important;
}}
.stTextInput > div > div > input::placeholder {{ color: {t['text_faint']} !important; }}
.stTextInput label {{ color: {t['text_muted']} !important; font-size: 0.83rem !important; font-weight: 500 !important; }}

[data-testid="stSelectbox"] > div > div {{
    background: {t['input_bg']} !important;
    border: 1px solid {t['input_border']} !important;
    border-radius: 10px !important;
    color: {t['text']} !important;
}}
.stSelectbox label {{ color: {t['text_muted']} !important; font-size: 0.83rem !important; }}

[data-testid="stFileUploaderDropzone"] * {{ pointer-events: auto !important; }}

[data-testid="stExpander"] {{
    background: {t['card_bg']} !important;
    border: 1px solid {t['card_border']} !important;
    border-radius: 10px !important; margin-bottom: 0.5rem !important;
}}
[data-testid="stExpander"] summary {{
    font-size: 0.86rem !important; font-weight: 600 !important;
    color: {t['text']} !important; padding: 0.75rem 1rem !important;
}}
[data-testid="stExpander"] summary:hover {{ color: {t['accent']} !important; }}
[data-testid="stExpander"] svg {{ color: {t['accent_muted']} !important; }}
[data-testid="stExpander"] > div:last-child {{
    padding: 0.25rem 1rem 1rem !important;
    border-top: 1px solid {t['divider']} !important;
}}

[data-testid="stVerticalBlockBorderWrapper"] {{
    background: {t['card_bg']} !important;
    border: 1px solid {t['card_border']} !important;
    border-radius: 14px !important; padding: 0 !important; overflow: hidden !important;
}}
[data-testid="stVerticalBlockBorderWrapper"] .stButton > button {{
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid {t['divider']} !important;
    border-radius: 0 !important; text-align: left !important;
    color: {t['text_muted']} !important;
    font-size: 0.83rem !important; font-weight: 400 !important;
    padding: 0.65rem 1.1rem !important; width: 100% !important;
    box-shadow: none !important; justify-content: flex-start !important; margin: 0 !important;
}}
[data-testid="stVerticalBlockBorderWrapper"] .stButton > button:hover {{
    background: {t['accent_bg']} !important;
    color: {t['text']} !important;
    border-bottom-color: {t['divider']} !important;
    transform: none !important; box-shadow: none !important;
}}

.chat-window {{
    background: {t['card_bg']};
    border: 1px solid {t['card_border']};
    border-radius: 16px; padding: 1.75rem;
    margin-bottom: 1.25rem;
}}
.msg-bubble-user {{
    background: {t['accent_bg']};
    border: 1px solid {t['accent_border']};
    color: {t['text']}; font-size: 0.9rem;
    padding: 0.75rem 1.1rem; border-radius: 14px 14px 3px 14px;
    max-width: 65%; line-height: 1.55;
}}
.msg-bubble-ai {{
    background: {t['card_bg']};
    border: 1px solid {t['card_border']};
    color: {t['text']}; font-size: 0.9rem;
    line-height: 1.65; padding: 0.75rem 1.1rem;
    border-radius: 3px 14px 14px 14px;
}}
.msg-avatar {{
    width: 30px; height: 30px; min-width: 30px;
    background: {t['accent_bg']}; border: 1px solid {t['accent_border']};
    border-radius: 8px; display: flex; align-items: center;
    justify-content: center; color: {t['accent']};
    font-size: 0.65rem; font-weight: 700;
}}
.msg-row-user {{ display: flex; justify-content: flex-end; margin: 0.75rem 0; }}
.msg-row-ai {{ display: flex; align-items: flex-start; gap: 0.75rem; margin: 0.75rem 0; }}
.msg-ai-inner {{ max-width: 70%; }}
.msg-ai-name {{
    font-size: 0.65rem; font-weight: 600; letter-spacing: 0.08em;
    text-transform: uppercase; color: {t['accent_muted']}; margin-bottom: 0.3rem;
}}
.empty-state {{ display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; text-align: center; gap: 0.75rem; }}
.empty-title {{ font-size: 1rem; font-weight: 600; color: {t['text_muted']}; }}
.empty-hint {{ font-size: 0.8rem; color: {t['text_faint']}; line-height: 1.6; max-width: 300px; }}

.stAlert {{ border-radius: 10px !important; }}
p, li, span {{ color: {t['text']} !important; }}
</style>
"""
