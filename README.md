# 🤖 Intelligent Market Research Assistant

> **Problem Statement #6** — Built with IBM Bob + IBM Cloud + IBM Granite

An agentic AI application that acts as an intelligent market research assistant, synthesizing real-time market data, enabling multimodal analysis, predicting market shifts, and visualizing competitive intelligence.

---

## 🏗️ Architecture

```
IntelligentMarket/
├── app.py                    ← Flask application entry point
├── requirements.txt          ← Python dependencies
├── config.env                ← IBM Cloud configuration
├── backend/
│   ├── config.py             ← IBM WatsonX / Granite configuration
│   ├── granite_client.py     ← IBM Granite 3 8B AI integration
│   ├── data_agent.py         ← Real-time data collection (RSS, news)
│   ├── predictive_engine.py  ← ML forecasting & alert generation
│   └── routes.py             ← Flask REST API endpoints
└── frontend/
    └── index.html            ← Full-stack SPA dashboard
```

---

## ✨ Features

### 1. 🌐 Fuse Disparate Sources
- Real-time RSS news aggregation from Reuters, CNN, Bloomberg, TechCrunch, CNBC
- Keyword-based news search across multiple categories
- Automatic fallback to curated synthetic data when feeds are unavailable

### 2. 🔬 Multimodal Analysis
- **Text queries** → IBM Granite AI analysis
- **File upload** (CSV, TXT, JSON, MD) → AI-powered document analysis
- **Structured output** → competitor comparisons, trend analysis, market snapshots

### 3. 🤖 Predictive & Agentic Layer
- **Linear regression demand forecasting** (12-month historical + 6-month forecast)
- **Sentiment shift detection** — automated alerts on sentiment drops/surges
- **Competitor activity alerts** — expansion, pricing, product launch signals
- **Market health scoring** — composite 0-100 score from 5 indicators
- **Strategic alerts** — growth opportunities & market contraction warnings

### 4. 📊 Market Pulse Dashboard
- **KPI Cards** — Market size, YoY growth, demand index, health score
- **Revenue Trend Chart** — Historical + ML forecast with Chart.js
- **Market Share Doughnut** — Competitor landscape visualization
- **Sentiment Timeline** — 30-day sentiment bar chart
- **AI Snapshot** — IBM Granite-generated market narrative
- **News Feed** — Live articles with sentiment badges
- **Alerts Panel** — Prioritized HIGH/MEDIUM/LOW alerts

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip

### Windows
```bat
run.bat
```

### Linux / macOS
```bash
chmod +x run.sh && ./run.sh
```

### Manual
```bash
pip install -r requirements.txt
python app.py
```

Then open: **http://localhost:5000**

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Service health check |
| POST | `/api/analyze` | AI market analysis (IBM Granite) |
| GET | `/api/news` | News feed (topic/keyword) |
| POST | `/api/sentiment` | Sentiment analysis |
| POST | `/api/competitors` | Competitor analysis |
| GET | `/api/forecast` | Market forecast + ML demand prediction |
| GET | `/api/dashboard` | Full dashboard data |
| POST | `/api/multimodal` | Text/file multimodal analysis |
| POST | `/api/snapshot` | Quick AI market snapshot |

---

## 🔧 Configuration

IBM credentials are pre-configured in `config.env`:
```
IBM_API_KEY=M-6oyiybKr3nuDXbeVI4PDsPpv_GDCq_a1_s0vBbeOKI
IBM_PROJECT_ID=b1f23f7e-33d1-4aeb-879e-69b65ec56960
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

Model used: **`ibm/granite-3-8b-instruct`**

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| AI Model | IBM Granite 3 8B Instruct |
| AI Platform | IBM WatsonX (IBM Cloud) |
| Backend | Python + Flask |
| Data Collection | feedparser, BeautifulSoup4, requests |
| Sentiment | TextBlob |
| ML Forecasting | NumPy, scikit-learn (linear regression) |
| Frontend | Vanilla JS + Chart.js |
| Styling | Custom CSS (dark theme) |

---

*Built for Problem Statement #6 — Intelligent Market Research Assistant*
*IBM Bob + IBM Cloud + IBM Granite*
