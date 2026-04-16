import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
from core.auth import sign_out
from core.session import restore_session
from core.theme import inject_theme, get_theme

if "owner_name" not in st.session_state:
    uid = st.query_params.get("uid")
    if uid:
        restore_session(uid)

if st.session_state.get("user_id"):
    st.query_params["uid"] = st.session_state["user_id"]

st.set_page_config(page_title="Finova · Graphs", layout="wide")

if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"
mode = st.session_state["theme"]
t = get_theme(mode)

if "owner_name" not in st.session_state:
    st.markdown(inject_theme(mode), unsafe_allow_html=True)
    st.markdown(f"""
    <div style="max-width:420px;margin:6rem auto;background:{t['card_bg']};border:1px solid {t['card_border']};border-radius:16px;padding:2.5rem 2rem;text-align:center;">
        <div style="font-size:1.1rem;font-weight:600;color:{t['text']};margin-bottom:0.5rem;">Sign in required</div>
        <div style="font-size:0.85rem;color:{t['text_muted']};margin-bottom:1.5rem;">Please sign in to access your graphs.</div>
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

# Plotly theme
PLOT_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(255,255,255,0.02)',
    font=dict(family='-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif', color='rgba(232,244,240,0.7)', size=12),
    xaxis=dict(gridcolor='rgba(82,183,136,0.08)', linecolor='rgba(82,183,136,0.12)', tickfont=dict(size=11)),
    yaxis=dict(gridcolor='rgba(82,183,136,0.08)', linecolor='rgba(82,183,136,0.12)', tickfont=dict(size=11)),
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='rgba(232,244,240,0.6)')),
)
COLORS = ['#52b788','#74c69d','#b7e4c7','#40916c','#2d6a4f','#95d5b2']

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
    if st.button("AI CFO", key="nav_chat"):
        st.switch_page("pages/1_Chat.py")
    if st.button("Switch account", key="nav_switch"):
        sign_out()
        st.query_params.clear()
        for k in ["user_id", "owner_name", "business_name", "business_type", "messages", "total_queries", "uploaded_files"]:
            st.session_state.pop(k, None)
        st.switch_page("app.py")

    st.markdown(f"""
    <div style="margin: 1.5rem 0; height: 1px; background: {t['divider']};"></div>
    """, unsafe_allow_html=True)

    if st.button(t['toggle_label'], key="theme_toggle"):
        st.session_state["theme"] = "light" if mode == "dark" else "dark"
        st.rerun()

# Header
st.markdown(f"""
<div class="page-title">Financial Graphs</div>
<div class="page-sub">{business_name} · Visual data dashboard.</div>
""", unsafe_allow_html=True)

# Upload
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
    if uploaded.size > 15 * 1024 * 1024:
        st.warning("File too large. Maximum size is 15MB.")
        st.stop()
    try:
        if uploaded.name.endswith(".csv"):
            df = pd.read_csv(uploaded)
        else:
            # Try to find the real header row — skip rows until we find one with mostly non-null values
            raw = pd.read_excel(uploaded, header=None)
            header_row = 0
            for i, row in raw.iterrows():
                non_null = row.notna().sum()
                if non_null >= max(2, len(raw.columns) * 0.4):
                    header_row = i
                    break
            df = pd.read_excel(uploaded, header=header_row)

        # Clean column names
        df.columns = [
            str(c).strip().lower().replace(" ", "_").replace("/", "_").replace("-", "_")
            for c in df.columns
        ]
        # Drop fully unnamed columns (e.g. "unnamed:_0", "unnamed:_1")
        df = df.loc[:, ~df.columns.str.match(r'^unnamed')]
        # Drop rows where all values are null
        df = df.dropna(how="all").reset_index(drop=True)
        # Convert any obvious numeric columns stored as strings
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="ignore")

        if df.empty or len(df.columns) < 2:
            st.error("Couldn't read usable data from this file. Make sure it has clear column headers and at least 2 columns.")
            st.stop()

        st.success(f"✓ {uploaded.name} loaded — {len(df)} rows, {len(df.columns)} columns")

        # Show columns detected
        st.markdown(f"""
        <div class="insight-strip">
            <strong>Columns detected:</strong> {', '.join(df.columns.tolist())}
        </div>
        """, unsafe_allow_html=True)

        # Filters
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

        # Auto-detect columns
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

        # GRAPH 1: Revenue Over Time
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

        # GRAPH 2: Expenses Breakdown
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

        # GRAPH 3: Profit & Loss
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

        # GRAPH 4: Cash Flow
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

        # GRAPH 5: Sales by Category
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

        # GRAPH 6: All Metrics Together
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

        # Raw Data Table
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
        <div style="font-size:3rem;margin-bottom:1rem;">📊</div>
        <div style="font-size:1.1rem;font-weight:700;color:rgba(232,244,240,0.35);margin-bottom:0.5rem;">
            Upload your financial data to see graphs</div>
        <div style="font-size:0.72rem;color:rgba(232,244,240,0.18);line-height:1.7;">
            Your CSV should have columns like:<br>
            Date · Revenue · Expenses · Profit · Cash Flow · Category · Sales
        </div>
    </div>
    """, unsafe_allow_html=True)
