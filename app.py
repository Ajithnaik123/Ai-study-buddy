import os
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load .env from the exact same folder as app.py
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="AI Study Buddy", page_icon="📚")
st.title("AI Study Notes & Quiz Generator")
st.write("Paste your study notes or an article below to get a summary and practice quiz.")

notes = st.text_area("Paste your notes here:", height=200)

if st.button("Generate Study Guide", type="primary"):
    if not notes.strip():
        st.warning("Please paste some text first!")
    else:
        with st.spinner("Generating summary and quiz..."):
            prompt = f"""
            Read the following study notes and create:
            1. **Quick Summary** (3 short bullet points)
            2. **Key Terms** (3 important terms with 1-sentence definitions)
            3. **3 Practice MCQs** (4 options each, and put the correct answers at the very bottom)

            Notes:
            {notes}
            """

            models_to_try = [
                "gemini-3.8-flash",
                "gemini-3.6-flash",
                "gemini-3.5-flash-lite",
            ]

            response = None
            for model_name in models_to_try:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )
                    break
                except Exception as e:
                    if ("503" in str(e) or "404" in str(e)) and model_name != models_to_try[-1]:
                        continue
                    raise e

            st.markdown(response.text)