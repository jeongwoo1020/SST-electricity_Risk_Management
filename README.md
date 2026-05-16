# ⚡ SST-Electricity Risk Prediction Dashboard

> **AI-Driven Parametric NDBI Platform: Turning Hot-Sea Power-Supply Risk into a 30-Day Cheque**  
> Samsung Fire & Marine Insurance · Risk Management Insight & Insur-novation · Team Gumjandi

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sst-electricityriskmanagement-dashboard.streamlit.app/)

---

## Overview

This dashboard provides an **AI-driven electricity supply risk prediction system** that translates sea-surface temperature (SST) data into quantified, priceable industrial risk.

Korean coastal SST is rising at **2× the global average**, directly threatening nuclear cooling efficiency and grid reserve margins — yet no existing insurance product covers this chain. This platform bridges that gap.

---

## Key Features

| Section | Description |
|--------|-------------|
| **Key Metrics Summary** | 14-day average LOLP, risk day breakdown, total reducible loss, peak risk day |
| **7-Day Power Risk Forecast** | Weather-style daily LOLP forecast with risk color coding (High Risk / Caution / Normal) |
| **Enterprise Loss Simulation** | Date-selectable loss comparison — maintain production vs. AI recommendation |
| **Optimal Production Recommendation** | Expected Loss minimization-based daily production adjustment |
| **NDBI Insurance Payout Estimation** | Parametric trigger-based insurance payout auto-calculation |

---

## Model Architecture

```
NIFS SST Data  ──┐
EPSIS Reserve  ──┼──► XGBoost LOLP Predictor ──► Risk Level
NOAA ENSO ONI  ──┘         │
                            ▼
                   Expected Loss Calculator
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
     Loss by Production  Optimal Qty  NDBI Trigger
       Comparison        Recommendation  Estimation
```

### Model Performance
- AUC ≥ 0.85
- SMOTE class imbalance correction applied
- ECE calibration completed
- Lagged Pearson correlation peak: lag-4 to lag-8 days (3–10 day lead time)

### EDA Evidence

Three data-driven findings validate the model:

1. **① Correlation proven** — SST ↔ reserve margin shows a clear negative relationship across all 4 nuclear sites (Hanbit, Hanbit NPP Yellow Sea, Wolseong, Gori)
2. **② Lead time exists** — Lagged Pearson correlation peaks at lag-4 to lag-8 days → today's SST predicts next week's grid stress
3. **③ ENSO is the year-ahead lever** — Adding lag-1y ENSO ANOM cuts SST forecast error from ~2°C to 1.10°C, making one-year-ahead risk pricing actuarially tractable

### Business Impact

| Stakeholder | Value |
|-------------|-------|
| **Industrial Tenants** | 3–10 day advance warning → production rescheduling → loss reduction |
| **Samsung F&M (Insurer)** | Parametric NDBI pricing baseline · actuarially tractable trigger |
| **Government / Grid** | Systemic climate-grid risk visibility · demand-side management lever |

---

## Getting Started

### Prerequisites

```
Python 3.11+
```

### Installation

```bash
git clone https://github.com/jeongwoo1020/SST-electricity_Risk_Management.git
cd SST-electricity_Risk_Management
pip install -r requirements.txt
```

### Run Locally

```bash
streamlit run dashboard.py
```

### Dependencies

```
streamlit==1.32.0
plotly==5.20.0
pandas==2.2.0
numpy
```

---

<p align="center">
  <b>Team Gumjandi</b> &nbsp;·&nbsp; Samsung Fire & Marine Insurance &nbsp;·&nbsp; Risk Management Insight & Insur-novation
</p>
