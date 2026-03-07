import streamlit as st
import random
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

# ------------------------------------------------
# PROFESSIONAL MEDICAL UI STYLE
# ------------------------------------------------

st.markdown("""
<style>

body{
background:#0a1120;
color:white;
}

/* PAGE TITLE */

.title{
font-size:34px;
font-weight:700;
margin-bottom:20px;
}

/* CARDS */

.card{
background:#121a2b;
padding:25px;
border-radius:12px;
border:1px solid #1f2a44;
box-shadow:0 4px 20px rgba(0,0,0,0.4);
margin-bottom:20px;
}

/* SECTION HEADERS */

.section{
font-size:20px;
font-weight:600;
margin-bottom:15px;
color:#9ecbff;
}

/* STATUS */

.status{
color:#22c55e;
font-weight:600;
}

/* TIMELINE */

.timeline{
background:#121a2b;
padding:20px;
border-radius:10px;
border:1px solid #1f2a44;
}

/* INFO PANEL */

.info-panel{
background:#1b3a5c;
padding:15px;
border-radius:8px;
color:#dbeafe;
}

/* SIDEBAR */

.css-1d391kg{
background:#0f172a;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# TITLE
# ------------------------------------------------

st.markdown('<div class="title">🧑‍⚕️ Patient Clinical Profile</div>', unsafe_allow_html=True)

# ------------------------------------------------
# PATIENT DATABASE
# ------------------------------------------------

patients = {
"39711498": "John Carter",
"32145159": "Emma Watson",
"34629895": "David Miller",
"32604416": "Sophia Brown",
"36084844": "James Wilson",
"32506122": "Olivia Taylor",
"39804682": "Daniel Anderson",
"37057036": "Charlotte Moore",
"35258379": "Benjamin Thomas",
"34617352": "Amelia Martin"
}

# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------

selected_patient = st.sidebar.selectbox(
"Select Patient",
list(patients.keys())
)

name = patients[selected_patient]

# ------------------------------------------------
# SAMPLE DATA
# ------------------------------------------------

age = random.randint(25,80)
gender = random.choice(["Male","Female"])
blood = random.choice(["A+","B+","O+","AB+","A-","B-"])

doctor = random.choice([
"Dr. Sharma","Dr. Patel","Dr. Iyer","Dr. Khan"
])

diagnosis = random.choice([
"Pneumonia",
"Respiratory Failure",
"Sepsis",
"Post Surgery Monitoring",
"Cardiac Observation"
])

admission = datetime.now() - timedelta(hours=random.randint(2,48))

# ------------------------------------------------
# MAIN LAYOUT
# ------------------------------------------------

col1,col2 = st.columns([1,2])

# ------------------------------------------------
# PATIENT DETAILS CARD
# ------------------------------------------------

with col1:

    st.markdown('<div class="card">',unsafe_allow_html=True)

    st.markdown('<div class="section">Patient Details</div>',unsafe_allow_html=True)

    st.write("**Patient ID**")
    st.write(selected_patient)

    st.write("**Name**")
    st.write(name)

    st.write("**Age**")
    st.write(age)

    st.write("**Gender**")
    st.write(gender)

    st.write("**Blood Group**")
    st.write(blood)

    st.markdown('</div>',unsafe_allow_html=True)

# ------------------------------------------------
# CLINICAL INFORMATION
# ------------------------------------------------

with col2:

    st.markdown('<div class="card">',unsafe_allow_html=True)

    st.markdown('<div class="section">Clinical Information</div>',unsafe_allow_html=True)

    st.write(f"**Diagnosis:** {diagnosis}")
    st.write(f"**Assigned Doctor:** {doctor}")
    st.write(f"**Admission Time:** {admission.strftime('%d %b %Y  %H:%M')}")

    st.write("**Allergies:** None reported")

    st.write("**Monitoring Status:**")

    st.markdown(
        '<span class="status">● ICU AI Monitoring Active</span>',
        unsafe_allow_html=True
    )

    st.write("")

    st.markdown(
        '<div class="info-panel">Patient currently under continuous ICU monitoring. AI system is tracking vital signs and predicting deterioration risk.</div>',
        unsafe_allow_html=True
    )

    st.markdown('</div>',unsafe_allow_html=True)

# ------------------------------------------------
# TIMELINE
# ------------------------------------------------

st.markdown('<div class="section">Recent Clinical Events</div>', unsafe_allow_html=True)

events = [
"Patient admitted to ICU",
"Oxygen therapy started",
"Vitals stabilized",
"AI monitoring activated",
"Nurse observation recorded"
]

st.markdown('<div class="timeline">',unsafe_allow_html=True)

for e in events:
    st.write(f"• {e}")

st.markdown('</div>',unsafe_allow_html=True)