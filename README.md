# 🛡️ CyberTwin AI: Autonomous Cyber Digital Twin Threat Detection & Defense Engine

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React 19](https://img.shields.io/badge/React-19.0-61DAFB?style=flat-square&logo=react)](https://react.dev/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-EE4C2C?style=flat-square&logo=pytorch)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

**CyberTwin AI** is an enterprise-grade, autonomous threat detection platform that continuously learns baseline "normal" behavior across access logs, network topologies, and command sequences. By combining a **Tri-Model Consensus Engine** (PyTorch Autoencoders, Sequence Transformers, and In-Memory Graph Topologies) with **Explainable AI (XAI)** and **Pre-emptive Trajectory Prediction**, CyberTwin AI stops zero-day intrusions and compromised credentials before impact.

---

## 📌 Project Overview

- **Problem Statement ID**: PS-CYBER-01
- **Problem Statement Title**: AI-Powered Behavioral Anomaly Detection for Cybersecurity
- **Theme**: Cyber Security / Artificial Intelligence & Machine Learning
- **Student Name**: Nigam Prasad Lenka
- **Student ID**: 23BCE11432

---

## ✨ Key Features

- **🚀 Hackathon Judge Click Simulator**: Dedicated top-header control button to inject simulated real-time user events (`usr-hackathon-XXXX`), test presets (Impossible Travel, Insider Threat), or custom JSON payloads into the pipeline with instant feedback.
- **⚡ Tri-Model Consensus Defense**:
  1. **Behavioral Autoencoder**: Point-in-time anomaly scoring (PyTorch MSE loss).
  2. **CyberSequenceTransformer**: Temporal "low-and-slow" multi-step sequence scoring.
  3. **NetworkX Streaming Graph Engine**: Real-time lateral movement and network hop distance calculation.
- **🔮 Pre-Emptive Trajectory Prediction**: Autoregressive Behavioral Twin model mathematically forecasts the attacker's next move ($P(a_{t+1} \vert a_1..a_t)$) with probabilities.
- **💡 Explainable AI (XAI) & NLG**: SHAP TreeExplainer feature attributions translated into plain-English incident reports.
- **🛡️ SOAR Playbook Automation**: Closed-loop one-click actions (*Force MFA*, *Host Isolation*, *Dynamic Decoy Honeypot*).

---

## 🏗️ System Architecture

```text
[ Synthetic Telemetry Stream ] 
              │
              ▼
[ FastAPI Ingestion / Redis Streams ] ──► (Feature Pipeline: Time Sine/Cos, Geo Velocity)
              │
  ┌───────────┼──────────────────────────┐
  ▼           ▼                          ▼
[ PyTorch   [ PyTorch Sequence      [ In-Memory Graph 
Autoencoder] Transformer ]          Topology Engine ]
  │           │                          │
  └───────────┼──────────────────────────┘
              ▼
[ Anomaly Fusion Engine ] ──► (Master Risk Score = Model Fusion x Consensus Boost)
              │
     ┌────────┴──────────────────────────┐
     ▼                                   ▼
[ Multi-Class XGBoost ATT&CK ]   [ Autoregressive Twin Predictor ]
     │                                   │
     └───────────┬───────────────────────┘
                 ▼
[ SHAP XAI Engine + NLG Translator ] ──► [ React SOC War Room & SOAR Playbooks ]
```

---

## 📂 Repository Structure

```text
cybertwin-ai/
├── backend/                  # FastAPI backend app, routes, schemas & workers
│   ├── app/
│   │   ├── api/              # Ingest, Alerts, Remediation & WebSocket endpoints
│   │   ├── services/         # Anomaly Fusion, XAI SHAP, NLG Generator
│   │   └── workers/          # ML Inference Worker & Redis Consumer
│   └── requirements.txt      # Python dependencies (PyTorch, XGBoost, SHAP, NetworkX)
├── behavior_twin/            # Autoregressive Behavioral Twin predictor models
├── dashboard/                # React 19 + Vite Analyst Dashboard & TopNav Simulator
│   ├── src/
│   │   ├── components/       # UI layout, charts, TopNav & Sidebar
│   │   ├── pages/            # Overview, Threat Feed, War Room, Graph & Settings
│   │   └── store/            # Zustand state management
├── graph_engine/             # NetworkX streaming graph topology manager
├── ml/                       # PyTorch Autoencoder & CyberSequenceTransformer models
├── synthetic_data/           # Telemetry log generator scripts
└── render.yaml               # 100% Free Tier Render Infrastructure-as-Code Blueprint
```

---

## ⚙️ Quick Start (Local Setup)

### Prerequisites
- Python 3.10+
- Node.js 18+

### 1. Backend Setup
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Run FastAPI backend server (Port 8000)
uvicorn backend.app.main:app --reload --port 8000
```
- Interactive Swagger API Docs: `http://localhost:8000/docs`

### 2. Dashboard Setup
```bash
# Navigate to dashboard directory
cd dashboard

# Install npm dependencies
npm install

# Start Vite dev server (Port 5173)
npm run dev
```
- Dashboard UI: `http://localhost:5173`

---

## ☁️ Cloud Deployment (Render Blueprint)

The repository includes a ready-to-use 100% free `render.yaml` Blueprint file for Render.com.

1. Push code to GitHub: `justynigam/AI-Cybertwin`
2. Go to [Render Dashboard](https://dashboard.render.com/) $\rightarrow$ **New +** $\rightarrow$ **Blueprint**.
3. Connect your repository. Render will automatically provision:
   - **PostgreSQL Database** (`cybertwin-postgres`)
   - **Redis Instance** (`cybertwin-redis`)
   - **FastAPI Web Service** (`cybertwin-api`)
   - **React Static Dashboard** (`cybertwin-dashboard`)

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
