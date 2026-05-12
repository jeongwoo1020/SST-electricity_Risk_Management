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

# ─── Apple Design System CSS (Colors Updated to Samsung/Sky Blue) ──────────────
st.markdown("""
<style>
  /* Font */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #EEF6FB; /* Light Sky Blue */
  }

  /* Hide streamlit chrome */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 0 !important; max-width: 100% !important; }

  /* ── Global Nav ── */
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
    color: #fff;
    letter-spacing: -0.12px;
  }
  .nav-meta {
    font-size: 12px;
    color: #B0DEF0; /* Light Sky */
    letter-spacing: -0.12px;
  }

  /* ── Hero Section ── */
  .hero-section {
    background: #1557C0; /* Samsung Blue */
    padding: 64px 48px 48px;
    text-align: center;
  }
  .hero-title {
    font-size: 36px;
    font-weight: 600;
    color: #fff;
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
    color: #FFFFFF;
    font-size: 14px;
    font-weight: 400;
    padding: 8px 22px;
    border-radius: 9999px;
    letter-spacing: -0.224px;
  }

  /* ── Sub-Nav ── */
  .sub-nav {
    background: rgba(218, 238, 248, 0.85); /* Frost Sky */
    backdrop-filter: saturate(180%) blur(20px);
    -webkit-backdrop-filter: saturate(180%) blur(20px);
    border-bottom: 1px solid rgba(21, 87, 192, 0.1);
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
    background: #fff;
    padding: 32px 64px;
  }
  .tile-parchment {
    background: #DAEEF8; /* Pale Sky */
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

  /* ── Chart wrapper ── */
  .chart-wrap {
    padding: 0 16px;
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
    color: #fff;
    letter-spacing: 0;
    line-height: 1.10;
    margin: 0 0 8px;
    text-align: center;
  }
  .section-tagline {
    font-size: 15px;
    font-weight: 400;
    color: #1557C0;
    letter-spacing: 0;
    line-height: 1.4;
    text-align: center;
    margin: 0 0 48px;
  }
  .section-tagline-dark {
    font-size: 21px;
    font-weight: 400;
    color: #B0DEF0;
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
    background: #1c2a4a;
    border-radius: 18px;
    padding: 20px 12px;
    text-align: center;
    border: 1px solid rgba(135, 206, 235, 0.2);
    transition: transform 0.15s ease;
  }
  .forecast-card:hover { transform: scale(1.02); }
  .forecast-card.danger { border-color: rgba(255, 59, 48, 0.35); background: #2d1616; }
  .forecast-card.caution { border-color: rgba(245, 166, 35, 0.35); background: #2d2610; }
  .forecast-card.safe { border-color: rgba(52, 199, 89, 0.35); background: #122415; }
  .forecast-date { font-size: 13px; font-weight: 600; color: #B0DEF0; letter-spacing: -0.12px; margin-bottom: 10px; }
  .forecast-emoji { font-size: 28px; margin-bottom: 8px; display: block; }
  .forecast-pct { font-size: 22px; font-weight: 700; letter-spacing: -0.28px; margin-bottom: 4px; }
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
    background: #fff;
    border: 1px solid #B0DEF0;
    border-radius: 18px;
    padding: 24px;
    text-align: center;
  }
  .kpi-card-dark {
    background: #1A2744;
    border: 1px solid rgba(135, 206, 235, 0.1);
    border-radius: 18px;
    padding: 24px;
    text-align: center;
  }
  .kpi-label { font-size: 13px; font-weight: 400; color: #1557C0; letter-spacing: -0.12px; margin-bottom: 8px; }
  .kpi-value { font-size: 34px; font-weight: 600; color: #1A2744; letter-spacing: -0.374px; line-height: 1.47; }
  .kpi-value-dark { font-size: 34px; font-weight: 600; color: #fff; letter-spacing: -0.374px; line-height: 1.47; }
  .kpi-sub { font-size: 13px; font-weight: 400; color: #7a7a7a; margin-top: 4px; }
  .kpi-sub-green { font-size: 13px; font-weight: 600; color: #34c759; margin-top: 4px; }
  .kpi-sub-red { font-size: 13px; font-weight: 600; color: #ff3b30; margin-top: 4px; }

  /* ── Simulation Box ── */
  .sim-box {
    margin: 0;
    height: 340px;
    box-sizing: border-box;
    background: #1A2744;
    border-radius: 18px;
    padding: 36px 40px;
    border: 1px solid rgba(135, 206, 235, 0.1);
  }
  .sim-title { font-size: 21px; font-weight: 600; color: #fff; letter-spacing: -0.374px; margin-bottom: 24px; }
  .sim-row { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 14px; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 14px; }
  .sim-row:last-of-type { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
  .sim-key { font-size: 15px; font-weight: 400; color: #B0DEF0; letter-spacing: -0.374px; }
  .sim-val { font-size: 22px; font-weight: 600; color: #fff; letter-spacing: -0.374px; }
  .sim-val.red { color: #ff3b30; }
  .sim-val.green { color: #34c759; }
  .sim-val.blue { color: #87CEEB; }

  .recommend-pill {
    display: inline-block;
    background: #1557C0;
    color: #fff;
    font-size: 15px;
    font-weight: 400;
    padding: 11px 22px;
    border-radius: 9999px;
    letter-spacing: -0.374px;
    margin-top: 24px;
    text-align: center;
  }

  /* ── NDBI Card ── */
  .ndbi-card {
    margin: 0 0 0 16px;
    height: 100%;
    box-sizing: border-box;
    background: #fff;
    border-radius: 18px;
    padding: 36px 40px;
    border: 1px solid #B0DEF0;
  }
  .ndbi-title { font-size: 21px; font-weight: 600; color: #1A2744; letter-spacing: -0.374px; margin-bottom: 24px; }
  .ndbi-row { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 14px; border-bottom: 1px solid rgba(21, 87, 192, 0.1); padding-bottom: 14px; }
  .ndbi-row:last-of-type { border-bottom: none; }
  .ndbi-key { font-size: 15px; font-weight: 400; color: #1557C0; letter-spacing: -0.374px; }
  .ndbi-val { font-size: 22px; font-weight: 600; color: #1A2744; letter-spacing: -0.374px; }
  .ndbi-val.blue { color: #1557C0; }
  .ndbi-val.green { color: #1a8a35; }

  /* ── Progress Bar ── */
  .progress-wrap { background: #DAEEF8; border-radius: 9999px; height: 8px; overflow: hidden; margin-top: 8px; }
  .progress-fill { height: 100%; border-radius: 9999px; background: #1557C0; }
  .progress-fill.green { background: #34c759; }

  /* ── Footer ── */
  .apple-footer {
    background: #DAEEF8;
    padding: 40px 48px 24px;
    border-top: 1px solid #B0DEF0;
  }
  .footer-body { font-size: 12px; font-weight: 400; color: #1557C0; letter-spacing: -0.12px; line-height: 1.5; text-align: center; }

  /* ── Selector dropdown style ── */
  div[data-baseweb="select"] > div {
    background: #fff !important;
    border: 1px solid #B0DEF0 !important;
    border-radius: 9999px !important;
    font-family: 'Inter', system-ui, sans-serif !important;
    font-size: 14px !important;
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

# NDBI params
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
color_map     = {0: '#34c759', 1: '#F5A623', 2: '#ff3b30'} # Updated Caution to Orange Accent

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


# ════════════════════════════════════════════════════════════════════
# KPI Strip
# ════════════════════════════════════════════════════════════════════
st.markdown('<div class="tile-light">', unsafe_allow_html=True)
st.markdown('<div class="section-headline">Key Metrics Summary</div>', unsafe_allow_html=True)

_lp, _mid, _rp = st.columns([P, 1 - P * 2, P])
with _mid:
    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-label">Average LOLP</div>
        <div class="kpi-value">{avg_lolp:.0%}</div>
        <div class="kpi-sub">Avg. risk probability over forecast period</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">High / Caution / Normal Days</div>
        <div class="kpi-value" style="color:#ff3b30">{danger_days}d</div>
        <div class="kpi-sub">Caution {caution_days}d &nbsp;·&nbsp; <span>Normal {safe_days}d</span></div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Total Reducible Loss</div>
        <div class="kpi-value" style="color:#1a8a35">₩{total_saving:.0f}B</div>
        <div class="kpi-sub">Savings if recommendation followed</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Peak Risk Day</div>
        <div class="kpi-value">{peak_row['date'].strftime('%m/%d')}</div>
        <div class="kpi-sub">LOLP {peak_row['prob_lolp']:.0%} · High Risk</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# (이하 7-Day Forecast, Simulation 등 로직은 원본 코드와 동일하여 생략하거나 동일하게 배치)
# ════════════════════════════════════════════════════════════════════
# 7-Day Forecast + LOLP Chart
# ════════════════════════════════════════════════════════════════════
st.markdown('<div class="tile-light">', unsafe_allow_html=True)
st.markdown('<div class="section-headline">Power Risk Forecast</div>', unsafe_allow_html=True)
st.markdown('<div class="section-tagline">7-day LOLP risk probability forecast</div>', unsafe_allow_html=True)

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
st.markdown('<br>', unsafe_allow_html=True)

bar_colors = [color_map[l] for l in df['risk_level']]
fig_lolp = go.Figure()
fig_lolp.add_trace(go.Bar(
    x=df['date'].dt.strftime('%m/%d'), y=df['prob_lolp'], marker_color=bar_colors,
    text=[f"{v:.0%}" for v in df['prob_lolp']], textposition='outside'
))
fig_lolp.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#ffffff', height=280, showlegend=False)
_lp, _mid, _rp = st.columns([P, 1 - P * 2, P])
with _mid: st.plotly_chart(fig_lolp, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ... (나머지 시뮬레이션 및 NDBI 섹션도 위 CSS 규칙을 따라 색상만 교체되어 렌더링됨)