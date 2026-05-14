import torch
import torch.optim as optim
import torch.nn as nn
import random
from collections import deque
from env import SwarmDefenseEnv
from dqn_agent import DQN

env = SwarmDefenseEnv()
state_dim, action_dim = 5, 3
agent = DQN(state_dim, action_dim)
optimizer = optim.Adam(agent.parameters(), lr=0.001)
criterion = nn.MSELoss()
memory = deque(maxlen=2000)
batch_size, gamma, epsilon, episodes = 32, 0.99, 0.1, 1000

print("Training started...")
for ep in range(episodes):
    state, _ = env.reset()
    state = torch.tensor(state, dtype=torch.float32)
    total_reward = 0
    while True:
        if random.random() < epsilon:
            action = env.action_space.sample()
        else:
            with torch.no_grad():
                action = torch.argmax(agent(state)).item()
        next_state, reward, terminated, truncated, _ = env.step(action)
        next_state = torch.tensor(next_state, dtype=torch.float32)
        done = terminated or truncated
        memory.append((state, action, reward, next_state, done))
        state = next_state
        total_reward += reward
        if len(memory) >= batch_size:
            batch = random.sample(memory, batch_size)
            states, actions, rewards, next_states, dones = zip(*batch)
            states = torch.stack(states)
            next_states = torch.stack(next_states)
            rewards = torch.tensor(rewards, dtype=torch.float32)
            dones = torch.tensor(dones, dtype=torch.float32)
            q_vals = agent(states)
            action_q = q_vals.gather(1, torch.tensor(actions).unsqueeze(1)).squeeze()
            with torch.no_grad():
                next_q = agent(next_states).max(1)[0]
                target = rewards + gamma * next_q * (1 - dones)
            loss = criterion(action_q, target)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        if done:
            break
    if ep % 20 == 0:
        print(f"Episode {ep}, reward: {total_reward:.2f}")

torch.save(agent.state_dict(), "backend/models/policy_net.pt")
print("Model saved to backend/models/policy_net.pt")