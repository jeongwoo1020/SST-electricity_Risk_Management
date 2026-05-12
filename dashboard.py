import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Electricity Supply Risk Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Samsung & Sky Blue Design System CSS ─────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700&family=Inter:wght@400;600;700&display=swap');

  /* Global Body Background (Light Sky Gradient) */
  .stApp {
    background: linear-gradient(to bottom, #DAEEF8, #EEF6FB);
    font-family: 'Inter', 'Noto Sans KR', sans-serif;
  }

  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 0 !important; max-width: 100% !important; }

  /* ── Navigation (Dark Navy) ────────────────────────────────────────────── */
  .global-nav {
    background: #1A2744;
    padding: 0 40px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 3px solid #1557C0;
  }
  .nav-brand {
    font-size: 20px;
    font-weight: 700;
    color: #FFFFFF;
  }

  /* ── Hero Section (Sky Blue Gradient) ──────────────────────────────────── */
  .hero-section {
    background: linear-gradient(135deg, #87CEEB, #B0DEF0);
    padding: 50px 40px;
    text-align: center;
    border-bottom: 1px solid #1557C0;
  }
  .hero-title {
    font-size: 42px;
    font-weight: 700;
    color: #1A2744;
    margin-bottom: 10px;
  }
  .hero-subtitle {
    font-size: 20px;
    color: #1557C0;
    font-weight: 600;
  }

  /* ── White Section Tiles ───────────────────────────────────────────────── */
  .tile-container {
    background: #FFFFFF;
    margin: 24px 40px;
    padding: 40px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(26, 39, 68, 0.08);
    border-top: 4px solid #1557C0; /* Section Divider Line */
  }

  .section-headline {
    font-size: 28px;
    font-weight: 700;
    color: #1A2744;
    margin-bottom: 30px;
    border-left: 6px solid #1557C0;
    padding-left: 15px;
  }

  /* ── KPI Metrics ───────────────────────────────────────────────────────── */
  .kpi-card {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 24px;
    text-align: center;
    transition: all 0.3s ease;
  }
  .kpi-card:hover { border-color: #1557C0; transform: translateY(-5px); }
  .kpi-label { font-size: 14px; color: #64748B; margin-bottom: 10px; font-weight: 600; }
  .kpi-value { font-size: 36px; font-weight: 700; color: #1557C0; }

  /* ── Forecast Cards ────────────────────────────────────────────────────── */
  .forecast-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 15px;
  }
  .forecast-card {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 20px 10px;
    text-align: center;
    border: 1px solid #E2E8F0;
  }
  .forecast-card.danger { border-top: 5px solid #FF3B30; }
  .forecast-card.caution { border-top: 5px solid #F5A623; } /* Orange Accent */
  .forecast-card.safe { border-top: 5px solid #34C759; }
  
  .forecast-date { font-size: 14px; color: #1A2744; font-weight: 700; margin-bottom: 10px; }
  .forecast-pct { font-size: 24px; font-weight: 700; margin-bottom: 5px; }
  .forecast-pct.danger { color: #FF3B30; }
  .forecast-pct.caution { color: #F5A623; }
  .forecast-pct.safe { color: #34C759; }

  /* ── Simulation & NDBI Box ─────────────────────────────────────────────── */
  .sim-box {
    background: #1A2744;
    color: #FFFFFF;
    border-radius: 12px;
    padding: 30px;
  }
  .sim-row {
    display: flex;
    justify-content: space-between;
    padding: 12px 0;
    border-bottom: 1px solid rgba(255,255,255,0.1);
  }
  .sim-val.orange { color: #F5A623; font-weight: 700; }
  .sim-val.green { color: #34C759; font-weight: 700; }

  .ndbi-card {
    background: #FFFFFF;
    border: 2px solid #1557C0;
    border-radius: 12px;
    padding: 30px;
  }
  .ndbi-title { color: #1557C0; font-weight: 700; font-size: 22px; margin-bottom: 20px; }

</style>
""", unsafe_allow_html=True)

# ─── Data & Logic ────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    # 데이터 경로는 정우 님의 환경에 맞게 수정하세요.
    df = pd.read_csv('dashboard_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()
avg_lolp = df['prob_lolp'].mean()
total_saving = df['saving_억'].sum()
peak_row = df.loc[df['prob_lolp'].idxmax()]

# ─── Nav ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="global-nav">
  <span class="nav-brand">SAMSUNG ENERGY AI</span>
  <span style="color:#FFFFFF; font-size:14px;">Risk Management System v2.0</span>
</div>
""", unsafe_allow_html=True)

# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-section">
  <div class="hero-title">Electricity Supply Risk Prediction</div>
  <div class="hero-subtitle">SST-Grid Matrix & XGBoost LOLP Analysis</div>
</div>
""", unsafe_allow_html=True)

# ─── KPI Section ──────────────────────────────────────────────────────────────
st.markdown('<div class="tile-container">', unsafe_allow_html=True)
st.markdown('<div class="section-headline">Strategic Overview</div>', unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Average LOLP</div><div class="kpi-value">{avg_lolp:.1%}</div></div>', unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Peak Risk Prob.</div><div class="kpi-value" style="color:#FF3B30;">{peak_row["prob_lolp"]:.1%}</div></div>', unsafe_allow_html=True)
with k3:
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Expected Savings</div><div class="kpi-value">₩{total_saving:.0f}B</div></div>', unsafe_allow_html=True)
with k4:
    st.markdown(f'<div class="kpi-card"><div class="kpi-label">Peak Risk Date</div><div class="kpi-value">{peak_row["date"].strftime("%m/%d")}</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ─── Forecast Section ─────────────────────────────────────────────────────────
st.markdown('<div class="tile-container">', unsafe_allow_html=True)
st.markdown('<div class="section-headline">7-Day Risk Forecast</div>', unsafe_allow_html=True)

f_cols = st.columns(7)
for i, (_, row) in enumerate(df.head(7).iterrows()):
    level_cls = {2: 'danger', 1: 'caution', 0: 'safe'}[row['risk_level']]
    with f_cols[i]:
        st.markdown(f"""
        <div class="forecast-card {level_cls}">
          <div class="forecast-date">{row['date'].strftime('%m/%d')}</div>
          <div style="font-size:30px;">{row['risk_emoji']}</div>
          <div class="forecast-pct {level_cls}">{row['prob_lolp']:.0%}</div>
          <div style="font-size:12px; font-weight:600; color:#64748B;">{row['risk_name']}</div>
        </div>
        """, unsafe_allow_html=True)

# Plotly Chart (Samsung Theme)
fig_lolp = px.bar(df, x=df['date'].dt.strftime('%m/%d'), y='prob_lolp',
             color='risk_level', 
             color_continuous_scale=[[0, '#34C759'], [0.5, '#F5A623'], [1, '#FF3B30']])
fig_lolp.update_layout(
    plot_bgcolor='white', paper_bgcolor='white',
    coloraxis_showscale=False, height=300,
    margin=dict(l=10, r=10, t=30, b=10),
    xaxis=dict(title="", tickfont=dict(color='#1A2744')),
    yaxis=dict(title="LOLP Probability", gridcolor='#E2E8F0', tickformat='.0%')
)
st.plotly_chart(fig_lolp, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ─── Simulation & NDBI ────────────────────────────────────────────────────────
st.markdown('<div class="tile-container">', unsafe_allow_html=True)
st.markdown('<div class="section-headline">Loss Simulation & NDBI Payout</div>', unsafe_allow_html=True)

selected_idx = st.select_slider("Select Forecast Date", options=range(len(df)), format_func=lambda i: df.iloc[i]['date'].strftime('%m/%d'))
sel = df.iloc[selected_idx]

c1, c2 = st.columns([1, 1])
with c1:
    st.markdown(f"""
    <div class="sim-box">
      <div style="font-size:18px; font-weight:700; margin-bottom:20px;">AI Simulation: {sel['date'].strftime('%Y-%m-%d')}</div>
      <div class="sim-row"><span>LOLP Probability</span><span class="sim-val orange">{sel['prob_lolp']:.1%}</span></div>
      <div class="sim-row"><span>Maintain Production Loss</span><span class="sim-val">₩{sel['maintain_loss_억']:.1f}B</span></div>
      <div class="sim-row"><span>Recommended Loss</span><span class="sim-val green">₩{sel['optimal_loss_억']:.1f}B</span></div>
      <div class="sim-row" style="border:none; margin-top:10px;">
        <span style="font-size:18px; font-weight:700;">Net Savings</span>
        <span style="font-size:24px; font-weight:700; color:#F5A623;">₩{sel['saving_억']:.1f}B</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="ndbi-card">
      <div class="ndbi-title">NDBI Estimated Payout</div>
      <div style="font-size:14px; color:#64748B; margin-bottom:20px;">Parametric insurance based on SST-Grid Matrix</div>
      <div class="sim-row" style="color:#1A2744; border-color:#E2E8F0"><span>Trigger Condition</span><span style="font-weight:700">LOLP ≥ 70%</span></div>
      <div class="sim-row" style="color:#1A2744; border-color:#E2E8F0"><span>SST Baseline</span><span style="font-weight:700">{sel['sst']}°C</span></div>
      <div class="sim-row" style="color:#1A2744; border-color:#E2E8F0"><span>Reserve Rate</span><span style="font-weight:700">{sel['reserve_rate']}%</span></div>
      <div style="margin-top:25px; text-align:center;">
        <div style="font-size:12px; color:#1557C0; font-weight:700;">ESTIMATED PAYOUT</div>
        <div style="font-size:32px; font-weight:700; color:#1557C0;">₩{(sel['saving_억']*0.35):.1f}B</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)