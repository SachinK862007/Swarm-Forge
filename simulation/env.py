import gymnasium as gym
from gymnasium import spaces
import numpy as np

class SwarmDefenseEnv(gym.Env):
    def __init__(self):
        self.observation_space = spaces.Box(low=0, high=10, shape=(5,), dtype=np.float32)
        self.action_space = spaces.Discrete(3)
        self.max_steps = 50
        self.reset()

    def reset(self, seed=None):
        super().reset(seed=seed)
        self.attacker = {'type': 0, 'attempts': 1, 'has_token': False}
        self.honeypots = [{'id': 0, 'isolated': False}]
        self.steps = 0
        return self._get_state(), {}

    def _get_state(self):
        return np.array([
            self.attacker['type'],
            self.attacker['attempts'],
            len(self.honeypots),
            1 if any(h['isolated'] for h in self.honeypots) else 0,
            1 if self.attacker['has_token'] else 0
        ], dtype=np.float32)

    def step(self, action):
        self.steps += 1
        if np.random.rand() < 0.3:
            self.attacker['type'] = np.random.choice([0, 1, 2])
        self.attacker['attempts'] += 1
        if action == 0:
            if np.random.rand() < 0.5:
                self.attacker['has_token'] = True
        elif action == 1:
            self.honeypots[0]['isolated'] = True
        elif action == 2:
            self.honeypots.append({'id': len(self.honeypots), 'isolated': False})
        reward = 0.0
        if action == 0:
            reward += 0.1 * self.steps
            if self.attacker['has_token']:
                reward += 5.0
        elif action == 1:
            reward += 2.0
            if self.honeypots[0]['isolated']:
                reward += 3.0
        elif action == 2:
            reward += 1.0
        if self.attacker['type'] == 2 and action != 1:
            reward -= 5.0
        terminated = False
        truncated = self.steps >= self.max_steps
        return self._get_state(), reward, terminated, truncated, {}