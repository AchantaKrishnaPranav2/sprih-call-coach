import streamlit as st
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from datetime import datetime
from io import BytesIO

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Sprih Call Coach",
    page_icon="🎯",
    layout="wide"
)

PRIMARY_GREEN = "1A3A2A"


# ---------------- HELPERS ----------------
def read_docx(uploaded_file):
    doc = Document(uploaded_file)
    return "\n".join(
        para.text for para in doc.paragraphs if para.text.strip()
    )


def generate_mock_report(rep_name, call_type, transcript):
    return {
        "rep": rep_name,
        "company": "Sample Prospect",
        "call_type": call_type,
        "origination": "Inbound",
        "deal_stage": "Discovery",
        "prev_notes": "Initial pain discovery completed.",
        "meddic": 8,
        "spiced": 7,
        "overall_score": 7.8,
        "feedback": "Strong discovery depth with clear pain signals.",
        "better_script": (
            "Can you help me quantify the business impact "
            "this issue is creating today?"
        ),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


def add_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def add_colored_paragraph(doc, text, color):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(11)
    run.font.color.rgb = RGBColor.from_string(color)
    return p


def create_docx_report(report):
    doc = Document()

    # HEADER
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True

    left = table.cell(0, 0)
    right = table.cell(0, 1)

    add_shading(left, PRIMARY_GREEN)
    add_shading(right, "F59E0B")

    run = left.paragraphs[0].add_run(
        f"CALL COACHING REPORT\n"
        f"{report['rep']} | {report['company']}\n"
        f"{report['timestamp']}\n"
        f"{report['call_type']} | {report['origination']}"
    )
    run.font.color.rgb = RGBColor(255, 255, 255)
    run.font.size = Pt(14)
    run.bold = True

    score_run = right.paragraphs[0].add_run(
        f"Overall Score\n{report['overall_score']}/10"
    )
    score_run.font.size = Pt(16)
    score_run.bold = True

    doc.add_paragraph()

    # CONTEXT SUMMARY
    doc.add_heading("1. CONTEXT SUMMARY", level=1)

    context_table = doc.add_table(rows=5, cols=2)
    context_table.style = "Table Grid"

    fields = [
        ("Call Type", report["call_type"]),
        ("Origination", report["origination"]),
        ("Discovery Previously Done", "Yes"),
        ("Deal Stage", report["deal_stage"]),
        ("Previous Call Notes", report["prev_notes"][:120])
    ]

    for i, (k, v) in enumerate(fields):
        context_table.cell(i, 0).text = k
        context_table.cell(i, 1).text = v

    doc.add_paragraph(
        "Calibration Note: Since this was an inbound discovery call, "
        "the scoring framework weighted discovery depth and pain clarity."
    )

    # CALL CLASSIFICATION
    doc.add_heading("2. CALL CLASSIFICATION", level=1)
    doc.add_paragraph(
        "This call is classified as a discovery call based on the "
        "buyer-led conversation and strong problem exploration."
    )

    # FRAMEWORK SCORES
    doc.add_heading("3. FRAMEWORK SCORES", level=1)

    score_table = doc.add_table(rows=3, cols=3)
    score_table.style = "Table Grid"

    score_table.cell(0, 0).text = "Framework"
    score_table.cell(0, 1).text = "Score"
    score_table.cell(0, 2).text = "Commentary"

    score_table.cell(1, 0).text = "MEDDIC"
    score_table.cell(1, 1).text = "8/10"
    score_table.cell(1, 2).text = (
        "Strong pain clarity. Path forward: quantify impact."
    )

    score_table.cell(2, 0).text = "SPICED"
    score_table.cell(2, 1).text = "7/10"
    score_table.cell(2, 2).text = (
        "Good situational understanding."
    )

    doc.add_paragraph(
        "Highest score: MEDDIC due to strong discovery.\n"
        "Lowest score: SPICED needs more impact quantification."
    )

    # DEAL HEALTH
    doc.add_heading("4. DEAL HEALTH", level=1)
    doc.add_paragraph("🟢 Discovery Depth — Strong")
    doc.add_paragraph("🔵 Pain Clarity — Adequate")
    doc.add_paragraph("🟠 Next Steps — Developing")
    doc.add_paragraph("⚪ Deal Control — Not Yet Explored")

    # COACHING MOMENTS
    doc.add_heading("5. COACHING MOMENTS", level=1)

    add_colored_paragraph(
        doc,
        "What happened: You asked a strong opening question.",
        "991B1B"
    )

    add_colored_paragraph(
        doc,
        "Why it matters: Great opportunity to deepen pain.",
        "6B7280"
    )

    add_colored_paragraph(
        doc,
        f"Better version: {report['better_script']}",
        "065F46"
    )

    # THEMES
    doc.add_heading("6. THEMES & INTELLIGENCE", level=1)
    doc.add_paragraph("• Signals & Objections: Budget sensitivity")
    doc.add_paragraph("• Requirements: Faster reporting workflows")
    doc.add_paragraph("• Patterns: Repeated operational inefficiencies")

    # TOP ACTIONS
    doc.add_heading("7. TOP 3 IMMEDIATE ACTIONS", level=1)
    doc.add_paragraph("TODAY — Send quantified follow-up questions")
    doc.add_paragraph("THIS WEEK — Confirm stakeholder map")
    doc.add_paragraph("BEFORE NEXT CALL — Build ROI narrative")

    # FOOTER
    doc.add_paragraph()
    footer = doc.add_paragraph()
    footer_run = footer.add_run(
        "Sprih Call Coach (automated)"
    )
    footer_run.italic = True
    footer_run.font.size = Pt(10)

    file_stream = BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)

    return file_stream


# ---------------- SESSION STATE ----------------
if "reports" not in st.session_state:
    st.session_state.reports = []

# ---------------- TITLE ----------------
st.title("🎯 Sprih Call Coach")
st.caption("Sales coaching workflow platform")

page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "New Analysis", "History"]
)

# ---------------- DASHBOARD ----------------
if page == "Dashboard":
    st.header("📊 Dashboard")
    st.metric("Total Calls", len(st.session_state.reports))

# ---------------- NEW ANALYSIS ----------------
elif page == "New Analysis":
    st.header("📝 New Call Analysis")

    rep_name = st.text_input("Sales Rep Name")
    call_type = st.selectbox(
        "Call Type",
        ["Discovery", "Demo", "Followup", "Mixed"]
    )

    transcript = st.text_area("Transcript", height=300)

    if st.button("🎯 Generate Report"):
        report = generate_mock_report(
            rep_name,
            call_type,
            transcript
        )

        st.session_state.reports.append(report)

        st.success("Report generated successfully")

        docx_file = create_docx_report(report)

        st.download_button(
            "📥 Download DOCX Report",
            docx_file,
            file_name=f"{rep_name}_call_coaching_report.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

# ---------------- HISTORY ----------------
elif page == "History":
    st.header("📚 History")

    for report in reversed(st.session_state.reports):
        with st.expander(report["rep"]):
            st.write(report)
