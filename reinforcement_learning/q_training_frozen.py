import gymnasium as gym
import numpy as np
import random
import mlflow

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment(experiment_id="0")

SEED = 19
random.seed(SEED)
np.random.seed(SEED)

# Save behavior on MLFlow for later analysis
with mlflow.start_run():

    # Create the environment
    env = gym.make("FrozenLake-v1", is_slippery=True)  # is_slippery == False makes training easier

    # Parameters
    alpha = 0.8         # learning rate
    gamma = 0.95        # discount rate
    epsilon = 1.0       # exploration rate
    epsilon_decay = 0.995
    min_epsilon = 0.01
    num_episodes = 5000
    max_steps = 100

    # Start Q-table
    state_space_size = env.observation_space.n  # 16
    action_space_size = env.action_space.n      # 4
    q_table = np.zeros((state_space_size, action_space_size))

    # Saving parameters in MLFlow
    mlflow.log_param("seed", SEED)
    mlflow.log_param("learning rate", alpha)
    mlflow.log_param("discount rate", gamma)
    mlflow.log_param("num_episodes", num_episodes)

    # Choose action function (epsilon-greedy)
    def choose_action(state):
        if random.uniform(0,1) < epsilon:
            return env.action_space.sample()
        else:
            return np.argmax(q_table[state])

    # Training loop
    for episode in range(num_episodes):
        state, _ = env.reset(seed=SEED)
        total_reward = 0
        
        for _ in range(max_steps):
            action = choose_action(state)
            next_state, reward, terminated, truncated, _ = env.step(action)

            # Update Q-table
            old_value = q_table[state, action]
            next_max = np.max(q_table[next_state])

            # Q-table update formula 
            q_table[state, action] = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)

            state = next_state
            total_reward += reward

            if terminated or truncated:
                break
        
        mlflow.log_metric("Total reward over episodes", total_reward, step=episode)
        mlflow.log_metric("Exploration rate over episodes", epsilon, step=episode)

        # Epsilon update
        epsilon = max(min_epsilon, epsilon * epsilon_decay)

        print(f"Episode {episode}, reward: {total_reward}, epsilon: {epsilon:.4f}")

        if episode % 500 == 0 or episode==num_episodes-1:
            np.save(f"q_table_frozen_slipery_{episode}.npy", q_table)
            print(f"Checkpoint saved in {episode} episode")

    env.close()
