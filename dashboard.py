import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Electricity Supply Risk Prediction Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Samsung & Sky Blue Theme CSS (Layout Strictly Maintained) ───────────────
st.markdown("""
<style>
  /* Font */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #EEF6FB; /* Light Sky Blue BG */
  }

  /* Hide streamlit chrome */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 0 !important; max-width: 100% !important; }

  /* ── Global Nav (Dark Navy) ── */
  .global-nav {
    background: #1A2744; /* Dark Navy */
    padding: 0 32px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 1000;
  }
  .nav-brand {
    font-size: 18px;
    font-weight: 600;
    color: #FFFFFF;
    letter-spacing: -0.12px;
  }
  .nav-meta {
    font-size: 12px;
    color: #B0DEF0;
    letter-spacing: -0.12px;
  }

  /* ── Hero Section (Samsung Blue) ── */
  .hero-section {
    background: #1557C0; /* Samsung Blue */
    padding: 64px 48px 48px;
    text-align: center;
  }
  .hero-title {
    font-size: 36px;
    font-weight: 600;
    color: #FFFFFF;
    letter-spacing: -0.28px;
    line-height: 1.07;
    margin: 0 0 12px;
  }
  .hero-subtitle {
    font-size: 21px;
    font-weight: 400;
    color: #B0DEF0;
    letter-spacing: 0;
    line-height: 1.19;
    margin: 0 0 32px;
  }
  .hero-date-pill {
    display: inline-block;
    background: transparent;
    border: 1px solid #B0DEF0;
    color: #B0DEF0;
    font-size: 14px;
    font-weight: 400;
    padding: 8px 22px;
    border-radius: 9999px;
    letter-spacing: -0.224px;
  }

  /* ── Sub-Nav ── */
  .sub-nav {
    background: rgba(238, 246, 251, 0.85); /* Frosted Sky */
    backdrop-filter: saturate(180%) blur(20px);
    -webkit-backdrop-filter: saturate(180%) blur(20px);
    border-bottom: 1px solid rgba(21, 87, 192, 0.08);
    padding: 0 48px;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 44px;
    z-index: 999;
  }
  .sub-nav-title {
    font-size: 21px;
    font-weight: 600;
    color: #1A2744;
    letter-spacing: 0.231px;
  }
  .sub-nav-meta {
    font-size: 14px;
    font-weight: 400;
    color: #1557C0;
    letter-spacing: -0.224px;
  }

  /* ── Section tiles ── */
  .tile-light {
    background: #FFFFFF;
    padding: 32px 64px;
  }
  .tile-parchment {
    background: #EEF6FB;
    padding: 64px 64px;
  }
  .tile-dark {
    background: #1A2744;
    padding: 64px 64px;
  }
  .tile-dark-2 {
    background: #1c2a4a;
    padding: 64px 64px;
  }

  /* ── Section Headlines ── */
  .section-headline {
    font-size: 26px;
    font-weight: 600;
    color: #1A2744;
    letter-spacing: 0;
    line-height: 1.10;
    margin: 0 0 8px;
    text-align: center;
  }
  .section-headline-dark {
    font-size: 40px;
    font-weight: 600;
    color: #FFFFFF;
    letter-spacing: 0;
    line-height: 1.10;
    margin: 0 0 8px;
    text-align: center;
  }
  .section-tagline {
    font-size: 15px;
    font-weight: 400;
    color: #1A2744;
    letter-spacing: 0;
    line-height: 1.4;
    text-align: center;
    margin: 0 0 48px;
  }

  /* ── Forecast Weather Row ── */
  .forecast-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 12px;
    margin: 0 5%;
  }
  .forecast-card {
    background: #1A2744;
    border-radius: 18px;
    padding: 20px 12px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.06);
  }
  .forecast-card.danger { border-color: rgba(255, 59, 48, 0.35); background: #2d1616; }
  .forecast-card.caution { border-color: rgba(245, 166, 35, 0.35); background: #2d2610; }
  .forecast-card.safe { border-color: rgba(52, 199, 89, 0.35); background: #122415; }
  .forecast-date { font-size: 13px; font-weight: 600; color: #B0DEF0; margin-bottom: 10px; }
  .forecast-pct { font-size: 22px; font-weight: 700; margin-bottom: 4px; }
  .forecast-pct.danger { color: #ff3b30; }
  .forecast-pct.caution { color: #F5A623; } /* Orange Accent */
  .forecast-pct.safe { color: #34c759; }
  .forecast-label { font-size: 11px; font-weight: 400; color: #B0DEF0; }

  /* ── KPI Metric Cards ── */
  .kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin: 0 0 48px;
  }
  .kpi-card {
    background: #FFFFFF;
    border: 1px solid #DAEEF8;
    border-radius: 18px;
    padding: 24px;
    text-align: center;
  }
  .kpi-label { font-size: 13px; font-weight: 400; color: #1557C0; margin-bottom: 8px; }
  .kpi-value { font-size: 34px; font-weight: 600; color: #1A2744; line-height: 1.47; }

  /* ── Simulation Box ── */
  .sim-box {
    background: #1A2744;
    border-radius: 18px;
    padding: 36px 40px;
    border: 1px solid rgba(255,255,255,0.06);
  }
  .sim-title { font-size: 21px; font-weight: 600; color: #FFFFFF; margin-bottom: 24px; }
  .sim-row { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 14px; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 14px; }
  .sim-key { font-size: 15px; color: #B0DEF0; }
  .sim-val { font-size: 22px; font-weight: 600; color: #FFFFFF; }
  .sim-val.red { color: #ff3b30; }
  .sim-val.green { color: #34c759; }

  .recommend-pill {
    background: #1557C0;
    color: #FFFFFF;
    padding: 11px 22px;
    border-radius: 9999px;
    margin-top: 24px;
  }

  /* ── NDBI Card ── */
  .ndbi-card {
    background: #FFFFFF;
    border-radius: 18px;
    padding: 36px 40px;
    border: 1px solid #DAEEF8;
  }
  .ndbi-title { font-size: 21px; font-weight: 600; color: #1A2744; margin-bottom: 24px; }
  .ndbi-row { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 14px; border-bottom: 1px solid rgba(0,0,0,0.06); padding-bottom: 14px; }
  .ndbi-key { font-size: 15px; color: #1557C0; }
  .ndbi-val { font-size: 22px; font-weight: 600; color: #1A2744; }
  .ndbi-val.blue { color: #1557C0; }

  /* ── Progress Bar ── */
  .progress-wrap { background: #DAEEF8; border-radius: 9999px; height: 8px; overflow: hidden; margin-top: 8px; }
  .progress-fill { height: 100%; border-radius: 9999px; background: #1557C0; }
  .progress-fill.green { background: #34c759; }

  /* ── Footer ── */
  .apple-footer {
    background: #EEF6FB;
    padding: 40px 48px 24px;
    border-top: 1px solid #DAEEF8;
  }
  .footer-body { font-size: 12px; color: #1557C0; text-align: center; }

  /* ── Selector & Slider ── */
  div[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border: 1px solid #DAEEF8 !important;
    border-radius: 9999px !important;
    color: #1A2744 !important;
  }
  .stSlider > div > div > div > div { background: #1557C0 !important; }
</style>
""", unsafe_allow_html=True)

# ─── Data ────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('dashboard_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()
INSURANCE_COVERAGE = 0.35
TRIGGER_THRESHOLD  = 0.70

# ─── Derived values ───────────────────────────────────────────────────────────
total_saving  = df['saving_억'].sum()
avg_lolp      = df['prob_lolp'].mean()
peak_row      = df.loc[df['prob_lolp'].idxmax()]
danger_days   = (df['risk_level'] == 2).sum()
caution_days  = (df['risk_level'] == 1).sum()
safe_days     = (df['risk_level'] == 0).sum()
trigger_days  = (df['prob_lolp'] >= TRIGGER_THRESHOLD).sum()
trigger_rate  = trigger_days / len(df)
ndbi_payout   = round(df.loc[df['prob_lolp'] >= TRIGGER_THRESHOLD, 'saving_억'].sum() * INSURANCE_COVERAGE, 1)
color_map     = {0: '#34c759', 1: '#F5A623', 2: '#ff3b30'} # Updated Caution to Orange

P = 0.1 

# ─── Global Nav ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="global-nav">
  <span class="nav-brand">SST-Electricity Risk Management</span>
  <span class="nav-meta">XGBoost LOLP Prediction · Enterprise Loss Simulation</span>
</div>
""", unsafe_allow_html=True)

# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-section">
  <span class="hero-title">Electricity Supply Risk Prediction Dashboard</span>
  <span class="hero-subtitle"><br>2024.07.01 — 2024.07.14 · 14-Day Analysis</span>
</div>
""", unsafe_allow_html=True)

# ─── KPI Strip ────────────────────────────────────────────────────────────────
st.markdown('<div class="tile-light">', unsafe_allow_html=True)
st.markdown('<div class="section-headline">Key Metrics Summary</div>', unsafe_allow_html=True)
_lp, _mid, _rp = st.columns([P, 1 - P * 2, P])
with _mid:
    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi-card"><div class="kpi-label">Average LOLP</div><div class="kpi-value">{avg_lolp:.0%}</div></div>
      <div class="kpi-card"><div class="kpi-label">High Risk Days</div><div class="kpi-value" style="color:#ff3b30">{danger_days}d</div></div>
      <div class="kpi-card"><div class="kpi-label">Total Reducible Loss</div><div class="kpi-value" style="color:#1557C0">₩{total_saving:.0f}B</div></div>
      <div class="kpi-card"><div class="kpi-label">Peak Risk Day</div><div class="kpi-value">{peak_row['date'].strftime('%m/%d')}</div></div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ─── 7-Day Forecast + LOLP Chart ──────────────────────────────────────────────
st.markdown('<div class="tile-light">', unsafe_allow_html=True)
st.markdown('<div class="section-headline">Power Risk Forecast</div>', unsafe_allow_html=True)
forecast_7 = df.head(7)
cards_html = '<div class="forecast-grid">'
for _, row in forecast_7.iterrows():
    level_cls = {2: 'danger', 1: 'caution', 0: 'safe'}[row['risk_level']]
    cards_html += f"""
    <div class="forecast-card {level_cls}">
      <div class="forecast-date">{row['date'].strftime('%m/%d')}</div>
      <span class="forecast-emoji">{row['risk_emoji']}</span>
      <div class="forecast-pct {level_cls}">{row['prob_lolp']:.0%}</div>
      <div class="forecast-label">{row['risk_name']}</div>
    </div>"""
cards_html += '</div>'
st.markdown(cards_html, unsafe_allow_html=True)

fig_lolp = go.Figure(go.Bar(x=df['date'].dt.strftime('%m/%d'), y=df['prob_lolp'], marker_color=[color_map[l] for l in df['risk_level']]))
fig_lolp.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#ffffff', height=280, showlegend=False)
_lp, _mid, _rp = st.columns([P, 1 - P * 2, P])
with _mid: st.plotly_chart(fig_lolp, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ─── Enterprise Loss Simulation ───────────────────────────────────────────────
st.markdown('<div class="tile-light">', unsafe_allow_html=True)
st.markdown('<div class="section-headline">Enterprise Loss Simulation</div>', unsafe_allow_html=True)
_lp, _sim_pad, col_sel, col_info, _rp = st.columns([P, 0.05, 1.45, 3.2, P])
with col_sel:
    selected_idx = st.selectbox("Date", range(len(df)), format_func=lambda i: df.iloc[i]['date'].strftime('%m/%d'), index=int(df['prob_lolp'].idxmax()))
selected = df.iloc[selected_idx]

_lp, _sim_pad, col_sim, col_chart, _rp = st.columns([P, 0.05, 1, 1, P])
with col_sim:
    st.markdown(f"""
    <div class="sim-box">
      <div class="sim-title">Risk: {selected['prob_lolp']:.0%}</div>
      <div class="sim-row"><span class="sim-key">Maintain Loss</span><span class="sim-val red">₩{selected['maintain_loss_억']:.1f}B</span></div>
      <div class="sim-row"><span class="sim-key">Recommended Loss</span><span class="sim-val green">₩{selected['optimal_loss_억']:.1f}B</span></div>
      <div class="sim-row"><span class="sim-key">Savings Effect</span><span class="sim-val" style="color:#F5A623">₩{selected['saving_억']:.1f}B</span></div>
    </div>
    """, unsafe_allow_html=True)
with col_chart:
    fig_loss = go.Figure(data=[
        go.Bar(name='Maintain', x=df['date'].dt.strftime('%m/%d'), y=df['maintain_loss_억'], marker_color='#ff3b30'),
        go.Bar(name='Follow', x=df['date'].dt.strftime('%m/%d'), y=df['optimal_loss_억'], marker_color='#34c759')
    ])
    fig_loss.update_layout(barmode='group', height=340, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_loss, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ─── Optimal Production Recommendation ───────────────────────────────────────
st.markdown('<div class="tile-light">', unsafe_allow_html=True)
st.markdown('<div class="section-headline">Optimal Production Recommendation</div>', unsafe_allow_html=True)
_lp, col_prod, col_cum, _rp = st.columns([P, 1, 1, P])
with col_prod:
    fig_prod = go.Figure(go.Scatter(x=df['date'].dt.strftime('%m/%d'), y=df['optimal_production'], mode='lines+markers', line=dict(color='#1557C0')))
    fig_prod.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#1A2744')
    st.plotly_chart(fig_prod, use_container_width=True)
with col_cum:
    fig_cum = go.Figure(go.Scatter(x=df['date'].dt.strftime('%m/%d'), y=df['saving_억'].cumsum(), fill='tozeroy', line=dict(color='#34c759')))
    fig_cum.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#1A2744')
    st.plotly_chart(fig_cum, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ─── NDBI Insurance Payout Estimation ─────────────────────────────────────────
st.markdown('<div class="tile-light">', unsafe_allow_html=True)
st.markdown('<div class="section-headline">NDBI Insurance Payout Estimation</div>', unsafe_allow_html=True)
_lp, col_ndbi, col_ndbi2, _rp = st.columns([P, 1, 1, P])
with col_ndbi:
    st.markdown(f"""
    <div class="ndbi-card">
      <div class="ndbi-title">Payout Summary</div>
      <div class="ndbi-row"><span class="ndbi-key">Est. Payout</span><span class="ndbi-val blue">₩{ndbi_payout:.1f}B</span></div>
      <div class="progress-wrap"><div class="progress-fill" style="width:{(ndbi_payout/total_saving)*100}%"></div></div>
    </div>
    """, unsafe_allow_html=True)
with col_ndbi2:
    fig_ndbi = go.Figure(go.Scatter(x=df['prob_lolp'], y=df['saving_억'], mode='markers', marker=dict(size=14, color=[color_map[l] for l in df['risk_level']])))
    fig_ndbi.update_layout(height=480, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_ndbi, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ─── Footer ───
st.markdown('<div class="apple-footer"><div class="footer-body">XGBoost LOLP Prediction Model · Samsung Energy AI</div></div>', unsafe_allow_html=True)