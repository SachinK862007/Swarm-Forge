from rl_agent import get_action
from pso_optimizer import optimize_params
from llm_explainer import explain_action
from supabase_client import insert_attack_log
from honeypot import engage, isolate, spawn

MITRE_MAP = {"recon": "T1595", "bruteforce": "T1110", "injection": "T1190"}
ATYPE_TO_INT = {"recon": 0, "bruteforce": 1, "injection": 2}

def handle_attack(attack_data: dict):
    ip = attack_data.get("ip", "unknown")
    attack_type = attack_data.get("type", "recon")
    attempts = attack_data.get("attempts", 1)
    honeypot_count = attack_data.get("honeypot_count", 3)
    isolated_flag = 0
    has_token = 1 if "token" in attack_data.get("details", "") else 0

    # Convert attack type string to integer for the RL model
    attack_type_int = ATYPE_TO_INT.get(attack_type, 0)
    state = [attack_type_int, attempts, honeypot_count, isolated_flag, has_token]
    action_id = get_action(state)

    action_str_map = {0: "engage", 1: "isolate", 2: "spawn"}
    action_str = action_str_map[action_id]
    mitre_id = MITRE_MAP.get(attack_type, "T1001")

    params = {}
    if action_id == 0:
        params = optimize_params(attack_type)
        result = engage(ip)
    elif action_id == 1:
        result = isolate(ip)
    else:
        result = spawn()

    explanation = explain_action(ip, attack_type, action_str, params)
    insert_attack_log(ip, attack_type, mitre_id, action_str, params, explanation)

    return {
        "action": action_str,
        "result": result,
        "explanation": explanation,
        "mitre_id": mitre_id
    }