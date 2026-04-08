import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("models/gemini-1.5-flash")

if analyze and transcript:
    try:
        prompt = f"""
You are a supportive senior sales coach.

Analyze this transcript using:
- MEDDIC
- SPICED
- Deal Health
- Coaching Moments

Address the rep as "you".

Transcript:
{transcript}
"""

        response = model.generate_content(prompt)

        result = response.text

        st.success("Analysis complete")
        st.write(result)

        st.download_button(
            "📥 Download Report",
            result,
            file_name="call_coaching_report.txt"
        )

    except Exception as e:
        st.error(f"Gemini API Error: {str(e)}")
