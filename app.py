import streamlit as st
import pandas as pd
from docx import Document
from datetime import datetime
from io import BytesIO

# =====================================================
# CONFIG
# =====================================================
st.set_page_config(
    page_title="Sprih Internal Automations",
    page_icon="🚀",
    layout="wide",
)

PRIMARY_GREEN = "#1a3a2a"

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
# SESSION
# =====================================================
if "coach_reports" not in st.session_state:
    st.session_state.coach_reports = []

if "gtm_reports" not in st.session_state:
    st.session_state.gtm_reports = []

if "latest_report" not in st.session_state:
    st.session_state.latest_report = None

# =====================================================
# HELPERS
# =====================================================
def classify_call(transcript):
    t = transcript.lower()

    if "pricing" in t or "commercial" in t:
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

    doc.add_paragraph(f"Rep: {h['rep_name']}")
    doc.add_paragraph(f"Company: {h['company']}")
    doc.add_paragraph(
        f"Classification: {report['classification']}"
    )

    doc.add_heading("Framework Scores", level=1)

    for k, v in report["meddic"].items():
        doc.add_paragraph(f"{k}: {v}/10")

    doc.add_heading("Manager Notes", level=1)
    doc.add_paragraph(report["manager_notes"])

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
        "📊 Dashboard",
        "🏆 Leaderboard",
        "📚 History",
        "📄 Weekly Summary",
    ]
)

# =====================================================
# HOME
# =====================================================
if module == "🏠 Home":
    st.header("🏠 Home Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Today's Calls",
        len(st.session_state.coach_reports)
    )

    avg_score = (
        round(
            sum(
                r["overall_score"]
                for r in st.session_state.coach_reports
            )
            / len(st.session_state.coach_reports),
            1
        )
        if st.session_state.coach_reports
        else 0
    )

    c2.metric("Avg Score", avg_score)

    c3.metric(
        "GTM Runs",
        len(st.session_state.gtm_reports)
    )

    c4.metric("Pending Follow-ups", 5)

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
            st.session_state.coach_reports.append(
                report
            )

            st.success("Step complete")

    if st.session_state.latest_report:
        report = st.session_state.latest_report

        if step == "2️⃣ Scoring":
            st.subheader(
                f"Classification: {report['classification']}"
            )

            for k, v in report["meddic"].items():
                st.metric(k, f"{v}/10")

            trend_df = pd.DataFrame({
                "Score": [
                    6.5,
                    7.0,
                    7.4,
                    report["overall_score"]
                ]
            })

            st.line_chart(trend_df)

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
# DASHBOARD
# =====================================================
elif module == "📊 Dashboard":
    st.header("📊 Team Dashboard")

    if st.session_state.coach_reports:
        df = pd.DataFrame([
            {
                "Rep": r["header"]["rep_name"],
                "Score": r["overall_score"]
            }
            for r in st.session_state.coach_reports
        ])

        st.bar_chart(df.set_index("Rep"))

# =====================================================
# LEADERBOARD
# =====================================================
elif module == "🏆 Leaderboard":
    st.header("🏆 Rep Leaderboard")

    if st.session_state.coach_reports:
        df = pd.DataFrame([
            {
                "Rep": r["header"]["rep_name"],
                "Avg Score": r["overall_score"]
            }
            for r in st.session_state.coach_reports
        ])

        df = df.sort_values(
            "Avg Score",
            ascending=False
        )

        st.dataframe(df)

# =====================================================
# HISTORY
# =====================================================
elif module == "📚 History":
    st.header("📚 History")

    for report in reversed(
        st.session_state.coach_reports
    ):
        with st.expander(
            f"{report['header']['rep_name']} | "
            f"{report['timestamp']}"
        ):
            st.write(
                f"Score: {report['overall_score']}"
            )
            st.write(
                f"Type: {report['classification']}"
            )

# =====================================================
# WEEKLY SUMMARY
# =====================================================
elif module == "📄 Weekly Summary":
    st.header("📄 Weekly Team Summary")

    if st.session_state.coach_reports:
        avg = round(
            sum(
                r["overall_score"]
                for r in st.session_state.coach_reports
            )
            / len(st.session_state.coach_reports),
            1
        )

        st.write(
            f"Weekly average score: {avg}"
        )

        st.write(
            "Main coaching focus: improve deal control"
        )
