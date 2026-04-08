import streamlit as st
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
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
CARD_BG = "#111827"
ACCENT = "#10b981"

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
        background-color: {CARD_BG};
        padding: 1rem;
        border-radius: 14px;
        border: 1px solid #1f2937;
        margin-bottom: 1rem;
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

# =====================================================
# HELPERS
# =====================================================
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

    coaching = [
        {
            "what": "You explored pain well.",
            "why": "This improves discovery depth.",
            "better": "Can you quantify the cost impact?"
        },
        {
            "what": "Decision authority not explored.",
            "why": "This affects deal control.",
            "better": "Who else signs off internally?"
        }
    ]

    actions = [
        "TODAY — send quantified follow-up",
        "THIS WEEK — map stakeholders",
        "BEFORE NEXT CALL — prepare ROI narrative",
    ]

    return {
        "header": data,
        "meddic": meddic,
        "coaching": coaching,
        "actions": actions,
        "overall_score": round(
            sum(meddic.values()) / len(meddic), 1
        ),
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
    doc.add_paragraph(f"Type: {h['call_type']}")

    doc.add_heading("Framework Scores", level=1)

    for k, v in report["meddic"].items():
        doc.add_paragraph(f"{k}: {v}/10")

    doc.add_heading("Coaching Moments", level=1)

    for c in report["coaching"]:
        doc.add_paragraph(f"What: {c['what']}")
        doc.add_paragraph(f"Why: {c['why']}")
        doc.add_paragraph(f"Better: {c['better']}")

    doc.add_heading("Actions", level=1)

    for a in report["actions"]:
        doc.add_paragraph(a)

    stream = BytesIO()
    doc.save(stream)
    stream.seek(0)

    return stream


# =====================================================
# HEADER
# =====================================================
st.title("🚀 Sprih Internal Automations")
st.caption(
    "Call Coach + GTM Outreach internal workflow platform"
)

# =====================================================
# SIDEBAR
# =====================================================
module = st.sidebar.radio(
    "Select",
    [
        "📞 Call Coach",
        "🎯 GTM Outreach",
        "📊 Dashboard",
        "📚 History",
    ]
)

# =====================================================
# DASHBOARD
# =====================================================
if module == "📊 Dashboard":
    st.header("📊 Dashboard")

    col1, col2 = st.columns(2)

    col1.metric(
        "Call Coach Reports",
        len(st.session_state.coach_reports)
    )

    col2.metric(
        "GTM Runs",
        len(st.session_state.gtm_reports)
    )

# =====================================================
# CALL COACH
# =====================================================
elif module == "📞 Call Coach":
    st.header("📞 Call Coach Workflow")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "1️⃣ Context",
        "2️⃣ Scoring",
        "3️⃣ Coaching",
        "4️⃣ Actions",
        "5️⃣ Download"
    ])

    with tab1:
        rep_name = st.text_input("Sales Rep Name")
        company = st.text_input("Prospect / Company")

        call_type = st.selectbox(
            "Call Type",
            ["Discovery", "Demo", "Follow-up"]
        )

        origination = st.selectbox(
            "Origination",
            ["Inbound", "Outbound", "Referral"]
        )

        deal_stage = st.selectbox(
            "Deal Stage",
            ["Discovery", "Proposal", "Negotiation"]
        )

        transcript = st.text_area(
            "Transcript",
            height=300
        )

        generate = st.button("Generate Workflow Report")

        if generate:
            report = generate_report({
                "rep_name": rep_name,
                "company": company,
                "call_type": call_type,
                "origination": origination,
                "deal_stage": deal_stage,
                "transcript": transcript
            })

            st.session_state.latest_report = report
            st.session_state.coach_reports.append(report)

            st.success("Workflow report generated")

    if "latest_report" in st.session_state:
        report = st.session_state.latest_report

        with tab2:
            st.subheader("Framework Scores")

            for k, v in report["meddic"].items():
                st.metric(k, f"{v}/10")

        with tab3:
            st.subheader("Coaching Moments")

            for c in report["coaching"]:
                st.error(f"What happened: {c['what']}")
                st.info(f"Why it matters: {c['why']}")
                st.success(f"Better version: {c['better']}")

        with tab4:
            st.subheader("Immediate Actions")

            for a in report["actions"]:
                st.warning(a)

        with tab5:
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
    st.header("🎯 GTM Outreach")

    company_name = st.text_input("Target Company")
    persona = st.text_input("Persona")
    hook = st.text_area("Hook")

    if st.button("Generate Outreach"):
        st.success("Outreach created")

        st.write(
            f"Hi {company_name} team,\n\n"
            f"I noticed {hook}."
        )

# =====================================================
# HISTORY
# =====================================================
elif module == "📚 History":
    st.header("📚 History")

    for report in reversed(
        st.session_state.coach_reports
    ):
        with st.expander(
            report["header"]["rep_name"]
        ):
            st.write(report)
