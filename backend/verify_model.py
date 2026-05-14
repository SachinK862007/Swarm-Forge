import torch, sys, os
sys.path.append(os.getcwd())
from simulation.dqn_agent import DQN

model = DQN(5, 3)
model.load_state_dict(torch.load("backend/models/policy_net.pt", map_location="cpu"))
model.eval()

tests = [
    ("nmap", 0, 1),
    ("nikto", 0, 1),
    ("hydra (1 attempt)", 1, 1),
    ("hydra (10 attempts)", 1, 10),
    ("sqlmap", 2, 1),
]

for name, atype, attempts in tests:
    state = torch.tensor([atype, attempts, 3, 0, 0], dtype=torch.float32).unsqueeze(0)
    with torch.no_grad():
        action_idx = torch.argmax(model(state)).item()
    action_str = ["ENGAGE", "ISOLATE", "SPAWN"][action_idx]
    print(f"{name:20} -> {action_str}")
