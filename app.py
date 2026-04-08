import streamlit as st
from docx import Document
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Sprih Call Coach",
    page_icon="🎯",
    layout="wide"
)

# ---------------- HELPERS ----------------
def read_docx(uploaded_file):
    doc = Document(uploaded_file)
    text = []

    for para in doc.paragraphs:
        if para.text.strip():
            text.append(para.text)

    return "\n".join(text)


def generate_mock_report(rep_name, call_type, transcript):
    transcript_lower = transcript.lower()

    meddic = 8
    spiced = 7

    if "budget" in transcript_lower:
        meddic += 1

    if "pain" in transcript_lower:
        spiced += 1

    feedback = (
        "You did a strong job uncovering buyer pain. "
        "The next opportunity is to quantify business impact."
    )

    better_script = (
        "Can you help me understand what this issue "
        "is costing the business each quarter?"
    )

    return {
        "rep": rep_name,
        "call_type": call_type,
        "meddic": meddic,
        "spiced": spiced,
        "feedback": feedback,
        "better_script": better_script,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


# ---------------- SESSION STATE ----------------
if "reports" not in st.session_state:
    st.session_state.reports = []

# ---------------- TITLE ----------------
st.title("🎯 Sprih Call Coach")
st.caption("AI-ready sales coaching workflow platform")

# ---------------- SIDEBAR ----------------
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "New Analysis", "History"]
)

# =========================================================
# DASHBOARD
# =========================================================
if page == "Dashboard":
    st.header("📊 Dashboard")

    total_calls = len(st.session_state.reports)

    avg_meddic = (
        round(
            sum(r["meddic"] for r in st.session_state.reports) / total_calls,
            1
        )
        if total_calls > 0
        else 0
    )

    avg_spiced = (
        round(
            sum(r["spiced"] for r in st.session_state.reports) / total_calls,
            1
        )
        if total_calls > 0
        else 0
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Calls", total_calls)
    col2.metric("Avg MEDDIC", avg_meddic)
    col3.metric("Avg SPICED", avg_spiced)

    st.markdown("---")

    st.subheader("Recent Reports")

    if total_calls == 0:
        st.info("No reports generated yet.")
    else:
        for report in reversed(st.session_state.reports[-3:]):
            with st.expander(
                f"{report['rep']} | {report['call_type']} | {report['timestamp']}"
            ):
                st.write(f"MEDDIC: {report['meddic']}/10")
                st.write(f"SPICED: {report['spiced']}/10")
                st.write(report["feedback"])

# =========================================================
# NEW ANALYSIS
# =========================================================
elif page == "New Analysis":
    st.header("📝 New Call Analysis")

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

        manual_input = st.text_area(
            "Or Paste Transcript",
            height=200
        )

        if manual_input.strip():
            transcript = manual_input

        generate = st.button("🎯 Generate Report")

    with col2:
        st.info("""
        **Frameworks Used**
        - MEDDIC
        - SPICED
        - Deal Health
        - Coaching Moments
        """)

    if generate:
        if not rep_name:
            st.error("Please enter Sales Rep Name")
        elif not transcript:
            st.error("Please upload or paste transcript")
        else:
            report = generate_mock_report(
                rep_name,
                call_type,
                transcript
            )

            st.session_state.reports.append(report)

            st.success("Report generated successfully")

            tab1, tab2, tab3 = st.tabs(
                ["📊 Scores", "🧠 Coaching", "🎯 Better Script"]
            )

            with tab1:
                c1, c2 = st.columns(2)
                c1.metric("MEDDIC", f"{report['meddic']}/10")
                c2.metric("SPICED", f"{report['spiced']}/10")

            with tab2:
                st.write(report["feedback"])

            with tab3:
                st.info(report["better_script"])

            download_text = f"""
Sprih Call Coach Report
========================

Rep: {report['rep']}
Call Type: {report['call_type']}
Date: {report['timestamp']}

MEDDIC: {report['meddic']}/10
SPICED: {report['spiced']}/10

Feedback:
{report['feedback']}

Better Script:
{report['better_script']}
"""

            st.download_button(
                "📥 Download Report",
                download_text,
                file_name=f"{rep_name}_report.txt"
            )

# =========================================================
# HISTORY
# =========================================================
elif page == "History":
    st.header("📚 Past Reports")

    if not st.session_state.reports:
        st.warning("No reports available yet.")
    else:
        for i, report in enumerate(reversed(st.session_state.reports)):
            with st.expander(
                f"{i+1}. {report['rep']} | {report['timestamp']}"
            ):
                st.write(f"Call Type: {report['call_type']}")
                st.write(f"MEDDIC: {report['meddic']}/10")
                st.write(f"SPICED: {report['spiced']}/10")
                st.write(report["feedback"])
                st.info(report["better_script"])
