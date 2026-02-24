from llm import call_ollama_chat, extract_json_block
import json

def grade_mcq(correct, chosen):
    return int((chosen or "").strip() == (correct or "").strip())

def llm_grade_short_answer(question, expected, student, rubric, model_name):
    system = "You are a fair grade-5 grader."
    user = f"Question: {question}\nExpected: {expected}\nStudent: {student}\nRubric: {rubric}"

    content = call_ollama_chat(
        [
            {"role": "system", "content": system}, 
            {"role": "user", "content": user}
        ],
        model=model_name,
    )
    block = extract_json_block(content or "")
    if not block:
        return {"score": 0, "feedback": "Couldn't grade."}
    
    return json.loads(block)