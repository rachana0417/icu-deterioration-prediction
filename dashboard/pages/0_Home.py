import streamlit as st
import time

st.set_page_config(page_title="AI ICU Guardian", layout="wide")

# -----------------------------
# ANIMATED HERO SECTION
# -----------------------------

st.markdown("""
<style>

.hero{
background:linear-gradient(90deg,#0f2027,#203a43,#2c5364);
padding:60px;
border-radius:15px;
text-align:center;
color:white;
animation: fadein 2s;
}

@keyframes fadein{
0%{opacity:0; transform:translateY(-30px);}
100%{opacity:1; transform:translateY(0);}
}

.feature-card{
background:#111827;
padding:25px;
border-radius:12px;
transition: transform 0.3s;
}

.feature-card:hover{
transform:scale(1.05);
}

.big-title{
font-size:48px;
font-weight:700;
}

.subtitle{
font-size:22px;
opacity:0.9;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">

<div class="big-title">🏥 AI ICU Guardian</div>

<div class="subtitle">
AI Powered ICU Monitoring & Patient Risk Prediction
</div>

<br>

Real-time vital monitoring • AI early warning detection • automated clinical reports

</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# -----------------------------
# LIVE SYSTEM STATUS
# -----------------------------

st.subheader("System Status")

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.metric("AI Monitoring", "ACTIVE")

with c2:
    st.metric("ICU Beds", "20")

with c3:
    st.metric("Patients Monitored", "10")

with c4:
    st.metric("System Mode", "Realtime")

st.write("")
st.write("")

# -----------------------------
# FEATURES SECTION
# -----------------------------

st.subheader("Platform Capabilities")

col1,col2,col3 = st.columns(3)

with col1:

    st.markdown("""
    <div class="feature-card">

    <h3>📊 Live ICU Monitoring</h3>

    Continuous monitoring of vital signs including
    heart rate, oxygen saturation, and respiratory rate.

    Real-time graphs simulate ICU bedside monitors.

    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div class="feature-card">

    <h3>🤖 AI Risk Prediction</h3>

    Machine learning models analyze patient
    vital trends to predict early clinical deterioration.

    Helps doctors intervene before critical events.

    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown("""
    <div class="feature-card">

    <h3>📄 Automated ICU Reports</h3>

    Generate professional clinical reports
    summarizing patient vitals, AI risk score
    and recommendations.

    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# -----------------------------
# INTERACTIVE SECTION
# -----------------------------

st.subheader("Explore the System")

col1,col2 = st.columns(2)

with col1:

    if st.button("Open ICU Monitoring Dashboard"):

        st.success("Navigate to 'ICU Dashboard' from sidebar")

with col2:

    if st.button("Generate Patient Report"):

        st.success("Open 'Patient Report' page from sidebar")

st.write("")
st.write("")

# -----------------------------
# ANIMATED FOOTER
# -----------------------------

st.markdown("""
<center>

AI ICU Guardian • Intelligent Healthcare Monitoring System

</center>
""", unsafe_allow_html=True)