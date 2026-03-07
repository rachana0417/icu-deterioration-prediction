import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import random
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide")

# ------------------------------------------------
# AUTO REFRESH (makes charts move)
# ------------------------------------------------

st_autorefresh(interval=2000, key="ward_refresh")

# ------------------------------------------------
# HOSPITAL DASHBOARD STYLE
# ------------------------------------------------

st.markdown("""
<style>

body {
background:#050c18;
color:white;
}

.section {
font-size:22px;
font-weight:600;
margin-top:30px;
color:#7dd3fc;
}

.bed-card {
background:#0b1220;
padding:20px;
border-radius:12px;
text-align:center;
border:1px solid #1f2937;
margin-bottom:20px;
}

.alert-box {
background:#2a0f0f;
padding:15px;
border-radius:10px;
border:1px solid #7f1d1d;
}

</style>
""", unsafe_allow_html=True)

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
# GENERATE RISK DATA
# ------------------------------------------------

risk_values=[random.randint(10,90) for _ in patients]

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

# ------------------------------------------------
# ICU BED STATUS GRID
# ------------------------------------------------

st.markdown('<div class="section">ICU Bed Status</div>',unsafe_allow_html=True)

beds=st.columns(5)

for i,row in df.iterrows():

    risk=row["Risk"]

    if risk<40:
        color="🟢"
        status="Stable"
    elif risk<70:
        color="🟡"
        status="Observation"
    else:
        color="🔴"
        status="Critical"

    beds[i%5].markdown(
        f"""
        <div class="bed-card">
        <h3>Bed {row['Bed']}</h3>
        <h1>{color}</h1>
        <p>Patient ID</p>
        <b>{row['Patient']}</b>
        <p>Status: {status}</p>
        <p>Risk Score: {risk}%</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ------------------------------------------------
# MOVING PATIENT RISK DISTRIBUTION
# ------------------------------------------------

st.markdown('<div class="section">Patient Risk Distribution</div>',unsafe_allow_html=True)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["Patient"],
    y=df["Risk"],
    mode="lines+markers",
    line=dict(color="#00D4FF", width=3),
    marker=dict(size=10,color="#00D4FF")
))

fig.update_layout(
    template="plotly_dark",
    plot_bgcolor="black",
    paper_bgcolor="black",
    yaxis_title="Risk %",
    xaxis_title="Patient ID",
    height=400
)

st.plotly_chart(fig,use_container_width=True)

# ------------------------------------------------
# MOVING ICU RISK HEATMAP
# ------------------------------------------------

st.markdown('<div class="section">ICU Risk Heatmap</div>',unsafe_allow_html=True)

heat=np.random.rand(5,5)

fig_heat=go.Figure(data=go.Heatmap(
z=heat,
colorscale=[
[0,"#16a34a"],
[0.4,"#facc15"],
[0.7,"#f97316"],
[1,"#dc2626"]
]
))

fig_heat.update_layout(
template="plotly_dark",
plot_bgcolor="black",
paper_bgcolor="black",
height=350
)

st.plotly_chart(fig_heat,use_container_width=True)

# ------------------------------------------------
# CRITICAL PATIENT ALERTS
# ------------------------------------------------

st.markdown('<div class="section">Critical Patient Alerts</div>',unsafe_allow_html=True)

critical=df[df["Risk"]>70]

if len(critical)==0:

    st.success("No critical patients in ICU")

else:

    for _,row in critical.iterrows():

        st.markdown(
            f"""
            <div class="alert-box">
            🚨 Patient <b>{row['Patient']}</b> (Bed {row['Bed']})
            — Risk Level: <b>{row['Risk']}%</b>
            </div>
            """,
            unsafe_allow_html=True
        )