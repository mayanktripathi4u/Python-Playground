import streamlit as st
from config import ALL_SUBJECTS, QUESTION_TYPES, DIFFICULTIES


def setup_sidebar():
    st.header("Setup")
    subject = st.radio("Subject", ALL_SUBJECTS)
    num_q = st.slider("Number of questions", 3, 15, 5)
    difficulty = st.selectbox("Difficulty", DIFFICULTIES)
    qtype = st.selectbox("Type", QUESTION_TYPES)
    model_name = st.text_input("Ollama model", value="llama3.1:8b")
    gen_clicked = st.button("Generate Test")
    return subject, num_q, difficulty, qtype, model_name, gen_clicked