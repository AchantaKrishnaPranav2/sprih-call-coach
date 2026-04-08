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
    st.success("Analysis complete")

    tab1, tab2, tab3 = st.tabs(
        ["📊 Scores", "🧠 Coaching", "🎯 Better Script"]
    )

    with tab1:
        c1, c2 = st.columns(2)
        c1.metric("MEDDIC", "8/10")
        c2.metric("SPICED", "7/10")

    with tab2:
        st.write("""
        You did a strong job uncovering buyer pain.
        The next opportunity is to quantify impact.
        """)

    with tab3:
        st.info("""
        Can you help me understand what this problem
        is costing the business each quarter?
        """)
