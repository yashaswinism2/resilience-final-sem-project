import streamlit as st
import requests
from docx import Document
from io import BytesIO

# -------------------------------------------------
# Helper function: Create Word document in memory
# -------------------------------------------------
def create_word_file(questions):
    doc = Document()
    doc.add_heading("Generated Questions", level=1)

    for i, q in enumerate(questions, start=1):
        doc.add_paragraph(f"Q{i}. {q}")

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    return buffer


# -------------------------------------------------
# Backend API URL
# -------------------------------------------------
API_URL = "http://127.0.0.1:8003/generate-questions"


# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Intelligent Question Generation System",
    page_icon="📘",
    layout="centered"
)

st.title("📘 Intelligent Question Generation System")
st.write(
    "Generate exam-style questions using NLP and Large Language Models (LLMs)."
)


# -------------------------------------------------
# Input Mode Selection
# -------------------------------------------------
mode = st.radio(
    "Choose input type",
    ["Topic based", "Content based"]
)


# -------------------------------------------------
# Input Fields
# -------------------------------------------------
topic = None
content = None

if mode == "Topic based":
    topic = st.text_input(
        "Enter Topic",
        placeholder="e.g. Operating Systems – Deadlocks"
    )
else:
    content = st.text_area(
        "Paste Content",
        height=200,
        placeholder="Paste your study material here..."
    )

num_questions = st.number_input(
    "Number of Questions",
    min_value=1,
    max_value=10,
    value=5
)

difficulty = st.selectbox(
    "Difficulty Level",
    ["easy", "medium", "hard"]
)


# -------------------------------------------------
# Generate Questions Button
# -------------------------------------------------
if st.button("Generate Questions"):

    # -------- Validation --------
    if mode == "Topic based" and not topic:
        st.warning("Please enter a topic.")
    elif mode == "Content based" and not content:
        st.warning("Please paste some content.")
    else:
        payload = {
            "topic": topic,
            "content": content,
            "num_questions": num_questions,
            "difficulty": difficulty
        }

        with st.spinner("Generating questions..."):
            try:
                response = requests.post(API_URL, json=payload)

                if response.status_code == 200:
                    data = response.json()

                    st.success("Questions Generated Successfully 🎉")

                    # Store questions in session state
                    st.session_state["questions"] = data["questions"]

                else:
                    st.error(f"Backend Error: {response.text}")

            except Exception as e:
                st.error(f"Could not connect to backend: {e}")


# -------------------------------------------------
# Display Questions (if available)
# -------------------------------------------------
if "questions" in st.session_state and st.session_state["questions"]:
    st.subheader("Generated Questions")

    for i, q in enumerate(st.session_state["questions"], start=1):
        st.write(f"**Q{i}.** {q}")

   
    # Download as Word File Button
    
    word_file = create_word_file(st.session_state["questions"])

    st.download_button(
        label="📄 Download Questions as Word File",
        data=word_file,
        file_name="generated_questions.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
