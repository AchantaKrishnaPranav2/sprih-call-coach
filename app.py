import streamlit as st

st.set_page_config(
    page_title="Sprih Call Coach",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Sprih Call Coach")
st.caption("AI-powered sales coaching dashboard")

st.sidebar.title("Automations")
option = st.sidebar.radio("Select", ["Call Coach"])

if option == "Call Coach":
    st.subheader("Analyze a Sales Call")

    rep_name = st.text_input("Sales Rep Name")

    call_type = st.selectbox(
        "Call Type",
        ["Discovery", "Demo", "Followup", "Mixed"]
    )

    transcript = st.text_area(
        "Paste Transcript",
        height=300
    )

    if st.button("Analyze Call"):
        st.success("Analysis complete")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("MEDDIC Score", "8/10")

        with col2:
            st.metric("SPICED Score", "7/10")

        st.write("### Coaching Feedback")
        st.write(
            "You did a strong job uncovering buyer pain. "
            "The next opportunity is to quantify impact."
        )

        st.write("### Better Script")
        st.info(
            "Can you help me understand what this problem "
            "is costing the business each quarter?"
        )
