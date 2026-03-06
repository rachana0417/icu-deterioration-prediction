import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(layout="wide")

st.title("🚨 ICU Alert Center")

# ------------------------------------------------
# PATIENT DATABASE
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

alert_list=[]

for pid,bed in patients.items():

    risk=random.randint(10,95)

    if risk < 40:
        status="Stable"
        icon="🟢"

    elif risk < 70:
        status="Warning"
        icon="🟡"

    else:
        status="Critical"
        icon="🔴"

    alert_list.append({
        "Patient ID":pid,
        "Bed":bed,
        "Risk %":risk,
        "Status":status,
        "Indicator":icon,
        "Time":datetime.now().strftime("%H:%M:%S")
    })

df=pd.DataFrame(alert_list)

# ------------------------------------------------
# ALERT SUMMARY
# ------------------------------------------------

st.subheader("ICU Alert Summary")

c1,c2,c3=st.columns(3)

c1.metric("Critical Patients",(df["Status"]=="Critical").sum())
c2.metric("Warning Patients",(df["Status"]=="Warning").sum())
c3.metric("Stable Patients",(df["Status"]=="Stable").sum())

# ------------------------------------------------
# CRITICAL ALERTS
# ------------------------------------------------

st.subheader("Critical Alerts")

critical=df[df["Status"]=="Critical"]

if len(critical)==0:

    st.success("No critical alerts")

else:

    for _,row in critical.iterrows():

        st.error(
            f"🚨 Patient {row['Patient ID']} | Bed {row['Bed']} | Risk {row['Risk %']}%"
        )

# ------------------------------------------------
# WARNING ALERTS
# ------------------------------------------------

st.subheader("Warning Alerts")

warning=df[df["Status"]=="Warning"]

for _,row in warning.iterrows():

    st.warning(
        f"⚠ Patient {row['Patient ID']} | Bed {row['Bed']} | Risk {row['Risk %']}%"
    )

# ------------------------------------------------
# ALERT TABLE
# ------------------------------------------------

st.subheader("Alert Log")

st.dataframe(df)