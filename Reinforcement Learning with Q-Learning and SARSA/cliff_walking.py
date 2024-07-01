import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import os
from IPython.display import clear_output

def save_frames_as_gif(frames, episode, algorithm_type, path='./Algorithm_Animations/', filename='gym_animation.gif'):
    if not os.path.exists(path):
        os.makedirs(path)
    plt.figure(figsize=(frames[0].shape[1] / 72.0, frames[0].shape[0] / 72.0), dpi=72)
    patch = plt.imshow(frames[0])
    plt.axis('off')
    plt.title(f"Run from episode {episode} {algorithm_type}")

    def animate(i):
        patch.set_data(frames[i])

    anim = animation.FuncAnimation(plt.gcf(), animate, frames=len(frames), interval=50)
    anim.save(path + filename, writer='pillow', fps=30)
    plt.close()

def eps_greedy_action(Q, s, eps):
    if np.random.rand() > eps:
        return np.argmax(Q[s, :])
    else:
        return np.random.randint(0, Q.shape[1])

def qlearning(env, Q, alpha, gamma, eps, episodes, render_interval=10):
    list_of_rewards = np.zeros(episodes)

    for episode in range(episodes):
        state = env.reset()[0]
        total_reward = 0

        for _ in range(100):
            action = eps_greedy_action(Q, state, eps)
            next_state, reward, done, _, _ = env.step(action)
            total_reward += reward

            best_next_action = np.argmax(Q[next_state])
            td_target = reward + gamma * Q[next_state][best_next_action]
            Q[state][action] += alpha * (td_target - Q[state][action])

            state = next_state

            if episode % render_interval == 0:
                env.render()
                clear_output(wait=True)

            if done:
                break

        list_of_rewards[episode] = total_reward
        print(f"Episode {episode + 1}/{episodes}, Total Reward: {total_reward}")

    return Q, list_of_rewards

def sarsa(env, Q, alpha, gamma, eps, episodes, render_interval=10):
    list_of_rewards = np.zeros(episodes)

    for episode in range(episodes):
        state = env.reset()[0]
        action = eps_greedy_action(Q, state, eps)
        total_reward = 0

        for _ in range(100):
            next_state, reward, done, _, _ = env.step(action)
            total_reward += reward

            next_action = eps_greedy_action(Q, next_state, eps)
            td_target = reward + gamma * Q[next_state][next_action]
            Q[state][action] += alpha * (td_target - Q[state][action])

            state, action = next_state, next_action

            if episode % render_interval == 0:
                env.render()
                clear_output(wait=True)

            if done:
                break

        list_of_rewards[episode] = total_reward
        print(f"Episode {episode + 1}/{episodes}, Total Reward: {total_reward}")

    return Q, list_of_rewards

def plot_results(qlearning_rewards, sarsa_rewards):
    plt.plot(qlearning_rewards, label='Q-Learning')
    plt.plot(sarsa_rewards, label='SARSA')
    plt.xlabel('Episode')
    plt.ylabel('Average Return')
    plt.title('Q-Learning vs SARSA on CliffWalking')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Create the environment with human render mode
    env = gym.make('CliffWalking-v0', render_mode="human")

    episodes = 1000
    alpha = 0.1
    gamma = 0.99
    eps = 0.1

    num_runs = 10
    qlearning_results = np.zeros(episodes)
    sarsa_results = np.zeros(episodes)

    for run in range(num_runs):
        print(f"Starting run {run + 1}/{num_runs}")
        Q_ql = np.zeros((env.observation_space.n, env.action_space.n))
        Q_sa = np.zeros((env.observation_space.n, env.action_space.n))

        _, qlearning_rewards = qlearning(env, Q_ql, alpha, gamma, eps, episodes)
        _, sarsa_rewards = sarsa(env, Q_sa, alpha, gamma, eps, episodes)

        qlearning_results += qlearning_rewards
        sarsa_results += sarsa_rewards

    qlearning_results /= num_runs
    sarsa_results /= num_runs

    plot_results(qlearning_results, sarsa_results)