import streamlit as st
import PyPDF2
import re

st.set_page_config(layout="wide")

st.title("Reading Practice App")

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Read PDF
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"

    # # --- Assume the PDF has passage first, then questions separated by a marker ---
    # # Example marker: "Questions:" or "Q1"
    # # You can tweak this logic based on your PDF structure
    # if "Questions" in text:
    #     passage, questions_raw = text.split("Questions", 1)
    #     questions = questions_raw.strip().split("\n")
    # else:
    #     # fallback if no marker found
    #     passage = text
    #     questions = ["Could not detect questions. Please check formatting."]

    # # Split screen
    # col1, col2 = st.columns(2)

    # with col1:
    #     st.subheader("Reading Passage")
    #     st.text_area("Passage", passage.strip(), height=600)

    # with col2:
    #     st.subheader("Questions")
    #     for i, q in enumerate(questions, 1):
    #         if q.strip():
    #             st.write(f"**{i}. {q.strip()}**")
    #             st.text_input(f"Answer {i}")




    # --- Split into passage and questions ---
    # Look for the "QUESTIONS" keyword in your format
    if "QUESTIONS" in text:
        passage, questions_raw = text.split("QUESTIONS", 1)
    else:
        passage = text
        questions_raw = ""

    # Clean passage (keep only Text A–D)
    passage_clean = []
    for block in re.split(r'(Text [A-D])', passage):
        if block.strip():
            passage_clean.append(block.strip())
    passage_final = "\n\n".join(passage_clean)

    # Split questions into list (look for numbers)
    questions = re.split(r"\n\d+\.", questions_raw)
    questions = [q.strip() for q in questions if q.strip()]

    # --- Layout ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Reading Passage (Text A–D)")
        st.text_area("Passage", passage_final, height=600)

    with col2:
        st.subheader("Questions")
        for i, q in enumerate(questions, 1):
            st.markdown(f"**{i}. {q}**")
            st.text_input(f"Answer {i}")