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

# ─── Color & CSS Update (Layout strictly maintained) ───────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    background: linear-gradient(to bottom, #DAEEF8, #EEF6FB); /* Slide BG (body) */
  }

  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 0 !important; max-width: 100% !important; }

  /* ── Global Nav (Dark Navy) ────────────────────────────────────────────── */
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
    color: #FFFFFF; /* Light text */
    letter-spacing: -0.12px;
  }
  .nav-meta {
    font-size: 12px;
    color: #B0DEF0;
    letter-spacing: -0.12px;
  }

  /* ── Hero Section (Sky Blue Gradient) ──────────────────────────────────── */
  .hero-section {
    background: linear-gradient(135deg, #87CEEB, #B0DEF0); /* Sky Blue Gradient */
    padding: 64px 48px 48px;
    text-align: center;
  }
  .hero-title {
    font-size: 36px;
    font-weight: 600;
    color: #1A2744; /* Dark Navy for readability */
    letter-spacing: -0.28px;
    line-height: 1.07;
    margin: 0 0 12px;
  }
  .hero-subtitle {
    font-size: 21px;
    font-weight: 400;
    color: #1557C0; /* Samsung Blue */
    letter-spacing: 0;
    line-height: 1.19;
    margin: 0 0 32px;
  }
  .hero-date-pill {
    display: inline-block;
    background: transparent;
    border: 1px solid #1557C0;
    color: #1557C0;
    font-size: 14px;
    font-weight: 400;
    padding: 8px 22px;
    border-radius: 9999px;
  }

  /* ── Sub-Nav ────────────────────────────────────────────────────────────── */
  .sub-nav {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: saturate(180%) blur(20px);
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
  }

  /* ── Section Tiles (White Background + Blue Divider) ────────────────────── */
  .tile-light, .tile-parchment {
    background: #FFFFFF; /* 배경은 흰 배경 */
    padding: 32px 64px;
    border-top: 4px solid #1557C0; /* Section divider line */
    margin-bottom: 2px;
  }
  .tile-dark {
    background: #1A2744;
    padding: 64px 64px;
    border-top: 4px solid #1557C0;
  }

  /* ── Section Headlines ───────────────────────────────────────────────────── */
  .section-headline {
    font-size: 26px;
    font-weight: 600;
    color: #1A2744;
    text-align: center;
    margin: 0 0 8px;
  }
  .section-tagline {
    font-size: 15px;
    color: #1557C0;
    text-align: center;
    margin: 0 0 48px;
  }

  /* ── Forecast & KPI ──────────────────────────────────────────────────────── */
  .forecast-card {
    background: #FFFFFF;
    border-radius: 18px;
    padding: 20px 12px;
    text-align: center;
    border: 1px solid #E2E8F0;
  }
  .forecast-card.danger { border-color: #FF3B30; }
  .forecast-card.caution { border-color: #F5A623; } /* Orange accent */
  .forecast-card.safe { border-color: #34C759; }
  .forecast-pct.caution { color: #F5A623; }

  .kpi-card {
    background: #fff;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 24px;
    text-align: center;
  }
  .kpi-value { font-size: 34px; font-weight: 600; color: #1557C0; }

  /* ── Simulation & NDBI ───────────────────────────────────────────────────── */
  .sim-box {
    background: #1A2744;
    border-radius: 18px;
    padding: 36px 40px;
    border: 1px solid #1557C0;
  }
  .sim-val.green { color: #34C759; }
  .sim-val.blue { color: #87CEEB; }

  .ndbi-card {
    background: #fff;
    border-radius: 18px;
    padding: 36px 40px;
    border: 1px solid #1557C0;
  }
  .ndbi-val.blue { color: #1557C0; }

  .progress-fill.green { background: #34C759; }
  .progress-fill { background: #1557C0; }

</style>
""", unsafe_allow_html=True)

# ─── Data (Same as original) ────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('dashboard_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()
INSURANCE_COVERAGE = 0.35
TRIGGER_THRESHOLD  = 0.70

# ─── Derived Values ─────────────────────────────────────────────────────────
total_saving  = df['saving_억'].sum()
avg_lolp      = df['prob_lolp'].mean()
peak_row      = df.loc[df['prob_lolp'].idxmax()]
danger_days   = (df['risk_level'] == 2).sum()
caution_days  = (df['risk_level'] == 1).sum()
safe_days     = (df['risk_level'] == 0).sum()
trigger_days  = (df['prob_lolp'] >= TRIGGER_THRESHOLD).sum()
trigger_rate  = trigger_days / len(df)
ndbi_payout   = round(df.loc[df['prob_lolp'] >= TRIGGER_THRESHOLD, 'saving_억'].sum() * INSURANCE_COVERAGE, 1)
color_map     = {0: '#34c759', 1: '#F5A623', 2: '#ff3b30'} # Orange for Caution

P = 0.1 

# ─── Global Nav ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="global-nav">
  <span class="nav-brand">SAMSUNG ENERGY AI</span>
  <span class="nav-meta">XGBoost LOLP Prediction · Enterprise Risk</span>
</div>
""", unsafe_allow_html=True)

# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-section">
  <span class="hero-title">Electricity Supply Risk Prediction</span>
  <span class="hero-subtitle"><br>Dynamic Analysis for Sustainable Energy</span>
</div>
""", unsafe_allow_html=True)

# ─── KPI Strip ────────────────────────────────────────────────────────────────
st.markdown('<div class="tile-light">', unsafe_allow_html=True)
st.markdown('<div class="section-headline">Key Metrics Summary</div>', unsafe_allow_html=True)
_lp, _mid, _rp = st.columns([P, 1 - P * 2, P])
with _mid:
    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-label">Average LOLP</div>
        <div class="kpi-value">{avg_lolp:.0%}</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">High Risk Days</div>
        <div class="kpi-value" style="color:#ff3b30">{danger_days}d</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Total Reducible Loss</div>
        <div class="kpi-value" style="color:#1557C0">₩{total_saving:.0f}B</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Peak Risk Day</div>
        <div class="kpi-value">{peak_row['date'].strftime('%m/%d')}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ─── Forecast Section ────────────────────────────────────────────────────────
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

# Plotly Chart (Using Samsung Blue colors)
bar_colors = [color_map[l] for l in df['risk_level']]
fig_lolp = go.Figure(go.Bar(x=df['date'].dt.strftime('%m/%d'), y=df['prob_lolp'], marker_color=bar_colors))
fig_lolp.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='white', height=280, showlegend=False)
_lp, _mid, _rp = st.columns([P, 1 - P * 2, P])
with _mid: st.plotly_chart(fig_lolp, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ─── Simulation Section ───────────────────────────────────────────────────────
st.markdown('<div class="tile-light">', unsafe_allow_html=True)
st.markdown('<div class="section-headline">Enterprise Loss Simulation</div>', unsafe_allow_html=True)
_lp, _sim_pad, col_sel, col_info, _rp = st.columns([P, 0.05, 1.45, 3.2, P])
with col_sel:
    selected_idx = st.selectbox("Select Date", range(len(df)), format_func=lambda i: df.iloc[i]['date'].strftime('%m/%d'), index=0)
selected = df.iloc[selected_idx]

_lp, _sim_pad, col_sim, col_chart, _rp = st.columns([P, 0.05, 1, 1, P])
with col_sim:
    st.markdown(f"""
    <div class="sim-box">
      <div class="sim-title" style="color:#FFF">Risk Probability: {selected['prob_lolp']:.0%}</div>
      <div class="sim-row"><span class="sim-key">Maintain Loss</span><span class="sim-val red">₩{selected['maintain_loss_억']:.1f}B</span></div>
      <div class="sim-row"><span class="sim-key">Savings Effect</span><span class="sim-val" style="color:#F5A623">₩{selected['saving_억']:.1f}B</span></div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ─── NDBI Section ──────────────────────────────────────────────────────────────
st.markdown('<div class="tile-light">', unsafe_allow_html=True)
st.markdown('<div class="section-headline">NDBI Insurance Payout Estimation</div>', unsafe_allow_html=True)
_lp, col_ndbi, col_ndbi2, _rp = st.columns([P, 1, 1, P])
with col_ndbi:
    st.markdown(f"""
    <div class="ndbi-card">
      <div class="ndbi-title">Insurance Payout</div>
      <div class="ndbi-row"><span class="ndbi-key">Est. Payout</span><span class="ndbi-val blue">₩{ndbi_payout:.1f}B</span></div>
      <div class="progress-wrap"><div class="progress-fill" style="width:{(ndbi_payout/total_saving)*100}%"></div></div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)