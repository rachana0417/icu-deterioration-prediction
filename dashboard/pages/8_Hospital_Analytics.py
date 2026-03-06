import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random

st.set_page_config(layout="wide")

st.title("🏥 Hospital ICU Analytics")

# ------------------------------------------------
# ICU PATIENT DATABASE
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
# GENERATE RISK DATA
# ------------------------------------------------

risk_values=[]

for p in patients.keys():
    risk_values.append(random.randint(10,90))

df=pd.DataFrame({
"Patient":list(patients.keys()),
"Bed":list(patients.values()),
"Risk":risk_values
})

# ------------------------------------------------
# ICU METRICS
# ------------------------------------------------

st.subheader("ICU Statistics")

c1,c2,c3=st.columns(3)

c1.metric("Total ICU Patients",len(df))
c2.metric("Available Beds",20-len(df))
c3.metric("Average Risk",round(df["Risk"].mean(),1))

# ------------------------------------------------
# RISK DISTRIBUTION PIE
# ------------------------------------------------

st.subheader("Patient Risk Distribution")

low=(df["Risk"]<40).sum()
mid=((df["Risk"]>=40)&(df["Risk"]<70)).sum()
high=(df["Risk"]>=70).sum()

fig=go.Figure(data=[go.Pie(
labels=["Stable","Moderate","Critical"],
values=[low,mid,high]
)])

fig.update_layout(template="plotly_dark")

st.plotly_chart(fig,width="stretch")

# ------------------------------------------------
# RISK BAR CHART
# ------------------------------------------------

st.subheader("Patient Risk Levels")

fig2=go.Figure(go.Bar(
x=df["Patient"],
y=df["Risk"]
))

fig2.update_layout(
yaxis_title="Risk %",
xaxis_title="Patient ID",
template="plotly_dark"
)

st.plotly_chart(fig2,width="stretch")

# ------------------------------------------------
# BED UTILIZATION
# ------------------------------------------------

st.subheader("ICU Bed Utilization")

beds=list(patients.values())

fig3=go.Figure(go.Bar(
x=beds,
y=[1]*len(beds)
))

fig3.update_layout(
xaxis_title="Bed Number",
yaxis_title="Occupied",
template="plotly_dark"
)

st.plotly_chart(fig3,width="stretch")