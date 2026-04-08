import streamlit as st
from docx import Document
import google.generativeai as genai

st.set_page_config(
    page_title="Sprih Call Coach",
    page_icon="🎯",
    layout="wide"
)
genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

model = genai.GenerativeModel("gemini-1.5-flash-latest")

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
    prompt = f"""
You are a supportive senior sales coach and deal strategist.

Analyze the transcript using:
- MEDDIC
- SPICED
- Deal Health
- Coaching Moments

Be constructive.
Address the rep directly as "you".

Output format:

## Scores
MEDDIC: X/10
SPICED: X/10

## Deal Health
...

## Coaching Feedback
...

## Better Script
...

Transcript:
{transcript}
"""

    response = model.generate_content(prompt)

    result = response.text

    st.success("Analysis complete")

    st.write("## AI Coaching Report")
    st.write(result)

    st.download_button(
        "📥 Download Report",
        result,
        file_name="call_coaching_report.txt"
    )
