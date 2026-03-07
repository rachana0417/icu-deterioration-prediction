import streamlit as st
import numpy as np
from datetime import datetime
import random
from fpdf import FPDF
import matplotlib.pyplot as plt
import tempfile

st.set_page_config(layout="wide")

# ----------------------------------------------------
# PROFESSIONAL STYLE
# ----------------------------------------------------

st.markdown("""
<style>

body{
background-color:#050c18;
}

.metric{
font-size:32px;
font-weight:600;
}

button[kind="secondary"]{
background-color:#1f2937;
border-radius:8px;
}

</style>
""",unsafe_allow_html=True)

st.title("📄 ICU Patient Report Generator")

# ----------------------------------------------------
# PATIENT DATABASE
# ----------------------------------------------------

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

selected_patient=st.selectbox(
"Select Patient",
list(patients.keys())
)

st.write("Patient ID:",selected_patient)
st.write("ICU Bed:",patients[selected_patient])

# ----------------------------------------------------
# GENERATE SAMPLE VITALS
# ----------------------------------------------------

heart_rate=random.randint(70,95)
spo2=random.randint(94,100)
rr=random.randint(12,20)
risk=random.uniform(20,80)

st.subheader("Patient Vital Summary")

c1,c2,c3=st.columns(3)

c1.metric("🟢 Heart Rate",f"{heart_rate} bpm")
c2.metric("🟡 SpO₂",f"{spo2} %")
c3.metric("🔵 Resp Rate",f"{rr} /min")

st.metric("🔴 AI Risk Score",f"{round(risk,1)} %")

# ----------------------------------------------------
# PDF REPORT CLASS
# ----------------------------------------------------

class ICUReport(FPDF):

    def header(self):

        self.set_font("Arial","B",22)
        self.cell(0,12,"AI ICU GUARDIAN REPORT",0,1,"C")

        self.set_font("Arial","I",10)
        self.cell(0,6,"AI Powered ICU Monitoring System",0,1,"C")

        self.ln(5)

    def footer(self):

        self.set_y(-15)

        self.set_font("Arial","I",8)

        self.cell(
            0,
            10,
            "Automatically generated clinical report",
            0,
            0,
            "C"
        )

# ----------------------------------------------------
# GENERATE PDF
# ----------------------------------------------------

def generate_pdf():

    pdf=ICUReport()

    pdf.add_page()

    pdf.set_font("Arial","",12)

    pdf.cell(40,10,"Patient ID",1)
    pdf.cell(0,10,selected_patient,1,1)

    pdf.cell(40,10,"Generated",1)
    pdf.cell(0,10,str(datetime.now()),1,1)

    pdf.ln(10)

    pdf.set_font("Arial","B",12)

    pdf.cell(60,10,"Parameter",1)
    pdf.cell(40,10,"Value",1)
    pdf.cell(0,10,"Normal Range",1,1)

    pdf.set_font("Arial","",12)

    pdf.cell(60,10,"Heart Rate",1)
    pdf.cell(40,10,f"{heart_rate} bpm",1)
    pdf.cell(0,10,"60-100 bpm",1,1)

    pdf.cell(60,10,"SpO2",1)
    pdf.cell(40,10,f"{spo2} %",1)
    pdf.cell(0,10,">95 %",1,1)

    pdf.cell(60,10,"Resp Rate",1)
    pdf.cell(40,10,f"{rr} /min",1)
    pdf.cell(0,10,"12-20 /min",1,1)

    pdf.ln(10)

    pdf.cell(60,10,"AI Risk Score",1)
    pdf.cell(0,10,f"{round(risk,1)} %",1,1)

    pdf.ln(10)

    # GRAPH

    hr=np.random.normal(heart_rate,2,40)
    spo=np.random.normal(spo2,0.2,40)

    fig,ax=plt.subplots()

    ax.plot(hr,label="Heart Rate")
    ax.plot(spo,label="SpO2")

    ax.legend()

    temp=tempfile.NamedTemporaryFile(delete=False,suffix=".png")

    fig.savefig(temp.name)

    pdf.image(temp.name,x=20,w=170)

    return pdf.output(dest="S").encode("latin-1")

# ----------------------------------------------------
# DOWNLOAD BUTTON
# ----------------------------------------------------

if st.button("Generate Patient Report"):

    pdf_bytes=generate_pdf()

    st.download_button(
        label="Download ICU Report",
        data=pdf_bytes,
        file_name=f"ICU_Report_{selected_patient}.pdf",
        mime="application/pdf"
    )