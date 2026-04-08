import streamlit as st
import pandas as pd
from docx import Document
from datetime import datetime
from io import BytesIO
import os

# =====================================================
# CONFIG
# =====================================================
st.set_page_config(
    page_title="Sprih Internal Automations",
    page_icon="🚀",
    layout="wide",
)

PRIMARY_GREEN = "#1a3a2a"
CSV_FILE = "coach_reports.csv"

# =====================================================
# CSS
# =====================================================
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: #0b1220;
        color: white;
    }}

    section[data-testid="stSidebar"] {{
        background-color: {PRIMARY_GREEN};
    }}

    .card {{
        background-color: #111827;
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border: 1px solid #1f2937;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================================
# STORAGE HELPERS
# =====================================================
def load_reports():
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        return df.to_dict("records")
    return []


def save_report_to_csv(report):
    row = {
        "timestamp": report["timestamp"],
        "rep_name": report["header"].get("rep_name", ""),
        "company": report["header"].get("company", ""),
        "classification": report.get("classification", "Discovery"),
        "overall_score": report.get("overall_score", 0),
        "manager_notes": report.get("manager_notes", ""),
    }

    df_new = pd.DataFrame([row])

    if os.path.exists(CSV_FILE):
        df_existing = pd.read_csv(CSV_FILE)
        df_final = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_final = df_new

    df_final.to_csv(CSV_FILE, index=False)


# =====================================================
# SESSION
# =====================================================
if "coach_reports" not in st.session_state:
    st.session_state.coach_reports = load_reports()

if "latest_report" not in st.session_state:
    st.session_state.latest_report = None


# =====================================================
# HELPERS
# =====================================================
def classify_call(transcript):
    t = transcript.lower()

    if "pricing" in t:
        return "Commercial"
    elif "demo" in t:
        return "Demo"
    elif "renewal" in t:
        return "Renewal"
    elif "expand" in t:
        return "Expansion"
    else:
        return "Discovery"


def generate_report(data):
    transcript = data["transcript"].lower()

    meddic = {
        "Metrics": 8 if "cost" in transcript else 6,
        "Economic Buyer": 7,
        "Decision Criteria": 8,
        "Decision Process": 7,
        "Identify Pain": 9 if "pain" in transcript else 6,
        "Champion": 5,
    }

    overall = round(
        sum(meddic.values()) / len(meddic), 1
    )

    coaching = [
        {
            "what": "You explored buyer pain clearly.",
            "why": "This improves discovery depth.",
            "better": "Can you quantify the cost impact?"
        },
        {
            "what": "Decision authority not explored.",
            "why": "This affects deal control.",
            "better": "Who else signs off?"
        }
    ]

    actions = [
        "TODAY — send quantified follow-up",
        "THIS WEEK — map stakeholders",
        "BEFORE NEXT CALL — build ROI deck",
    ]

    return {
        "header": data,
        "classification": classify_call(
            data["transcript"]
        ),
        "meddic": meddic,
        "coaching": coaching,
        "actions": actions,
        "manager_notes": "",
        "overall_score": overall,
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        ),
    }


def create_docx(report):
    doc = Document()

    doc.add_heading("Call Coach Report", 0)

    h = report["header"]

    doc.add_paragraph(f"Rep: {h.get('rep_name', '')}")
    doc.add_paragraph(f"Company: {h.get('company', '')}")
    doc.add_paragraph(
        f"Classification: {report.get('classification', 'Discovery')}"
    )

    doc.add_heading("Framework Scores", level=1)

    for k, v in report.get("meddic", {}).items():
        doc.add_paragraph(f"{k}: {v}/10")

    doc.add_heading("Manager Notes", level=1)
    doc.add_paragraph(report.get("manager_notes", ""))

    stream = BytesIO()
    doc.save(stream)
    stream.seek(0)

    return stream


# =====================================================
# HEADER
# =====================================================
st.title("🚀 Sprih Internal Automations")
st.caption(
    "Sales Enablement + GTM Workflow Platform"
)

# =====================================================
# SIDEBAR
# =====================================================
role = st.sidebar.selectbox(
    "Role",
    ["Manager", "AE", "SDR", "GTM", "Admin"]
)

module = st.sidebar.radio(
    "Select",
    [
        "🏠 Home",
        "📞 Call Coach",
        "🎯 GTM Outreach",
        "📚 History",
        "📄 Weekly Summary",
    ]
)

# =====================================================
# HOME
# =====================================================
if module == "🏠 Home":
    st.header("🏠 Home Dashboard")

    total_calls = len(st.session_state.coach_reports)

    avg_score = (
        round(
            sum(
                float(r.get("overall_score", 0))
                for r in st.session_state.coach_reports
            ) / total_calls,
            1
        )
        if total_calls > 0
        else 0
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Calls", total_calls)
    c2.metric("Avg Score", avg_score)
    c3.metric("Pending Follow-ups", 5)

# =====================================================
# CALL COACH
# =====================================================
elif module == "📞 Call Coach":
    st.header("📞 Call Coach Workflow")

    step = st.radio(
        "Workflow Step",
        [
            "1️⃣ Context",
            "2️⃣ Scoring",
            "3️⃣ Coaching",
            "4️⃣ Actions",
            "5️⃣ Manager Notes",
            "6️⃣ Download",
        ],
        horizontal=True,
    )

    if step == "1️⃣ Context":
        rep_name = st.text_input("Sales Rep Name")
        company = st.text_input("Prospect / Company")

        transcript = st.text_area(
            "Transcript",
            height=300
        )

        if st.button("Generate Workflow Report"):
            report = generate_report({
                "rep_name": rep_name,
                "company": company,
                "transcript": transcript,
            })

            st.session_state.latest_report = report
            save_report_to_csv(report)

            # reload session from CSV
            st.session_state.coach_reports = load_reports()

            st.success("Report saved permanently")

    if st.session_state.latest_report:
        report = st.session_state.latest_report

        if step == "2️⃣ Scoring":
            st.subheader(
                f"Classification: {report['classification']}"
            )

            for k, v in report["meddic"].items():
                st.metric(k, f"{v}/10")

        elif step == "3️⃣ Coaching":
            for c in report["coaching"]:
                st.error(c["what"])
                st.info(c["why"])
                st.success(c["better"])

        elif step == "4️⃣ Actions":
            for a in report["actions"]:
                st.warning(a)

        elif step == "5️⃣ Manager Notes":
            notes = st.text_area(
                "Manager Coaching Notes",
                value=report["manager_notes"]
            )

            if st.button("Save Notes"):
                report["manager_notes"] = notes
                st.success("Saved")

        elif step == "6️⃣ Download":
            docx = create_docx(report)

            st.download_button(
                "📥 Download DOCX",
                docx,
                file_name="call_coach_report.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

# =====================================================
# GTM
# =====================================================
elif module == "🎯 GTM Outreach":
    st.header("🎯 GTM Outreach Workflow")

    step = st.radio(
        "Workflow",
        [
            "Research",
            "Persona",
            "Pain Signals",
            "Hook",
            "Email",
            "LinkedIn",
        ],
        horizontal=True,
    )

    company = st.text_input("Target Company")

    if step == "Research":
        st.text_area("Company Research")

    elif step == "Persona":
        st.text_input("Persona")

    elif step == "Pain Signals":
        st.text_area("Pain Signals")

    elif step == "Hook":
        st.text_area("Personalized Hook")

    elif step == "Email":
        st.text_area("Email Draft")

    elif step == "LinkedIn":
        st.text_area("LinkedIn Message")

# =====================================================
# HISTORY
# =====================================================
elif module == "📚 History":
    st.header("📚 History")

    reports = st.session_state.coach_reports

    if not reports:
        st.info("No saved reports yet")

    for report in reversed(reports):
        with st.expander(
            f"{report.get('rep_name', 'Unknown')} | "
            f"{report.get('timestamp', '')}"
        ):
            st.write(
                f"Score: {report.get('overall_score', 0)}"
            )
            st.write(
                f"Type: {report.get('classification', 'Discovery')}"
            )
            st.write(
                f"Company: {report.get('company', '')}"
            )

# =====================================================
# WEEKLY SUMMARY
# =====================================================
elif module == "📄 Weekly Summary":
    st.header("📄 Weekly Team Summary")

    reports = st.session_state.coach_reports

    if reports:
        avg = round(
            sum(
                float(r.get("overall_score", 0))
                for r in reports
            ) / len(reports),
            1
        )

        st.write(f"Weekly average score: {avg}")
        st.write(
            "Main coaching focus: improve deal control"
        )
