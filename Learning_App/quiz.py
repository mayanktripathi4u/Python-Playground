import json, random
from kb import KB, FALLBACK_BANK
from llm import call_ollama_chat, extract_json_block

def build_context(subject, topics):
    notes = []
    kb = KB.get(subject, {})
    if not topics:
        topics = list(kb.keys())
    for t in topics:
        if t in kb:
            notes.append(f"Topic: {t}\nNotes: {kb[t]}")
    return "\n\n".join(notes)

def llm_generate_questions(subject, topics, n, difficulty, qtype, model_name):
    context = build_context(subject, topics)
    system = "You are a helpful grade-5 tutor who generates quizzes in JSON only."
    user = f"Generate {n} {qtype} questions for {subject}. Use notes: {context}"

    content = call_ollama_chat(
        [
            {"role": "system", "content": system}, 
            {"role": "user", "content": user}
        ],
        model=model_name,
    )
    block = extract_json_block(content)
    if not block:
        return None
    try:
        return json.loads(block)
    except Exception:
        return None


def fallback_generate_questions(subject, topics, n, qtype):
    bank = FALLBACK_BANK.get(subject, {})
    if not topics:
        topics = list(bank.keys())
    pool = []
    for t in topics:
        pool.extend(bank.get(t, []))
    random.shuffle(pool)
    return pool[:n]