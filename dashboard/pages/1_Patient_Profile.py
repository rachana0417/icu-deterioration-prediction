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
# ADD NEW PATIENT (NEW FEATURE)
# ------------------------------------------------

st.sidebar.markdown("### ➕ Register New Patient")

with st.sidebar.form("add_patient"):

    new_id = st.text_input("Patient ID")
    new_name = st.text_input("Patient Name")

    add_patient = st.form_submit_button("Add Patient")

    if add_patient:

        if new_id and new_name:
            patients[new_id] = new_name
            st.sidebar.success("Patient added successfully")
        else:
            st.sidebar.error("Enter both Patient ID and Name")

# ------------------------------------------------
# SIDEBAR PATIENT SELECT
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

# ------------------------------------------------
# MANUAL VITAL ENTRY (NEW FEATURE)
# ------------------------------------------------

st.markdown('<div class="section">Enter Patient Vitals</div>', unsafe_allow_html=True)

with st.form("vitals_form"):

    colA,colB,colC = st.columns(3)

    with colA:
        heart_rate = st.number_input("Heart Rate (bpm)",40,200)

    with colB:
        spo2 = st.number_input("SpO2 (%)",70,100)

    with colC:
        temperature = st.number_input("Temperature (°C)",30.0,42.0)

    blood_pressure = st.number_input("Blood Pressure (mmHg)",50,200)

    submit_vitals = st.form_submit_button("Submit Vitals")

    if submit_vitals:

        st.success("Vitals submitted to ICU AI monitoring system")

        st.write("### Current Recorded Vitals")

        st.write("Heart Rate:",heart_rate,"bpm")
        st.write("SpO2:",spo2,"%")
        st.write("Temperature:",temperature,"°C")
        st.write("Blood Pressure:",blood_pressure,"mmHg")

        # ------------------------------------------------
# UPLOAD PATIENT REPORT
# ------------------------------------------------

import pandas as pd

st.markdown('<div class="section">Upload Patient Medical Report</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload patient report (CSV)",
    type=["csv"]
)

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    st.write("### Report Data")
    st.dataframe(data)