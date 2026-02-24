import streamlit as st
from ui import setup_sidebar
from quiz import llm_generate_questions, fallback_generate_questions
from grading import grade_mcq, llm_grade_short_answer


st.set_page_config(page_title="🎒 Grade 5 Tutor", layout="wide")
st.title("🎒 Grade 5 Tutor: Math & ELA")


subject, num_q, difficulty, qtype, model_name, gen_clicked = setup_sidebar()

if gen_clicked:
    qs = llm_generate_questions(subject, [], num_q, difficulty, qtype, model_name)
    if not qs:
        qs = fallback_generate_questions(subject, [], num_q, qtype)
    st.session_state["quiz"] = qs

quiz = st.session_state.get("quiz", [])

if quiz:
    for i, q in enumerate(quiz):
        st.write(f"Q{i+1}: {q['question']}")
        if q["type"] == "mcq":
            ans = st.radio("Choose:", q["choices"], key=f"a{i}")
        else:
            ans = st.text_area("Answer:", key=f"a{i}")
        st.session_state[f"ans{i}"] = ans

        