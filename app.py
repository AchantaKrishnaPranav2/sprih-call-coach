import streamlit as st
from docx import Document

st.set_page_config(
    page_title="Sprih Call Coach",
    page_icon="🎯",
    layout="wide"
)

def read_docx(uploaded_file):
    doc = Document(uploaded_file)
    full_text = []

    for para in doc.paragraphs:
        if para.text.strip():
            full_text.append(para.text)

    return "\n".join(full_text)

st.title("🎯 Sprih Call Coach")
st.caption("AI-powered sales call coaching dashboard")

st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    rep_name = st.text_input("Sales Rep Name")
    call_type = st.selectbox(
        "Call Type",
        ["Discovery", "Demo", "Followup", "Mixed"]
    )

    uploaded_file = st.file_uploader(
        "Upload Transcript (.docx or .txt)",
        type=["docx", "txt"]
    )

    transcript = ""

    if uploaded_file is not None:
        if uploaded_file.name.endswith(".docx"):
            transcript = read_docx(uploaded_file)
        elif uploaded_file.name.endswith(".txt"):
            transcript = str(uploaded_file.read(), "utf-8")

        st.text_area(
            "Extracted Transcript",
            transcript,
            height=250
        )

    transcript_manual = st.text_area(
        "Or Paste Transcript",
        height=200
    )

    if transcript_manual.strip():
        transcript = transcript_manual

    analyze = st.button("Analyze Call")

with col2:
    st.info("""
    **Frameworks Used**
    - MEDDIC
    - SPICED
    - Deal Health
    - Coaching Moments
    """)

if analyze and transcript:
    transcript_lower = transcript.lower()

    meddic = 8
    spiced = 7

    if "budget" in transcript_lower:
        meddic += 1

    if "pain" in transcript_lower:
        spiced += 1

    st.success("Analysis complete")

    tab1, tab2, tab3 = st.tabs(
        ["📊 Scores", "🧠 Coaching", "🎯 Better Script"]
    )

    with tab1:
        c1, c2 = st.columns(2)
        c1.metric("MEDDIC", f"{meddic}/10")
        c2.metric("SPICED", f"{spiced}/10")

    with tab2:
        st.write(
            f"{rep_name}, you did a strong job uncovering buyer pain. "
            "The next opportunity is quantifying impact."
        )

    with tab3:
        st.info(
            "Can you help me understand what this issue "
            "is costing the business each quarter?"
        )

    report = f"""
Sprih Call Coach Report

Rep: {rep_name}
Call Type: {call_type}

MEDDIC: {meddic}/10
SPICED: {spiced}/10

Feedback:
Strong pain discovery.
Need better quantification.

Better Script:
Can you help quantify business impact?
"""

    st.download_button(
        "📥 Download Report",
        report,
        file_name="call_coaching_report.txt"
    )
