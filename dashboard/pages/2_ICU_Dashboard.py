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

# ---------------------------------------------------------
# PROFESSIONAL ICU THEME
# ---------------------------------------------------------

st.markdown("""
<style>

body{
background:#071028;
color:white;
}

.metric-card{
background:#121c35;
padding:18px;
border-radius:12px;
border:1px solid #1e2c4a;
text-align:center;
}

.section{
font-size:22px;
font-weight:600;
margin-top:25px;
color:#7dd3fc;
}

.event-log{
background:#0f172a;
padding:15px;
border-radius:10px;
border:1px solid #1e293b;
font-family:monospace;
}

</style>
""", unsafe_allow_html=True)

st.title("🏥 AI ICU Guardian – Patient Monitoring Dashboard")

# ----------------------------------------------------------
# DEMO MODE
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
# SIDEBAR CONTROL PANEL
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

# ----------------------------------------------------------
# AUTO REFRESH
# ----------------------------------------------------------

if demo_mode:
    st_autorefresh(interval=1500,key="icu_refresh")

# ----------------------------------------------------------
# CURRENT PATIENT
# ----------------------------------------------------------

st.markdown('<div class="section">Monitoring Patient</div>',unsafe_allow_html=True)

st.write(f"Patient ID: **{selected_patient}**")
st.write(f"Assigned ICU Bed: **{patients[selected_patient]}**")

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

st.markdown('<div class="section">Live Patient Vital Signs</div>',unsafe_allow_html=True)

v1,v2,v3=st.columns(3)

v1.metric("Heart Rate",f"{round(new_hr,1)} bpm")
v2.metric("SpO₂",f"{round(new_spo2,1)} %")
v3.metric("Respiratory Rate",f"{round(new_rr,1)} /min")

# ----------------------------------------------------------
# ECG MONITOR
# ----------------------------------------------------------

st.markdown('<div class="section">Real-Time ECG Monitor</div>',unsafe_allow_html=True)

t=np.linspace(0,1,200)
ecg=np.sin(20*np.pi*t)+np.random.normal(0,0.1,200)

fig_ecg=go.Figure()

fig_ecg.add_trace(go.Scatter(
y=ecg,
mode="lines",
line=dict(color="#00ff9c",width=2)
))

fig_ecg.update_layout(
template="plotly_dark",
height=300,
plot_bgcolor="black",
margin=dict(l=20,r=20,t=20,b=20)
)

st.plotly_chart(fig_ecg,use_container_width=True)

# ----------------------------------------------------------
# VITAL TRENDS
# ----------------------------------------------------------

col1,col2=st.columns(2)

with col1:

    st.subheader("Heart Rate Trend")

    fig_hr=go.Figure()
    fig_hr.add_trace(go.Scatter(y=hr_data,mode="lines"))
    fig_hr.update_layout(template="plotly_dark")

    st.plotly_chart(fig_hr,use_container_width=True)

with col2:

    st.subheader("SpO₂ Trend")

    fig_spo2=go.Figure()
    fig_spo2.add_trace(go.Scatter(y=spo2_data,mode="lines"))
    fig_spo2.update_layout(template="plotly_dark")

    st.plotly_chart(fig_spo2,use_container_width=True)

# ----------------------------------------------------------
# RESP RATE TREND
# ----------------------------------------------------------

st.subheader("Respiratory Rate Trend")

fig_rr=go.Figure()
fig_rr.add_trace(go.Scatter(y=rr_data,mode="lines"))
fig_rr.update_layout(template="plotly_dark")

st.plotly_chart(fig_rr,use_container_width=True)

# ----------------------------------------------------------
# NEWS SCORE
# ----------------------------------------------------------

st.markdown('<div class="section">Early Warning Score (NEWS)</div>',unsafe_allow_html=True)

ews=0

if new_hr>100 or new_hr<60:
    ews+=2

if new_spo2<94:
    ews+=2

if new_rr>22:
    ews+=2

st.metric("NEWS Score",ews)

# ----------------------------------------------------------
# AI RECOMMENDATION
# ----------------------------------------------------------

st.markdown('<div class="section">AI Clinical Recommendation</div>',unsafe_allow_html=True)

recommendation=""

if new_spo2<92:
    recommendation+="⚠ Oxygen saturation critically low.\n\n"

elif new_spo2<95:
    recommendation+="⚠ Oxygen slightly low.\n\n"

if new_hr>110:
    recommendation+="⚠ Elevated heart rate.\n\n"

elif new_hr<60:
    recommendation+="⚠ Low heart rate.\n\n"

if new_rr>22:
    recommendation+="⚠ Respiratory distress suspected.\n\n"

if recommendation=="":
    recommendation="✅ Patient vital signs within normal limits."

st.info(recommendation)

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
# AI RISK PREDICTION
# ----------------------------------------------------------

st.markdown('<div class="section">AI Patient Risk Prediction</div>',unsafe_allow_html=True)

input_data=np.array([
hr_data[-20:],
spo2_data[-20:],
rr_data[-20:]
]).T

input_tensor=torch.tensor(input_data,dtype=torch.float32).unsqueeze(0)

with torch.no_grad():
    prediction=model(input_tensor)

risk=float(prediction.item()*100)

if demo_mode:
    risk+=random.uniform(-5,5)

risk=max(0,min(100,risk))

if risk<40:
    st.success("Patient stable → Continue monitoring")

elif risk<70:
    st.warning("Moderate risk → Increase monitoring")

else:
    st.error("High risk → Immediate intervention")

# ----------------------------------------------------------
# RISK GAUGE
# ----------------------------------------------------------

fig=go.Figure(go.Indicator(
mode="gauge+number",
value=risk,
title={'text':"AI Patient Risk Score"},
gauge={
'axis':{'range':[0,100]},
'bar':{'color':"#00bfff"},
'steps':[
{'range':[0,40],'color':"#15803d"},
{'range':[40,70],'color':"#facc15"},
{'range':[70,100],'color':"#dc2626"}
]
}
))

fig.update_layout(height=400)

st.plotly_chart(fig,use_container_width=True)

# ----------------------------------------------------------
# EVENT LOG
# ----------------------------------------------------------

st.markdown('<div class="section">Patient Event Log</div>',unsafe_allow_html=True)

if "event_log" not in st.session_state:
    st.session_state.event_log=[]

time=datetime.now().strftime("%H:%M:%S")

event=f"{time} | HR {round(new_hr)} | SpO2 {round(new_spo2)}"

st.session_state.event_log.insert(0,event)
st.session_state.event_log=st.session_state.event_log[:10]

st.markdown('<div class="event-log">',unsafe_allow_html=True)

for e in st.session_state.event_log:
    st.write(e)

st.markdown('</div>',unsafe_allow_html=True)

# ----------------------------------------------------------
# DIGITAL TWIN
# ----------------------------------------------------------

st.markdown('<div class="section">24 Hour Patient Digital Twin</div>',unsafe_allow_html=True)

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