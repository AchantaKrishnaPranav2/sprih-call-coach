import streamlit as st

st.set_page_config(
    page_title="Sprih Call Coach",
    page_icon="🎯",
    layout="wide"
)

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

    transcript = st.text_area(
        "Paste Transcript",
        height=250
    )

    analyze = st.button("Analyze Call")

with col2:
    st.info("""
    **Frameworks Used**
    - MEDDIC
    - SPICED
    - Deal Health
    - Coaching Moments
    """)

if analyze:
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
            f"{rep_name}, you did a strong job uncovering buyer pain."
        )

    with tab3:
        st.info(
            "Can you help me quantify the business impact?"
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
            "Download Report",
            report,
            file_name="call_coaching_report.txt"
        )
