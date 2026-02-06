import streamlit as st
import requests
from docx import Document
from io import BytesIO

# -------------------------------------------------
# Helper: Create Word document
# -------------------------------------------------
def create_word_file(questions):
    doc = Document()
    doc.add_heading("Generated Questions", level=1)
    for i, q in enumerate(questions, 1):
        doc.add_paragraph(f"Q{i}. {q}")
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer


TEXT_API = "http://127.0.0.1:8000/generate-questions"
PDF_API = "http://127.0.0.1:8000/generate-questions-from-pdf"

st.set_page_config("Question Generator", "📘")
st.title("📘 Intelligent Question Generation System")

tab1, tab2 = st.tabs(["📝 Text / Topic", "📄 PDF"])

# =================================================
# TEXT / TOPIC
# =================================================
with tab1:
    mode = st.radio(
        "Input type",
        ["Topic based", "Content based"],
        key="text_mode"
    )

    topic = None
    content = None

    if mode == "Topic based":
        topic = st.text_input("Topic", key="text_topic")
    else:
        content = st.text_area("Content", height=200, key="text_content")

    keywords_input = st.text_input(
        "Keywords (optional, comma-separated)",
        placeholder="e.g. Deadlock, Starvation, Mutual Exclusion",
        key="text_keywords"
    )

    keywords = (
        [k.strip() for k in keywords_input.split(",") if k.strip()]
        if keywords_input else None
    )

    num_questions = st.number_input(
        "Number of Questions",
        1, 20, 5,
        key="text_num_questions"
    )

    difficulty = st.selectbox(
        "Difficulty",
        ["easy", "medium", "hard"],
        key="text_difficulty"
    )

    if st.button("Generate Questions", key="text_generate_btn"):
        payload = {
            "topic": topic,
            "content": content,
            "keywords": keywords,
            "num_questions": num_questions,
            "difficulty": difficulty
        }

        res = requests.post(TEXT_API, json=payload)
        if res.status_code == 200:
            st.session_state["questions"] = res.json()["questions"]
        else:
            st.error(res.text)


# =================================================
# PDF
# =================================================
with tab2:
    uploaded_pdf = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        key="pdf_uploader"
    )

    pdf_keywords_input = st.text_input(
        "Keywords (optional, comma-separated)",
        key="pdf_keywords"
    )

    pdf_keywords = (
        [k.strip() for k in pdf_keywords_input.split(",") if k.strip()]
        if pdf_keywords_input else None
    )

    pdf_num_questions = st.number_input(
        "Number of Questions",
        1, 50, 10,
        key="pdf_num_questions"
    )

    pdf_difficulty = st.selectbox(
        "Difficulty",
        ["easy", "medium", "hard"],
        key="pdf_difficulty"
    )

    if uploaded_pdf and st.button("Generate Questions", key="pdf_generate_btn"):
        files = {
            "file": (uploaded_pdf.name, uploaded_pdf.getvalue(), "application/pdf")
        }

        params = {
            "num_questions": pdf_num_questions,
            "difficulty": pdf_difficulty
        }

        if pdf_keywords:
            params["keywords"] = pdf_keywords

        res = requests.post(PDF_API, files=files, params=params)
        if res.status_code == 200:
            st.session_state["questions"] = res.json()["questions"]
        else:
            st.error(res.text)


# =================================================
# OUTPUT
# =================================================
if "questions" in st.session_state:
    st.subheader("Generated Questions")
    for i, q in enumerate(st.session_state["questions"], 1):
        st.write(f"**Q{i}.** {q}")

    st.download_button(
        "📄 Download as Word",
        create_word_file(st.session_state["questions"]),
        "generated_questions.docx"
    )
