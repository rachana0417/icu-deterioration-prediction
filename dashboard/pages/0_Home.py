import streamlit as st
import time

st.set_page_config(page_title="AI ICU Guardian", layout="wide")

# -------------------------------------------------------
# ADVANCED UI STYLE
# -------------------------------------------------------

st.markdown("""
<style>

/* BACKGROUND */

body{
background: radial-gradient(circle at top,#0f172a,#020617);
color:white;
}

/* HERO SECTION */

.hero{
background: linear-gradient(120deg,#0f172a,#1e3a8a,#0891b2);
padding:70px;
border-radius:18px;
text-align:center;
color:white;
box-shadow:0 20px 60px rgba(0,0,0,0.5);
animation: floatHero 6s ease-in-out infinite;
}

@keyframes floatHero{
0%{transform:translateY(0px)}
50%{transform:translateY(-6px)}
100%{transform:translateY(0px)}
}

.big-title{
font-size:52px;
font-weight:800;
letter-spacing:1px;
}

.subtitle{
font-size:22px;
opacity:0.9;
}

/* AI STATUS PULSE */

.ai-status{
color:#22c55e;
font-weight:600;
}

.pulse{
display:inline-block;
width:10px;
height:10px;
background:#22c55e;
border-radius:50%;
margin-right:8px;
animation:pulse 1.5s infinite;
}

@keyframes pulse{
0%{box-shadow:0 0 0 0 rgba(34,197,94,0.6)}
70%{box-shadow:0 0 0 10px rgba(34,197,94,0)}
100%{box-shadow:0 0 0 0 rgba(34,197,94,0)}
}

/* FEATURE CARDS */

.feature-card{
background: rgba(17,24,39,0.6);
padding:30px;
border-radius:16px;
border:1px solid rgba(255,255,255,0.05);
transition:all 0.4s ease;
backdrop-filter: blur(10px);
}

.feature-card:hover{
transform:translateY(-10px) scale(1.02);
box-shadow:0 20px 50px rgba(0,255,255,0.15);
border:1px solid rgba(0,255,255,0.2);
}

/* BUTTON STYLE */

button[kind="primary"]{
background: linear-gradient(90deg,#06b6d4,#3b82f6);
border:none;
padding:10px 20px;
border-radius:10px;
font-weight:600;
}

button[kind="primary"]:hover{
box-shadow:0 0 20px rgba(0,200,255,0.6);
}

/* FOOTER */

.footer{
text-align:center;
padding:30px;
opacity:0.6;
font-size:14px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# HERO SECTION
# -------------------------------------------------------

st.markdown("""
<div class="hero">

<div class="big-title">🏥 AI ICU Guardian</div>

<div class="subtitle">
AI Powered ICU Monitoring & Patient Risk Prediction
</div>

<br>

<span class="pulse"></span>
<span class="ai-status">AI Monitoring System Active</span>

<br><br>

Real-time vital monitoring • Early warning detection • automated clinical reports

</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# -------------------------------------------------------
# SYSTEM STATUS
# -------------------------------------------------------

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

# -------------------------------------------------------
# FEATURES SECTION
# -------------------------------------------------------

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

# -------------------------------------------------------
# INTERACTIVE SECTION
# -------------------------------------------------------

st.subheader("Explore the System")

col1,col2 = st.columns(2)

with col1:

    if st.button("Open ICU Monitoring Dashboard", type="primary"):
        st.success("Navigate to 'ICU Dashboard' from sidebar")

with col2:

    if st.button("Generate Patient Report", type="primary"):
        st.success("Open 'Patient Report' page from sidebar")

st.write("")
st.write("")

# -------------------------------------------------------
# FOOTER
# -------------------------------------------------------

st.markdown("""
<div class="footer">

AI ICU Guardian • Intelligent Healthcare Monitoring Platform

</div>
""", unsafe_allow_html=True)