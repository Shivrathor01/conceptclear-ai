import streamlit as st
import google.generativeai as genai

import os
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
if "history" not in st.session_state:
    st.session_state.history = []


model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title="ConceptClear AI", page_icon="🧠")
st.title("🧠 ConceptClear AI")
st.subheader("Engineering concept - simple explanation")

# Subject filter
subject = st.selectbox("Apna subject choose karo:", 
    ["Computer Science", "Electronics (EC)", "Mechanical", "Civil", "General"])

# Language toggle
language = st.radio("Explanation Language:", ["Hinglish 🇮🇳", "English 🇬🇧"], horizontal=True)

if language == "Hinglish 🇮🇳":
    lang_instruction = "simple Hindi-English (Hinglish) mein samjhao"
else:
    lang_instruction = "simple English mein samjhao"

# Input
topic = st.text_input("Kaunsa concept samajhna hai?", placeholder="e.g. Transformer, Recursion, DBMS")

if st.button("Explain Karo!"):
    if topic:
        with st.spinner("Samjha raha hoon..."):
            prompt = f"""
            Tu ek expert teacher hai jo Indian engineering students ko concepts {lang_instruction}.
            Subject: {subject}
            Concept: {topic}
            Isko explain kar:
            1. Simple definition (1-2 lines)
            2. Real life example
            3. Engineering mein use kahan hota hai
            """
            response = model.generate_content(prompt)
            st.success("Done!")
            st.write(response.text)

        st.session_state.history.append({
            "topic": topic,
            "subject": subject,
            "answer": response.text
        })
    else:
        st.warning("Pehle concept ka naam likho!")

if st.session_state.history:
    st.divider()
    st.subheader("📚 Previous Concepts")
    for item in reversed(st.session_state.history):
        with st.expander(f"🔹 {item['topic']} — {item['subject']}"):
            st.write(item["answer"])