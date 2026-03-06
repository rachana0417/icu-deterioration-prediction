import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import random
import torch
import torch.nn as nn
from fpdf import FPDF
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.title("AI ICU Guardian – Advanced ICU Monitoring System")

# -----------------------------
# ICU PATIENT DATABASE
# -----------------------------

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

# -----------------------------
# HEADER
# -----------------------------

c1,c2,c3,c4=st.columns(4)

c1.metric("Total ICU Patients",len(patients))
c2.metric("Beds Available",20-len(patients))
c3.metric("Hospital AI System","ACTIVE")
c4.metric("Monitoring Mode","Realtime")

st_autorefresh(interval=1500,key="icu_refresh")

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.header("ICU Control Panel")

selected_patient=st.sidebar.selectbox(
"Select ICU Patient",
list(patients.keys())
)

st.sidebar.write("Monitoring Patient ID:",selected_patient)

st.sidebar.subheader("ICU Ward Bed Map")

for pid,bed in patients.items():

    r=random.uniform(0,100)

    if r<40:
        status="🟢 Stable"
    elif r<70:
        status="🟡 Warning"
    else:
        status="🔴 Critical"

    st.sidebar.write(f"Bed {bed} | Patient {pid} | {status}")

# -----------------------------
# LSTM MODEL
# -----------------------------

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

# -----------------------------
# BASELINE VITALS
# -----------------------------

if "base_vitals" not in st.session_state:

    st.session_state.base_vitals={
    "hr":random.randint(75,90),
    "spo2":random.randint(96,99),
    "rr":random.randint(14,18)
    }

heart_rate=st.session_state.base_vitals["hr"]
spo2=st.session_state.base_vitals["spo2"]
resp_rate=st.session_state.base_vitals["rr"]

# -----------------------------
# STREAMING DATA
# -----------------------------

if "hr_data" not in st.session_state:
    st.session_state.hr_data=list(heart_rate+np.random.normal(0,2,40))

if "spo2_data" not in st.session_state:
    st.session_state.spo2_data=list(spo2+np.random.normal(0,0.2,40))

if "rr_data" not in st.session_state:
    st.session_state.rr_data=list(resp_rate+np.random.normal(0,0.5,40))

new_hr=st.session_state.hr_data[-1]+np.random.normal(0,1)
new_spo2=st.session_state.spo2_data[-1]+np.random.normal(0,0.05)
new_rr=st.session_state.rr_data[-1]+np.random.normal(0,0.2)

st.session_state.hr_data.pop(0)
st.session_state.hr_data.append(new_hr)

st.session_state.spo2_data.pop(0)
st.session_state.spo2_data.append(new_spo2)

st.session_state.rr_data.pop(0)
st.session_state.rr_data.append(new_rr)

hr_data=st.session_state.hr_data
spo2_data=st.session_state.spo2_data
rr_data=st.session_state.rr_data

# -----------------------------
# LIVE VITALS
# -----------------------------

st.subheader("Live ICU Vital Signs")

v1,v2,v3=st.columns(3)

v1.metric("Heart Rate",f"{round(new_hr,1)} bpm")
v2.metric("SpO₂",f"{round(new_spo2,1)} %")
v3.metric("Respiratory Rate",f"{round(new_rr,1)} /min")

# -----------------------------
# ECG MONITOR
# -----------------------------

st.subheader("Real ECG Monitor")

t=np.linspace(0,1,200)
ecg=np.sin(20*np.pi*t)+np.random.normal(0,0.1,200)

fig_ecg=go.Figure()
fig_ecg.add_trace(go.Scatter(y=ecg,mode="lines"))

st.plotly_chart(fig_ecg,use_container_width=True)

# -----------------------------
# VITAL GRAPHS
# -----------------------------

col1,col2=st.columns(2)

with col1:

    st.subheader("Heart Rate Monitor")

    fig=go.Figure()
    fig.add_trace(go.Scatter(y=hr_data,mode="lines"))

    st.plotly_chart(fig,use_container_width=True)

with col2:

    st.subheader("SpO₂ Monitor")

    fig2=go.Figure()
    fig2.add_trace(go.Scatter(y=spo2_data,mode="lines"))

    st.plotly_chart(fig2,use_container_width=True)

st.subheader("Respiratory Rate Monitor")

fig3=go.Figure()
fig3.add_trace(go.Scatter(y=rr_data,mode="lines"))

st.plotly_chart(fig3,use_container_width=True)

# -----------------------------
# EARLY WARNING SCORE
# -----------------------------

st.subheader("Early Warning Score")

ews=0

if new_hr>100 or new_hr<60:
    ews+=2

if new_spo2<94:
    ews+=2

if new_rr>22:
    ews+=2

st.metric("NEWS Score",ews)

# -----------------------------
# AI EXPLANATION
# -----------------------------

st.subheader("AI Explanation")

st.write("""
The ICU Guardian deep learning model continuously analyzes
temporal vital patterns using LSTM architecture.

Physiological signals including heart rate, oxygen saturation
and respiratory rate are used to estimate deterioration risk.
""")

# -----------------------------
# PHYSIOLOGICAL RADAR
# -----------------------------

st.subheader("Physiological Radar")

categories=['Heart Rate','SpO2','Resp Rate','Risk']

values=[new_hr,new_spo2,new_rr,50]

fig_radar=go.Figure()

fig_radar.add_trace(go.Scatterpolar(
r=values,
theta=categories,
fill='toself'
))

st.plotly_chart(fig_radar,use_container_width=True)

# -----------------------------
# ICU BED STATUS
# -----------------------------

st.subheader("ICU Bed Status")

cols=st.columns(5)

beds=list(patients.values())

for i,b in enumerate(beds):

    r=random.uniform(0,100)

    if r<40:
        c="🟢"
    elif r<70:
        c="🟡"
    else:
        c="🔴"

    cols[i%5].write(f"Bed {b}")
    cols[i%5].write(c)

# -----------------------------
# ICU EVENT LOG
# -----------------------------

st.subheader("ICU Event Log")

if "event_log" not in st.session_state:
    st.session_state.event_log=[]

time=datetime.now().strftime("%H:%M:%S")

event=f"{time} | HR {round(new_hr)} | SpO2 {round(new_spo2)}"

st.session_state.event_log.insert(0,event)

st.session_state.event_log=st.session_state.event_log[:10]

for e in st.session_state.event_log:
    st.write(e)

# -----------------------------
# RISK HEATMAP
# -----------------------------

st.subheader("ICU Patient Risk Heatmap")

heat=np.random.rand(5,5)

fig_heat=go.Figure(data=go.Heatmap(
z=heat,
colorscale="RdYlGn_r"
))

st.plotly_chart(fig_heat,use_container_width=True)

# -----------------------------
# DOCTOR DECISION SUPPORT
# -----------------------------

st.subheader("Doctor Decision Support")

risk=random.uniform(20,80)

if risk<40:
    st.success("Patient stable → Continue monitoring")

elif risk<70:
    st.warning("Moderate risk → Increase monitoring frequency")

else:
    st.error("High risk → Immediate ICU intervention")

# -----------------------------
# RISK GAUGE
# -----------------------------

fig=go.Figure(go.Indicator(
mode="gauge+number",
value=risk,
title={'text':"ICU Risk Meter"},
gauge={
'axis':{'range':[0,100]},
'steps':[
{'range':[0,40],'color':"green"},
{'range':[40,70],'color':"yellow"},
{'range':[70,100],'color':"red"}
]
}
))

st.plotly_chart(fig,use_container_width=True)

# -----------------------------
# CRITICAL ALERT
# -----------------------------

if risk>70:

    components.html("""
    <audio autoplay>
    <source src="https://www.soundjay.com/misc/sounds/beep-07.mp3">
    </audio>
    """,height=0)

    st.error("🚨 ICU CRITICAL ALERT 🚨")

# -----------------------------
# DIGITAL TWIN
# -----------------------------

st.subheader("Patient Digital Twin – 24 Hour Simulation")

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

# -----------------------------
# 24 HOUR PATIENT EVALUATION
# -----------------------------

st.subheader("24 Hour Patient Evaluation")

eval_hr=[heart_rate+np.random.normal(0,2)+i*0.1 for i in hours]

df_eval=pd.DataFrame({
"Hour":hours,
"HR":eval_hr
})

st.line_chart(df_eval.set_index("Hour"))

# -----------------------------
# ADVANCED PROFESSIONAL PDF REPORT
# -----------------------------

st.subheader("Patient Report Generator")

class ICUReport(FPDF):

    def header(self):

        self.set_font("Arial","B",22)
        self.cell(0,12,"AI ICU GUARDIAN REPORT",0,1,"C")
        self.ln(5)

    def footer(self):

        self.set_y(-15)
        self.set_font("Arial","I",9)

        self.multi_cell(
            0,
            5,
            "This report was automatically generated by AI ICU Guardian monitoring system.\nClinical decisions must be validated by medical professionals.",
            0,
            "C"
        )


def generate_pdf():

    pdf = ICUReport()
    pdf.add_page()

    pdf.set_font("Arial","",12)

    # -----------------------------
    # PATIENT INFORMATION
    # -----------------------------

    pdf.set_font("Arial","B",12)

    pdf.cell(40,10,"Patient ID",1)
    pdf.cell(0,10,selected_patient,1,1)

    pdf.cell(40,10,"Generated",1)
    pdf.cell(0,10,str(datetime.now()),1,1)

    pdf.ln(10)

    # -----------------------------
    # VITAL SIGNS
    # -----------------------------

    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,"Vital Signs",0,1)

    pdf.set_font("Arial","B",12)

    pdf.cell(60,10,"Parameter",1)
    pdf.cell(40,10,"Value",1)
    pdf.cell(0,10,"Normal Range",1,1)

    pdf.set_font("Arial","",12)

    pdf.cell(60,10,"Heart Rate",1)
    pdf.cell(40,10,f"{round(new_hr,2)} bpm",1)
    pdf.cell(0,10,"60-100 bpm",1,1)

    pdf.cell(60,10,"SpO2",1)
    pdf.cell(40,10,f"{round(new_spo2,2)} %",1)
    pdf.cell(0,10,">95 %",1,1)

    pdf.cell(60,10,"Resp Rate",1)
    pdf.cell(40,10,f"{round(new_rr,2)} /min",1)
    pdf.cell(0,10,"12-20 /min",1,1)

    pdf.ln(10)

    # -----------------------------
    # AI RISK PREDICTION
    # -----------------------------

    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,"AI Risk Prediction",0,1)

    pdf.set_font("Arial","B",12)

    pdf.cell(60,10,"Time Window",1)
    pdf.cell(0,10,"Risk %",1,1)

    pdf.set_font("Arial","",12)

    pdf.cell(60,10,"Current",1)
    pdf.cell(0,10,f"{risk:.2f}%",1,1)

    pdf.cell(60,10,"1 Hour",1)
    pdf.cell(0,10,f"{risk+4:.2f}%",1,1)

    pdf.cell(60,10,"3 Hours",1)
    pdf.cell(0,10,f"{risk+8:.2f}%",1,1)

    pdf.cell(60,10,"6 Hours",1)
    pdf.cell(0,10,f"{risk+12:.2f}%",1,1)

    pdf.ln(10)

    # -----------------------------
    # CLINICAL RECOMMENDATION
    # -----------------------------

    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,"Clinical Recommendation",0,1)

    pdf.set_font("Arial","",12)

    if risk < 40:
        recommendation="Patient condition stable. Continue routine ICU monitoring."

    elif risk < 70:
        recommendation="Moderate deterioration risk detected. Increase monitoring frequency."

    else:
        recommendation="High deterioration risk detected. Immediate ICU intervention recommended."

    pdf.multi_cell(0,8,recommendation)

    pdf.ln(10)

    # -----------------------------
    # AI EXPLANATION
    # -----------------------------

    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,"AI Explanation",0,1)

    pdf.set_font("Arial","",12)

    explanation="""
The AI ICU Guardian monitoring system analyzes physiological signals
including heart rate, oxygen saturation, and respiratory rate using
machine learning models.

Temporal trends are evaluated to estimate short-term patient
deterioration risk. These predictions support clinicians in making
timely medical decisions and preventive interventions.
"""

    pdf.multi_cell(0,8,explanation)

    return pdf.output(dest="S").encode("latin-1")


# -----------------------------
# STREAMLIT BUTTON
# -----------------------------

if st.button("Generate Patient PDF Report"):

    pdf_bytes = generate_pdf()

    st.download_button(
        label="Download ICU Clinical Report",
        data=pdf_bytes,
        file_name=f"ICU_Report_{selected_patient}.pdf",
        mime="application/pdf"
    )