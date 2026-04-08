import streamlit as st
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from datetime import datetime
from io import BytesIO

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Sprih Internal Automations",
    page_icon="🚀",
    layout="wide",
)

PRIMARY_GREEN = "#1a3a2a"
CARD_BG = "#111827"
ACCENT = "#10b981"

# =========================================================
# GLOBAL STYLING
# =========================================================
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

    .main-card {{
        background-color: {CARD_BG};
        padding: 1rem;
        border-radius: 14px;
        border: 1px solid #1f2937;
        margin-bottom: 1rem;
    }}

    .section-title {{
        font-size: 24px;
        font-weight: 700;
        color: white;
        margin-bottom: 0.8rem;
    }}

    .metric-card {{
        background: #111827;
        padding: 1rem;
        border-radius: 12px;
        border-left: 5px solid {ACCENT};
        margin-bottom: 1rem;
    }}

    .coach-card {{
        background: #111827;
        padding: 1rem;
        border-radius: 12px;
        border-left: 5px solid #ef4444;
        margin-bottom: 1rem;
    }}

    .good-card {{
        background: #111827;
        padding: 1rem;
        border-radius: 12px;
        border-left: 5px solid #22c55e;
        margin-bottom: 1rem;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# SESSION
# =========================================================
if "coach_reports" not in st.session_state:
    st.session_state.coach_reports = []

if "gtm_reports" not in st.session_state:
    st.session_state.gtm_reports = []

# =========================================================
# HELPERS
# =========================================================
def shade_cell(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def generate_call_coach_report(data):
    transcript = data["transcript"].lower()

    meddic = {
        "Metrics": 8 if "cost" in transcript else 6,
        "Economic Buyer": 7,
        "Decision Criteria": 8,
        "Decision Process": 7,
        "Identify Pain": 9 if "pain" in transcript else 6,
        "Champion": 5,
    }

    deal_health = {
        "Discovery Depth": "Strong",
        "Pain Clarity": "Adequate",
        "Deal Control": "Developing",
        "Next Steps": "Adequate",
    }

    actions = [
        "TODAY — send quantified follow-up questions",
        "THIS WEEK — map stakeholders",
        "BEFORE NEXT CALL — build ROI narrative",
    ]

    return {
        "header": data,
        "meddic": meddic,
        "deal_health": deal_health,
        "actions": actions,
        "overall_score": round(
            sum(meddic.values()) / len(meddic), 1
        ),
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        ),
    }


def create_docx_report(report):
    doc = Document()

    table = doc.add_table(rows=1, cols=2)
    left = table.cell(0, 0)
    right = table.cell(0, 1)

    shade_cell(left, "1A3A2A")
    shade_cell(right, "F59E0B")

    h = report["header"]

    run = left.paragraphs[0].add_run(
        f"{h['rep_name']}\n"
        f"{h['company']}\n"
        f"{h['call_type']} | {h['origination']}"
    )
    run.font.color.rgb = RGBColor(255, 255, 255)

    right.paragraphs[0].add_run(
        f"{report['overall_score']}/10"
    )

    stream = BytesIO()
    doc.save(stream)
    stream.seek(0)

    return stream


# =========================================================
# APP HEADER
# =========================================================
st.title("🚀 Sprih Internal Automations")
st.caption(
    "Call Coach + GTM Outreach internal workflow platform"
)

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("Automations")

module = st.sidebar.radio(
    "Select",
    [
        "📞 Call Coach",
        "🎯 GTM Outreach",
        "📊 Dashboard",
        "📚 History",
    ],
)

# =========================================================
# DASHBOARD
# =========================================================
if module == "📊 Dashboard":
    st.markdown(
        '<div class="section-title">📊 Dashboard</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <h3>Call Coach Reports</h3>
                <h1>{len(st.session_state.coach_reports)}</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <h3>GTM Outreach Runs</h3>
                <h1>{len(st.session_state.gtm_reports)}</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )

# =========================================================
# CALL COACH
# =========================================================
elif module == "📞 Call Coach":
    st.markdown(
        '<div class="section-title">📞 Call Coach</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        rep_name = st.text_input("Sales Rep Name")
        company = st.text_input("Prospect / Company")

        call_date = st.date_input("Call Date")

        call_type = st.selectbox(
            "Call Type",
            [
                "Discovery",
                "Demo",
                "Follow-up",
                "Commercial",
            ],
        )

        origination = st.selectbox(
            "Origination",
            [
                "Inbound",
                "Outbound",
                "Referral",
            ],
        )

        deal_stage = st.selectbox(
            "Deal Stage",
            [
                "Discovery",
                "Qualification",
                "Proposal",
                "Negotiation",
            ],
        )

        discovery_done = st.selectbox(
            "Discovery Previously Done",
            ["Yes", "No", "Partial"],
        )

        previous_notes = st.text_area(
            "Previous Call Notes"
        )

        calibration_note = st.text_area(
            "Calibration Note"
        )

        transcript = st.text_area(
            "Transcript",
            height=250,
        )

        generate = st.button("🎯 Generate Report")

    with col2:
        st.markdown(
            """
            <div class="main-card">
                <h3>Frameworks</h3>
                <ul>
                    <li>MEDDIC</li>
                    <li>Deal Health</li>
                    <li>Coaching Moments</li>
                    <li>Themes</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if generate:
        data = {
            "rep_name": rep_name,
            "company": company,
            "call_date": str(call_date),
            "call_type": call_type,
            "origination": origination,
            "deal_stage": deal_stage,
            "discovery_done": discovery_done,
            "previous_notes": previous_notes,
            "calibration_note": calibration_note,
            "transcript": transcript,
        }

        report = generate_call_coach_report(data)
        st.session_state.coach_reports.append(report)

        st.success("Report generated")

        st.metric(
            "Overall Score",
            f"{report['overall_score']}/10",
        )

        st.subheader("Framework Scores")
        for k, v in report["meddic"].items():
            st.markdown(
                f"""
                <div class="metric-card">
                    <b>{k}</b><br>
                    {v}/10
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.subheader("Deal Health")
        for k, v in report["deal_health"].items():
            st.markdown(
                f"""
                <div class="good-card">
                    <b>{k}</b><br>
                    {v}
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.subheader("Top Actions")
        for action in report["actions"]:
            st.markdown(
                f"""
                <div class="coach-card">
                    {action}
                </div>
                """,
                unsafe_allow_html=True,
            )

        docx = create_docx_report(report)

        st.download_button(
            "📥 Download DOCX Report",
            docx,
            file_name=f"{rep_name}_call_coach_report.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

# =========================================================
# GTM OUTREACH
# =========================================================
elif module == "🎯 GTM Outreach":
    st.markdown(
        '<div class="section-title">🎯 GTM Outreach</div>',
        unsafe_allow_html=True,
    )

    company_name = st.text_input("Target Company")
    persona = st.text_input("Persona")
    hook = st.text_area("Hook / Personalisation")

    if st.button("Generate Outreach Brief"):
        st.success("Outreach brief created")

        st.markdown(
            f"""
            <div class="main-card">
                <h3>Email Draft</h3>
                <p>Hi {company_name} team,</p>
                <p>I noticed {hook}.</p>
                <p>Would love to connect regarding ESG workflows.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# =========================================================
# HISTORY
# =========================================================
elif module == "📚 History":
    st.markdown(
        '<div class="section-title">📚 History</div>',
        unsafe_allow_html=True,
    )

    for report in reversed(
        st.session_state.coach_reports
    ):
        with st.expander(
            report["header"]["rep_name"]
        ):
            st.write(report)
