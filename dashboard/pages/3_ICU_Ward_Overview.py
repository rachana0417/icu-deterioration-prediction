import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random

st.set_page_config(layout="wide")

st.title("🏥 ICU Ward Overview")

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
# GENERATE PATIENT RISK
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
# TOP METRICS
# ------------------------------------------------

c1,c2,c3=st.columns(3)

c1.metric("Total ICU Patients",len(df))
c2.metric("Critical Patients",(df["Risk"]>70).sum())
c3.metric("Stable Patients",(df["Risk"]<40).sum())

st.write("")
st.write("")

# ------------------------------------------------
# ICU BED STATUS GRID
# ------------------------------------------------

st.subheader("ICU Bed Status")

cols=st.columns(5)

for i,row in df.iterrows():

    r=row["Risk"]

    if r<40:
        light="🟢"
    elif r<70:
        light="🟡"
    else:
        light="🔴"

    cols[i%5].markdown(f"### Bed {row['Bed']}")
    cols[i%5].markdown(f"# {light}")
    cols[i%5].write(f"Patient {row['Patient']}")

# ------------------------------------------------
# PATIENT RISK BAR CHART
# ------------------------------------------------

st.subheader("Patient Risk Distribution")

fig=go.Figure(go.Bar(
x=df["Patient"],
y=df["Risk"]
))

fig.update_layout(
yaxis_title="Risk %",
xaxis_title="Patient ID",
template="plotly_dark"
)

st.plotly_chart(fig,width="stretch")

# ------------------------------------------------
# ICU RISK HEATMAP
# ------------------------------------------------

st.subheader("ICU Risk Heatmap")

heat=np.random.rand(5,5)

fig_heat=go.Figure(data=go.Heatmap(
z=heat,
colorscale="RdYlGn_r"
))

fig_heat.update_layout(template="plotly_dark")

st.plotly_chart(fig_heat,width="stretch")

# ------------------------------------------------
# CRITICAL PATIENT ALERTS
# ------------------------------------------------

st.subheader("Critical Patient Alerts")

critical=df[df["Risk"]>70]

if len(critical)==0:

    st.success("No critical patients in ICU")

else:

    for _,row in critical.iterrows():

        st.error(
            f"🚨 Patient {row['Patient']} (Bed {row['Bed']}) "
            f"Risk Level: {row['Risk']}%"
        )