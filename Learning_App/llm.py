import re, json, random, requests

def call_ollama_chat(messages, model="llama3.1:8b", host="http://localhost:11434", timeout=90):
    try:
        resp = requests.post(
        f"{host}/api/chat",
        json={"model": model, "messages": messages, "stream": False},
        timeout=timeout,
        )
        resp.raise_for_status()
        return resp.json().get("message", {}).get("content", "")
    except Exception:
        return None


def extract_json_block(text):
    if not text:
        return None
    m = re.search(r"\[.*\]", text, flags=re.DOTALL)
    if m:
        return m.group(0)
    m = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if m:
        return m.group(0)
    return None