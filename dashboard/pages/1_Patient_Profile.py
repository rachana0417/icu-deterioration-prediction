import streamlit as st
import random
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

st.title("🧑‍⚕️ Patient Clinical Profile")

# ------------------------------------------------
# SAMPLE PATIENT DATABASE
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
# SIDEBAR PATIENT SELECTION
# ------------------------------------------------

selected_patient = st.sidebar.selectbox(
"Select Patient",
list(patients.keys())
)

name = patients[selected_patient]

# ------------------------------------------------
# GENERATE SAMPLE CLINICAL DATA
# ------------------------------------------------

age = random.randint(25,80)
gender = random.choice(["Male","Female"])
blood = random.choice(["A+","B+","O+","AB+","A-","B-"])
doctor = random.choice(["Dr. Sharma","Dr. Patel","Dr. Iyer","Dr. Khan"])
diagnosis = random.choice([
"Pneumonia",
"Respiratory Failure",
"Sepsis",
"Post Surgery Monitoring",
"Cardiac Observation"
])

admission = datetime.now() - timedelta(hours=random.randint(2,48))

# ------------------------------------------------
# PROFILE CARD
# ------------------------------------------------

col1,col2 = st.columns([1,2])

with col1:

    st.subheader("Patient Details")

    st.metric("Patient ID",selected_patient)
    st.metric("Name",name)
    st.metric("Age",age)
    st.metric("Gender",gender)
    st.metric("Blood Group",blood)

with col2:

    st.subheader("Clinical Information")

    st.write(f"**Diagnosis:** {diagnosis}")
    st.write(f"**Assigned Doctor:** {doctor}")
    st.write(f"**Admission Time:** {admission.strftime('%d %b %Y  %H:%M')}")

    st.write("**Allergies:** None reported")

    st.write("**Clinical Notes:**")
    st.info(
        "Patient currently under continuous ICU monitoring. "
        "AI system is tracking vital signs and predicting deterioration risk."
    )

# ------------------------------------------------
# MEDICAL TIMELINE
# ------------------------------------------------

st.subheader("Recent Clinical Events")

events = [
"Patient admitted to ICU",
"Oxygen therapy started",
"Vitals stabilized",
"AI monitoring activated",
"Nurse observation recorded"
]

for e in events:
    st.write(f"• {e}")