import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide")

# ------------------------------------------------
# AUTO REFRESH (LIVE MONITOR)
# ------------------------------------------------

st_autorefresh(interval=2000,key="ai_refresh")

st.title("🤖 AI Explainability – Risk Analysis")

# ------------------------------------------------
# PATIENT DATABASE
# ------------------------------------------------

patients={
"39711498":8,
"32145159":4,
"34629895":3,
"32604416":1,
"36084844":2,
"32506122":6,
"39804682":7,
"37057036":10,
"35258379":9,
"34617352":5
}

# ------------------------------------------------
# SELECT PATIENT
# ------------------------------------------------

selected_patient=st.selectbox(
"Select Patient",
list(patients.keys())
)

st.write("Analyzing AI decision for Patient:",selected_patient)

# ------------------------------------------------
# SIMULATED CURRENT VITALS (LIVE)
# ------------------------------------------------

heart_rate=random.randint(70,110)
spo2=random.randint(92,100)
resp_rate=random.randint(14,24)

st.subheader("Current Vital Signs")

c1,c2,c3=st.columns(3)

c1.metric("🟢 Heart Rate",f"{heart_rate} bpm")
c2.metric("🟡 SpO₂",f"{spo2}%")
c3.metric("🔵 Resp Rate",f"{resp_rate}/min")

# ------------------------------------------------
# FEATURE IMPORTANCE CALCULATION
# ------------------------------------------------

importance={
"Heart Rate":abs(heart_rate-80),
"SpO₂":abs(98-spo2),
"Resp Rate":abs(resp_rate-16)
}

df=pd.DataFrame(
list(importance.items()),
columns=["Vital Sign","Contribution"]
)

# ------------------------------------------------
# FEATURE IMPORTANCE BAR CHART
# ------------------------------------------------

st.subheader("AI Feature Contribution")

colors=[
"#00FF66",   # heart rate
"#FFD400",   # spo2
"#00D4FF"    # resp rate
]

fig=go.Figure()

fig.add_trace(
go.Bar(
x=df["Vital Sign"],
y=df["Contribution"],
marker_color=colors
)
)

fig.update_layout(
template="plotly_dark",
plot_bgcolor="black",
paper_bgcolor="black",
yaxis_title="Contribution to Risk",
xaxis_title="Vital Sign",
height=400
)

st.plotly_chart(fig,use_container_width=True)

# ------------------------------------------------
# PATIENT CLINICAL SUMMARY
# ------------------------------------------------

st.subheader("Patient Clinical Summary")

risk=random.randint(20,85)

if risk < 40:
    status="Stable"
elif risk < 70:
    status="Moderate Risk"
else:
    status="Critical"

summary_data={
"Patient ID":selected_patient,
"ICU Bed":patients[selected_patient],
"Heart Rate":f"{heart_rate} bpm",
"SpO₂":f"{spo2} %",
"Resp Rate":f"{resp_rate} /min",
"Risk Level":f"{risk} %",
"Status":status
}

summary_df=pd.DataFrame(
summary_data.items(),
columns=["Parameter","Value"]
)

st.table(summary_df)

# ------------------------------------------------
# PHYSIOLOGICAL RADAR
# ------------------------------------------------

st.subheader("Physiological Radar")

categories=['Heart Rate','SpO₂','Resp Rate']

values=[heart_rate,spo2,resp_rate]

fig_radar=go.Figure()

fig_radar.add_trace(go.Scatterpolar(
r=values,
theta=categories,
fill='toself',
line=dict(color="#7c3aed")
))

fig_radar.update_layout(
template="plotly_dark",
polar=dict(
bgcolor="black"
),
height=400
)

st.plotly_chart(fig_radar,use_container_width=True)

# ------------------------------------------------
# AI EXPLANATION PANEL
# ------------------------------------------------

st.subheader("AI Explanation")

if risk < 40:

    st.success("AI predicts patient condition is stable based on current vitals.")

elif risk < 70:

    st.warning("AI detects moderate risk due to deviations in vital signs.")

else:

    st.error("AI detects high deterioration risk. Immediate clinical review recommended.")