import httpx

OLLAMA_URL = "http://localhost:11434/api/generate"

def explain_action(ip, attack_type, action, params):
    prompt = f"""
    An attacker from IP {ip} performed a {attack_type} attack.
    The SwarmForge AI chose action: '{action}' with parameters {params}.
    Explain in 2 technical sentences why this action was chosen to deceive and collect TTPs.
    """
    try:
        resp = httpx.post(OLLAMA_URL, json={
            "model": "qwen2.5:3b",
            "prompt": prompt,
            "stream": False
        }, timeout=10)
        return resp.json()["response"].strip()
    except Exception:
        return "Explanation unavailable."