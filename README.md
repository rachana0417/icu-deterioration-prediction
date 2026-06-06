# 🏥 AI ICU Guardian

> AI-Powered ICU Patient Deterioration Prediction System using Time Series Deep Learning

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![LSTM](https://img.shields.io/badge/Model-LSTM-green)

## 📌 Overview
AI ICU Guardian is a real-time ICU patient monitoring and deterioration prediction system. It uses an LSTM deep learning model trained on clinical time series data to predict early patient deterioration, helping doctors intervene before critical events.

## 🚀 Features
- 🔴 **Live ICU Monitoring** — Real-time vital signs tracking
- 🤖 **AI Risk Prediction** — LSTM model predicts deterioration risk
- 📊 **ICU Ward Overview** — Bird's eye view of all patients
- 📈 **Patient Timeline** — Historical vitals and trends
- 🧠 **AI Explainability** — Understand model decisions
- 📄 **Automated Reports** — Generate clinical PDF reports
- 🚨 **ICU Alert Center** — Critical alerts and notifications
- 🏥 **Hospital Analytics** — Overall hospital performance

## 🛠️ Tech Stack
- **Frontend:** Streamlit, Custom CSS
- **Backend:** Python
- **ML Model:** LSTM (PyTorch)
- **Data:** MIMIC-IV Clinical Database

## ⚙️ Installation
```bash
git clone https://github.com/rachana0417/icu-deterioration-prediction.git
cd icu-deterioration-prediction
pip install -r requirements.txt
```

## ▶️ Run
```bash
streamlit run dashboard/app.py
```

## 📁 Project Structure
├── dashboard/
│   ├── pages/
│   │   ├── 0_Home.py
│   │   ├── 1_Patient_Profile.py
│   │   ├── 2_ICU_Dashboard.py
│   │   └── ...
│   └── app.py
├── data/
├── models/
│   └── lstm_model.pth
├── training/
└── utils/
## 👩‍💻 Author
**Rachana Nagaraj** — [github.com/rachana0417](https://github.com/rachana0417)
