import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="전력 수급 리스크 예측 대시보드",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Apple Design System CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
  /* Font */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #f5f5f7;
  }

  /* Hide streamlit chrome */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 0 !important; max-width: 100% !important; }

  /* ── Global Nav (true black) ────────────────────────────────────────────── */
  .global-nav {
    background: #000;
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
    color: #cccccc;
    letter-spacing: -0.12px;
  }

  /* ── Hero Section (dark tile) ────────────────────────────────────────────── */
  .hero-section {
    background: #272729;
    padding: 64px 48px 48px;
    text-align: center;
  }
  .hero-title {
    font-size: 56px;
    font-weight: 600;
    color: #fff;
    letter-spacing: -0.28px;
    line-height: 1.07;
    margin: 0 0 12px;
  }
  .hero-subtitle {
    font-size: 21px;
    font-weight: 400;
    color: #cccccc;
    letter-spacing: 0;
    line-height: 1.19;
    margin: 0 0 32px;
  }
  .hero-date-pill {
    display: inline-block;
    background: transparent;
    border: 1px solid #0066cc;
    color: #2997ff;
    font-size: 14px;
    font-weight: 400;
    padding: 8px 22px;
    border-radius: 9999px;
    letter-spacing: -0.224px;
  }

  /* ── Sub-Nav (frosted parchment) ─────────────────────────────────────────── */
  .sub-nav {
    background: rgba(245, 245, 247, 0.85);
    backdrop-filter: saturate(180%) blur(20px);
    -webkit-backdrop-filter: saturate(180%) blur(20px);
    border-bottom: 1px solid rgba(0,0,0,0.08);
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
    color: #1d1d1f;
    letter-spacing: 0.231px;
  }
  .sub-nav-meta {
    font-size: 14px;
    font-weight: 400;
    color: #7a7a7a;
    letter-spacing: -0.224px;
  }

  /* ── Section tiles ───────────────────────────────────────────────────────── */
  .tile-light {
    background: #fff;
    padding: 32px 64px;
  }
  .tile-parchment {
    background: #f5f5f7;
    padding: 64px 64px;
  }
  .tile-dark {
    background: #272729;
    padding: 64px 64px;
  }
  .tile-dark-2 {
    background: #2a2a2c;
    padding: 64px 64px;
  }

  /* ── Chart wrapper — 좌우 패딩 ──────────────────────────────────────────── */
  .chart-wrap {
    padding: 0 16px;
  }

  /* ── Section Headlines ───────────────────────────────────────────────────── */
  .section-headline {
    font-size: 40px;
    font-weight: 600;
    color: #1d1d1f;
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
    font-size: 21px;
    font-weight: 400;
    color: #1d1d1f;
    letter-spacing: 0;
    line-height: 1.4;
    text-align: center;
    margin: 0 0 48px;
  }
  .section-tagline-dark {
    font-size: 21px;
    font-weight: 400;
    color: #cccccc;
    letter-spacing: 0;
    line-height: 1.4;
    text-align: center;
    margin: 0 0 48px;
  }

  /* ── Forecast Weather Row ─────────────────────────────────────────────────── */
  .forecast-grid {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 12px;
    margin: 0 5%;
  }
  .forecast-card {
    background: #1a1a1c;
    border-radius: 18px;
    padding: 20px 12px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.06);
    transition: transform 0.15s ease;
  }
  .forecast-card:hover { transform: scale(1.02); }
  .forecast-card.danger { border-color: rgba(255, 59, 48, 0.35); background: #1f1212; }
  .forecast-card.caution { border-color: rgba(255, 196, 0, 0.35); background: #1c1a0f; }
  .forecast-card.safe { border-color: rgba(52, 199, 89, 0.35); background: #0f1c11; }
  .forecast-date { font-size: 13px; font-weight: 600; color: #7a7a7a; letter-spacing: -0.12px; margin-bottom: 10px; }
  .forecast-emoji { font-size: 28px; margin-bottom: 8px; display: block; }
  .forecast-pct { font-size: 22px; font-weight: 700; letter-spacing: -0.28px; margin-bottom: 4px; }
  .forecast-pct.danger { color: #ff3b30; }
  .forecast-pct.caution { color: #ffc400; }
  .forecast-pct.safe { color: #34c759; }
  .forecast-label { font-size: 11px; font-weight: 400; color: #7a7a7a; }

  /* ── KPI Metric Cards ─────────────────────────────────────────────────────── */
  .kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin: 0 5% 48px; 
  }
  .kpi-card {
    background: #fff;
    border: 1px solid #e0e0e0;
    border-radius: 18px;
    padding: 24px;
    text-align: center;
  }
  .kpi-card-dark {
    background: #1a1a1c;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 24px;
    text-align: center;
  }
  .kpi-label { font-size: 13px; font-weight: 400; color: #7a7a7a; letter-spacing: -0.12px; margin-bottom: 8px; }
  .kpi-value { font-size: 34px; font-weight: 600; color: #1d1d1f; letter-spacing: -0.374px; line-height: 1.47; }
  .kpi-value-dark { font-size: 34px; font-weight: 600; color: #fff; letter-spacing: -0.374px; line-height: 1.47; }
  .kpi-sub { font-size: 13px; font-weight: 400; color: #7a7a7a; margin-top: 4px; }
  .kpi-sub-green { font-size: 13px; font-weight: 600; color: #34c759; margin-top: 4px; }
  .kpi-sub-red { font-size: 13px; font-weight: 600; color: #ff3b30; margin-top: 4px; }

  /* ── Simulation Box ──────────────────────────────────────────────────────── */
  .sim-box {
    margin: 0 0 0 16px;
    height: 340px;  
    box-sizing: border-box;
    background: #1a1a1c;
    border-radius: 18px;
    padding: 36px 40px;
    border: 1px solid rgba(255,255,255,0.06);
  }
  .sim-title { font-size: 21px; font-weight: 600; color: #fff; letter-spacing: -0.374px; margin-bottom: 24px; }
  .sim-row { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 14px; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 14px; }
  .sim-row:last-of-type { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
  .sim-key { font-size: 15px; font-weight: 400; color: #cccccc; letter-spacing: -0.374px; }
  .sim-val { font-size: 22px; font-weight: 600; color: #fff; letter-spacing: -0.374px; }
  .sim-val.red { color: #ff3b30; }
  .sim-val.green { color: #34c759; }
  .sim-val.blue { color: #2997ff; }

  .recommend-pill {
    display: inline-block;
    background: #0066cc;
    color: #fff;
    font-size: 15px;
    font-weight: 400;
    padding: 11px 22px;
    border-radius: 9999px;
    letter-spacing: -0.374px;
    margin-top: 24px;
    text-align: center;
  }

  /* ── NDBI Card ────────────────────────────────────────────────────────────── */
  .ndbi-card {
    margin: 0 0 0 16px;
    height: 100%;
    box-sizing: border-box;
    background: #fff;
    border-radius: 18px;
    padding: 36px 40px;
    border: 1px solid #e0e0e0;
    box-shadow: rgba(0, 0, 0, 0.22) 3px 5px 30px 0;
  }
  .ndbi-title { font-size: 21px; font-weight: 600; color: #1d1d1f; letter-spacing: -0.374px; margin-bottom: 24px; }
  .ndbi-row { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 14px; border-bottom: 1px solid rgba(0,0,0,0.06); padding-bottom: 14px; }
  .ndbi-row:last-of-type { border-bottom: none; }
  .ndbi-key { font-size: 15px; font-weight: 400; color: #7a7a7a; letter-spacing: -0.374px; }
  .ndbi-val { font-size: 22px; font-weight: 600; color: #1d1d1f; letter-spacing: -0.374px; }
  .ndbi-val.blue { color: #0066cc; }
  .ndbi-val.green { color: #1a8a35; }

  /* ── Progress Bar ─────────────────────────────────────────────────────────── */
  .progress-wrap { background: #f0f0f0; border-radius: 9999px; height: 8px; overflow: hidden; margin-top: 8px; }
  .progress-fill { height: 100%; border-radius: 9999px; background: #0066cc; }
  .progress-fill.green { background: #34c759; }

  /* ── Footer ──────────────────────────────────────────────────────────────── */
  .apple-footer {
    background: #f5f5f7;
    padding: 40px 48px 24px;
    border-top: 1px solid #e0e0e0;
  }
  .footer-body { font-size: 12px; font-weight: 400; color: #7a7a7a; letter-spacing: -0.12px; line-height: 1.5; text-align: center; }

  /* ── Selector dropdown style ─────────────────────────────────────────────── */
  div[data-baseweb="select"] > div {
    background: #fff !important;
    border: 1px solid #e0e0e0 !important;
    border-radius: 9999px !important;
    font-family: 'Inter', system-ui, sans-serif !important;
    font-size: 14px !important;
    color: #1d1d1f !important;
  }
  .stSlider > div > div > div > div { background: #0066cc !important; }
</style>
""", unsafe_allow_html=True)


# ─── Data ────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('dashboard_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# NDBI params (insurances)
INSURANCE_COVERAGE = 0.35   # 35% of loss covered
TRIGGER_THRESHOLD  = 0.70   # LOLP ≥ 0.7 triggers insurance

# ─── Derived values ────────────────────────────────────────────────────────────
total_saving      = df['saving_억'].sum()
avg_lolp          = df['prob_lolp'].mean()
peak_row          = df.loc[df['prob_lolp'].idxmax()]
danger_days       = (df['risk_level'] == 2).sum()
caution_days      = (df['risk_level'] == 1).sum()
safe_days         = (df['risk_level'] == 0).sum()
trigger_days      = (df['prob_lolp'] >= TRIGGER_THRESHOLD).sum()
trigger_rate      = trigger_days / len(df)
ndbi_payout       = round(df.loc[df['prob_lolp'] >= TRIGGER_THRESHOLD, 'saving_억'].sum() * INSURANCE_COVERAGE, 1)

# ─── Global Nav ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="global-nav">
  <span class="nav-brand">SST-Electricity Risk Management</span>
  <span class="nav-meta">XGBoost LOLP 예측 기반 기업 손실 시뮬레이션</span>
</div>
""", unsafe_allow_html=True)

# ─── Sub Nav ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-section">
  <span class="hero-title">전력 수급 리스크 예측 대시보드</span>
  <span class="hero-subtitle"><br>2024.07.01 — 2024.07.14 · 14일 분석</span>
</div>
""", unsafe_allow_html=True)


# ─── KPI Strip (parchment tile) ───────────────────────────────────────────────
st.markdown('<div class="tile-light">', unsafe_allow_html=True)
st.markdown('<div class="section-tagline">주요 지표 요약</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card">
    <div class="kpi-label">평균 LOLP</div>
    <div class="kpi-value">{avg_lolp:.0%}</div>
    <div class="kpi-sub">예측 기간 평균 위험 확률</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">위험일 / 주의일 / 정상일</div>
    <div class="kpi-value" style="color:#ff3b30">{danger_days}일</div>
    <div class="kpi-sub"">주의 {caution_days}일 &nbsp;·&nbsp; <span>정상 {safe_days}일</span></div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">총 절감 가능 손실</div>
    <div class="kpi-value" style="color:#1a8a35">{total_saving:.0f}억</div>
    <div class="kpi-sub">권고 이행 시 절감액</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">최고 위험일</div>
    <div class="kpi-value"">{peak_row['date'].strftime('%m/%d')}</div>
    <div class="kpi-sub">LOLP {peak_row['prob_lolp']:.0%} · 위험</div>
  </div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ─── 7-Day Forecast  ───────────────────────────────────────────────
st.markdown('<div class="tile-light">', unsafe_allow_html=True)
st.markdown('<div class="section-headline">전력 위험 확률</div>', unsafe_allow_html=True)
st.markdown('<div class="section-tagline">7일 간 전력 위험 LOLP 확률을 예측합니다</div>', unsafe_allow_html=True)


# Build forecast cards (first 7 rows)
forecast_7 = df.head(7)
cards_html = '<div class="forecast-grid">'
for _, row in forecast_7.iterrows():
    level_cls = {2: 'danger', 1: 'caution', 0: 'safe'}[row['risk_level']]
    pct_str   = f"{row['prob_lolp']:.0%}"
    date_str  = row['date'].strftime('%m/%d')
    emoji     = row['risk_emoji']
    cards_html += f"""
    <div class="forecast-card {level_cls}">
      <div class="forecast-date">{date_str}</div>
      <span class="forecast-emoji">{emoji}</span>
      <div class="forecast-pct {level_cls}">{pct_str}</div>
      <div class="forecast-label">{row['risk_name']}</div>
    </div>"""
cards_html += '</div>'
st.markdown(cards_html, unsafe_allow_html=True)
st.markdown('<br>', unsafe_allow_html=True)

# Interactive Full 14-day LOLP Chart
color_map = {0: '#34c759', 1: '#ffc400', 2: '#ff3b30'}
bar_colors = [color_map[l] for l in df['risk_level']]

fig_lolp = go.Figure()
fig_lolp.add_trace(go.Bar(
    x=df['date'].dt.strftime('%m/%d'),
    y=df['prob_lolp'],
    marker_color=bar_colors,
    marker_line_color='rgba(255,255,255,0.15)',
    marker_line_width=1,
    text=[f"{v:.0%}" for v in df['prob_lolp']],
    textposition='outside',
    textfont=dict(color='#1d1d1f', size=11, family='Inter'),
    hovertemplate='<b>%{x}</b><br>LOLP: %{y:.1%}<extra></extra>',
))
fig_lolp.add_hline(y=0.70, line_dash='dash', line_color='#111111', line_width=2, annotation_text='위험 기준 0.7', annotation_font_color='#111111')
fig_lolp.add_hline(y=0.30, line_dash='dash', line_color='#555555', line_width=1.5, annotation_text='주의 기준 0.3', annotation_font_color='#555555')
fig_lolp.add_hrect(y0=0.70, y1=1.05, fillcolor='rgba(255,59,48,0.07)', line_width=0)
fig_lolp.add_hrect(y0=0.30, y1=0.70, fillcolor='rgba(255,196,0,0.05)', line_width=0)
fig_lolp.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='#ffffff',
    height=280,
    margin=dict(l=24, r=24, t=10, b=10),
    showlegend=False,
    xaxis=dict(showgrid=False, tickfont=dict(color='#1d1d1f', size=11), color='#1d1d1f', linecolor='#e0e0e0'),
    yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.08)', tickformat='.0%', tickfont=dict(color='#1d1d1f', size=11), range=[0, 1.12]),
    bargap=0.25,
    font=dict(family='Inter'),
)
st.plotly_chart(fig_lolp, use_container_width=True, config={'displayModeBar': False})
st.markdown('</div>', unsafe_allow_html=True)

# ─── Simulation Section (light tile) ──────────────────────────────────────────
st.markdown('<div class="tile-light">', unsafe_allow_html=True)
st.markdown('<div class="section-headline">기업 손실 시뮬레이션</div>', unsafe_allow_html=True)
st.markdown('<div class="section-tagline">선택 일시의 권고 이행 효과를 확인하세요</div>', unsafe_allow_html=True)

# Date selector
col_pad, col_sel, col_info = st.columns([0.3, 1.5, 3.2])
# col_sel, col_info = st.columns([2, 3])
with col_sel:
    date_options = df['date'].dt.strftime('%m/%d (%a)').tolist()
    selected_idx = st.selectbox(
        "날짜 선택",
        range(len(date_options)),
        format_func=lambda i: date_options[i],
        index=int(df['prob_lolp'].idxmax()),
        label_visibility='collapsed',
    )
selected = df.iloc[selected_idx]
level_labels = {2: '🔴 위험', 1: '🟡 주의', 0: '🟢 정상'}
level_colors = {2: '#ff3b30', 1: '#ffc400', 0: '#34c759'}

with col_info:
    st.markdown(f"""
    <div style="font-size:14px; color:#7a7a7a; font-family:Inter; padding:8px 0;">
      선택된 날짜: <strong style="color:#1d1d1f">{selected['date'].strftime('%Y년 %m월 %d일')}</strong>
      &nbsp;·&nbsp; 위험 등급: <strong style="color:{level_colors[selected['risk_level']]}">{level_labels[selected['risk_level']]}</strong>
      &nbsp;·&nbsp; SST: <strong style="color:#1d1d1f">{selected['sst']}°C</strong>
      &nbsp;·&nbsp; 예비율: <strong style="color:#1d1d1f">{selected['reserve_rate']}%</strong>
    </div>
    """, unsafe_allow_html=True)

col_sim, col_chart = st.columns([1, 1])
with col_sim:
    saving = selected['saving_억']
    saving_pct = round((1 - selected['optimal_loss_억'] / selected['maintain_loss_억']) * 100) if selected['maintain_loss_억'] > 0 else 0
    st.markdown(f"""
    <div class="sim-box">
      <div class="sim-title">위험 확률 {selected['prob_lolp']:.0%} 기준</div>
      <div class="sim-row">
        <span class="sim-key">AI 권고</span>
        <span class="sim-val">생산량 {selected['optimal_production']}%로 조정</span>
      </div>
      <div class="sim-row">
        <span class="sim-key">생산 유지 시 예상 손실</span>
        <span class="sim-val red">{selected['maintain_loss_억']:.1f}억</span>
      </div>
      <div class="sim-row">
        <span class="sim-key">권고 이행 시 예상 손실</span>
        <span class="sim-val green">{selected['optimal_loss_억']:.1f}억</span>
      </div>
      <div class="sim-row">
        <span class="sim-key">절감 효과</span>
        <span class="sim-val">{saving:.1f}억 ({saving_pct}%↓)</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_chart:
    # Loss comparison bar chart for all dates
    fig_loss = go.Figure()
    fig_loss.add_trace(go.Bar(
        name='생산 유지',
        x=df['date'].dt.strftime('%m/%d'),
        y=df['maintain_loss_억'],
        marker_color='rgba(255,59,48,0.75)',
        marker_line_color='rgba(255,255,255,0.2)',
        marker_line_width=0.5,
        hovertemplate='%{x}<br>생산유지: %{y:.1f}억<extra></extra>',
    ))
    fig_loss.add_trace(go.Bar(
        name='권고 이행',
        x=df['date'].dt.strftime('%m/%d'),
        y=df['optimal_loss_억'],
        marker_color='rgba(52,199,89,0.75)',
        marker_line_color='rgba(255,255,255,0.2)',
        marker_line_width=0.5,
        hovertemplate='%{x}<br>권고이행: %{y:.1f}억<extra></extra>',
    ))
    # Highlight selected date
    sel_date_str = selected['date'].strftime('%m/%d')
    fig_loss.add_vline(
        x=sel_date_str, line_color='rgba(0,102,204,0.5)', line_width=2
    )
    fig_loss.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        barmode='group',
        height=340,
        # margin=dict(l=24, r=24, t=10, b=10),
        margin=dict(l=24, r=24, t=4, b=4),
        legend=dict(font=dict(color='#1d1d1f', size=12), bgcolor='rgba(0,0,0,0)'),
        xaxis=dict(showgrid=False, tickfont=dict(color='#7a7a7a', size=10)),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.06)', tickfont=dict(color='#7a7a7a', size=10), title='예상 손실 (억원)', title_font=dict(color='#7a7a7a', size=11)),
        bargap=0.2,
        font=dict(family='Inter'),
    )
    st.plotly_chart(fig_loss, use_container_width=True, config={'displayModeBar': False})

st.markdown('</div>', unsafe_allow_html=True)

# ─── Optimal Production Section ─────────────────────────────────
st.markdown('<div class="tile-light">', unsafe_allow_html=True)
st.markdown('<div class="section-headline">최적 생산량 권고</div>', unsafe_allow_html=True)
st.markdown('<div class="section-tagline">Expected Loss 최소화 기반 일별 생산량 조정 권고입니다</div>', unsafe_allow_html=True)

col_prod, col_cum = st.columns([1, 1])
with col_prod:
    fig_prod = go.Figure()
    prod_colors = [color_map[l] for l in df['risk_level']]
    fig_prod.add_trace(go.Scatter(
        x=df['date'].dt.strftime('%m/%d'),
        y=df['optimal_production'],
        mode='lines+markers+text',
        line=dict(color='#2997ff', width=3),
        marker=dict(size=11, color=prod_colors, line=dict(color='white', width=2.5)),
        text=[f"{v}%" for v in df['optimal_production']],
        textposition='top center',
        textfont=dict(color='#ffffff', size=11, family='Inter'),
        fill='tozeroy',
        fillcolor='rgba(41,151,255,0.25)',
        hovertemplate='%{x}<br>권고 생산량: %{y}%<extra></extra>',
    ))
    fig_prod.add_hline(y=100, line_dash='dot', line_color='rgba(255,255,255,0.5)', annotation_text='현재 100%', annotation_font_color='rgba(255,255,255,0.7)')
    fig_prod.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#2a2a2c',
        height=300,
        margin=dict(l=24, r=24, t=10, b=10),
        showlegend=False,
        xaxis=dict(showgrid=False, tickfont=dict(color='#cccccc', size=10), linecolor='rgba(255,255,255,0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.10)', tickfont=dict(color='#cccccc', size=10), range=[0, 125], title='권고 생산량 (%)', title_font=dict(color='#cccccc', size=11)),
        font=dict(family='Inter'),
    )
    st.plotly_chart(fig_prod, use_container_width=True, config={'displayModeBar': False})

with col_cum:
    cumulative = df['saving_억'].cumsum()
    fig_cum = go.Figure()
    fig_cum.add_trace(go.Scatter(
        x=df['date'].dt.strftime('%m/%d'),
        y=cumulative,
        mode='lines+markers',
        line=dict(color='#34c759', width=2.5),
        marker=dict(size=8, color='#34c759', line=dict(color='white', width=2)),
        fill='tozeroy',
        fillcolor='rgba(52,199,89,0.15)',
        hovertemplate='%{x}<br>누적 절감: %{y:.1f}억<extra></extra>',
    ))
    # Final value annotation
    fig_cum.add_annotation(
        x=df['date'].dt.strftime('%m/%d').iloc[-1],
        y=cumulative.iloc[-1],
        text=f"총 {total_saving:.0f}억 절감!!",
        showarrow=True, arrowhead=2,
        arrowcolor='#34c759',
        font=dict(color='#34c759', size=12, family='Inter'),
        bgcolor='rgba(42,44,42,0.8)',
        bordercolor='#34c759',
        borderwidth=1.5,
        borderpad=6,
    )
    fig_cum.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#2a2a2c',
        height=300,
        margin=dict(l=24, r=24, t=10, b=10),
        showlegend=False,
        xaxis=dict(showgrid=False, tickfont=dict(color='#cccccc', size=10)),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.10)', tickfont=dict(color='#cccccc', size=10), title='누적 절감액 (억원)', title_font=dict(color='#cccccc', size=11)),
        font=dict(family='Inter'),
    )
    st.plotly_chart(fig_cum, use_container_width=True, config={'displayModeBar': False})

st.markdown('</div>', unsafe_allow_html=True)

# ─── NDBI Insurance Section (light tile) ─────────────────────────────────────
st.markdown('<div class="tile-light">', unsafe_allow_html=True)
st.markdown('<div class="section-headline">NDBI 보험금 추정</div>', unsafe_allow_html=True)
st.markdown('<div class="section-tagline">NDBI 트리거에 따른 보험금 산출을 추정합니다</div>', unsafe_allow_html=True)

col_ndbi, col_ndbi2 = st.columns([1, 1])
with col_ndbi:
    trigger_pct = round(trigger_rate * 100, 1)
    st.markdown(f"""
    <div class="ndbi-card">
      <div class="ndbi-title">보험금 추정 요약</div>
      <div class="ndbi-row">
        <span class="ndbi-key">트리거 기준 (LOLP ≥ 0.7)</span>
        <span class="ndbi-val">{trigger_days}일 / 14일</span>
      </div>
      <div class="ndbi-row">
        <span class="ndbi-key">트리거 달성률</span>
        <span class="ndbi-val blue">{trigger_pct}%</span>
      </div>
      <div class="ndbi-row">
        <span class="ndbi-key">예상 보험금 (손실의 35%)</span>
        <span class="ndbi-val green">{ndbi_payout:.1f}억</span>
      </div>
      <div class="ndbi-row">
        <span class="ndbi-key">최고 위험일 LOLP</span>
        <span class="ndbi-val">{peak_row['prob_lolp']:.1%}</span>
      </div>
      <div style="margin-top:20px">
        <div style="font-size:13px; color:#7a7a7a; margin-bottom:6px; font-family:Inter">트리거 달성률 {trigger_pct}%</div>
        <div class="progress-wrap"><div class="progress-fill green" style="width:{trigger_pct}%"></div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_ndbi2:
    # Scatter: LOLP vs saving with trigger zone
    fig_ndbi = go.Figure()
    fig_ndbi.add_vrect(x0=0.70, x1=1.0, fillcolor='rgba(0,102,204,0.07)', line_width=0, annotation_text='트리거 구간', annotation_font_color='#0066cc', annotation_position='top left')
    colors_scatter = [color_map[l] for l in df['risk_level']]
    fig_ndbi.add_trace(go.Scatter(
        x=df['prob_lolp'],
        y=df['saving_억'],
        mode='markers+text',
        marker=dict(size=14, color=colors_scatter, line=dict(color='white', width=1.5), opacity=0.9),
        text=df['date'].dt.strftime('%m/%d'),
        textposition='top center',
        textfont=dict(size=9, color='#7a7a7a'),
        hovertemplate='%{text}<br>LOLP: %{x:.1%}<br>절감액: %{y:.1f}억<extra></extra>',
    ))
    fig_ndbi.add_vline(x=0.70, line_dash='dash', line_color='#0066cc', line_width=1.5)
    fig_ndbi.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=480,
        # margin=dict(l=24, r=24, t=10, b=10),
        margin=dict(l=24, r=24, t=4, b=4),
        showlegend=False,
        xaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.06)', tickformat='.0%', tickfont=dict(color='#7a7a7a', size=10), title='LOLP 예측 확률', title_font=dict(color='#7a7a7a', size=11)),
        yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.06)', tickfont=dict(color='#7a7a7a', size=10), title='절감 가능액 (억원)', title_font=dict(color='#7a7a7a', size=11)),
        font=dict(family='Inter'),
    )
    st.plotly_chart(fig_ndbi, use_container_width=True, config={'displayModeBar': False})

st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="apple-footer">
  <div class="footer-body">
    본 대시보드는 XGBoost LOLP 예측 모델 기반 시뮬레이션 결과입니다.
  </div>
</div>
""", unsafe_allow_html=True)