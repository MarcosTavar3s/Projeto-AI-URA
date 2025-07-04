import random
import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt

env = gym.make('Taxi-v3', is_slippery=False)

# parameters
alpha = 0.9   # learning rate
gamma = 0.95  # discount rate
epsilon = 1 # exploration rate (randomness) - begin random (0 to 1) - 1 means the maximum of randomness
epsilon_decay = 0.9995 
min_epsilon = 0.01
num_episodes = 10000 # epochs
max_steps = 100 # maximum steps

# q_table is made of the numbers of states and actions
q_table = np.zeros((env.observation_space.n, env.action_space.n))

def choose_action(state):
    if random.uniform(0,1) < epsilon:
        return env.action_space.sample()
    else:
        return np.argmax(q_table[state, :])
    
for episode in range(num_episodes):
    state, _ = env.reset()
    
    done = False
    
    for step in range(max_steps):
        action = choose_action(state)
        
        next_state, reward, done, truncated, info = env.step(action)
        
        # current state
        old_value = q_table[state, action]
        next_max = np.max(q_table[next_state, :])
        
        # how rewardful is taking a certain path
        q_table[state, action] = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        
        if done or truncated:
            break
        
    epsilon = max(epsilon * epsilon_decay, min_epsilon)
    

# TESTING
env = gym.make("Taxi-v3", render_mode="human")

for episode in range(5):
    state, _ = env.reset() 
    done = False
    
    print("Episode: ", episode)
    
    for step in range(max_steps):
        img = env.render()
        action = np.argmax(q_table[state, :])
        next_state, reward, terminated, truncated, info = env.step(action)
        
        state = next_state
        
        if terminated or truncated:
            img = env.render()
            print("Finished episode ", episode, "with reward: ", reward)
            break

env.close()
