"""
POC: Grade 5 Learning App (Math & ELA) with Streamlit + (optional) RAG + Ollama LLM
------------------------------------------------------------------------------------
Quick start
1) Install dependencies (minimal):
   pip install streamlit requests
   # Optional (for CSV export pretty formatting)
   pip install pandas

2) Install & run Ollama locally (https://ollama.com):
   - Install Ollama for your OS
   - Pull a model (examples):
       ollama pull llama3.1:8b     # good balance for local laptops
       # or choose a smaller one, e.g. phi3:mini or mistral:7b
   - Ensure the Ollama server is running (default http://localhost:11434)

3) Save this file as: streamlit_poc_grade5_tutor_app.py
   Run:  streamlit run streamlit_poc_grade5_tutor_app.py

Notes
- This is a self‑contained POC. It works even without an LLM by falling back to a small built‑in
  question bank. When an LLM is available, it uses topic notes (RAG‑lite) to guide generation.
- Designed to keep content friendly, factual, and grade‑appropriate.
- You can swap in any local Ollama model by typing its name in the sidebar.
"""

from __future__ import annotations

import json
import random
import re
import textwrap
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests
import streamlit as st

try:
    import pandas as pd  # optional; used for exporting results
except Exception:  # pragma: no cover
    pd = None

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(
    page_title="🎒 Grade 5 Tutor (Math & ELA)", page_icon="🎒", layout="wide"
)

# -------------------------------
# Small, friendly knowledge base (RAG-lite)
# -------------------------------
KB: Dict[str, Dict[str, str]] = {
    "Math": {
        "Place Value": "In base-10, each digit has a place value. From right to left: ones, tens, hundreds, thousands. A 0 holds a place.",
        "Fractions": "A fraction a/b represents a parts out of b equal parts. Equivalent fractions name the same amount (e.g., 1/2 = 2/4). To add same-denominator fractions: add numerators.",
        "Decimals": "Decimals are fractions with denominators of 10, 100, 1000... Example: 0.3 = 3/10. Line up the decimal points when adding or subtracting decimals.",
        "Multiplication & Division": "Multiplication is repeated addition; division is sharing or grouping. Know basic facts up to 12x12. Use area models and equal groups.",
        "Word Problems": "Solve using the four operations. Read carefully, identify what is asked, choose an operation, compute, and label the answer with units.",
        "Geometry": "Classify shapes by properties (sides, angles). Perimeter adds all sides; area of rectangles is length × width.",
        "Measurement & Data": "Use units (cm, m, g, kg, mL, L). Convert within the same system. Read bar graphs and line plots.",
    },
    "ELA": {
        "Grammar": "A complete sentence has a subject and predicate. Nouns name people, places, or things; verbs show action or state. Use correct capitalization and punctuation.",
        "Vocabulary": "Use context clues (definition, example, restatement) to infer meaning. Prefixes and suffixes can change meaning (re-, un-, -ful).",
        "Reading Comprehension": "Identify main idea and key details. Summarize using beginning, middle, end. Make inferences using text evidence.",
        "Figurative Language": "Similes compare using 'like' or 'as'; metaphors say one thing is another. Personification gives human traits to non-human things.",
        "Writing": "Plan, draft, revise, and edit. Use a clear topic sentence and supporting details. Keep tone and audience in mind.",
    },
}

ALL_SUBJECTS = list(KB.keys())  # ["Math", "ELA"]

QUESTION_TYPES = ["Multiple Choice", "Short Answer", "Mixed"]
DIFFICULTIES = ["Easy", "Medium", "Hard"]

# Built-in fallback question bank (if LLM is unavailable)
FALLBACK_BANK: Dict[str, Dict[str, List[Dict[str, Any]]]] = {
    "Math": {
        "Fractions": [
            {
                "type": "mcq",
                "question": "Which fraction is equivalent to 1/2?",
                "choices": ["2/4", "1/3", "3/5", "2/3"],
                "answer": "2/4",
                "explanation": "Multiplying numerator and denominator by 2 gives 2/4, equal to 1/2.",
            },
            {
                "type": "mcq",
                "question": "Add: 2/8 + 3/8 = ?",
                "choices": ["5/16", "5/8", "1/8", "3/16"],
                "answer": "5/8",
                "explanation": "Same denominator: add numerators 2+3=5.",
            },
        ],
        "Word Problems": [
            {
                "type": "mcq",
                "question": "Lena has 3 packs of stickers with 8 in each pack. How many stickers in total?",
                "choices": ["11", "24", "21", "26"],
                "answer": "24",
                "explanation": "3 × 8 = 24.",
            },
            {
                "type": "mcq",
                "question": "A rope is 36 m long. You cut it into 4 equal pieces. How long is each piece?",
                "choices": ["8 m", "9 m", "6 m", "12 m"],
                "answer": "9 m",
                "explanation": "36 ÷ 4 = 9.",
            },
        ],
        "Decimals": [
            {
                "type": "mcq",
                "question": "What is 0.4 + 0.25?",
                "choices": ["0.65", "0.9", "0.045", "0.625"],
                "answer": "0.65",
                "explanation": "Line up decimals: 0.40 + 0.25 = 0.65.",
            },
        ],
        "Geometry": [
            {
                "type": "mcq",
                "question": "Find the area of a rectangle with length 7 cm and width 3 cm.",
                "choices": ["21 cm²", "10 cm²", "14 cm²", "18 cm²"],
                "answer": "21 cm²",
                "explanation": "Area = l × w = 7 × 3 = 21 cm².",
            }
        ],
    },
    "ELA": {
        "Grammar": [
            {
                "type": "mcq",
                "question": "Which sentence is complete?",
                "choices": [
                    "Because the dog.",
                    "Running fast in the park.",
                    "The cat slept on the sofa.",
                    "When the bell rang.",
                ],
                "answer": "The cat slept on the sofa.",
                "explanation": "It has a subject (the cat) and a predicate (slept on the sofa).",
            }
        ],
        "Vocabulary": [
            {
                "type": "mcq",
                "question": "Using context clues: 'After the long hike, the children were famished.' What does 'famished' most nearly mean?",
                "choices": ["sad", "tired", "hungry", "excited"],
                "answer": "hungry",
                "explanation": "After a long hike, children are likely very hungry.",
            }
        ],
        "Reading Comprehension": [
            {
                "type": "short",
                "question": "Read: 'Ava practiced piano every day and improved her recital piece.' What is the main idea?",
                "rubric": "Award 2 points if student states that practice led to improvement; 1 point for partial idea about practicing or improving; 0 otherwise.",
                "answer": "With daily practice, Ava improved her piano piece.",
                "explanation": "Main idea connects practice to improvement.",
            }
        ],
    },
}

# -------------------------------
# Ollama LLM client (chat endpoint)
# -------------------------------

def call_ollama_chat(
    messages: List[Dict[str, str]],
    model: str = "llama3.1:8b",
    host: str = "http://localhost:11434",
    timeout: int = 90,
) -> Optional[str]:
    """Call local Ollama chat API. Returns assistant content or None on failure."""
    try:
        resp = requests.post(
            f"{host}/api/chat",
            json={"model": model, "messages": messages, "stream": False},
            timeout=timeout,
        )
        resp.raise_for_status()
        data = resp.json()
        content = data.get("message", {}).get("content", "")
        return content or None
    except Exception as e:
        return None


# -------------------------------
# Utilities
# -------------------------------

def extract_json_block(text: str) -> Optional[str]:
    """Try to extract the first JSON array/object from a string."""
    if not text:
        return None
    # Prefer an array of questions
    m = re.search(r"\[.*\]", text, flags=re.DOTALL)
    if m:
        return m.group(0)
    # Fallback: single object
    m = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if m:
        return m.group(0)
    return None


def build_context(subject: str, topics: List[str]) -> str:
    """Return concatenated topic notes as grounding (RAG-lite)."""
    notes = []
    kb = KB.get(subject, {})
    if not topics:
        topics = list(kb.keys())
    for t in topics:
        if t in kb:
            notes.append(f"Topic: {t}\nNotes: {kb[t]}")
    return "\n\n".join(notes)


def llm_generate_questions(
    subject: str,
    topics: List[str],
    n: int,
    difficulty: str,
    qtype: str,
    model_name: str,
    include_word_problem_for_math: bool = True,
) -> Optional[List[Dict[str, Any]]]:
    """Ask the LLM to produce n questions as JSON. Returns list or None."""
    context = build_context(subject, topics)

    # Always keep it gentle + age-appropriate
    safety_rules = (
        "Keep all content friendly, factual, kid-safe, and appropriate for grade 5. "
        "Avoid any sensitive or violent topics."
    )

    # Ensure at least one word problem for Math if requested
    word_problem_clause = (
        "Include at least one word problem involving real-life scenarios and units."
        if include_word_problem_for_math and subject == "Math"
        else ""
    )

    # Question type handling
    qtype_instruction = {
        "Multiple Choice": (
            "Create only multiple-choice questions with exactly 4 choices and a clear answer key."
        ),
        "Short Answer": (
            "Create only short-answer questions with a concise expected answer and a one-sentence rubric."
        ),
        "Mixed": (
            "Mix multiple-choice and short-answer questions (about half each). MCQs must have exactly 4 choices."
        ),
    }[qtype]

    system = (
        "You are a helpful grade-5 tutor who generates quizzes in strict JSON. "
        "Never include markdown or commentary, only the JSON array."
    )

    user = f"""
Use the following topic notes as grounding (RAG):
{context}

Subject: {subject}
Difficulty: {difficulty}
Number of questions: {n}
{word_problem_clause}

{qtype_instruction}

Return ONLY a JSON array of objects. Each object has:
- type: "mcq" or "short"
- topic: one of the provided topics
- question: the question text (for Math, keep numbers simple; show units if used)
- choices: array of 4 strings (ONLY for type="mcq")
- answer: string with the correct answer (for mcq: must match one of the choices exactly)
- explanation: one short sentence explaining the solution
- rubric: (ONLY for type="short") very short rubric (1-2 sentences) to guide grading
"""

    content = call_ollama_chat(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        model=model_name,
    )

    if not content:
        return None

    block = extract_json_block(content)
    if not block:
        return None

    try:
        data = json.loads(block)
        # Light validation & trimming
        questions: List[Dict[str, Any]] = []
        topics_available = topics or list(KB.get(subject, {}).keys())
        for q in data:
            if not isinstance(q, dict):
                continue
            t = q.get("type")
            if t not in {"mcq", "short"}:
                continue
            # Fill topic if missing
            if "topic" not in q or q.get("topic") not in topics_available:
                q["topic"] = random.choice(topics_available) if topics_available else "General"
            # MCQ checks
            if t == "mcq":
                choices = q.get("choices") or []
                if not (isinstance(choices, list) and len(choices) == 4):
                    # skip malformed MCQs
                    continue
                ans = q.get("answer")
                if ans not in choices:
                    continue
            # Short answer: ensure rubric exists
            if t == "short" and not q.get("rubric"):
                q["rubric"] = "Answer should directly address the prompt in 1-2 sentences."
            # Common fields
            if not q.get("question") or not q.get("answer"):
                continue
            if not q.get("explanation"):
                q["explanation"] = ""
            questions.append(q)
        # Trim to n
        return questions[:n]
    except Exception:
        return None


def fallback_generate_questions(
    subject: str, topics: List[str], n: int, qtype: str
) -> List[Dict[str, Any]]:
    """Use built-in bank to assemble a quiz if LLM isn't available."""
    bank = FALLBACK_BANK.get(subject, {})
    if not topics:
        topics = list(bank.keys())
    pool: List[Dict[str, Any]] = []
    for t in topics:
        pool.extend(bank.get(t, []))
    random.shuffle(pool)

    # Filter by type if needed
    def type_ok(q):
        if qtype == "Mixed":
            return True
        if qtype == "Multiple Choice":
            return q.get("type") == "mcq"
        if qtype == "Short Answer":
            return q.get("type") == "short"
        return True

    filtered = [q for q in pool if type_ok(q)]

    # If not enough, duplicate with slight numeric tweaks for math MCQs
    result: List[Dict[str, Any]] = []
    i = 0
    while len(result) < n and i < len(filtered):
        result.append(filtered[i])
        i += 1
    # If still short, pad with simple generator
    while len(result) < n:
        if subject == "Math":
            a, b = random.randint(2, 12), random.randint(2, 12)
            ans = a * b
            ch = sorted(list({ans, ans + 1, ans - 1, ans + 2}))
            q = {
                "type": "mcq",
                "topic": "Multiplication & Division",
                "question": f"What is {a} × {b}?",
                "choices": [str(x) for x in ch],
                "answer": str(ans),
                "explanation": f"{a} × {b} = {ans}.",
            }
            result.append(q)
        else:  # ELA simple vocab
            word, meaning = random.choice([
                ("brisk", "quick"),
                ("gleam", "shine"),
                ("sturdy", "strong"),
            ])
            wrong = ["sad", "tiny", "noisy"]
            random.shuffle(wrong)
            q = {
                "type": "mcq",
                "topic": "Vocabulary",
                "question": f"What is the closest meaning of '{word}'?",
                "choices": [meaning] + wrong[:3],
                "answer": meaning,
                "explanation": f"'{word}' most nearly means '{meaning}'.",
            }
            result.append(q)
    return result[:n]


# -------------------------------
# Grading
# -------------------------------

def grade_mcq(correct: str, chosen: Optional[str]) -> int:
    return int((chosen or "").strip() == (correct or "").strip())


def llm_grade_short_answer(
    question: str, expected: str, student: str, rubric: str, model_name: str
) -> Dict[str, Any]:
    """Use the LLM to grade a short answer (0/1/2) with brief feedback."""
    system = (
        "You are a fair grade-5 grader. Score the student's short answer 0, 1, or 2, "
        "where 2=fully correct, 1=partly correct, 0=incorrect. Be kind and brief."
    )
    user = f"""
Question: {question}
Expected (teacher notes): {expected}
Student answer: {student}
Rubric: {rubric}
Return ONLY a compact JSON object: {{"score": 0|1|2, "feedback": "..."}}
"""
    content = call_ollama_chat(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        model=model_name,
    )
    block = extract_json_block(content or "")
    try:
        data = json.loads(block) if block else {}
        score = int(data.get("score", 0))
        score = max(0, min(2, score))
        feedback = str(data.get("feedback", ""))[:300]
        return {"score": score, "feedback": feedback}
    except Exception:
        # Simple keyword overlap fallback
        score = 2 if expected and student and expected.split()[0].lower() in student.lower() else 1 if student else 0
        return {"score": score, "feedback": "Thanks! Review the key idea above."}


# -------------------------------
# UI Helpers
# -------------------------------

def subject_topics(subject: str) -> List[str]:
    return list(KB.get(subject, {}).keys())


def ensure_session_state():
    if "quiz" not in st.session_state:
        st.session_state.quiz: List[Dict[str, Any]] = []
    if "answers" not in st.session_state:
        st.session_state.answers: Dict[int, Any] = {}
    if "graded" not in st.session_state:
        st.session_state.graded = False
    if "report" not in st.session_state:
        st.session_state.report: Dict[str, Any] = {}


ensure_session_state()

# -------------------------------
# Sidebar Controls
# -------------------------------
with st.sidebar:
    st.header("Setup")
    subject = st.radio("Subject", ALL_SUBJECTS, horizontal=True)

    available_topics = subject_topics(subject)
    chosen_topics = st.multiselect(
        "Topics (leave empty for *all*)", options=available_topics, default=[]
    )

    num_q = st.slider("Number of questions", 3, 15, 6)
    difficulty = st.selectbox("Difficulty", DIFFICULTIES, index=1)
    qtype = st.selectbox("Question type", QUESTION_TYPES, index=0)

    st.divider()
    st.subheader("LLM (optional)")
    use_llm = st.toggle("Use Ollama to generate questions", value=True)
    model_name = st.text_input("Ollama model", value="llama3.1:8b")
    ollama_host = st.text_input("Ollama host", value="http://localhost:11434")

    st.caption(
        "If LLM fails or is off, the app will fall back to a small built‑in question bank."
    )

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        gen_clicked = st.button("🧪 Generate Test", use_container_width=True)
    with col_btn2:
        if st.button("♻️ Reset", use_container_width=True):
            st.session_state.quiz = []
            st.session_state.answers = {}
            st.session_state.graded = False
            st.session_state.report = {}
            st.experimental_rerun()

# -------------------------------
# Generate Quiz
# -------------------------------
if gen_clicked:
    # Build questions via LLM if possible
    questions = None
    if use_llm and model_name.strip():
        questions = llm_generate_questions(
            subject=subject,
            topics=chosen_topics,
            n=num_q,
            difficulty=difficulty,
            qtype=qtype,
            model_name=model_name.strip(),
            include_word_problem_for_math=True,
        )
    if not questions:
        questions = fallback_generate_questions(subject, chosen_topics, num_q, qtype)

    # Persist quiz
    st.session_state.quiz = questions
    st.session_state.answers = {}
    st.session_state.graded = False
    st.session_state.report = {}


# -------------------------------
# Main: Render Quiz
# -------------------------------
st.title("🎒 Grade 5 Tutor: Math & ELA")
st.write(
    "Pick a subject and topics on the left, then click **Generate Test** to begin."
)

quiz = st.session_state.quiz

if quiz:
    st.subheader("Your Test")
    for i, q in enumerate(quiz):
        with st.container(border=True):
            meta = f"**Q{i+1}.** ({q.get('topic', 'General')})"
            st.markdown(meta)
            st.write(q.get("question", ""))

            if q.get("type") == "mcq":
                key = f"q_{i}_mcq"
                choice = st.radio(
                    "Choose one:",
                    q.get("choices", []),
                    index=None,
                    key=key,
                )
                st.session_state.answers[i] = choice
            else:
                key = f"q_{i}_short"
                ans = st.text_area("Your answer:", key=key)
                st.session_state.answers[i] = ans

    col_submit, col_export = st.columns([1, 1])
    with col_submit:
        if st.button("✅ Submit & Grade", use_container_width=True):
            # Grade the quiz
            total = 0
            max_score = 0
            details = []
            for i, q in enumerate(quiz):
                if q.get("type") == "mcq":
                    score = grade_mcq(q.get("answer", ""), st.session_state.answers.get(i))
                    max_score += 1
                    total += score
                    details.append(
                        {
                            "q#": i + 1,
                            "type": "MCQ",
                            "topic": q.get("topic", ""),
                            "question": q.get("question", ""),
                            "your_answer": st.session_state.answers.get(i),
                            "correct_answer": q.get("answer", ""),
                            "explanation": q.get("explanation", ""),
                            "score": score,
                            "max": 1,
                        }
                    )
                else:
                    # Short answer graded by LLM if available, else light heuristic
                    r = llm_grade_short_answer(
                        question=q.get("question", ""),
                        expected=q.get("answer", ""),
                        student=st.session_state.answers.get(i, ""),
                        rubric=q.get("rubric", "Give a concise, correct answer."),
                        model_name=model_name if use_llm else "",
                    )
                    score = r.get("score", 0)
                    feedback = r.get("feedback", "")
                    max_score += 2
                    total += score
                    details.append(
                        {
                            "q#": i + 1,
                            "type": "Short",
                            "topic": q.get("topic", ""),
                            "question": q.get("question", ""),
                            "your_answer": st.session_state.answers.get(i, ""),
                            "expected": q.get("answer", ""),
                            "rubric": q.get("rubric", ""),
                            "explanation": q.get("explanation", ""),
                            "score": score,
                            "max": 2,
                            "feedback": feedback,
                        }
                    )

            percent = round(100 * total / max_score) if max_score else 0
            st.session_state.graded = True
            st.session_state.report = {
                "total": total,
                "max_score": max_score,
                "percent": percent,
                "details": details,
                "subject": subject,
                "topics": chosen_topics or ["All"],
                "graded_at": datetime.now().isoformat(timespec="seconds"),
            }
            st.experimental_rerun()

    with col_export:
        if st.session_state.graded and pd is not None:
            if st.button("⬇️ Export Results (CSV)", use_container_width=True):
                df = pd.DataFrame(st.session_state.report["details"])
                csv_path = f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                df.to_csv(csv_path, index=False)
                st.success(f"Saved {csv_path} next to the app.")

# -------------------------------
# Results / Report
# -------------------------------
if st.session_state.get("graded"):
    rep = st.session_state.get("report", {})
    st.subheader("Results")
    st.metric("Score", f"{rep.get('total', 0)}/{rep.get('max_score', 0)}", f"{rep.get('percent', 0)}%")
    st.caption(
        f"Subject: {rep.get('subject')} · Topics: {', '.join(rep.get('topics', []))} · {rep.get('graded_at', '')}"
    )

    # Show per-question feedback
    for d in rep.get("details", []):
        with st.expander(f"Q{d['q#']}: {d.get('topic', '')} – {d.get('type')}"):
            st.write(d.get("question", ""))
            if d.get("type") == "MCQ":
                st.write(f"**Your answer:** {d.get('your_answer')}  ")
                st.write(f"**Correct answer:** {d.get('correct_answer')}")
            else:
                st.write(f"**Your answer:** {d.get('your_answer')}")
                st.write(f"**Expected (teacher notes):** {d.get('expected')}")
                if d.get("feedback"):
                    st.info(d.get("feedback"))
            if d.get("explanation"):
                st.caption(f"Explanation: {d.get('explanation')}")
            st.progress(d.get("score", 0) / max(1, d.get("max", 1)))

# -------------------------------
# Tips box
# -------------------------------
with st.expander("⚙️ Tips & Customization"):
    st.markdown(
        """
- **Add more topics**: Edit the `KB` dictionary to include more grade‑level notes. The LLM will use these as grounding.
- **Force more word problems**: In `llm_generate_questions`, increase the emphasis or filter MCQs whose text includes real‑life scenarios.
- **Switch models**: Try `mistral:7b`, `phi3:mini`, or any model you have in Ollama. Smaller models generate faster.
- **No LLM?** The app still works using the fallback question bank and a tiny generator. Expand it over time.
- **Scoring weights**: MCQ=1 point, Short=2 points by default. Adjust in the grading section.
- **Data export**: If `pandas` is installed, you can export detailed results as CSV.
        """
    )
