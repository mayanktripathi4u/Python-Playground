import streamlit as st
import io
import re

# Try to import PyMuPDF for high-fidelity text extraction (lines, fonts, highlights)
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except Exception as e:
    PYMUPDF_AVAILABLE = False

st.set_page_config(layout="wide")
st.title("PDF → Split-Screen Reading & Questions (Streamlit)")

st.markdown(
    '''
    **How it works**
    - Upload a PDF containing **Text A–D** followed by **QUESTIONS**.
    - Left pane shows the passage (line-by-line, no merging).
    - Right pane shows the questions (parsed by numbering).
    - Optional: detect **bold** lines and list **highlighted** excerpts (if present in the PDF).
    '''
)

with st.sidebar:
    st.header("Options")
    split_keyword = st.text_input("Keyword that marks questions section", value="QUESTIONS")
    group_passages = st.checkbox("Group passage into Text A–D expanders", value=True)
    show_formatting = st.checkbox("Show detected bold lines & highlights", value=True)
    st.markdown("---")
    if not PYMUPDF_AVAILABLE:
        st.warning("PyMuPDF not installed. To enable bold/highlight detection and exact line handling, run:\n\n`pip install pymupdf`")
    st.caption("Tip: No LLM required. All parsing is done locally.")

uploaded = st.file_uploader("Upload your PDF", type=["pdf"])

def extract_with_pymupdf(file_bytes: bytes):
    # \"\"\"Extract lines, bold-line indices, and highlight snippets using PyMuPDF.\"\"\"
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    all_lines = []
    bold_line_idx = set()
    highlights = []
    # Iterate pages
    for pno in range(len(doc)):
        page = doc[pno]
        # ----- Lines (preserve line structure) -----
        data = page.get_text("dict")
        for block in data.get("blocks", []):
            if "lines" not in block:
                continue
            for line in block["lines"]:
                # Concatenate spans to form a visual line
                spans = line.get("spans", [])
                if not spans:
                    continue
                line_text = "".join(span.get("text", "") for span in spans).rstrip("\n")
                # Skip empty lines but keep explicit blank lines (optional)
                if line_text is None:
                    continue
                # Record line and bold-ness
                this_idx = len(all_lines)
                all_lines.append(line_text)
                # Heuristic: a line is bold if any span font includes "Bold" or "Black"
                is_bold = any(("Bold" in (s.get("font","")) or "Black" in (s.get("font",""))) for s in spans)
                if is_bold:
                    bold_line_idx.add(this_idx)

        # ----- Highlight annotations (if any) -----
        annot = page.first_annot
        while annot:
            try:
                if annot.type[0] == 8:  # highlight
                    # Use the annot rectangle to capture text roughly inside the highlight
                    rect = annot.rect
                    txt = page.get_text("text", clip=rect)
                    if txt and txt.strip():
                        highlights.append(txt.strip())
            except Exception:
                pass
            annot = annot.next

    return all_lines, bold_line_idx, highlights

def split_passage_questions(lines, split_key="QUESTIONS"):
    # \"\"\"Split into passage lines and question lines using an exact heading match for QUESTIONS (case-insensitive).\"\"\"
    # Find a line that exactly matches 'QUESTIONS' (ignoring surrounding spaces / case)
    q_index = None
    for i, ln in enumerate(lines):
        if ln.strip().lower() == split_key.strip().lower():
            q_index = i
            break
    if q_index is None:
        # Fallback: leave everything as passage
        return lines, []
    # Exclude the heading line itself from question lines
    return lines[:q_index], lines[q_index+1:]

def group_passage_by_text_sections(passage_lines):
    # \"\"\"Group passage lines into sections Text A, Text B, Text C, Text D (if present).\"\"\"
    sections = []
    current_title = "Passage"
    current_buf = []
    def flush():
        if current_buf:
            sections.append((current_title, current_buf.copy()))
            current_buf.clear()

    # print(f"Grouping passage into sections based on 'Text A–D and Part A' headers.")
    # print(f"Total passage lines: {len(passage_lines)}")
    # print(f"Sample lines:\n {passage_lines[:60]}")

    for ln in passage_lines:
        # m = re.match(r"^\s*Text\s+([A-D])\s*(.*)$", ln, flags=re.IGNORECASE)
        m = re.match(r"^\s*(Text\s+[A-D]|Part\s+A)\b(.*)$", ln, flags=re.IGNORECASE)
        if m:
            # print(f"Detected section header: {ln}, and title: {m}")
            # Start new section
            flush()
            suffix = m.group(2).strip()
            title = f"{m.group(1).upper()}" + (f": {suffix}" if suffix else "")
            current_title = title
        else:
            current_buf.append(ln)

    flush()
    return sections

def parse_numbered_questions(question_lines):
    # \"\"\"Parse numbered questions into a dict {number: text}.\"\"\"
    questions_text = "\n".join(question_lines)
    # Split on line-start "n." patterns, multiline aware, capture the number
    parts = re.split(r"(?m)^\s*(\d{1,2})\.\s+", questions_text)
    # parts will look like: [pre, num1, text1, num2, text2, ...]
    q = {}
    # Start from index 1 to skip preamble
    for i in range(1, len(parts)-1, 2):
        num = parts[i]
        body = parts[i+1].strip()
        # Stop at the next number heading artifact (if any leftover noise)
        try:
            q[int(num)] = body
        except Exception:
            pass
    return q


# filter out any line (or short sequence of lines) that matches those patterns.
# def clean_passage_lines(lines):
#     """
#     Remove filler like 'Go to', 'Questions', and digit sequences
#     that appear between Text A, B, C, D.
#     """
#     cleaned = []
#     for ln in lines:
#         t = ln.strip()
#         if not t:
#             continue
#         # Remove "Go to" / "Questions"
#         if t.lower() in {"go to", "questions"}:
#             continue
#         # Remove lines that are just numbers in quotes “1” “2” … “20”
#         if re.match(r"^[“\d\s”]+$", t):
#             continue
#         cleaned.append(ln)
#     return cleaned

def clean_passage_lines(lines):
    """
    Remove filler like 'Go to' followed immediately by 'Questions',
    plus digit sequences (e.g., “1” “2” … “20”).
    If 'Questions' is not right after 'Go to', keep them.
    """
    cleaned = []
    skip_next = False

    for i, ln in enumerate(lines):
        if skip_next:
            skip_next = False
            continue

        t = ln.strip()
        if not t:
            continue

        # Check for "Go to" followed by "Questions"
        if t.lower() == "go to" and i + 1 < len(lines) and lines[i+1].strip().lower() == "questions":
            # skip both this and the next line
            skip_next = True
            continue

        # Remove lines that are just numbers in quotes “1” “2” … “20”
        if re.match(r'^[“\d\s”]+$', t):
            continue

        # Remove lines that are exactly “Text A”, “Text B”, “Text C”, “Text D”
        if re.match(r'^“Text [A-D]”$', t):
            continue

        # # Check for "Go to" followed by "Questions"
        # if t.lower() == "to" and i + 1 < len(lines) and lines[i+1].strip().lower() == "\"Text":
        #     # skip both this and the next line
        #     skip_next = True
        #     continue

        cleaned.append(ln)

    return cleaned


# def clean_passage_lines(lines):
#     """
#     Remove filler lines in passages:
#     - 'Go to' followed immediately by 'Questions'
#     - 'Go to' followed immediately by 'Text A', 'Text B', 'Text C', or 'Text D'
#     - Digit sequences (e.g., “1” “2” … “20”)
#     Only remove 'Go to' if the next line matches the specific condition.
#     """
#     cleaned = []
#     skip_next = False
#     text_targets = {"“text a”", "“text b”", "“text c”", "“text d”", "questions"}  # lowercase for comparison

#     for i, ln in enumerate(lines):
#         if skip_next:
#             skip_next = False
#             continue

#         t = ln.strip()
#         if not t:
#             continue

#         # Check for "Go to" followed by specified targets
#         if (t.lower() == "go to" or t.lower() == "to" ) and i + 1 < len(lines):
#             next_line = lines[i+1].strip().lower()
#             if next_line in text_targets:
#                 skip_next = True
#                 continue

#         # Remove lines that are just numbers in quotes “1” “2” … “20”
#         if re.match(r'^[“\d\s”]+$', t):
#             continue

#         cleaned.append(ln)

#     return cleaned

import time
from streamlit_autorefresh import st_autorefresh

# Automatically refresh the app every 1 second (1000 milliseconds)
st_autorefresh(interval=1000, key="timer_refresh")

if uploaded:
    raw = uploaded.read()

    # Initialize timer in session_state
    if "timer_start" not in st.session_state or st.session_state.get("last_uploaded") != uploaded.name:
        st.session_state["timer_start"] = time.time()
        st.session_state["last_uploaded"] = uploaded.name

    elapsed = int(time.time() - st.session_state["timer_start"])
    st.markdown(f"### ⏱️ Time elapsed: {elapsed} seconds")

    if PYMUPDF_AVAILABLE:
        lines, bold_idx, highlights = extract_with_pymupdf(raw)
        # print(f"Extracted {len(lines)} lines from PDF using PyMuPDF.")
        # print(f"Sample lines:\n {lines[:60]}")
        # print(f"Detected {len(bold_idx)} bold lines, and {len(highlights)} highlights.")

        # Clean up passage
        lines = clean_passage_lines(lines)
        # print(f"After Clean: Extracted {len(lines)} lines from PDF using PyMuPDF.")
        # print(f"After Clean: Sample lines:\n {lines[:60]}")
        # print(f"After Clean: Detected {len(bold_idx)} bold lines, and {len(highlights)} highlights.")

    else:
        # Minimal fallback: show entire file as one blob (line fidelity may be reduced)
        st.error("PyMuPDF not available. Please install `pymupdf` to preserve lines and detect formatting.")
        lines = []
        bold_idx = set()
        highlights = []

    if lines:
        # Split into passage vs questions
        passage_lines, question_lines = split_passage_questions(lines, split_keyword)
        # print(f"Passage lines: {len(passage_lines)}, Question lines: {len(question_lines)}")
        # print(f"Passage Preview:\n {passage_lines[:55]}")
        print(f"\n\nQuestion Preview:\n {question_lines[:50]}")

        # Clean up passage
        passage_lines = clean_passage_lines(passage_lines)
        # print(f"After Clean up Passage Preview:\n {passage_lines[:55]}")

        # --- UI Layout ---
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Reading Passage")
            if group_passages:
                sections = group_passage_by_text_sections(passage_lines)
                if sections:
                    # st.write(f"Detected {len(sections)} sections (Text A–D).")
                    for title, seg_lines in sections:
                        # st.write(f"### {title}, and {len(seg_lines)} lines")
                        with st.expander(title, expanded=True):
                            st.text_area(
                                label="",
                                value="\n".join(seg_lines),
                                height=400,
                                key=f"passage_{title}",
                                disabled=True
                            )
                else:
                    st.text_area("", value="\n".join(passage_lines), height=600, disabled=True)
            else:
                st.text_area("", value="\n".join(passage_lines), height=600, disabled=True)

            if show_formatting and PYMUPDF_AVAILABLE:
                with st.expander("Detected formatting (experimental)", expanded=False):
                    # Bold lines
                    if bold_idx:
                        st.markdown(f"**Bold lines detected:** {len(bold_idx)}")
                        # show a preview (first 15)
                        preview = [f"{i+1}: {passage_lines[i]}" for i in sorted(bold_idx) if i < len(passage_lines)]
                        if preview:
                            st.text("\n".join(preview[:15]) + ("\n..." if len(preview) > 15 else ""))
                        else:
                            st.caption("Bold detected outside passage section.")
                    else:
                        st.caption("No bold lines detected.")
                    # Highlights
                    if highlights:
                        st.markdown(f"**Highlight excerpts:** {len(highlights)} found")
                        for h in highlights[:10]:
                            st.markdown(f"- {h}")
                        if len(highlights) > 10:
                            st.caption("... more highlights not shown")
                    else:
                        st.caption("No highlights detected.")

        with col2:
            st.subheader("Questions")
            qs = parse_numbered_questions(question_lines)
            if not qs:
                # Show raw text if parsing fails
                st.text_area("", value="\n".join(question_lines), height=600, disabled=True)
            else:
                for n in sorted(qs.keys()):
                    st.markdown(f"**{n}. {qs[n]}**")
                    st.text_input(f"Answer {n}", key=f"ans_{n}")

else:
    st.info("Upload a PDF to begin.")
