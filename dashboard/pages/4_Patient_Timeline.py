import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random
import torch
import torch.nn as nn

st.set_page_config(layout="wide")

st.title("📈 Patient Timeline & Vital History")

# ----------------------------------------------------------
# ICU PATIENT DATABASE
# ----------------------------------------------------------

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

# ----------------------------------------------------------
# PATIENT SELECTOR
# ----------------------------------------------------------

selected_patient=st.selectbox(
"Select Patient",
list(patients.keys())
)

st.write("Monitoring History for Patient:",selected_patient)
st.write("ICU Bed:",patients[selected_patient])

# ----------------------------------------------------------
# GENERATE HISTORICAL VITAL DATA
# ----------------------------------------------------------

time_steps=50

hr_history=np.random.normal(80,3,time_steps)
spo2_history=np.random.normal(97,0.4,time_steps)
rr_history=np.random.normal(16,1,time_steps)

# ----------------------------------------------------------
# HEART RATE HISTORY
# ----------------------------------------------------------

st.subheader("Heart Rate History")

fig_hr=go.Figure()

fig_hr.add_trace(
go.Scatter(
y=hr_history,
mode="lines+markers",
name="Heart Rate"
)
)

fig_hr.update_layout(
yaxis_title="BPM",
xaxis_title="Time",
template="plotly_dark"
)

st.plotly_chart(fig_hr,width="stretch")

# ----------------------------------------------------------
# SPO2 HISTORY
# ----------------------------------------------------------

st.subheader("SpO₂ History")

fig_spo2=go.Figure()

fig_spo2.add_trace(
go.Scatter(
y=spo2_history,
mode="lines+markers",
name="SpO₂"
)
)

fig_spo2.update_layout(
yaxis_title="SpO₂ %",
xaxis_title="Time",
template="plotly_dark"
)

st.plotly_chart(fig_spo2,width="stretch")

# ----------------------------------------------------------
# RESPIRATORY RATE HISTORY
# ----------------------------------------------------------

st.subheader("Respiratory Rate History")

fig_rr=go.Figure()

fig_rr.add_trace(
go.Scatter(
y=rr_history,
mode="lines+markers",
name="Resp Rate"
)
)

fig_rr.update_layout(
yaxis_title="Breaths/min",
xaxis_title="Time",
template="plotly_dark"
)

st.plotly_chart(fig_rr,width="stretch")

# ----------------------------------------------------------
# LSTM MODEL
# ----------------------------------------------------------

class LSTMModel(nn.Module):

    def __init__(self):

        super().__init__()

        self.lstm=nn.LSTM(3,64,2,batch_first=True)
        self.fc=nn.Linear(64,1)
        self.sig=nn.Sigmoid()

    def forward(self,x):

        out,_=self.lstm(x)
        out=out[:,-1,:]
        out=self.fc(out)

        return self.sig(out)

@st.cache_resource
def load_model():

    model=LSTMModel()

    try:
        model.load_state_dict(torch.load("icu_lstm_model.pth",map_location="cpu"))
    except:
        pass

    model.eval()

    return model

model=load_model()

# ----------------------------------------------------------
# AI RISK TIMELINE
# ----------------------------------------------------------

st.subheader("AI Risk Timeline")

risk_history=[]

for i in range(time_steps):

    sample=np.array([
        hr_history[max(0,i-20):i+1],
        spo2_history[max(0,i-20):i+1],
        rr_history[max(0,i-20):i+1]
    ]).T

    if len(sample)<5:
        risk_history.append(random.uniform(20,40))
        continue

    input_tensor=torch.tensor(sample,dtype=torch.float32).unsqueeze(0)

    with torch.no_grad():
        pred=model(input_tensor)

    risk_history.append(float(pred.item()*100))

fig_risk=go.Figure()

fig_risk.add_trace(
go.Scatter(
y=risk_history,
mode="lines+markers",
name="Risk %"
)
)

fig_risk.update_layout(
yaxis_title="Risk %",
xaxis_title="Time",
template="plotly_dark"
)

st.plotly_chart(fig_risk,width="stretch")

# ----------------------------------------------------------
# PATIENT DETERIORATION ALERT
# ----------------------------------------------------------

st.subheader("Deterioration Analysis")

latest_risk=risk_history[-1]

if latest_risk<40:

    st.success("Patient condition stable")

elif latest_risk<70:

    st.warning("Moderate deterioration risk")

else:

    st.error("High deterioration risk detected")

# ----------------------------------------------------------
# SUMMARY
# ----------------------------------------------------------

st.info(
"Timeline analysis shows how patient vitals and AI risk prediction evolve over time."
)