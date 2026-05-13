import torch
import sys, os

# Allow importing from the parent folder (simulation)
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from simulation.dqn_agent import DQN

# Build the absolute path to the model, relative to THIS file
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "policy_net.pt")

model = DQN(5, 3)
model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
model.eval()

def get_action(state):
    state_t = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
    with torch.no_grad():
        return torch.argmax(model(state_t)).item()