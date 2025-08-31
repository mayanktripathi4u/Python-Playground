
import streamlit as st
import re

try:
    import fitz  # PyMuPDF for line-preserving extraction
    PYMUPDF_AVAILABLE = True
except Exception:
    PYMUPDF_AVAILABLE = False

st.set_page_config(layout="wide")
st.title("PDF → Split-Screen Reading & Questions (Improved)")

uploaded = st.file_uploader("Upload your PDF", type=["pdf"])

def extract_lines(file_bytes: bytes):
    # Extract text lines using PyMuPDF
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    all_lines = []
    for pno in range(len(doc)):
        page = doc[pno]
        data = page.get_text("dict")
        for block in data.get("blocks", []):
            if "lines" not in block:
                continue
            for line in block["lines"]:
                spans = line.get("spans", [])
                if not spans:
                    continue
                line_text = "".join(span.get("text", "") for span in spans).rstrip("\n")
                if line_text is None:
                    continue
                all_lines.append(line_text)
    return all_lines

def split_passage_questions(lines, split_key="QUESTIONS"):
    # Split lines into passage vs questions
    q_index = None
    for i, ln in enumerate(lines):
        if ln.strip().lower().startswith(split_key.lower()):
            q_index = i
            break
    if q_index is None:
        return lines, []
    return lines[:q_index], lines[q_index:]

def group_passage_sections(lines):
    # Group Text A-D passages
    sections = []
    current_title = "Passage"
    buf = []
    for ln in lines:
        if re.match(r"^\s*Text\s+[A-D]", ln, flags=re.IGNORECASE):
            if buf:
                sections.append((current_title, buf.copy()))
                buf.clear()
            current_title = ln.strip()
        else:
            buf.append(ln)
    if buf:
        sections.append((current_title, buf))
    return sections

def parse_questions_with_sections(question_lines):
    # Keep section headers (Questions 1-7...) and questions
    sections = []
    current_title = "Questions"
    current_qs = []

    for ln in question_lines:
        if re.match(r"^\s*Questions\s+\d+", ln, flags=re.IGNORECASE):
            if current_qs:
                sections.append((current_title, current_qs.copy()))
                current_qs.clear()
            current_title = ln.strip()
        elif re.match(r"^\s*\d+\.", ln):
            current_qs.append(ln.strip())
        else:
            if ln.strip():
                current_qs.append(ln.strip())

    if current_qs:
        sections.append((current_title, current_qs))
    return sections

if uploaded:
    if not PYMUPDF_AVAILABLE:
        st.error("PyMuPDF not installed. Run `pip install pymupdf` to enable parsing.")
    else:
        raw = uploaded.read()
        lines = extract_lines(raw)
        passage_lines, question_lines = split_passage_questions(lines, "QUESTIONS")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Reading Passage")
            sections = group_passage_sections(passage_lines)
            for title, seg_lines in sections:
                with st.expander(title, expanded=True):
                    st.text_area("", "\n".join(seg_lines), height=400, disabled=True)

        with col2:
            st.subheader("Questions")
            q_sections = parse_questions_with_sections(question_lines)
            for title, qs in q_sections:
                st.markdown(f"### {title}")
                for q in qs:
                    if re.match(r"^\d+\.", q):
                        num, text = q.split(".", 1)
                        st.markdown(f"**{q}**")
                        st.text_input(f"Answer {num.strip()}", key=f"ans_{num.strip()}")
                    else:
                        st.markdown(q)
