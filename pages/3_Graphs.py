import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io

st.set_page_config(page_title="Finova · Graphs", layout="wide")

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

.page-header { padding: 1.5rem 0 2rem; animation: fadein 0.7s ease both; }
.page-title {
    font-size: 2.4rem; font-weight: 800; letter-spacing: -0.03em; line-height: 1.05;
    background: linear-gradient(135deg, #fff 0%, #00ffaa 55%, #00c8ff 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.page-sub {
    font-family: 'Instrument Serif', serif; font-style: italic;
    font-size: 0.95rem; color: rgba(232,244,240,0.35); margin-top: 0.3rem;
}

.section-label {
    font-family: 'DM Mono', monospace; font-size: 0.58rem;
    letter-spacing: 0.22em; text-transform: uppercase;
    color: rgba(0,255,170,0.45); margin-bottom: 0.9rem;
    display: flex; align-items: center; gap: 0.6rem;
}
.section-label::after { content: ''; flex: 1; height: 1px; background: rgba(0,255,170,0.07); }

.upload-area {
    background: rgba(255,255,255,0.02); border: 1.5px dashed rgba(0,255,170,0.18);
    border-radius: 20px; padding: 2rem; text-align: center;
    transition: all 0.3s ease; margin-bottom: 1rem;
}
.upload-icon { font-size: 2.5rem; display: block; margin-bottom: 0.75rem; animation: float 3s ease-in-out infinite; }
.upload-title { font-size: 1rem; font-weight: 700; color: #e8f4f0; margin-bottom: 0.3rem; }
.upload-sub { font-family: 'DM Mono', monospace; font-size: 0.68rem; color: rgba(232,244,240,0.25); }

.filter-bar {
    background: rgba(255,255,255,0.02); border: 1px solid rgba(0,255,170,0.1);
    border-radius: 16px; padding: 1.2rem 1.5rem; margin-bottom: 1.5rem;
    display: flex; gap: 1rem; align-items: center; flex-wrap: wrap;
    animation: fadein 0.8s ease 0.1s both;
}

.stButton > button {
    background: linear-gradient(135deg, #00ffaa, #00c8ff) !important;
    color: #020608 !important; font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important; border: none !important;
    border-radius: 12px !important; padding: 0.7rem 1.2rem !important;
    width: 100% !important; transition: all 0.25s ease !important;
    box-shadow: 0 4px 15px rgba(0,255,170,0.15) !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 8px 28px rgba(0,255,170,0.3) !important; }

[data-testid="stFileUploader"] * { color: #e8f4f0 !important; }
[data-testid="stFileUploader"] section {
    background: rgba(255,255,255,0.02) !important;
    border: 1px dashed rgba(0,255,170,0.18) !important; border-radius: 12px !important;
}

.stSelectbox > div > div, .stMultiSelect > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(0,255,170,0.18) !important;
    border-radius: 12px !important; color: #e8f4f0 !important;
}
.stSelectbox label, .stMultiSelect label {
    color: rgba(232,244,240,0.5) !important; font-size: 0.8rem !important;
    font-family: 'Syne', sans-serif !important; font-weight: 600 !important;
}

.insight-strip {
    background: rgba(0,255,170,0.04); border: 1px solid rgba(0,255,170,0.12);
    border-radius: 14px; padding: 1rem 1.4rem; margin-bottom: 1.5rem;
    font-family: 'DM Mono', monospace; font-size: 0.75rem;
    color: rgba(232,244,240,0.55); line-height: 1.6;
}
.insight-strip strong { color: #00ffaa; }

@keyframes fadein { from { opacity:0; transform:translateY(14px); } to { opacity:1; transform:translateY(0); } }
@keyframes float { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-8px); } }
@keyframes blink { 0%,100% { opacity:1; } 50% { opacity:0.2; } }
</style>
""", unsafe_allow_html=True)

# Plotly dark theme
PLOT_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(255,255,255,0.02)',
    font=dict(family='Syne, sans-serif', color='rgba(232,244,240,0.7)', size=12),
    xaxis=dict(gridcolor='rgba(0,255,170,0.06)', linecolor='rgba(0,255,170,0.1)', tickfont=dict(size=11)),
    yaxis=dict(gridcolor='rgba(0,255,170,0.06)', linecolor='rgba(0,255,170,0.1)', tickfont=dict(size=11)),
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='rgba(232,244,240,0.6)')),
)
COLORS = ['#00ffaa','#00c8ff','#ff6b9d','#ffd166','#a29bfe','#fd79a8']

# ── Sidebar ──
with st.sidebar:
    st.markdown(f"""
    <div style="padding:0.75rem 0 1.5rem;">
        <div style="font-size:1.6rem;font-weight:800;
            background:linear-gradient(135deg,#00ffaa,#00c8ff);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">💎 Finova</div>
        <div style="font-family:'DM Mono',monospace;font-size:0.55rem;letter-spacing:0.18em;
            color:rgba(232,244,240,0.25);text-transform:uppercase;margin-top:0.25rem;">AI Chief Financial Officer</div>
    </div>
    <div style="background:rgba(0,255,170,0.05);border:1px solid rgba(0,255,170,0.12);
        border-radius:14px;padding:1rem;margin-bottom:1.2rem;">
        <div style="font-size:0.95rem;font-weight:700;color:#e8f4f0;margin-bottom:0.1rem;">{business_name}</div>
        <div style="font-family:'DM Mono',monospace;font-size:0.68rem;color:rgba(232,244,240,0.3);">{owner_name}</div>
    </div>
    <div style="font-family:'DM Mono',monospace;font-size:0.55rem;letter-spacing:0.18em;
        text-transform:uppercase;color:rgba(0,255,170,0.35);margin-bottom:0.6rem;">Navigation</div>
    """, unsafe_allow_html=True)

    if st.button("Dashboard", key="nav_dash"): st.switch_page("pages/2_Dashboard.py")
    if st.button("Graphs", key="nav_graphs"): st.switch_page("pages/3_Graphs.py")
    if st.button("CFO Chat", key="nav_chat"): st.switch_page("pages/1_Chat.py")

    st.markdown("<div style='margin:1.2rem 0;height:1px;background:rgba(0,255,170,0.07);'></div>", unsafe_allow_html=True)

    if st.button("Logout", key="logout"):
        for k in ["owner_name","business_name","business_type","messages","total_queries","uploaded_files"]:
            st.session_state.pop(k, None)
        st.switch_page("app.py")

# ── Header ──
st.markdown(f"""
<div class="page-header">
    <div class="page-title">Financial Graphs</div>
    <div class="page-sub">{business_name} · Visual Intelligence Dashboard</div>
</div>
""", unsafe_allow_html=True)

# ── Upload ──
st.markdown('<div class="section-label">Upload Your Financial Data</div>', unsafe_allow_html=True)
st.markdown("""
<div class="upload-area">
    <span class="upload-icon"></span>
    <div class="upload-title">Upload CSV or Excel to generate graphs</div>
    <div class="upload-sub">Your file should have columns like: Date, Revenue, Expenses, Profit, Category, Sales</div>
</div>
""", unsafe_allow_html=True)

uploaded = st.file_uploader(
    "Upload financial data",
    type=["csv","xlsx"],
    label_visibility="collapsed",
    key="graphs_upload"
)

if uploaded:
    try:
        if uploaded.name.endswith(".csv"):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded)

        df.columns = [c.strip().lower().replace(" ","_") for c in df.columns]

        st.success(f"✓ {uploaded.name} loaded — {len(df)} rows, {len(df.columns)} columns")

        # Show columns detected
        st.markdown(f"""
        <div class="insight-strip">
            <strong>Columns detected:</strong> {', '.join(df.columns.tolist())}
        </div>
        """, unsafe_allow_html=True)

        # ── Filters ──
        st.markdown('<div class="section-label">Filters & Time Period</div>', unsafe_allow_html=True)

        date_cols = [c for c in df.columns if any(x in c for x in ['date','time','month','year','week','quarter','period'])]
        num_cols = df.select_dtypes(include='number').columns.tolist()
        cat_cols = df.select_dtypes(include='object').columns.tolist()

        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            date_col = st.selectbox("Date / Time Column", ["None"] + date_cols + cat_cols, key="date_col")
        with fc2:
            period = st.selectbox("Time Period", ["All","Weekly","Monthly","Quarterly","Yearly"], key="period")
        with fc3:
            chart_type = st.selectbox("Default Chart Style", ["Line","Bar","Area","Scatter"], key="chart_style")

        # Try to parse date
        if date_col != "None":
            try:
                df[date_col] = pd.to_datetime(df[date_col])
                if period == "Monthly":
                    df = df.groupby(df[date_col].dt.to_period("M")).mean(numeric_only=True).reset_index()
                    df[date_col] = df[date_col].astype(str)
                elif period == "Quarterly":
                    df = df.groupby(df[date_col].dt.to_period("Q")).mean(numeric_only=True).reset_index()
                    df[date_col] = df[date_col].astype(str)
                elif period == "Yearly":
                    df = df.groupby(df[date_col].dt.year).mean(numeric_only=True).reset_index()
                elif period == "Weekly":
                    df = df.groupby(df[date_col].dt.to_period("W")).mean(numeric_only=True).reset_index()
                    df[date_col] = df[date_col].astype(str)
            except:
                pass

        st.markdown("---")

        # ── Auto-detect columns ──
        rev_col = next((c for c in num_cols if 'revenue' in c or 'sales' in c or 'income' in c), num_cols[0] if num_cols else None)
        exp_col = next((c for c in num_cols if 'expense' in c or 'cost' in c or 'spend' in c), num_cols[1] if len(num_cols)>1 else None)
        profit_col = next((c for c in num_cols if 'profit' in c or 'net' in c or 'margin' in c), num_cols[2] if len(num_cols)>2 else None)
        cash_col = next((c for c in num_cols if 'cash' in c or 'flow' in c or 'balance' in c), None)
        cat_col = next((c for c in cat_cols if 'category' in c or 'type' in c or 'product' in c or 'segment' in c), cat_cols[0] if cat_cols else None)

        x_axis = date_col if date_col != "None" else (df.index.name or "index")
        if x_axis == "index": df["index"] = df.index

        def make_fig(fig):
            fig.update_layout(**PLOT_LAYOUT)
            fig.update_traces(marker_line_width=0)
            return fig

        # ── GRAPH 1: Revenue Over Time ──
        if rev_col:
            st.markdown('<div class="section-label">Revenue Over Time</div>', unsafe_allow_html=True)
            if chart_type == "Bar":
                fig1 = px.bar(df, x=x_axis, y=rev_col, color_discrete_sequence=[COLORS[0]], title="Revenue Over Time")
            elif chart_type == "Area":
                fig1 = px.area(df, x=x_axis, y=rev_col, color_discrete_sequence=[COLORS[0]], title="Revenue Over Time")
            elif chart_type == "Scatter":
                fig1 = px.scatter(df, x=x_axis, y=rev_col, color_discrete_sequence=[COLORS[0]], title="Revenue Over Time")
            else:
                fig1 = px.line(df, x=x_axis, y=rev_col, color_discrete_sequence=[COLORS[0]], title="Revenue Over Time", markers=True)
            fig1.update_traces(line=dict(width=2.5))
            st.plotly_chart(make_fig(fig1), use_container_width=True)

        # ── GRAPH 2: Expenses Breakdown ──
        if exp_col:
            st.markdown('<div class="section-label">Expenses Over Time</div>', unsafe_allow_html=True)
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                if chart_type == "Bar":
                    fig2a = px.bar(df, x=x_axis, y=exp_col, color_discrete_sequence=[COLORS[2]], title="Expenses Over Time")
                else:
                    fig2a = px.line(df, x=x_axis, y=exp_col, color_discrete_sequence=[COLORS[2]], title="Expenses Over Time", markers=True)
                    fig2a.update_traces(line=dict(width=2.5))
                st.plotly_chart(make_fig(fig2a), use_container_width=True)

            with col_g2:
                if cat_col and exp_col:
                    try:
                        pie_data = df.groupby(cat_col)[exp_col].sum().reset_index()
                        fig2b = px.pie(pie_data, names=cat_col, values=exp_col,
                                      title="Expense by Category",
                                      color_discrete_sequence=COLORS,
                                      hole=0.45)
                        fig2b.update_traces(textposition='inside', textinfo='percent+label')
                        st.plotly_chart(make_fig(fig2b), use_container_width=True)
                    except:
                        st.info("Add a 'category' column to see expense breakdown by category!")
                else:
                    st.info("Add a 'category' column to your data to see a donut chart breakdown!")

        # ── GRAPH 3: Profit & Loss ──
        if rev_col and exp_col:
            st.markdown('<div class="section-label">Profit & Loss Analysis</div>', unsafe_allow_html=True)
            df["__pl__"] = df[rev_col] - df[exp_col]
            fig3 = go.Figure()
            fig3.add_trace(go.Bar(name="Revenue", x=df[x_axis], y=df[rev_col], marker_color=COLORS[0], opacity=0.85))
            fig3.add_trace(go.Bar(name="Expenses", x=df[x_axis], y=df[exp_col], marker_color=COLORS[2], opacity=0.85))
            if profit_col:
                fig3.add_trace(go.Scatter(name="Net Profit", x=df[x_axis], y=df[profit_col],
                                          mode='lines+markers', line=dict(color=COLORS[1], width=2.5),
                                          marker=dict(size=6)))
            else:
                fig3.add_trace(go.Scatter(name="Net Profit (calculated)", x=df[x_axis], y=df["__pl__"],
                                          mode='lines+markers', line=dict(color=COLORS[1], width=2.5, dash='dot'),
                                          marker=dict(size=6)))
            fig3.update_layout(barmode='group', title="Revenue vs Expenses vs Profit")
            st.plotly_chart(make_fig(fig3), use_container_width=True)

        # ── GRAPH 4: Cash Flow ──
        if cash_col:
            st.markdown('<div class="section-label">Cash Flow</div>', unsafe_allow_html=True)
            fig4 = px.area(df, x=x_axis, y=cash_col, title="Cash Flow Over Time",
                          color_discrete_sequence=[COLORS[1]])
            fig4.update_traces(line=dict(width=2.5), fill='tozeroy', fillcolor='rgba(0,200,255,0.08)')
            st.plotly_chart(make_fig(fig4), use_container_width=True)
        elif rev_col and exp_col:
            st.markdown('<div class="section-label">Estimated Cash Flow</div>', unsafe_allow_html=True)
            df["__cf__"] = df[rev_col].cumsum() - df[exp_col].cumsum()
            fig4 = px.area(df, x=x_axis, y="__cf__", title="Cumulative Cash Flow (Estimated)",
                          color_discrete_sequence=[COLORS[1]])
            fig4.update_traces(line=dict(width=2.5), fill='tozeroy', fillcolor='rgba(0,200,255,0.08)')
            st.plotly_chart(make_fig(fig4), use_container_width=True)

        # ── GRAPH 5: Sales by Category ──
        if cat_col and rev_col:
            st.markdown('<div class="section-label">Sales by Category</div>', unsafe_allow_html=True)
            col_g3, col_g4 = st.columns(2)
            with col_g3:
                try:
                    cat_data = df.groupby(cat_col)[rev_col].sum().reset_index().sort_values(rev_col, ascending=False)
                    fig5a = px.bar(cat_data, x=cat_col, y=rev_col, title="Revenue by Category",
                                  color=cat_col, color_discrete_sequence=COLORS)
                    st.plotly_chart(make_fig(fig5a), use_container_width=True)
                except:
                    pass
            with col_g4:
                try:
                    fig5b = px.pie(cat_data, names=cat_col, values=rev_col, title="Revenue Share by Category",
                                  color_discrete_sequence=COLORS, hole=0.4)
                    fig5b.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(make_fig(fig5b), use_container_width=True)
                except:
                    pass

        # ── GRAPH 6: All Metrics Together ──
        if len(num_cols) >= 2:
            st.markdown('<div class="section-label">Full Financial Overview</div>', unsafe_allow_html=True)
            selected_metrics = st.multiselect(
                "Select metrics to compare",
                num_cols,
                default=num_cols[:min(4, len(num_cols))],
                key="metrics_select"
            )
            if selected_metrics:
                fig6 = px.line(df, x=x_axis, y=selected_metrics,
                              title="Multi-Metric Financial Overview",
                              color_discrete_sequence=COLORS,
                              markers=True)
                fig6.update_traces(line=dict(width=2))
                st.plotly_chart(make_fig(fig6), use_container_width=True)

        # ── Raw Data Table ──
        st.markdown('<div class="section-label">Raw Data Preview</div>', unsafe_allow_html=True)
        st.dataframe(
            df.head(50).style.background_gradient(cmap='Greens', axis=0),
            use_container_width=True
        )

    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.info("Make sure your CSV/Excel has proper column headers and numeric data!")

else:
    st.markdown("""
    <div style="text-align:center;padding:4rem 2rem;color:rgba(232,244,240,0.2);">
        <div style="font-size:3rem;margin-bottom:1rem;animation:float 3s ease-in-out infinite;">📊</div>
        <div style="font-size:1.1rem;font-weight:700;color:rgba(232,244,240,0.35);margin-bottom:0.5rem;">
            Upload your financial data to see graphs</div>
        <div style="font-family:'DM Mono',monospace;font-size:0.72rem;color:rgba(232,244,240,0.18);line-height:1.7;">
            Your CSV should have columns like:<br>
            Date · Revenue · Expenses · Profit · Cash Flow · Category · Sales
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="margin-top:3rem;text-align:center;font-family:'DM Mono',monospace;
    font-size:0.52rem;letter-spacing:0.2em;color:rgba(232,244,240,0.07);">
</div>
""", unsafe_allow_html=True)