# Reinforcement Learning with Q-Learning and SARSA

## Introduction

In this Task, we compared two temporal-difference learning algorithms, SARSA and Q-learning, on the CliffWalking environment. We used the `gymnasium` library to create and interact with the environment. The task involves implementing both algorithms, running them, and comparing their performance.

## Environment Setup

Install the `gymnasium` library using the following command:

```sh
pip install gymnasium
```

Create the CliffWalking environment:

```python
import gymnasium as gym
env = gym.make('CliffWalking-v0')
```

## Q-Learning

We first implemented the Q-learning algorithm and tested it on the CliffWalking environment. Using the following settings:
- ϵ-greedy policy with ϵ = 0.1
- γ (discount factor) = 0.99
- α (learning rate) = 0.1

We terminated each episode when the environment indicates it (through the `done` flag) or when 100 steps have elapsed. Record the sum of rewards received for each episode.

## SARSA

Next, we implemented the SARSA algorithm using the same settings and parameters as Q-learning above.

## Accompolishments

For both algorithms, we do the following:
1. Run each algorithm for 1000 episodes.
2. Record the return for each episode.
3. Repeat the entire procedure 10 times and average the results over these runs. This gave us a list of length 1000, where each entry represents the average return for that episode.

We Plot the results for both algorithms on the same axes and label each line appropriately.

### Deliverables

1. **Code**: Include our implementation of both Q-learning and SARSA.
2. **Plot**: A plot showing the average returns for both algorithms over 1000 episodes.
3. **Discussion**: A brief discussion (3-4 sentences) analyzing the results, focusing on why the curves might look different.

### Discussion

- Analyze the difference between the Q-learning and SARSA curves.
- Explain why Q-learning might perform differently from SARSA in this environment.
- Consider the impact of the exploration strategy and the update rules on the learning process.

---
