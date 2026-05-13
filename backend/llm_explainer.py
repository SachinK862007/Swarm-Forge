import httpx

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

def explain_action(ip, attack_type, action, params):
    prompt = f"""
You are a cybersecurity assistant writing a short technical report.
The system detected {attack_type} activity from {ip}.
The system automatically chose the defensive action '{action}' with configuration {params}.
Write exactly two sentences:
- The first sentence explains why this action was selected from a security perspective.
- The second sentence describes what information was gained about the attacker.
Do not describe any attack methods.
    """
    try:
        resp = httpx.post(OLLAMA_URL, json={
            "model": "llama3.1:8b",
            "prompt": prompt,
            "stream": False
        }, timeout=15)
        return resp.json()["response"].strip()
    except Exception:
        return "Explanation unavailable."