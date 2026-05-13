import torch
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from simulation.dqn_agent import DQN

# Load the trained model
model = DQN(5, 3)   # 5 inputs, 3 actions
model.load_state_dict(torch.load("models/policy_net.pt", map_location="cpu"))
model.eval()

def get_action(state):
    """state: list of 5 numbers [attack_type, attempts, honeypot_count, isolated_flag, has_token]"""
    state_t = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
    with torch.no_grad():
        q_values = model(state_t)
        return torch.argmax(q_values).item()