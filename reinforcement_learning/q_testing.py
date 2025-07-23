import gymnasium as gym
import numpy as np

# Create the environment
env = gym.make("FrozenLake-v1", is_slippery=False, render_mode="human")  # not slippery makes it easier

# Load q_table
q_table = np.load("q_table_frozen_slipery_4999.npy")

# Max steps per episode
max_steps = 50

# Agent testing in 5 episodes
for _ in range(5):
    state, _ = env.reset()
    env.render()

    # done = False
    
    # while not done:
    for _ in range(100):
        action = np.argmax(q_table[state])
        state, reward, terminated, truncated, _ = env.step(action)
        env.render()
        done = terminated or truncated

    print("Final reward:", reward)
env.close()
