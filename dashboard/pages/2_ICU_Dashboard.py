import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import random
import torch
import torch.nn as nn
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide")

st.title("🏥 AI ICU Guardian – Patient Monitoring Dashboard")

# ----------------------------------------------------------
# AUTO DEMO MODE
# ----------------------------------------------------------

st.sidebar.subheader("Demo Mode")

demo_mode = st.sidebar.toggle("Enable Live ICU Simulation", value=True)

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
# SIDEBAR PATIENT SELECTION
# ----------------------------------------------------------

st.sidebar.header("ICU Control Panel")

selected_patient=st.sidebar.selectbox(
"Select ICU Patient",
list(patients.keys())
)

st.sidebar.write("Monitoring Patient:",selected_patient)

# ----------------------------------------------------------
# HEADER METRICS
# ----------------------------------------------------------

c1,c2,c3,c4=st.columns(4)

c1.metric("Total ICU Patients",len(patients))
c2.metric("Beds Available",20-len(patients))
c3.metric("Hospital AI System","ACTIVE")
c4.metric("Monitoring Mode","Realtime")

# Auto refresh only in demo mode
if demo_mode:
    st_autorefresh(interval=1500,key="icu_refresh")

# ----------------------------------------------------------
# CURRENT PATIENT INFO
# ----------------------------------------------------------

st.subheader(f"Monitoring Patient ID: {selected_patient}")
st.write(f"Assigned ICU Bed: {patients[selected_patient]}")

# ----------------------------------------------------------
# BASELINE VITALS
# ----------------------------------------------------------

if "base_vitals" not in st.session_state:

    st.session_state.base_vitals={
        "hr":random.randint(75,90),
        "spo2":random.randint(96,99),
        "rr":random.randint(14,18)
    }

heart_rate=st.session_state.base_vitals["hr"]
spo2=st.session_state.base_vitals["spo2"]
resp_rate=st.session_state.base_vitals["rr"]

# ----------------------------------------------------------
# STREAMING DATA
# ----------------------------------------------------------

if "hr_data" not in st.session_state:
    st.session_state.hr_data=list(heart_rate+np.random.normal(0,2,40))

if "spo2_data" not in st.session_state:
    st.session_state.spo2_data=list(spo2+np.random.normal(0,0.2,40))

if "rr_data" not in st.session_state:
    st.session_state.rr_data=list(resp_rate+np.random.normal(0,0.5,40))

# Demo simulation
if demo_mode:

    new_hr = st.session_state.hr_data[-1] + np.random.normal(0,2)
    new_spo2 = st.session_state.spo2_data[-1] + np.random.normal(0,0.2)
    new_rr = st.session_state.rr_data[-1] + np.random.normal(0,0.5)

else:

    new_hr = st.session_state.hr_data[-1]
    new_spo2 = st.session_state.spo2_data[-1]
    new_rr = st.session_state.rr_data[-1]

st.session_state.hr_data.pop(0)
st.session_state.hr_data.append(new_hr)

st.session_state.spo2_data.pop(0)
st.session_state.spo2_data.append(new_spo2)

st.session_state.rr_data.pop(0)
st.session_state.rr_data.append(new_rr)

hr_data=st.session_state.hr_data
spo2_data=st.session_state.spo2_data
rr_data=st.session_state.rr_data

# ----------------------------------------------------------
# LIVE VITALS
# ----------------------------------------------------------

st.subheader("Live Patient Vital Signs")

v1,v2,v3=st.columns(3)

v1.metric("Heart Rate",f"{round(new_hr,1)} bpm")
v2.metric("SpO₂",f"{round(new_spo2,1)} %")
v3.metric("Respiratory Rate",f"{round(new_rr,1)} /min")

# ----------------------------------------------------------
# ECG MONITOR
# ----------------------------------------------------------

st.subheader("Real-Time ECG Monitor")

t=np.linspace(0,1,200)
ecg=np.sin(20*np.pi*t)+np.random.normal(0,0.1,200)

fig_ecg=go.Figure()
fig_ecg.add_trace(go.Scatter(y=ecg,mode="lines"))

fig_ecg.update_layout(template="plotly_dark",height=300)

st.plotly_chart(fig_ecg,width="stretch")

# ----------------------------------------------------------
# VITAL TRENDS
# ----------------------------------------------------------

col1,col2=st.columns(2)

with col1:

    st.subheader("Heart Rate Trend")

    fig_hr=go.Figure()
    fig_hr.add_trace(go.Scatter(y=hr_data,mode="lines"))
    fig_hr.update_layout(template="plotly_dark")

    st.plotly_chart(fig_hr,width="stretch")

with col2:

    st.subheader("SpO₂ Trend")

    fig_spo2=go.Figure()
    fig_spo2.add_trace(go.Scatter(y=spo2_data,mode="lines"))
    fig_spo2.update_layout(template="plotly_dark")

    st.plotly_chart(fig_spo2,width="stretch")

# ----------------------------------------------------------
# RESPIRATORY RATE
# ----------------------------------------------------------

st.subheader("Respiratory Rate Trend")

fig_rr=go.Figure()
fig_rr.add_trace(go.Scatter(y=rr_data,mode="lines"))
fig_rr.update_layout(template="plotly_dark")

st.plotly_chart(fig_rr,width="stretch")

# ----------------------------------------------------------
# NEWS SCORE
# ----------------------------------------------------------

st.subheader("Early Warning Score (NEWS)")

ews=0

if new_hr>100 or new_hr<60:
    ews+=2

if new_spo2<94:
    ews+=2

if new_rr>22:
    ews+=2

st.metric("NEWS Score",ews)

# ----------------------------------------------------------
# AI CLINICAL RECOMMENDATION
# ----------------------------------------------------------

st.subheader("AI Clinical Recommendation")

recommendation=""

if new_spo2<92:
    recommendation+="⚠ Oxygen saturation critically low.\n\n"

elif new_spo2<95:
    recommendation+="⚠ Oxygen saturation slightly below optimal.\n\n"

if new_hr>110:
    recommendation+="⚠ Elevated heart rate detected.\n\n"

elif new_hr<60:
    recommendation+="⚠ Low heart rate detected.\n\n"

if new_rr>22:
    recommendation+="⚠ Respiratory distress suspected.\n\n"

if recommendation=="":
    recommendation="✅ Patient vital signs within normal limits."

st.info(recommendation)

# ----------------------------------------------------------
# LSTM AI MODEL
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
# AI RISK PREDICTION
# ----------------------------------------------------------

st.subheader("AI Patient Risk Prediction")

input_data=np.array([
hr_data[-20:],
spo2_data[-20:],
rr_data[-20:]
]).T

input_tensor=torch.tensor(input_data,dtype=torch.float32).unsqueeze(0)

with torch.no_grad():
    prediction=model(input_tensor)

risk=float(prediction.item()*100)

# Demo fluctuation
if demo_mode:
    risk += random.uniform(-5,5)
    risk=max(0,min(100,risk))

# Occasional deterioration event
if demo_mode and random.random() < 0.05:
    risk += random.uniform(15,25)
    risk=max(0,min(100,risk))

if risk<40:
    st.success("Patient stable → Continue monitoring")
elif risk<70:
    st.warning("Moderate risk → Increase monitoring frequency")
else:
    st.error("High risk → Immediate ICU intervention")

# ----------------------------------------------------------
# RISK GAUGE
# ----------------------------------------------------------

fig=go.Figure(go.Indicator(
mode="gauge+number",
value=risk,
title={'text':"Patient Risk Meter"},
gauge={
'axis':{'range':[0,100]},
'steps':[
{'range':[0,40],'color':"green"},
{'range':[40,70],'color':"yellow"},
{'range':[70,100],'color':"red"}
]
}
))

st.plotly_chart(fig,width="stretch")

# ----------------------------------------------------------
# EVENT LOG
# ----------------------------------------------------------

st.subheader("Patient Event Log")

if "event_log" not in st.session_state:
    st.session_state.event_log=[]

time=datetime.now().strftime("%H:%M:%S")

event=f"{time} | HR {round(new_hr)} | SpO2 {round(new_spo2)}"

st.session_state.event_log.insert(0,event)
st.session_state.event_log=st.session_state.event_log[:10]

for e in st.session_state.event_log:
    st.write(e)

# ----------------------------------------------------------
# DIGITAL TWIN SIMULATION
# ----------------------------------------------------------

st.subheader("24 Hour Patient Digital Twin")

hours=np.arange(1,25)

sim_hr=[heart_rate+np.random.normal(0,2)+i*0.1 for i in hours]
sim_rr=[resp_rate+np.random.normal(0,1)+i*0.05 for i in hours]
sim_spo2=[spo2+np.random.normal(0,0.2)-i*0.02 for i in hours]

df=pd.DataFrame({
"Hour":hours,
"Heart Rate":sim_hr,
"Resp Rate":sim_rr,
"SpO2":sim_spo2
})

st.line_chart(df.set_index("Hour"))