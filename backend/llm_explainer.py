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
            "model": "llama3.1:8b",           # <-- changed to llama3.1
            "prompt": prompt,
            "stream": False
        }, timeout=15)                        # slightly longer timeout for 8B
        return resp.json()["response"].strip()
    except Exception:
        return "Explanation unavailable."